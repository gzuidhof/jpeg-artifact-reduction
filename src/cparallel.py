from __future__ import division

try:
    import pathos
    import dill
    from pathos.helpers import mp as multip
    print "Using pathos/dill for multiprocessing."
except:
    import multiprocessing as multip
import Queue

from threading import Thread
import numpy as np
import time

class ContinuousParallelBatchIterator(object):
    """
    Uses a producer-consumer model to prepare batches on the CPU in different processes or threads (while you are training on the GPU).
    Continuous version, continues between and after batches.
    
    Constructor arguments:
        batch_generator: function which can be called to yield a new batch.
        
        ordered: boolean (default=False), whether the order of the batches matters
        batch_size: integer (default=1), amount of points in one batch
        
        multiprocess: boolean (default=True), multiprocess instead of multithrea
        n_producers: integer (default=4), amount of producers (threads or processes)
        max_queue_size: integer (default=3*n_producers)
    """

    def __init__(self, batch_generator, batch_size=1, ordered=False, multiprocess=True, n_producers=4, max_queue_size=None):
        self.generator = batch_generator
        self.ordered = ordered
        self.multiprocess = multiprocess
        self.n_producers = n_producers
        self.batch_size = batch_size

        if max_queue_size is None:
            self.max_queue_size = n_producers*3
        else:
            self.max_queue_size = max_queue_size
        
        if self.multiprocess:
            self.job_queue = multip.Queue()
        else:
            self.job_queue = Queue.Queue()

        self.last_retrieved_job = 0
        self.last_added_job = 0
        self.started = False

    def start(self):
        
        max_queue_size = 1 if self.ordered else self.max_queue_size//2

        self.queue = multip.Queue(maxsize=max_queue_size) if self.multiprocess else Queue.Queue(maxsize=self.max_queue_size)
    
        # Flag used for keeping values in completed queue in order
        self.last_completed_job = multip.Value('i', -1)
        self.exit = multip.Event()


        if self.multiprocess and self.ordered:
            self.cache_queue = Queue.Queue(maxsize=self.max_queue_size)
            def batcher(queue, cache_queue):
                while not self.exit.is_set():
                    job_index, item = queue.get()
                    cache_queue.put((job_index, item))
                    
                    time.sleep(0.0001) #to be sure..
            
            # As Queues in Python are __!__NOT__!__ First in first out in a multiprocessing setting
            # We use a seperate thread to synchronously put them in order
            p = Thread(target=batcher, args=(self.queue, self.cache_queue), name='Synchronous batcher worker')
            p.daemon = True
            p.start()

        else:
            self.cache_queue = self.queue

        # Start worker processes or threads
        for i in xrange(self.n_producers):
            name = "ContinuousParallelBatchIterator worker {0}".format(i)
        
            if self.multiprocess:
                p = multip.Process(target=_produce_helper, args=(i,self.generator, self.job_queue, self.queue, self.last_completed_job, self.ordered, self.exit), name=name)
            else:
                p = Thread(target=_produce_helper, args=(i,self.generator, self.job_queue, self.queue, self.last_completed_job, self.ordered, self.exit), name=name)

            # Make the process daemon, so the main process can die without these finishing
            p.daemon = True
            p.start()

        self.started = True

    def append(self, todo):
        batches = list(chunks(todo, self.batch_size))

        for job in batches:
            self.job_queue.put((self.last_added_job, job))
            self.last_added_job += 1

        return len(batches)

    def __call__(self, n_batches, X=None):
        if X is not None:
            self.append(X)

        if not self.started:
            self.start()

        n_upcoming_batches = self.last_added_job - self.last_retrieved_job

        if n_upcoming_batches < n_batches:
            print "Not enough X appended to retrieve this many batches"
            print "Returning the maximum amount instead ({})".format(n_upcoming_batches)
            n_batches = n_upcoming_batches

        return GeneratorLen(self.__gen_batch(n_batches), n_batches)

    def __gen_batch(self, n_batches):
        # Run as consumer (read items from queue, in current thread)
        for x in xrange(n_batches):

            job_index, item = self.cache_queue.get()

            self.last_retrieved_job += 1
            if item is not None:
                yield item # Yield the item to the consumer (user)


    def stop(self):
        self.exit.set()
        if not multiprocess:
            self.queue.close()
            self.job_queue.close()
            self.cache_queue.close()

class GeneratorLen(object):
    def __init__(self, gen, length):
        self.gen = gen
        self.length = length

    def __len__(self): 
        return self.length

    def __iter__(self):
        return self.gen

def _produce_helper(id, generator, jobs, result_queue, last_completed_job, ordered, exit):
    """
        What one worker executes, defined as a top level function as this is required for the Windows platform.
    """

    np.random.seed()

    while not exit.is_set():
        job_index, task = jobs.get()

        result = generator(task)

        # Put result onto the 'done'-queue
        while not exit.is_set():
            # My turn to add job result (to keep it in order)?
            if not ordered or last_completed_job.value == job_index-1:
                with last_completed_job.get_lock():
                    result_queue.put((job_index, result))
                    last_completed_job.value += 1
                    break

            
        

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
        from http://goo.gl/DZNhk
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
