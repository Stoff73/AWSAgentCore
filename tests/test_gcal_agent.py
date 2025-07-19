import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.gcal_agent import GoogleCalendarAgent


def test_agent_import():
    assert GoogleCalendarAgent is not None


def test_has_reschedule():
    assert hasattr(GoogleCalendarAgent, "reschedule_event")
