import requests
from generators import create_new_user
from data import URLS, ENDPOINTS




# Получение токена пользователя
def get_token(email, password):
      response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_USER_AUTHORIZATION}', data={"email": email, "password": password})
      return response.json().get("accessToken")
      
# Отправка DELETE-запроса на удаление пользователя
def delete_user(access_token):
   headers = {'Authorization': access_token}
   if access_token:
      requests.delete(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_USER_DELETION}', headers=headers)
   
# Получение ингредиента
def get_ingredients():
   ingredients = requests.get(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_GET_INGREDIENTS}')
   return ingredients.json()

def register_and_get_auth_token():
   payload = create_new_user()
    
   requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_USER}', data=payload)
   token = get_token(payload["email"], payload["password"])
    
   return token
