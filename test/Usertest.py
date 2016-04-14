import sys
sys.path.append('..')
from app.main import models

user = models.User(id=000001,email="eclipse_sv@163.com",
					username="wm",password="abc@123",
					location="whu")

models.User.generate_fake(100)
