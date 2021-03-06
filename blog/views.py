from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, Http404
from django.utils import timezone
from .models import Post, Comment, Status
from django.contrib.auth.models import User
from .forms import PostForm, UserForm, CommentForm, StatusForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import django.contrib.auth.views

@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') #lte - less than or equal to
    query = request.GET.get("q")
    if query:
        posts = posts.filter(text__icontains = query)

    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render (request, 'blog/post_detail.html', {'post' : post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, "Post kreiran! <a href = '/blog/'</a>Natrag", extra_tags="html_safe")
            return redirect ('post_detail', pk=post.pk)
        else:
            messages.error(request, "Error pri kreiranju posta!")
    else:
            form = PostForm()
    return render (request, 'blog/post_edit.html', {'form' : form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect ('post_detail', pk = post.pk)
    else:
            form = PostForm(instance = post)
    return render (request, 'blog/post_edit.html', {'form':form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, "Post izbrisan!")
    return redirect('blog.views.post_list')


def register_new(request):
    if request.method == 'POST':
        form_register_new = UserForm(request.POST)
        if form_register_new.is_valid():
            user = form_register_new.save(commit=False)
            username = form_register_new.cleaned_data['username']
            password = form_register_new.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('blog.views.register_accept')
            messages.success(request, "Korisnik je registriran!")
        else:
            messages.error(request, "Error pri registraciji!")
    else:
            form_register_new = UserForm()
    return render (request, 'registration/registration_form.html', {'form_register_new': form_register_new})

def register_accept(request):
    return render (request, 'registration/registration_accept.html')

@login_required
def add_comment_to_post(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form_comment = CommentForm(request.POST)
        if form_comment.is_valid():
            comment = form_comment.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.created_date = timezone.now()
            comment.save()
            return redirect ('blog.views.post_detail', pk = post.pk)
    else:
        form_comment = CommentForm()
    return render (request, 'blog/add_comment_to_post.html', {'form_comment':form_comment} )

@login_required
def delete_own_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, "Komentar izbrisan!")
    return redirect('blog.views.post_detail', pk=post_pk)


def welcome(request):
    if request.user.is_authenticated():
        return redirect('blog.views.post_list')   #raise Http404
    else:
        return render (request, 'blog/welcome.html')

@login_required
def title(request):
    return render (request, 'blog/title.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form_status = StatusForm(request.POST)
        if form_status.is_valid():
            status = form_status.save(commit = False)
            status.author = request.user
            status.created_date = timezone.now()
            status.save()
            return redirect ('blog.views.profile')
    else:
            form_status = PostForm()
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') #lte - less than or equal to
            status = Status.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
            query = request.GET.get("q")
            if query:
                posts = posts.filter(text__icontains = query)
    return render (request, 'blog/profile.html', {'posts' : posts, 'status':status, 'form_status' : form_status})
