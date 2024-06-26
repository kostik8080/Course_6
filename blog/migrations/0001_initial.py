# Generated by Django 5.0.3 on 2024-04-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('slug', models.SlugField(verbose_name='Слаг')),
                ('content', models.TextField(verbose_name='Содержание статьи')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='blog/%d/%m/%Y', verbose_name='Изображение')),
                ('count_views', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество просмотров')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
        ),
    ]
