import pytest
import requests
import allure
from data import URLS, ENDPOINTS

class TestUserLogin:

   @allure.title("Проверка успешной авторизации")   
   @allure.description("Авторизуемся зарегистрированными данными пользователя")
   def test_successful_authorization(self, register_and_auto_delete):   
      existing_payload = register_and_auto_delete

      payload = {
         "email": existing_payload["email"],
         "password": existing_payload["password"]
      }

      with allure.step("Отправка POST-запроса на авторизацию пользователя"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_USER_AUTHORIZATION}', data=payload)
         assert response.status_code == 200
         assert response.json().get("success") is True



   @allure.title("Проверка авторизации при вводе неправильных данных")   
   @allure.description("Вводим данные для авторизации с вариантами неправильно указанных логина/пароля")
   @pytest.mark.parametrize("field, wrong_value", [
    ("email", "WrongAddress@yandex.ru"),
    ("password", "WrongPassword87"),
])
   def test_wrong_login_or_pass(self, field, wrong_value, register_and_auto_delete):
      existing_payload = register_and_auto_delete
      
      payload = {
         "email": existing_payload["email"],
         "password": existing_payload["password"]
      }

      payload[field] = wrong_value

      with allure.step("Отправка POST-запроса на авторизацию пользователя с неправильными данными"):
         response = requests.post(f'{URLS.BASE_URL}{ENDPOINTS.ENDPOINT_USER_AUTHORIZATION}', data = payload)

         assert response.status_code == 401
         assert "email or password are incorrect" in response.json()["message"]