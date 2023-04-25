from django.db import models

# Create your models here.


class News(models.Model):
    news_id = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    link = models.URLField()
    source = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    favorite = models.BooleanField(default=False)
    user = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.headline
