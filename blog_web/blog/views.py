from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Category, Blog, Comment
from contact.models import About
from django.db.models import Q
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.cache import never_cache

# Create your views here.
def home(request):
    categories = Category.objects.all()
    featured_blogs = Blog.objects.filter(is_featured = True, status = 'Published').order_by('updated_at')
    normal_blogs = Blog.objects.filter(is_featured = False, status = 'Published').order_by('-created_at')[:3]

    # fetching about
    try:
        about = About.objects.get()
    except:
        about = None

    context = {
        'categories': categories,
        'featured_blogs': featured_blogs,
        'normal_blogs': normal_blogs,
        'about': about
    }
    return render(request, 'home.html', context)

def blogs_by_category(request, category_id):
    blogs = Blog.objects.filter(status = 'Published', category_id = category_id)
    
    category = get_object_or_404(Category, pk = category_id)

    context = {
        'blogs': blogs,
        'category': category
    }
    return render(request, 'blogs_by_category.html', context)

def individual_blog(request, slug):
    single_blog = get_object_or_404(Blog, status = 'Published', slug = slug)

    # for comments
    comments = Comment.objects.filter(blog = single_blog)
    comment_count = comments.count()

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()

        if comment:
            Comment.objects.create(user = request.user, blog = single_blog, comment = comment)
            return redirect('individual_blog', slug=slug)

    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count,
    }

    return render(request, 'individual_blog.html', context)

def search(request):
    keyword = request.GET.get('keyword')

    blogs = Blog.objects.filter((Q(title__icontains = keyword)| Q(short_description__icontains = keyword) | Q(blog_body__icontains = keyword)), status = 'Published')

    context = {
        'blogs': blogs,
        'keyword': keyword
    }
    return render(request, 'search.html', context)

@never_cache
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@never_cache
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@never_cache
def logout_view(request):
    logout(request)
    return redirect('home')

