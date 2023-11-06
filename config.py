import os

host = '192.168.100.9'
#host = '10.10.16.2'
user = 'postgres'
password = 'postgres'
bd_name = 'main_avito_django_bot'
port = '5432'

# api_reg = os.getenv("API_BOT_161")#.split(":")
# api_bot_reg = api_reg.split(":")
# bot_login = api_bot_reg[0]
# api_key = api_bot_reg[1]
# token = api_reg
# chat_id = bot_login

params = {
    'host': '192.168.100.9',
    #'host': '10.10.16.2',
    'port': 5432,
    'dbname': 'main_avito_django_bot',
    'user': 'postgres',
    'password': 'postgres'
}


# config(
# dbname = bd_name,
# user = user,
# host = host,
# password = password
#  )

# config = {
#     'host': host,
#     'user': user,
#     'password': password,
#     'database': bd_name,
#     'token': api_reg,
# }


"""
sql:

CREATE DATABASE realty
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
"""

#import os
#from urllib.parse import urlparse
#import urllib
#print(os.getenv("API_BOT_161"))
#print(os.environ.get("API_BOT_161"))

# api_reg = os.getenv("API_BOT_161")#.split(":")
# api_bot_reg = api_reg.split(":")
# bot_login = api_bot_reg[0]
# api_key = api_bot_reg[1]
#print(f"login {bot_login}, api {api_key}")
#print(f"token {token}, api {api_key}, chat_id {chat_id}")
