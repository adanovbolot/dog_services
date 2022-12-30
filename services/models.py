from django.db import models


class ContentEmployee(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тема|', blank=True, null=True)
    content = models.TextField(verbose_name='Описание|', blank=True, null=True)
    img = models.ImageField(verbose_name='Картинка|', blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
