import os


def api_prefix():
    return "https://api.float.com/v3"

def api_key():
    return os.getenv("FLOAT_API_KEY")