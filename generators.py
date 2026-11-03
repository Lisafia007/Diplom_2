import random
import string



def create_new_user():
   random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
   return {
      "email": f"{random_string}@yandex.ru",
      "password": random_string,
      "name": random_string
   }

