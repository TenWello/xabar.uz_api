from django.db import models

class News(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    image = models.URLField(null=True, blank=True)
    time_ago = models.CharField(max_length=100)
    published_at = models.DateTimeField(null=True, blank=True)

    # published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
