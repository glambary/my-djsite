from django.db import models
from django.urls import reverse


# Create your models here.
# Первичная модель
class Departure(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Имя')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return reverse('departure', kwargs={'departure_id': self.pk})
        return reverse('departure', kwargs={'departure_slug': self.slug})

    class Meta:
        # отображение в админке
        verbose_name = 'Отправление'
        verbose_name_plural = 'Отправления'
        ordering = ['id']


# Вторичная модель
class Travel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок') # verbose_name - подпись в админке и БД
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Контент') # blank=True - может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото') # upload_to - описывает шаблон загрузки изображений на сервер,
# photos/%Y/%m/%d/ - описывает вложенные папки как год, месяц, день!!! По умолчанию пустая строка
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания') # auto_now_add=True принимает текущее время и никогда больше не меняется
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения') # auto_now=True меняется каждый раз, когда изменяется что либо в записи
    is_published = models.BooleanField(default=True, verbose_name='Публикация') # default=True по умолчанию будет заполнено True
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    duration = models.CharField(max_length=50, verbose_name='Продолжительность')
    dep = models.ForeignKey(Departure, on_delete=models.PROTECT, verbose_name='Отправление')

    def __str__(self):
        return f'{self.title} - ({self.pk})'

    def get_absolute_url(self):
        return reverse('tour', kwargs={'tour_slug': self.slug})

    class Meta:
        # отображение в админке
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'
        #ordering = ['-time_create', 'title']
        ordering = ['id']


