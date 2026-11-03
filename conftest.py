import pytest
import random
import requests
from helpers import delete_user, get_ingredients, register_and_get_auth_token
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

# Фикстура возвращает тело запроса для создания заказа с хэшем ингридиента(ов) 
@pytest.fixture
def get_payload():
   ingredients_data = get_ingredients()
   max_ingredients = len(ingredients_data['data']) - 1

   def _generate_payload(*indices):
      if not indices:
         random_index = random.randint(0, max_ingredients)
         indices = [random_index]

      ing_ids = [ingredients_data['data'][ind]['_id'] for ind in indices]
      return {"ingredients": [ing_ids]}
   return _generate_payload