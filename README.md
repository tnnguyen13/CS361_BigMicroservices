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

## Report Exporter Microservice
This microservice converts application data into **CSV** or **Markdown table** format. It can be used by multiple main 
programs, such as the Personal Bucket List, Restaurant Finder, or Expense Tracker, as long as each main program sends
data in the required format.

### Start the Service
```bash
cd CS361_BigMicroservices
source venv/bin/activate
python report_exporter_microservice/report_exporter.py
```
The service runs at: `http://127.0.0.1:5002`

### API Endpoints 
#### Export to CSV
Endpoint: `POST /export/csv`

Example Request Body:
```json
{
  "items": [
    {"name": "Send a V6", "completed": true},
    {"name": "Walk 7K steps everyday for 2 weeks", "completed": true}
  ]
}
```
Example Response:
```text
name,completed
Send a V6,True
Walk 7K steps everyday for 2 weeks,True
```

#### Export to Markdown
Endpoint: `POST /export/markdown`

Example Request Body:
```json
{
  "items": [
    {"name": "Send a V6", "completed": true},
    {"name": "Walk 7K steps everyday for 2 weeks", "completed": true}
  ]
}
```
Example Response:
```markdown
| name | completed |
| --- | --- |
| Send a V6 | True |
| Walk 7K steps everyday for 2 weeks | True |
```

### How Main Programs Use This Microservice
A main program sends a POST request to either `/export/csv` or `/export/markdown` with a JSON body containing an
`"items"` field. The `"items"` field must contain a **list of dictionaries**, where each dictionary represents one 
record to export. The exporter will automatically detect all dictionary keys and use them as table columns. If an item
does not contain a particular key, that value is left blank in the exported output.



Example Python Call:
```python
import requests

data = {
    "items": [
        {"name": "Send a V6", "completed": True},
        {"name": "Walk 7K steps everyday for 2 weeks", "completed": True}
    ]
}

response = requests.post(
    "http://127.0.0.1:5002/export/csv",
    json=data
)

csv_output = response.text

with open("activities.csv", "w") as f:
    f.write(csv_output)
```
The main program can save `response.text` to a file such as `activities.csv` or `activities.md`.

### Example Integration With File Converter Microservice
1. Send application data to `/export/csv` or `/export/markdown`
2. Save returned text to a local file
3. Send that file path to the File Converter Microservice
