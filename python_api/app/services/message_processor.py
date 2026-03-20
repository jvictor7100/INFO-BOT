import shlex

import app.services.task_manager.order_processor as task_manager

# TO-DO: verificar para qual serviço o pedido deve ser passado
def process_message(user_id, message):
    def extract_parts(message: str):
        try:
            return shlex.split(message)
        except ValueError:
            return None
    
    parts = extract_parts(message)

    if not parts:
        return "Ocorreu um erro ao processar a mensagem."
    
    return task_manager.process_order(user_id, parts)

if __name__ == '__main__':
    # para testes

    user_id = '278353156284433@lid'
    command = 'help'
    print(process_message(user_id, command))
