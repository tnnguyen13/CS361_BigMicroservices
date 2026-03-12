# CS361_BigMicroservices

## Climbing Microservice

The climbing microservice helps the user track climbs, and uses ZeroMQ for communication.

1. Install dependencies (pip install -r requirements.txt)
2. Run server.py
3. import client.py into your script (see below code)
4. Reset the database as needed with clear_db.py.

```python
from client import ClimbingLogClient

with ClimbingLogClient() as client:
    # add a climb
    client.add("tee", "El Cap", "5.16", 10, location="El Capitan", attempts=1)

    # list climbs
    client.list("tee")

```

