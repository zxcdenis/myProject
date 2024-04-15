from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


class Article(models.Model):
    title = models.CharField('Заголовок',max_length=100)
    content = models.TextField('Описание')
    published_date = models.DateTimeField('Дата публикации',auto_now_add=True)
    image = models.ImageField('Изображение', upload_to='articles_images/', blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='articles', blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    thread = models.ForeignKey(Thread, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]  
    
class ArticleComment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_comments', blank=True)

    def __str__(self):
        return self.text[:20]

    def add_like(self, user):
        self.dislikes.remove(user)
        self.likes.add(user)

    def add_dislike(self, user):
        self.likes.remove(user)
        self.dislikes.add(user)