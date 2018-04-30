import os

# OS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# VK
AUTH_REDIRECT_URI = os.environ.get(
    'VK_AUTH_REDIRECT_URI',
    'https://rptp.herokuapp.com/auth'
)

APP_ID = os.environ['VK_APP_ID']
CLIENT_SECRET = os.environ['VK_CLIENT_SECRET']

API_VERSION = os.environ.get(
    'VK_API_VERSION',
    5.73
)

# MONGO
MONGO_URL = os.environ['MONGO_URL']
MONGO_DB = os.environ['MONGO_DB']
