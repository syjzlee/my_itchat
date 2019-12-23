# import threading
# import time
#
#
# def loop(start, end):
#     for i in range(start,end):
#         print('thread %s >>> %s' % (threading.current_thread().name, i), (start,end))
#         time.sleep(10)
#         if i%5 == 1:
#             return True
#
# thread_list = list()
# for i in range(5):
#     thread_list.append(threading.Thread(target=loop, args=(i*20, (i+1)*20)))
#
# for i in thread_list:
#     i.start()
#


import time
import threading

def fun1():
    while True:
        time.sleep(2)
        print("fun1",time.time())

def fun2():
    while True:
        time.sleep(6)
        print("fun2",time.time())

threads = []
threads.append(threading.Thread(target=fun1))
threads.append(threading.Thread(target=fun2))
print(threads)
if __name__ == '__main__':
    for t in threads:
        print(t)
        t.start()
