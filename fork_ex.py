#from https://code-maven.com/parallel-processing-using-fork-in-python
import os
import multiprocessing
from time import sleep

SLEEP_TIME_SECONDS = .015
NUMB_CHILDREN = 3
NUMB_ITEMS_IN_QUEUE = 10

#create a queue to share between the child processes
#queues are both process and thread threadsafe
q = multiprocessing.Queue()
q_out = multiprocessing.Queue()
child_process_list = []

# add stuff to queue
for i in range(NUMB_ITEMS_IN_QUEUE):
    q.put(i)

print("Process id before forking: {}".format(os.getpid()))

def child_proc_func():
    '''
    runs in seperate child process
    :return:
    '''
    print("In child process that has the PID {}".format(os.getpid()))
    while (not q.empty()):
        a = q.get()
        print("In the child process that has the PID {} processing q value {}".format(os.getpid(), a))
        q_out.put(a)
        sleep(SLEEP_TIME_SECONDS)
    exit()


#start bunch of processes
for i in range(NUMB_CHILDREN):
    try:
        pid = os.fork()
    except OSError:
        exit("Could not create a child process")

    if pid == 0:
        child_proc_func()
    else:
        print("Parent process forked child pid= {}".format(pid))
        child_process_list.append(pid)  #save for waiting on

#lets wait for all children to finish before exiting
for p in child_process_list:
    finished = os.waitpid(p,0)
    print("finished with process {}".format(finished))

print("q.qsize()= {} and q_out.qsize()= {}".format(q.qsize(), q_out.qsize()))
