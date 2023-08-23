from multiprocessing import Process
import os

def info(title):
    print()
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line\n')
    p1 = Process(target=f, args=('Alice',))
    #p2 = Process(target=f, args=('Bob',))
    p1.start()
    #p2.start()
    p1.join()
    #p2.join()