from django.db import models
from django.utils.dateformat import *
from django.utils import timezone
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import re

class Template(models.Model):
    name = models.CharField(max_length=200, unique=True)
    template_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PageBlock(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='page_blocks/', null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.CharField(max_length=255, null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, null=True, blank=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Блок страницы'
        verbose_name_plural = 'Блоки страницы'

    def __str__(self):
        return self.title


class FeedBack(models.Model):
    phone = models.CharField(max_length=16, verbose_name="Телефон", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="Имя", null=True, blank=True)
    email = models.CharField(max_length=80, verbose_name="email", null=True, blank=True)
    text = models.TextField(max_length=500, verbose_name="Сообщение", null=True, blank=True)
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


class ThemeSettings(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    primary_color = models.CharField(max_length=7, default='#0d6efd')
    secondary_color = models.CharField(max_length=7, default='#6c757d')
    success_color = models.CharField(max_length=7, default='#198754')
    info_color = models.CharField(max_length=7, default='#0dcaf0')
    warning_color = models.CharField(max_length=7, default='#ffc107')
    danger_color = models.CharField(max_length=7, default='#dc3545')
    light_color = models.CharField(max_length=7, default='#f8f9fa')
    dark_color = models.CharField(max_length=7, default='#212529')
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.name

# models.py
class Page(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    theme = models.ForeignKey(ThemeSettings, on_delete=models.SET_NULL, null=True, blank=True)
    blocks = models.ManyToManyField(PageBlock, blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class URLPattern(models.Model):
    path = models.CharField(max_length=200, unique=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.path} -> {self.page}"
    

class Redirect(models.Model):
    old_path = models.CharField(max_length=200, unique=True, null=True, blank=True)
    new_path = models.ForeignKey(URLPattern, on_delete=models.CASCADE)
    is_root_redirect = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.old_path} -> {self.new_path.path}"


class Photo(models.Model):
    original_image = models.ImageField(upload_to='photos/')
    cropped_image = models.ImageField(upload_to='photos/cropped/', null=True, blank=True)
    page_block = models.ForeignKey(PageBlock, on_delete=models.CASCADE, related_name='photos')
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f"Фото {self.pk} (Блок: {self.page_block.title})"

    def crop_image(self):
        image = Image.open(self.original_image.path)
        # Здесь вы можете изменить размеры и параметры обрезки, если хотите
        cropped_image = image.resize((300, 300), Image.ANTIALIAS).crop((0, 0, 300, 300))
        
        # Convert the image to RGB mode if it has an alpha channel
        if cropped_image.mode == 'RGBA':
            cropped_image = cropped_image.convert('RGB')

        # Сохраняем обрезанное изображение
        temp_image = BytesIO()
        cropped_image.save(temp_image, format='JPEG')
        temp_image.seek(0)

        file_name = f"{self.original_image.name.split('.')[0]}_cropped.jpg"
        self.cropped_image.save(file_name, ContentFile(temp_image.read()), save=False)
        temp_image.close()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.cropped_image:
            self.crop_image()
            self.save()