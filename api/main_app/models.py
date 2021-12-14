from django.db import models


class TelegramUser(models.Model):
    username = models.CharField('Юзернейм телеграмм', max_length=127, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=127, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=127, blank=True, null=True)

    def __str__(self):
        return self.username or self.id

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Пользователи телеграм'
