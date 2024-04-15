from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

from .models import Article, Thread, Comment,ArticleComment,Tag

from .forms import ThreadForm,SignUpForm, CommentForm, NewsForm, ArticleCommentForm
from django.db.models import Q

from django.core.paginator import Paginator
from django.http import JsonResponse

def search_results(request):
    query = request.GET.get('q')
    tags = request.GET.getlist('tags')
    
    articles = Article.objects.all()
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    if tags:
        articles = articles.filter(tags__name__in=tags).distinct()
    
    return render(request, 'news_app/search_results.html', {'articles': articles})


def all_news_view(request):
    all_articles = Article.objects.all().order_by('-published_date')
    paginator = Paginator(all_articles, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_app/all_news.html', {'page_obj': page_obj})

def index(request):
    filter_type = request.GET.get('filter', 'latest')
    all_tags = Tag.objects.all()
    articles = Article.objects.all().order_by('-published_date')
    selected_tags_ids = request.GET.getlist('tags')
    if selected_tags_ids:
        articles = articles.filter(tags__id__in=selected_tags_ids).distinct()
    tags_ids = request.GET.getlist('tag')
    if tags_ids:
        articles = articles.filter(tags__id__in=tags_ids).distinct()

    threads = Thread.objects.all().order_by('-published_date')[:20]

    return render(request, 'news_app/index2.html', {
        'title': 'Главная страница',
        'articles': articles,
        'threads': threads,
        'all_tags': all_tags,
        'selected_tags_ids': selected_tags_ids,
    })
                  

def threads_list(request):
    threads = Thread.objects.all().order_by('-published_date')
    return render(request, 'news_app/threads_list.html', {'threads': threads})



@login_required(login_url='/sign-in/')
def add_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user  
            thread.save()
            return redirect('home')
    else:
        form = ThreadForm()
    return render(request, 'news_app/add_thread.html', {'form': form})



from django.contrib import messages

def sign_in(request):
    signup_form = SignUpForm()  
    login_form = AuthenticationForm()  

    if request.method == 'POST':
        if 'submit_signup' in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, "Регистрация прошла успешно!")
                return redirect('home')
            else:
                messages.error(request, "Ошибка при регистрации.")
        elif 'submit_login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Вход выполнен успешно!")
                    return redirect('home')
                else:
                    messages.error(request, "Неверный логин или пароль.")
            else:
                messages.error(request, "Неверный логин или пароль.")

    return render(request, 'news_app/sign_in.html', {'signup_form': signup_form, 'login_form': login_form})


def is_moderator(user):
    return user.groups.filter(name='Модераторы').exists() or user.is_superuser




@login_required
def delete_article_comment(request, comment_id):
    comment = get_object_or_404(ArticleComment, pk=comment_id)
    if request.user == comment.author or request.user.groups.filter(name='Модераторы').exists() or request.user.is_superuser:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        return HttpResponseForbidden()
    
@login_required
def delete_thread_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author or request.user.groups.filter(name='Модераторы').exists() or request.user.is_superuser:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        return HttpResponseForbidden()

@login_required
@user_passes_test(is_moderator)
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'news_app/add_news.html', {'form': form})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    comments = thread.comments.filter(parent__isnull=True)

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id', None)
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            if parent_id:
                comment.parent_id = int(parent_id)
            comment.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = CommentForm()

    return render(request, 'news_app/thread_detail.html', {'thread': thread, 'comments': comments, 'form': form})


def news_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.filter(parent__isnull=True)
    
    if request.method == "POST" and request.user.is_authenticated:
        comment_form = ArticleCommentForm(request.POST)
        if comment_form.is_valid():
            parent_id = request.POST.get('parent_id', None)
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            if parent_id:
                comment.parent_id = int(parent_id)
            comment.save()
            return redirect('news_detail', article_id=article.id)
    else:
        comment_form = ArticleCommentForm()
    
    return render(request, 'news_app/news_detail.html', {'article': article, 'comments': comments, 'comment_form': comment_form})
from django.template.loader import render_to_string


# def news_detail(request, article_id):
#     article = get_object_or_404(Article, pk=article_id)
#     comments = article.comments.filter(parent__isnull=True)
#     comment_form = ArticleCommentForm(request.POST or None)

#     if request.method == "POST" and comment_form.is_valid():
#         new_comment = comment_form.save(commit=False)
#         new_comment.article = article
#         new_comment.author = request.user
#         parent_id = request.POST.get('parent_id')
#         if parent_id:
#             new_comment.parent_id = int(parent_id)
#         new_comment.save()

#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             html = render_to_string('news_app/article_respond.html', {'comment': new_comment}, request=request)
#             return JsonResponse({'new_comment_html': html})

#         return redirect('news_detail', article_id=article.id)

#     return render(request, 'news_app/news_detail.html', {
#         'article': article,
#         'comments': comments,
#         'comment_form': comment_form
#     })  
               
@login_required
def edit_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.user != thread.author and not request.user.groups.filter(name="Модераторы").exists():
        return redirect('thread_detail', thread_id=thread.id)
    
    if request.method == "POST":
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = ThreadForm(instance=thread)
    
    return render(request, 'news_app/edit_thread.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test

def is_moderator(user):
    return user.groups.filter(name="Модераторы").exists()


@login_required(login_url='/sign-in/', redirect_field_name='next')
def handle_comment_reaction(request, comment_id, action):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment = get_object_or_404(ArticleComment, id=comment_id)
        liked = comment.likes.filter(id=request.user.id).exists()
        disliked = comment.dislikes.filter(id=request.user.id).exists()

        if action == 'like':
            if liked:
                comment.likes.remove(request.user)
            else:
                comment.add_like(request.user)
        elif action == 'dislike':
            if disliked:
                comment.dislikes.remove(request.user)
            else:
                comment.add_dislike(request.user)

        return JsonResponse({
            'likes': comment.likes.count(),
            'dislikes': comment.dislikes.count(),
            'liked': liked,  
            'disliked': disliked
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def edit_article_comment(request, comment_id):
    comment = get_object_or_404(ArticleComment, pk=comment_id)

    if request.user != comment.author:
        return redirect('home')  

    if request.method == "POST":
        form = ArticleCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = ArticleCommentForm(instance=comment)
    
    context = {'form': form}
    return render(request, 'news_app/edit_article_comment.html', context)

@login_required
def edit_thread_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.user != comment.author:
        return redirect('thread_detail', thread_id=comment.thread.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', thread_id=comment.thread.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'news_app/edit_thread_comment.html', {'form': form, 'comment': comment})


@login_required
@user_passes_test(is_moderator)
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=article)  
        if form.is_valid():
            form.save()
            return redirect('news_detail', article_id=article.id)
    else:
        form = NewsForm(instance=article)
    return render(request, 'news_app/edit_article.html', {'form': form, 'article': article})


@login_required
@user_passes_test(is_moderator)
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('home')  
    return render(request, 'news_app/confirm_delete_article.html', {'article': article})

@login_required
@user_passes_test(is_moderator)
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        thread.delete()
        return redirect('home') 
    else:
        return render(request, 'news_app/confirm_delete_thread.html', {'thread': thread})
