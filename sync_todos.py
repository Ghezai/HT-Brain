import hashlib
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client


ROOT = Path(__file__).resolve().parent
TODOS_PATH = ROOT / "General" / "todos.json"
REQUIRED_ENV = [
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
    "SUPABASE_USER_EMAIL",
    "SUPABASE_USER_PASSWORD",
    "GMULTI_ORGANIZATION_ID",
]


def load_required_env() -> dict[str, str]:
    load_dotenv(ROOT / ".env")
    values = {name: os.getenv(name, "").strip() for name in REQUIRED_ENV}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise ValueError("Missing required environment values: " + ", ".join(missing))
    return values


def load_todos() -> list[dict]:
    with TODOS_PATH.open("r", encoding="utf-8") as handle:
        todos = json.load(handle)

    if not isinstance(todos, list):
        raise ValueError("todos.json must contain a JSON list.")

    for index, todo in enumerate(todos, start=1):
        if not isinstance(todo, dict):
            raise ValueError(f"Todo #{index} must be an object.")
        if not str(todo.get("title", "")).strip():
            raise ValueError(f"Todo #{index} is missing a title.")

    return todos


def make_external_key(organization_id: str, user_id: str, title: str) -> str:
    key_source = "|".join([organization_id, user_id, title.strip().lower()])
    return hashlib.sha256(key_source.encode("utf-8")).hexdigest()


def build_payloads(todos: list[dict], organization_id: str, user_id: str) -> list[dict]:
    payloads = []
    for todo in todos:
        title = str(todo["title"]).strip()
        payloads.append(
            {
                "title": title,
                "description": str(todo.get("description", "")).strip(),
                "status": str(todo.get("status", "pending")).strip() or "pending",
                "priority": str(todo.get("priority", "medium")).strip() or "medium",
                "organization_id": organization_id,
                "created_by": user_id,
                "user_id": user_id,
                "source": "vscode-codex",
                "external_key": make_external_key(organization_id, user_id, title),
            }
        )
    return payloads


def sync_todos() -> int:
    env = load_required_env()
    todos = load_todos()

    supabase = create_client(env["SUPABASE_URL"], env["SUPABASE_ANON_KEY"])
    auth_response = supabase.auth.sign_in_with_password(
        {
            "email": env["SUPABASE_USER_EMAIL"],
            "password": env["SUPABASE_USER_PASSWORD"],
        }
    )

    user = getattr(auth_response, "user", None)
    user_id = getattr(user, "id", None)
    if not user_id:
        raise RuntimeError("Supabase sign in did not return a user.")

    payloads = build_payloads(todos, env["GMULTI_ORGANIZATION_ID"], user_id)
    if payloads:
        supabase.table("todos").upsert(payloads, on_conflict="external_key").execute()

    print(f"Todo sync completed successfully. Synced {len(payloads)} todo(s).")
    return 0


def main() -> int:
    try:
        return sync_todos()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Todo sync failed: {error}", file=sys.stderr)
        return 1
    except Exception:
        print("Todo sync failed. Check Supabase credentials, table permissions, and todos schema.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
