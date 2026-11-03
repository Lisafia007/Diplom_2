import requests
import allure
from data import URLS, ENDPOINTS


class TestOrderCreation:

   @allure.title("Проверка успешного создания заказа авторизованным пользователем")   
   @allure.description("Авторизуемся зарегистрированными данными пользователя, выбираем ингредиент и создаём заказ")
   def test_create_order_with_authorization(self, get_user_headers_and_auto_delete, get_payload):
      headers = get_user_headers_and_auto_delete
      payload = get_payload()
      with allure.step("Отправка POST-запроса на создание заказа"):
         response_ing = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_ORDER}', data=payload, headers=headers)
         assert response_ing.status_code == 200
         assert "number" in response_ing.json()["order"]


   @allure.title("Проверка создания заказа без авторизации пользователя")   
   @allure.description("Не авторизовываясь, выбираем ингредиент и создаём заказ")
   def test_create_order_without_authorization(self, get_payload):
      payload = get_payload()
      with allure.step("Отправка POST-запроса на создание заказа"):
         response_ing = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_ORDER}', data=payload)
         assert response_ing.status_code == 200
         assert "number" in response_ing.json()["order"]


   @allure.title("Проверка создания заказа с ингредиентами (списком)")   
   @allure.description("Выбираем ингредиенты и создаём заказ")
   def test_create_order_with_ingredients(self, get_payload):

      payload = get_payload(1, 2, 3)

      with allure.step("Отправка POST-запроса на создание заказа"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_ORDER}', data=payload)
         assert response.status_code == 200
         assert "number" in response.json()["order"]


   @allure.title("Проверка создания заказа без ингредиентов")   
   @allure.description("Создаём заказ, не выбирая ингредиенты")
   def test_create_order_without_ingredients(self):

      with allure.step("Отправка POST-запроса на создание заказа"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_ORDER}')
         assert response.status_code == 400
         assert "Ingredient ids must be provided" in response.json()["message"]


   @allure.title("Проверка создания заказа с указанием неверным хешем ингредиента")   
   @allure.description("Указываем неверный хеш ингредиента и создаём заказ")
   def test_create_order_with_incorrect_ingredients(self, get_payload):
      payload = get_payload()
      with allure.step("Извлекаем id ингредиента и делаем его неверным"):
         correct_id = payload["ingredients"][0]
         incorrect_id = f"{correct_id}d"
         payload_ing = {
            "ingredients": [incorrect_id]
         }

      with allure.step("Отправка POST-запроса на создание заказа"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_ORDER}', data=payload_ing)
         assert response.status_code == 500