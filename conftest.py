import pytest
import requests
from helpers import delete_user, register_and_get_auth_token, get_token
from generators import create_new_user
from data import URLS, ENDPOINTS



# Фикстура регистрирует пользователя и удаляет созданного польззователя после теста
@pytest.fixture
def register_and_auto_delete():
   payload = create_new_user()
   response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_USER}', data=payload)
   token = response.json().get("accessToken")

   yield payload

   if token:
      delete_user(token)

# Фикстура возвращает токен зарегистрированного пользователя, после теста пользователь удаляется
@pytest.fixture
def get_user_headers_and_auto_delete():
   token = register_and_get_auth_token()
   headers = {"Authorization": token}

   yield headers
   if token:
      delete_user(token)

# Фикстура для тестов регистрации - удаляет пользователя после теста
@pytest.fixture
def auto_delete_created_user():
   user_data = {}  
   yield user_data

   if "email" in user_data and "password" in user_data:
      token = get_token(user_data["email"], user_data["password"])
      if token:
         delete_user(token)
