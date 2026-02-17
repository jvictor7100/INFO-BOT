from app.services.database import create_task, list_tasks, complete_task, delete_task
from datetime import datetime

standardResponse = 'Não foi possível executar esse comando.'

commands = {
    'create_task': 'addtask',
    'list_tasks': 'ls',
    'complete_task': 'complete',
    'delete_task': 'del',
}

def process_user_message(user_id: str, message: str) -> str:
    def get_task_id_by_index(user_id: str, index: int):
        tasks = list_tasks(user_id)
        task_id = None

        if index >= 1 and index <= len(tasks):
            task_id = tasks[index - 1]['id']

        return task_id
    
    response = ''

    request = message.strip().lower().split()

    if not request:
        return standardResponse

    command = request[0]

    try:
        if command == commands['create_task']:
            # Exemplo:
            # addtask estudar_python 2026-02-20T18:00:00

            if len(request) < 3:
                return f"Formato: {commands['create_task']} <descricao> <data_iso>"

            # TO-DO: Pedir a descrição entre aspas
            # TO-DO: Facilitar a inserção da data de expiração
            description = request[1]
            expiry_date = datetime.fromisoformat(request[2])

            status = create_task(user_id, description, expiry_date)
            response = "✅ Tarefa criada com sucesso."

        elif command == commands['list_tasks']:
            tasks = list_tasks(user_id)

            if not tasks:
                return "📭 Você não tem tarefas pendentes."

            lines = []
            for index, task in enumerate(tasks, start=1):
                lines.append(
                    f"{index} - {task['description']} (Expira: {task['expiry_date']})"
                )

            response = "\n".join(lines)

        elif command == commands['complete_task']:
            if len(request) < 2:
                return f"Formato: {commands['complete_task']} <índice>"

            index = int(request[1])
            task_id = get_task_id_by_index(user_id, index)

            if not task_id:
                return "❌ Índice inválido."

            status = complete_task(task_id)
            response = "✅ Tarefa marcada como concluída."

        elif command == commands['delete_task']:
            if len(request) < 2:
                return f"Formato: {commands['delete_task']} <índice>"
            
            index = int(request[1])
            task_id = get_task_id_by_index(user_id, index)

            if not task_id:
                return "❌ Índice inválido."
            
            status = delete_task(task_id)
            response = status['message']

        else:
            response = standardResponse

    except Exception:
        response = "Erro ao executar comando."

    return response


def process_admin_message(user_id: str, message: str) -> str:
    response = process_user_message(user_id, message)

    if response == standardResponse:
        pass

    return response
