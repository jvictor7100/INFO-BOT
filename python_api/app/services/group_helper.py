standardResponse = 'Não foi possível executar esse comando'

def process_user_message(message: str) -> str:
    response = ''

    if message == 'ping':
        response = 'pong'
    else:
        response = standardResponse
    
    return response

def process_admin_message(message: str) -> str:
    response = process_user_message(message)

    if response == standardResponse:
        
        if message == 'admin':
            response = 'Você tem permição de administrador'

    return response
