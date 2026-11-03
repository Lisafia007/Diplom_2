import pytest
import requests
import allure
from data import URLS, ENDPOINTS
from generators import create_new_user

class TestUserCreation:

   @allure.title("Проверка успешного создания уникального пользователя")   
   @allure.description("Создаём пользователя с уникальными данными")
   def test_create_user(self):
      payload = create_new_user()

      with allure.step("Отправка POST-запроса на создание уникального пользователя"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_USER}', data=payload)

      assert response.status_code == 200
      assert response.json().get("success") is True


   @allure.title("Проверка создания пользователя, который уже зарегистрирован")   
   @allure.description("Создаём пользователя, после регистрации пользователя с идентичными данными")
   def test_create_already_registered_user(self, register_and_auto_delete):
      
      existing_payload = register_and_auto_delete

      with allure.step("Отправка POST-запроса на создание дублирующего пользователя"):      
         response_second = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_USER}', data=existing_payload)
         assert response_second.status_code == 403
         assert "User already exists" in response_second.json()["message"]


   @allure.title("Проверка создания пользователя без заполнения одного из обязательных полей")   
   @allure.description("Создаём пользователя с отсутствием одного из обязательных полей")
   @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
   def test_create_user_without_required_fields(self, missing_field):
      payload = create_new_user()

      del payload[missing_field]

      with allure.step("Отправка POST-запроса на создание пользователя без заполнения одного из обязательных полей"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_CREATE_USER}', data=payload)

         assert response.status_code == 403
         assert "Email, password and name are required fields" in response.json()["message"]
