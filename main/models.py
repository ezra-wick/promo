from django.db import models

class PageBlock(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='page_blocks/', null=True, blank=True)
    content = models.TextField()
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.CharField(max_length=255, null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, null=True, blank=True)
    template = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
