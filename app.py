import json
import os
from collections import Counter
from itertools import groupby
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


ROOT = Path(__file__).resolve().parent
TODOS_PATH = ROOT / "General" / "todos.json"
STATUS_LABELS = {
    "pending": "pending",
    "in_progress": "in progress",
    "done": "done",
    "blocked": "blocked",
}

app = Flask(__name__)


def load_todos() -> tuple[list[dict], str | None]:
    try:
        with TODOS_PATH.open("r", encoding="utf-8-sig") as handle:
            todos = json.load(handle)
    except FileNotFoundError:
        return [], "todos.json was not found."
    except json.JSONDecodeError:
        return [], "todos.json is not valid JSON."

    if not isinstance(todos, list):
        return [], "todos.json must contain a JSON list."

    normalized = []
    for index, todo in enumerate(todos, start=1):
        if not isinstance(todo, dict):
            continue
        normalized.append(
            {
                "number": index,
                "label": f"todo-{index:03d}",
                "title": str(todo.get("title", "")).strip() or f"Untitled todo {index}",
                "description": str(todo.get("description", "")).strip(),
                "status": str(todo.get("status", "pending")).strip() or "pending",
                "status_label": STATUS_LABELS.get(
                    str(todo.get("status", "pending")).strip() or "pending",
                    str(todo.get("status", "pending")).strip() or "pending",
                ),
                "priority": str(todo.get("priority", "medium")).strip() or "medium",
                "area": str(todo.get("area", "General")).strip() or "General",
                "group": str(todo.get("group", "Backlog")).strip() or "Backlog",
                "todo_today": bool(todo.get("todo_today", False)),
            }
        )

    return normalized, None


def read_raw_todos() -> list[dict]:
    with TODOS_PATH.open("r", encoding="utf-8-sig") as handle:
        todos = json.load(handle)
    if not isinstance(todos, list):
        raise ValueError("todos.json must contain a JSON list.")
    return todos


def write_raw_todos(todos: list[dict]) -> None:
    with TODOS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(todos, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


@app.route("/")
def home():
    todos, error = load_todos()
    status_counts = Counter(todo["status"] for todo in todos)
    priority_counts = Counter(todo["priority"] for todo in todos)
    area_counts = Counter(todo["area"] for todo in todos)
    group_counts = Counter(todo["group"] for todo in todos)
    today_count = sum(1 for todo in todos if todo["todo_today"])
    grouped_todos = [
        {"area": area, "todos": list(area_todos)}
        for area, area_todos in groupby(
            sorted(todos, key=lambda todo: (todo["area"], todo["group"], todo["number"])),
            key=lambda todo: todo["area"],
        )
    ]

    return render_template(
        "index.html",
        todos=todos,
        grouped_todos=grouped_todos,
        error=error,
        total_count=len(todos),
        status_counts=dict(sorted(status_counts.items())),
        priority_counts=dict(sorted(priority_counts.items())),
        area_counts=dict(sorted(area_counts.items())),
        group_counts=dict(sorted(group_counts.items())),
        today_count=today_count,
        status_labels=STATUS_LABELS,
    )


@app.post("/todos/<int:todo_index>/today")
def update_todo_today(todo_index: int):
    todos = read_raw_todos()
    if 0 <= todo_index < len(todos):
        todos[todo_index]["todo_today"] = request.form.get("todo_today") == "true"
        write_raw_todos(todos)
    return redirect(url_for("home"))


@app.post("/todos/<int:todo_index>/status")
def update_todo_status(todo_index: int):
    todos = read_raw_todos()
    status = request.form.get("status", "").strip()
    if 0 <= todo_index < len(todos) and status:
        todos[todo_index]["status"] = status
        write_raw_todos(todos)
    return redirect(url_for("home"))


if __name__ == "__main__":
    port = int(os.getenv("HT_BRAIN_PORT", "5001"))
    app.run(debug=False, port=port)
