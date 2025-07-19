"""Google Calendar agent using Langchain"""

from __future__ import annotations

import datetime as dt
from typing import List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from langchain_community.llms import OpenAI


class GoogleCalendarAgent:
    """Agent for interacting with Google Calendar."""

    def __init__(self, credentials: Credentials, llm: Optional[OpenAI] = None, calendar_id: str = "primary") -> None:
        self.creds = credentials
        self.service = build("calendar", "v3", credentials=credentials)
        self.calendar_id = calendar_id
        self.llm = llm or OpenAI()

    def create_event(self, summary: str, start: dt.datetime, end: dt.datetime, **kwargs) -> str:
        event = {
            "summary": summary,
            "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": end.isoformat()},
            **kwargs,
        }
        created = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        return created.get("id")

    def update_event(self, event_id: str, **updates) -> None:
        event = self.service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()
        event.update(updates)
        self.service.events().update(calendarId=self.calendar_id, eventId=event_id, body=event).execute()

    def delete_event(self, event_id: str) -> None:
        self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()

    def reschedule_event(
        self,
        event_id: str,
        new_start: dt.datetime,
        new_end: dt.datetime,
        **updates,
    ) -> None:
        """Change the time of an existing event."""
        updates.setdefault("start", {"dateTime": new_start.isoformat()})
        updates.setdefault("end", {"dateTime": new_end.isoformat()})
        self.update_event(event_id, **updates)

    def _list_events(self, time_min: dt.datetime, time_max: dt.datetime):
        return (
            self.service.events()
            .list(calendarId=self.calendar_id, timeMin=time_min.isoformat(), timeMax=time_max.isoformat(), singleEvents=True, orderBy="startTime")
            .execute()
            .get("items", [])
        )

    def find_time_gaps(self, start: dt.datetime, end: dt.datetime) -> List[tuple[dt.datetime, dt.datetime]]:
        events = self._list_events(start, end)
        gaps = []
        cursor = start
        for ev in events:
            ev_start = dt.datetime.fromisoformat(ev["start"]["dateTime"])
            if ev_start > cursor:
                gaps.append((cursor, ev_start))
            cursor = dt.datetime.fromisoformat(ev["end"]["dateTime"])
        if cursor < end:
            gaps.append((cursor, end))
        return gaps

    def daily_summary(self, date: dt.date) -> str:
        start = dt.datetime.combine(date, dt.time.min)
        end = dt.datetime.combine(date, dt.time.max)
        events = self._list_events(start, end)
        text = "\n".join(f"- {e['summary']}" for e in events)
        prompt = f"Summarize today's schedule:\n{text}"
        return self.llm(prompt)

    def task_list(self, date: dt.date) -> str:
        summary = self.daily_summary(date)
        prompt = f"Provide a list of tasks for the day based on the following schedule summary:\n{summary}"
        return self.llm(prompt)
