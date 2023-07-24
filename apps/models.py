from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, CharField, EmailField, TextField, Model, IntegerField, ForeignKey, CASCADE, \
    DateTimeField, TextChoices


class User(AbstractUser):
    image = ImageField(upload_to='pic/', blank=True, null=True)
    fullname = CharField(max_length=255)
    phone = CharField(max_length=50)
    email = EmailField()
    about = TextField(null=True)
    instagram = CharField(max_length=50, null=True)
    linkedin = CharField(max_length=50, null=True)

    def __str__(self):
        return self.fullname


class Category(Model):
    image = ImageField(upload_to='img/', blank=True, null=True)
    name = CharField(max_length=50)
    about = TextField()
    location = CharField(max_length=255)
    area = CharField(max_length=20)
    room = IntegerField()
    floor = IntegerField()
    price = IntegerField()
    author = ForeignKey('apps.User', CASCADE, related_name='my_category')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Blog(Model):
    class Status(TextChoices):
        TRAVEL = 'travel', 'Travel'
        DISCOUNT = 'discount', 'Discount'
        NEWS = 'news', 'News'
    image = ImageField(upload_to='jpg/', blank=True, null=True)
    title = CharField(max_length=50)
    category = CharField(max_length=50, choices=Status.choices, default=Status.TRAVEL)
    about = TextField()
    author = ForeignKey('apps.User', CASCADE, related_name='my_blog')
    created_at = DateTimeField(auto_now_add=True)


class Email(Model):
    name = CharField(max_length=70)
    email = EmailField()
    text = TextField()

    def __str__(self):
        return self.name


class TextToCategory(Model):
    image = ImageField(upload_to='tst/', blank=True, null=True)
    fullname = CharField(max_length=70)
    text = TextField()
    to_category = ForeignKey('apps.Category', CASCADE, related_name='my_family')
    created_at = DateTimeField(auto_now_add=True)


class Comment(Model):
    fullname = CharField(max_length=70)
    email = EmailField()
    text = TextField()
    to_blog = ForeignKey('apps.Blog', CASCADE, related_name='my_comment')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname
