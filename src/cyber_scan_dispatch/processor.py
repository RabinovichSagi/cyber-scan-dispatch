import logging
from multiprocessing import Process, Queue
from typing import Union, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.cyber_scan_dispatch.db import DatabaseEngine
from src.cyber_scan_dispatch.db_models import ScanJob
from src.cyber_scan_dispatch.mock_cache import MockCache
from src.cyber_scan_dispatch.mock_queue import MockScanJobQueue
from src.cyber_scan_dispatch.mock_scanner import MockScanner


def _set_scan_job_status(session, mock_status_cache: MockCache, scan_jobs, status):
    for s in scan_jobs:  # may not produce the most optimal update but let's leave it for now
        s.status = status

    session.commit()

    # here i update the cache after commit so cache failures won't fail the status update
    # we can use some TTL per value in the cache so in case there is a mismatch between cache value and the database because of such cases,
    # the cache, it wont be for long, or some other technique
    for s in scan_jobs:
        mock_status_cache.put(key=s.id, value=s.status)


def _process_scan_job(session: Session, scanner: MockScanner, scan_job_ids: List[str]):
    scan_jobs: Union[List[ScanJob], None] = None
    try:
        logging.debug(f'starting to scan jobs {scan_job_ids} ')
        scan_jobs = list(session.scalars(select(ScanJob).where(ScanJob.id.in_(scan_job_ids))))

        _set_scan_job_status(session, scan_jobs, "Running")

        logging.debug(f'completed scan jobs {scan_job_ids} ')

        scanner.scan(scan_jobs)
        _set_scan_job_status(session, scan_jobs, "Completed")
    except Exception as e:
        # Assuming here that is one scan fails then we fail all.
        # we can try one by one or have the mock report on specific failed scans, etc.
        logging.exception(f"Error processing scan ids: {scan_job_ids}", e)
        if scan_jobs:
            _set_scan_job_status(session, scan_jobs, "Error")


def _process_worker(share_queue, batch_size, batch_timeout):
    job_queue = MockScanJobQueue(share_queue)
    mock_scanner = MockScanner()
    with Session(DatabaseEngine.engine()) as session:
        while True:
            scan_job_ids = job_queue.dequeue(batch_size,
                                             batch_timeout=batch_timeout)  # assume blocking until an item is available an
            _process_scan_job(session, mock_scanner, scan_job_ids)


def processor(num_workers, batch_size, batch_timeout):
    processes = []
    q = Queue()
    for _ in range(num_workers):
        p = Process(target=_process_worker, args=(q, batch_size, batch_timeout,))
        p.start()
        processes.append(p)

    # join just for a clean shutdown
    for p in processes:
        p.join()


if __name__ == "__main__":
    processor(2, 1, 1)  # TODO: read from config or environment variables
