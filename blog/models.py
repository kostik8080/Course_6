from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=50, verbose_name='Слаг')
    content = models.TextField(verbose_name='Содержание статьи')
    photo = models.ImageField(upload_to='blog/%d/%m/%Y', verbose_name='Изображение', **NULLABLE)
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
