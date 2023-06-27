import random
import time


class MockScanner:

    def scan(self, scan_target):
        if random.randint(0, 10) < 7:
            time.sleep(random.randint(3, 6))
        else:
            raise RuntimeError("Oops... completely unexpected error")
        return True
