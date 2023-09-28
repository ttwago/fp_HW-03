from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Merchants', 'Торговцы'),
        ('Guild Masters', 'Гилдмастеры'),
        ('Quest Givers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Tanners', 'Кожевники'),
        ('Potion Makers', 'Зельевары'),
        ('Spell Masters', 'Мастера заклинаний')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    comment = RichTextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, )
    creation_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, null=True, choices=[('Y', 'Принято'),
                                                                ('N', 'Отклонено')])