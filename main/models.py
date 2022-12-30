from django.db import models

class User(models.Model):
    name = models.CharField('Имя пользователя', max_length=100, blank=True)
    chat_id = models.IntegerField('ID в Telegram')
    score = models.IntegerField('Счёт игрока в игре!', default=1)
    user_id = models.CharField('ID пользователя', max_length=100, blank=True)
    count_link = models.IntegerField('Переходы по ссылке', default=0)

    def __str__(self) -> str:
        return self.name