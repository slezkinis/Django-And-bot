from django.db import models

class User(models.Model):
    name = models.CharField('Имя пользователя', max_length=100)
    chat_id = models.IntegerField('ID в Telegram')

    def __str__(self) -> str:
        return self.name