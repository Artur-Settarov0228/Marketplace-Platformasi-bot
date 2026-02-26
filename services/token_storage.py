user_tokens = {}

def save_token(telegram_id, token):
    user_tokens[telegram_id] = token

def get_token(telegram_id):
    return user_tokens.get(telegram_id)