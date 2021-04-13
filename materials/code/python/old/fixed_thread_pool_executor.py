# Source code: https://gist.github.com/tliron/81dd915166b0bfc64be08b4f8e22c835
# Ported to Python3

from threading import Thread, Lock
from queue import Queue
import itertools, traceback, multiprocessing

class FixedThreadPoolExecutor(object):
    """
    Executes tasks in a fixed thread pool.
    
    Makes sure to gather all returned results and thrown exceptions in one place, in order of task
    submission.
    
    Example::
    
        def sum(arg1, arg2):
            return arg1 + arg2
            
        executor = FixedThreadPoolExecutor(10)
        try:
            for value in range(100):
                executor.submit(sum, value, value)
            executor.drain()
        except:
            executor.close()
        executor.raise_first()
        print executor.returns
    
    You can also use it with the Python "with" keyword, in which case you don't need to call "close"
    explicitly::
    
        with FixedThreadPoolExecutor(10) as executor:
            for value in range(100):
                executor.submit(sum, value, value)
            executor.drain()
            executor.raise_first()
            print executor.returns
    """
    
    def __init__(self, size = multiprocessing.cpu_count() * 2 + 1, timeout = None, print_exceptions = False):
        """
        :param size: Number of threads in the pool (fixed).
        :param timeout: Timeout in seconds for all blocking operations. (Defaults to none, meaning no timeout) 
        :param print_exceptions: Set to true in order to print exceptions from tasks. (Defaults to false)
        """
        self.size = size
        self.timeout = timeout
        self.print_exceptions = print_exceptions

        self._tasks = Queue()
        self._returns = {}
        self._exceptions = {}
        self._id_creator = itertools.count()
        self._lock = Lock() # for console output

        self._workers = [FixedThreadPoolExecutor._Worker(self, index) for index in range(size)]
    
    def submit(self, fn, *args, **kwargs):
        """
        Submit a task for execution.
        
        The task will be called ASAP on the next available worker thread in the pool.
        """
        self._tasks.put((next(self._id_creator), fn, args, kwargs), timeout=self.timeout)

    def close(self):
        """
        Blocks until all current tasks finish execution and all worker threads are dead.
        
        You cannot submit tasks anymore after calling this.
        
        This is called automatically upon exit if you are using the "with" keyword.
        """
        self.drain()
        while self.is_alive:
            self._tasks.put(FixedThreadPoolExecutor._CYANIDE, timeout=self.timeout)
        self._workers =  None

    def drain(self):
        """
        Blocks until all current tasks finish execution, but leaves the worker threads alive.
        """
        self._tasks.join() # oddly, the API does not support a timeout parameter

    @property
    def is_alive(self):
        """
        True if any of the worker threads are alive.
        """
        for worker in self._workers:
            if worker.is_alive():
                return True
        return False
    
    @property
    def returns(self):
        """
        The returned values from all tasks, in order of submission.
        """
        return [self._returns[k] for k in sorted(self._returns)]

    @property
    def exceptions(self):
        """
        The raised exceptions from all tasks, in order of submission.
        """
        return [self._exceptions[k] for k in sorted(self._exceptions)]

    def raise_first(self):
        """
        If exceptions were thrown by any task, then the first one will be raised.
        
        This is rather arbitrary: proper handling would involve iterating all the
        exceptions. However, if you want to use the "raise" mechanism, you are
        limited to raising only one of them.
        """
        exceptions = self.exceptions
        if exceptions:
            raise exceptions[0]

    _CYANIDE = object()
    """
    Special task marker used to kill worker threads.
    """

    class _Worker(Thread):
        """
        Worker thread.
        
        Keeps executing tasks until fed with cyanide.
        """
        def __init__(self, executor, index):
            super(FixedThreadPoolExecutor._Worker, self).__init__(name='FixedThreadPoolExecutor%d' % index)
            self.executor = executor
            self.daemon = True
            self.start()
        
        def run(self):
            while True:
                if not self.executor._execute_next_task():
                    break
    
    def _execute_next_task(self):
        task = self._tasks.get(timeout=self.timeout)
        if task == FixedThreadPoolExecutor._CYANIDE:
            # Time to die :(
            return False
        self._execute_task(*task)
        return True

    def _execute_task(self, id, fn, args, kwargs):
        try:
            r = fn(*args, **kwargs)
            self._returns[id] = r
        except Exception as e:
            self._exceptions[id] = e
            if self.print_exceptions:
                with self._lock:
                    traceback.print_exc()
        self._tasks.task_done()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        return False