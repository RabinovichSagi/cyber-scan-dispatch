import uvicorn as uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session

from db import DatabaseEngine
from db_models import ScanJob
from mock_cache import MockCache

app = FastAPI()

# some amazing thread-safe caching service
job_status_cache = MockCache()


@app.get("/status/{scan_id}")
def check_status(scan_id: str):
    # we can use a caching mechanism in case we want to avoid query overload to the DB.
    # we can keep the statuses for a maximum of 20 minutes according to requirements
    status = job_status_cache.get(scan_id)

    if not status:
        with Session(DatabaseEngine.engine()) as session:
            scan_job = session.query(ScanJob).get(scan_id)
            if scan_job:
                status = scan_job.status
            else:
                # NOTE: returning a 404 status code require throwing an HTTPException
                # which will change the format of the response, to something other than what is requested.
                status = "Not-Found"
    return status


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8011)
