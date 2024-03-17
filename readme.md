# Project Setup

To initialize and run this project locally, you can follow these steps:

Clone the project repository from GitHub:

```shell
git clone https://github.com/username/repo.git
```

Install the required dependencies using pip:


```shell
pip install -r requirements.txt
```

Set the OpenAI API key in the `open_ai_key` variable in the code. You can obtain an API key from the OpenAI website.

Run the FastAPI server:

```shell
uvicorn main:app --reload
```

Access the API endpoints using a web browser or an API testing tool like Postman.

- To check if the server is running, visit `http://localhost:8000/` in your browser. You should see a message saying "Grokker backend is up and running!".

- To get a grok pattern for a plain text log line, send a POST request to `http://localhost:8000/grok` with the log line in the request body as JSON. For example:

```json
POST /grok
Content-Type: application/json

{
  "text": "This is a log line."
}
```

The response will be the generated grok pattern in JSON format.

```json
[
  {
    "pattern": "\\[%{TIMESTAMP_ISO8601:timestamp}\\] %{LOGLEVEL:loglevel}  \\[%{DATA:source}\\]: \\[pid:%{NUMBER:pid}\\] %{DATA:message} \\[ssrc:%{NUMBER:ssrc}, payloadType:%{NUMBER:payloadType}\\]",
    "confidence": 0.85
  },
  {
    "pattern": "\\[%{TIMESTAMP_ISO8601:logdate}\\] %{WORD:loglevel}  \\[%{NOTSPACE:info}\\]: \\[pid:%{NUMBER:process_id}\\] %{GREEDYDATA:log_message} \\[ssrc:%{NUMBER:ssrc}, payloadType:%{NUMBER:payloadType}\\]",
    "confidence": 0.75
  }
]

```