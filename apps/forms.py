from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from apps.models import User, Category, Blog, Email, Comment, TextToCategory


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'image', 'fullname', 'phone', 'email', 'about', 'instagram', 'linkedin', 'password']

    def clean_password(self):
        return make_password(self.cleaned_data['password'])


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['image', 'name', 'about', 'location', 'area', 'room', 'floor', 'price', 'author']


class TextCategoryForm(ModelForm):
    class Meta:
        model = TextToCategory
        fields = ['image', 'fullname', 'text']


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['image', 'title', 'category', 'about', 'author']


class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ['name', 'email', 'text']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['fullname', 'email', 'text']



