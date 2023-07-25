from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.forms import RegistrationForm, CategoryForm, BlogForm, EmailForm, CommentForm, TextCategoryForm
from apps.models import User, Category, Blog, Comment, TextToCategory


def about(request):
    agents_list = User.objects.all()
    paginator = Paginator(agents_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'about.html', {'page_obj': page_obj})


def base(request, pk):
    main_user = User.objects.filter(pk=pk).first()
    # max_id = Category.objects.latest('id').id
    # print(max_id)
    return render(request, 'base.html', {'main_user': main_user})


def agent_single(request, pk):
    login_agent = User.objects.filter(pk=pk).first()
    agent_categories = Category.objects.filter(author_id=pk)
    count_categories = Category.objects.filter(author_id=pk).count()
    return render(request, 'agent-single.html', {'login_agent': login_agent, 'agent_categories': agent_categories,
                                                 'count_categories': count_categories})


def agents_grid(request):
    agents = User.objects.all()
    return render(request, 'agents-grid.html', {'agents': agents})


def blog_grid(request):
    blogs_list = Blog.objects.all()
    paginator = Paginator(blogs_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog-grid.html', {'page_obj': page_obj})


def blog_single(request, pk):
    blog = Blog.objects.filter(id=pk).first()
    author = User.objects.filter(id=blog.author_id).first()
    comments = Comment.objects.filter(to_blog=pk)
    comments_count = Comment.objects.filter(to_blog=pk).count()
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.to_blog = blog
            form.save()
            return redirect(reverse('blog_single', args=(pk,)))
    return render(request, 'blog-single.html',
                  {'blog': blog, 'author': author, 'comments': comments, 'comments_count': comments_count})


def contact(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email_sender = form.save()

            subject = 'Email from {}'.format(email_sender.name)
            sender = email_sender.email
            message = f"from: {sender}\nText: {email_sender.text}"
            recipient_list = ['nourimanov@gmail.com']
            send_mail(subject, message, 'tulqinov571@gmail.com', recipient_list)

            return redirect('index')
    else:
        form = EmailForm()

    return render(request, 'contact.html', {'form': form})


def index(request):
    agents = User.objects.all()[:3]
    categories = Category.objects.all()
    blogs = Blog.objects.all()
    text_category = TextToCategory.objects.all()
    return render(request, 'index.html', {'agents': agents, 'categories': categories, 'blogs': blogs,
                                          'text_category': text_category})


def property_grid(request):
    if request.method == 'GET':
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        categories = Category.objects.all()
        paginator = Paginator(categories, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if min_price and max_price:
            categories = categories.filter(price__gte=min_price, price__lte=max_price)

        return render(request, 'property-grid.html', {'categories': categories, 'page_obj': page_obj})


def property_single(request, pk):
    category = Category.objects.filter(id=pk).first()
    category_owner = User.objects.filter(id=category.author_id)
    text_category = TextToCategory.objects.filter(to_category=category.id)
    if request.POST:
        form = TextCategoryForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.to_category = category
            form.save()
            return redirect(reverse('property_single', args=(pk,)))
    return render(request, 'property-single.html', {'category': category, 'category_owner': category_owner,
                                                    'text_category': text_category})


def signup(request):
    if request.POST:
        form = RegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        if errors := form.errors:
            print(errors.as_json(escape_html=True))
            return render(request, 'signup.html', {'errors': errors})
    return render(request, 'signup.html')


def signin(request):
    data = request.POST
    if data:
        username = data.get('username')
        password = data.get('password')
        person = authenticate(username=username, password=password)
        if person:
            login(request, person)
            return redirect('index')
    return render(request, 'signin.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def add_category(request):
    if request.POST:
        data = request.POST.copy()
        data['author'] = request.user
        form = CategoryForm(data=data, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        if errors := form.errors:
            print(errors.as_json(escape_html=True))
            return render(request, 'category.html', {'errors': errors})
    return render(request, 'category.html')


def add_blog(request):
    if request.POST:
        data = request.POST.copy()
        data['author'] = request.user
        form = BlogForm(data=data, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        if errors := form.errors:
            print(errors.as_json(escape_html=True))
            return render(request, 'blog.html', {'errors': errors})
    return render(request, 'blog.html')
