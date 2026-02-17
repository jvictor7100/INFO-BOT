from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def create_task(user_id: str, description: str, expiry_date: datetime):

    user = supabase.table("users").select("*").eq("id", user_id).execute()

    if not user.data:
        supabase.table("users").insert({"id": user_id}).execute()

    new_task = supabase.table("tasks").insert({
        "user_id": user_id,
        "description": description,
        "expiry_date": expiry_date.isoformat()
    }).execute()

    return new_task.data


def list_tasks(user_id: str):

    task = supabase.table("tasks") \
        .select("*") \
        .eq("user_id", user_id) \
        .eq("completed", False) \
        .order("expiry_date") \
        .execute()

    return task.data


def complete_task(task_id: str):

    task = supabase.table("tasks") \
        .update({"completed": True}) \
        .eq("id", task_id) \
        .execute()

    return task.data


def delete_task(task_id: str):
    res = {"message": ""}

    response = supabase.table("tasks") \
        .delete() \
        .eq("id", task_id) \
        .execute()
    
    if response:
        res["message"] = "🗑️ Tarefa deletada com sucesso!"
    else:
        res["message"] = "Não foi possível deletar essa tarefa."

    return res
