from django.db import models
from django.utils.dateformat import *
from django.utils import timezone
import re

class PageBlock(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='page_blocks/', null=True, blank=True)
    content = models.TextField()
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.CharField(max_length=255, null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, null=True, blank=True)
    template = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Блок страницы'
        verbose_name_plural = 'Блоки страницы'

    def __str__(self):
        return self.title
    
class FeedBack(models.Model):
    phone = models.CharField(max_length=16, verbose_name="Телефон", null=True, blank=True, unique=True)
    name = models.CharField(max_length=50, verbose_name="Имя", null=True, blank=True, unique=True)
    email = models.CharField(max_length=80, verbose_name="email", null=True, blank=True, unique=True)
    text = models.CharField(max_length=500, verbose_name="Сообщение", null=True, blank=True)
    datetime_create = models.DateTimeField(default=timezone.now, verbose_name="Дата и время создания")
    complete = models.BooleanField(default=False, verbose_name="Отметка о выполнении")


    def save_phone(self, phone):
        phone = re.sub(r'\+?[78](\d{3})(\d{3})(\d\d)(\d\d)', r'+7\1\2\3\4', phone)
        if phone[0] == '9' and len(phone) == 10:
            phone = '+7' + phone

        self.phone = re.sub(r'\+?[78](\d{3})(\d{3})(\d\d)(\d\d)', r'+7\1\2\3\4', phone)
        self.username = re.sub(r'\+?[78](\d{3})(\d{3})(\d\d)(\d\d)', r'+7\1\2\3\4', phone)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.name + " Дата и время создания: %s" % (format(self.datetime_create, "d.m.Y H:i"))
