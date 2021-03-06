"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===

This module runs timing experiments to determine how the time taken
to enqueue or dequeue grows as the queue size grows.

To complete this code, you will use the Timer class.  Here is a template
for how to use it.

Read through the docstring of the Timer class to understand how to use it.
"""
from myqueue import Queue
from timer import Timer


def _profile_enqueue(queue_size: int, n: int) -> None:
    """Report the time taken to perform enqueue operations.

    Specifically, report the time taken to perform a single Queue.enqueue
    operation on <n> queues, each of size <queue_size>.
    (We do this on multiple queues to slow down the trials a little.)
    """
    # TODO: implement this function by following the steps in the comments.
    # Experiment preparation: make a list containing <n> queues,
    # each of size <queue_size>. The elements you enqueue don't matter.
    # You can "cheat" here and set your queue's _items attribute
    # directly to a list of the appropriate size by writing something like
    #
    # queue._items = list(range(queue_size))
    #
    # to save a bit of time in setting up the experiment.

    # First, make a list containing <n> queues of size <queue_size>.

    # Second, for each of the <n> queues, enqueue a single item.
    # (Wrap the code in a Timer block to measure the total time taken.)

    queue_list = []
    for _ in range(n):
        queue = Queue()
        queue.__items = list(range(queue_size))
        queue_list.append(queue)


    with Timer("Profile Enqueue") as timer:
        for queue in queue_list:
            queue.enqueue(1)
    return timer.interval

def _profile_dequeue(queue_size: int, n: int) -> None:
    """Report the time taken to perform enqueue operations.

    Specifically, report the time taken to perform a single Queue.enqueue
    operation on <n> queues, each of size <queue_size>.
    (We do this on multiple queues to slow down the trials a little.)
    """
    # TODO: implement this function in a similar way to _profile_enqueue.
    # Experiment preparation: make a list containing <n> queues,
    # each of size <queue_size>.
    # You can "cheat" here and set your queue's _items attribute
    # directly to a list of the appropriate size by writing something like
    #
    # queue._items = list(range(queue_size))
    #
    # to save a bit of time in setting up the experiment.
    queue_list = []
    for _ in range(n):
        queue = Queue()
        queue.__items = list(range(queue_size))
        queue_list.append(queue)

    with Timer("Profile Dequeue") as timer:
        for queue in queue_list:
            queue.dequeue()

    return timer.interval

def time_queue() -> None:
    """Profile enqueue and dequeue on various queue sizes."""
    # The different parameters for our timing runs.
    # Feel free to adjust this a little if it runs very slowly
    # on your computers.
    sizes = [10000, 20000, 40000, 80000, 160000, 320000]
    trials = 500

    enqueue_intervals = []
    dequeue_intervals = []

    for size in sizes:
        enqueue_intervals.append(_profile_enqueue(size, trials))
    for size in sizes:
        dequeue_intervals.append(_profile_dequeue(size, trials))
    import matplotlib.pyplot as plt
    plt.plot(enqueue_intervals, 'ro')
    plt.plot(dequeue_intervals, 'bo')
    plt.show()

if __name__ == '__main__':
    time_queue()
