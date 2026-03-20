from pathlib import Path

from app.services.task_manager.handlers import *


base_dir = Path(__file__).resolve().parent
commands_file = base_dir.parent / "commands.json"
with open(commands_file, "r", encoding="utf-8") as file:
    commands = json.load(file)['task_manager']


def process_order(user_id: str, order: list) -> str:
    command = order[0].lower()

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
        response = ''

        handler_parameters = handler.__code__.co_varnames[:handler.__code__.co_argcount]

        if not handler_parameters:
            response = handler()
        elif all(p in handler_parameters for p in ('user_id', 'order')):
            response = handler(user_id, order)
        elif 'user_id' in handler_parameters:
            response = handler(user_id)
        
        return response
    except Exception as e:
        print("Erro interno: ", e)
        return "Ocorreu um erro interno ao processar a sua mensagem."
