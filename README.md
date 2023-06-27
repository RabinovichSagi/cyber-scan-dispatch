# Cyber scan job dispatching system

## Architecture

The main components are 
* **ingest.py** - implements the ingest endpoint 
* **status.py** - implements the status endpoint
* **processor** - implements a simple consumer with multiprocessing with an option to do in bastes per process. i.e. each process can query for a batch of scan jobs and maybe the scanner has some optimization for it.

These services are intended to run in docker container on k8s with auto-scaling (specially for the processor) to handle spikes in workload.

The concurrency level can be tuned with batch size, number of processor per pod, and number of pod replicas.

The endpoints are implemented with fastapi.


## Things left out
- I did not clear the scan jobs from the DB, we can implement a cleaner job to do that and avoid exploding the database.
- The queue is just a mock and the items from the ingest won't really get processed.
- There is some degree of error handling just for demonstration
- There is some logging
- Not much input validation except what is given for free with fastapi, concurrency control, and security measures
- proper database session management. need to further validate that everything is committed/rollbacked and connection is closed as appropriate.
