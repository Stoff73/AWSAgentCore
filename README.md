# AWSAgentCore

This repository demonstrates an agent that integrates with Google Calendar using the [LangChain](https://github.com/hwchase17/langchain) framework. It provides helper methods to create, update, and delete calendar events, find free time gaps, and generate daily summaries and task lists with an LLM.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure Google Calendar API credentials. You can use OAuth credentials stored in `token.json` or any other method supported by `google-api-python-client`.
3. Set environment variables for your LLM provider (e.g., `OPENAI_API_KEY`).

## Usage
Create an instance of `GoogleCalendarAgent` by passing valid Google credentials. Then call the provided methods to manage calendar events or generate summaries. Example:
```python
from google.oauth2.credentials import Credentials
from agent.gcal_agent import GoogleCalendarAgent

creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/calendar"])
agent = GoogleCalendarAgent(creds)

# create a new event
agent.create_event("Meeting", start_datetime, end_datetime)

# reschedule the event
agent.reschedule_event(event_id, new_start, new_end)
```

## Deploying to AWS Bedrock AgentCore
The code here is designed to be used in the AWS Bedrock AgentCore serverless environment. Package the repository and deploy it following the Bedrock documentation. Ensure that your environment contains the proper credentials and API keys.
