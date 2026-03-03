from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Category, Blog
from .forms import CategoryForm, BlogForm, UserForm, EditUserForm
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required

# Create your views here.

def dashboard(request):
    category_count = Category.objects.all().count()
    blog_count = Blog.objects.all().count()

    context = {
        'category_count': category_count,
        'blog_count': blog_count
    }
    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    
    return render(request, 'dashboard/categories.html')

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')   
    else:
        form = CategoryForm()

    return render(request, 'dashboard/add_category.html', {'form': form})

@staff_member_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk = pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/edit_category.html', {'form' : form})

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk = pk)

    if request.method == 'POST':
        category.delete()
        return redirect('categories')

def posts(request):
    posts = Blog.objects.all()
    return render(request, 'dashboard/posts.html', {'posts': posts})

@staff_member_required
def add_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # for getting the primary key so that we can make the slug unique
            post.save()
            post.slug = slugify(post.title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    else:
        form = BlogForm()

    return render(request, 'dashboard/add_post.html', {'form': form})

@staff_member_required
def edit_post(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            post = form.save()
            post.slug = slugify(post.title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'dashboard/edit_post.html', {'form': form})

@staff_member_required
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')

@staff_member_required
@permission_required('auth.view_user', raise_exception=True)
def users(request):
    users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users': users})

@staff_member_required
@permission_required('auth.add_user', raise_exception=True)
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = UserForm()

    return render(request, 'dashboard/add_user.html', {'form': form})

@staff_member_required
@permission_required('auth.change_user', raise_exception=True)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'dashboard/edit_user.html', {'form': form})

@staff_member_required
@permission_required('auth.delete_user', raise_exception=True)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.delete()
        return redirect('users')