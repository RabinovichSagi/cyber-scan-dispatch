import uuid
from multiprocessing import Queue

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import DatabaseEngine
from db_models import ScanJob
from mock_queue import MockScanJobQueue

app = FastAPI()


class ScanRequest(BaseModel):
    scan_target: str


def _dispatch_scan(session: Session, mock_queue, request: ScanRequest):
    scan_id = str(uuid.uuid4())

    # NOTE: need to wrap errors here with user facing errors
    scan_job = ScanJob(id=scan_id, status='Accepted', target=request.scan_target)
    session.add(scan_job)
    session.commit()

    try:
        mock_queue.enqueue(scan_id)
    except Exception as e:
        scan_job.status = 'Error'
        session.commit()

    return scan_id


@app.post("/scan")
def scan(request: ScanRequest):
    mock_queue = MockScanJobQueue(
        Queue())  # in reality this will use some real queue, in this case all is lost when request is done.
    with Session(DatabaseEngine.engine()) as session:
        scan_id = _dispatch_scan(session, mock_queue, request)
    return scan_id


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8010)

    # Invoke-RestMethod -Uri http://127.0.0.1/scan -Method POST -ContentType "application/json" -Body '{"scan_target": "some-company"}'
