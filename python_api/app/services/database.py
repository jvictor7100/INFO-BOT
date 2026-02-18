from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def create_task(user_id: str, description: str, due_date: datetime=None):

    user = supabase.table("users").select("*").eq("id", user_id).execute()

    if not user.data:
        supabase.table("users").insert({"id": user_id}).execute()

    data = {
        "user_id": user_id,
        "description": description,
    }

    if due_date:
        data["due_date"] = due_date.isoformat()

    new_task = supabase.table("tasks").insert(data).execute()

    return new_task.data


def list_tasks(user_id: str):

    tasks = supabase.table("tasks") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("due_date") \
        .execute()

    return tasks.data


def complete_task(task_id: str):

    task = supabase.table("tasks") \
        .update({"completed": True}) \
        .eq("id", task_id) \
        .execute()

    return task.data


def delete_task(task_id: str):

    response = supabase.table("tasks") \
        .delete() \
        .eq("id", task_id) \
        .execute()

    return response
