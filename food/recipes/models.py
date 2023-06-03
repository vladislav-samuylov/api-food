from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Recipes(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    anons = models.CharField(max_length=500, verbose_name="Анонс")
    content = models.TextField(verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')
    ingredients = models.ManyToManyField('Ingredient', verbose_name='Ингредиенты')
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=True, verbose_name='Автор')
    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        ordering = ['-time_create']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Ingredient(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Ингредиент')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredients', kwargs={'ingredients_slug': self.slug})

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']