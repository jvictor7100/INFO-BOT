from app.services.database import create_task, list_tasks, complete_task, delete_task
from datetime import datetime
import shlex
import dateparser

standardResponse = 'Não foi possível executar esse comando.'

commands = {
    'create_task': 'addtask',
    'list_tasks': 'ls',
    'complete_task': 'complete',
    'delete_task': 'del',
    'help': 'help'
}


def handle_help(user_id, parts):
    return (
        "🤖 *Guia de Uso do INFO-BOT*\n\n"
        "📌 *Criar tarefa*\n"
        f'Formato: {commands["create_task"]} "[descrição da tarefa]" [data opcional]\n\n'
        "Exemplos:\n"
        f'{commands["create_task"]} "Estudar matemática"\n'
        f'{commands["create_task"]} "Prova de Tufão" 25/02/2026\n'
        f'{commands["create_task"]} "Trabalho de Geografia" amanhã\n'
        f'{commands["create_task"]} "Atividade de filosofia" em 3 dias\n\n'
        "📋 *Listar tarefas*\n"
        f'Formato: {commands["list_tasks"]}\n\n'
        "✅ *Marcar como concluída*\n"
        f'Formato: {commands["complete_task"]} [NÚMERO]\n\n'
        f'Ex.: {commands["complete_task"]} 1\n\n'
        "🗑️ *Remover tarefa*\n"
        f'Formato: {commands["delete_task"]} [NÚMERO]\n\n'
        f'Ex.: {commands["delete_task"]} 2'
    )


def parse_date(date_str: str):

    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        pass

    parsed = dateparser.parse(date_str, languages=['pt'])

    return parsed.date() if parsed else None


def extract_parts(message: str):
    try:
        return shlex.split(message)
    except ValueError:
        return None
    

def handle_addtask(user_id, parts):
    if len(parts) < 2:
        return f'Use: {commands["create_task"]} "descrição da tarefa" [data opcional]'

    description = parts[1].strip()

    if not description:
        return "A descrição da tarefa não pode estar vazia."

    due_date = None

    if len(parts) > 2:
        date_text = " ".join(parts[2:])
        due_date = parse_date(date_text)

        if not due_date:
            return "❌ Data inválida."

    try:
        data = create_task(user_id, description, due_date=due_date)

        if not data:
            return "❌ Não foi possível criar a tarefa."

        if due_date:
            return f"✅ Tarefa criada com sucesso!\n\n📌 {description}\n📅 Vence em: {due_date.strftime('%d/%m/%Y')}"
        else:
            return f"✅ Tarefa criada com sucesso!\n\n📌 {description}\n📅 Vence em: [SEM VENCIMENTO]"

    except Exception:
        return "❌ Erro ao criar tarefa."


def handle_list(user_id, parts):
    try:
        tasks = list_tasks(user_id)

        if not tasks:
            return "📭 Você não possui tarefas cadastradas."

        response_lines = ["📋 Suas tarefas:\n"]

        for index, task in enumerate(tasks, start=1):
            status = "✅" if task.get("completed") else "⏳"

            description = task.get("description")

            due_date = task.get("due_date")
            if due_date:
                due_date = datetime.fromisoformat(due_date).strftime("%d/%m/%Y")
                line = f"{index}. {status} {description} (📅 {due_date})"
            else:
                line = f"{index}. {status} {description}"

            response_lines.append(line)

        return "\n".join(response_lines)

    except Exception:
        return "❌ Erro ao listar tarefas."


def handle_complete(user_id, parts):
    if len(parts) < 2:
        return f"Use: {commands['complete_task']} [número da tarefa]"

    try:
        index = int(parts[1])
    except ValueError:
        return "❌ O índice deve ser um número."

    tasks = list_tasks(user_id)

    if not tasks:
        return "📭 Você não possui tarefas."

    if index < 1 or index > len(tasks):
        return "❌ Índice inválido."

    task = tasks[index - 1]
    task_id = task["id"]

    if task.get("completed"):
        return "⚠️ Essa tarefa já está marcada como concluída."

    try:
        complete_task(task_id)
        return f"🎉 Tarefa concluída!\n📌 Descrição: {task['description']}"

    except Exception:
        return "❌ Erro ao concluir tarefa."


def handle_delete(user_id, parts):
    if len(parts) < 2:
        return f"Use: {commands['delete_task']} [número da tarefa]"

    try:
        index = int(parts[1])
    except ValueError:
        return "❌ O índice deve ser um número."

    tasks = list_tasks(user_id)

    if not tasks:
        return "📭 Você não possui tarefas."

    if index < 1 or index > len(tasks):
        return "❌ Índice inválido."

    task = tasks[index - 1]
    task_id = task["id"]

    try:
        delete_task(task_id)
        return f"🗑️ Tarefa removida!\n📌 Descrição: {task['description']}"

    except Exception:
        return "❌ Erro ao remover tarefa."
    

def process_user_message(user_id, message: str) -> str:
    if not message:
        return standardResponse

    parts = extract_parts(message)

    if not parts:
        return "Erro ao processar o comando."

    command = parts[0].lower()

    command_map = {
        commands['create_task']: handle_addtask,
        commands['list_tasks']: handle_list,
        commands['complete_task']: handle_complete,
        commands['delete_task']: handle_delete,
        commands['help']: handle_help
    }

    handler = command_map.get(command)

    if not handler:
        return "Comando não reconhecido."

    try:
        return handler(user_id, parts)
    except Exception as e:
        print("Erro interno: ", e)
        return standardResponse


def process_admin_message(user_id: str, message: str) -> str:
    response = process_user_message(user_id, message)

    if response == standardResponse:
        pass

    return response
