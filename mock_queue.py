from multiprocessing import Queue
from typing import List

from db_models import ScanJob


class MockScanJobQueue:
    """

    IMPORTANT: Assume thread-safety and support for multi-processes

    """

    def __init__(self, shared_queue: Queue):
        self.queue = shared_queue

    def enqueue(self, scanJob: str) -> None:
        self.queue.put(scanJob)

    def dequeue(self, n, batch_timeout) -> List[str]:
        """
        assume will block until AT-LEAST one item is available and return max n items.
        If one item is available and timeout is hit, return whatever is available until that time

        :param n:
        :return:
        """
        # MOCK IMPLEMENTATION not according to what in comments
        return [self.queue.get() for _ in range(n)]

