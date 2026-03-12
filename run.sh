#!/bin/bash
uv run granian test_task.main:app --interface asgi --host 0.0.0.0 --port 8080 --reload
