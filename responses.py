import random

def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == 'hello':
        return 'hey there'
    
    if p_message == 'roll':
        return str(random.randint(1, 20))
    
    if p_message == '!help':
        return "`This is a help message to modify`"
    
    return "WHAT WAS THAT, SONNY??"