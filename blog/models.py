from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=50, verbose_name='Слаг')
    content = models.TextField(verbose_name='Содержание статьи')
    photo = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
