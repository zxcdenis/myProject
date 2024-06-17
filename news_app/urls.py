from django.urls import path 
from . import views 

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import sign_in, thread_detail, news_detail,delete_thread_comment,edit_thread,edit_article_comment, edit_thread_comment,delete_article_comment
from .views import edit_article, delete_article,delete_thread,all_news_view
from django.conf.urls.static import static
from django.conf import settings
from .views import search_results
from django.contrib.auth import views as auth_views

from .views import add_comment,add_thread_comment
urlpatterns = [
    
    path('',views.index,name = 'home'),
    path('add_thread/', views.add_thread),
    path('threads/', views.threads_list),
    path('sign-in/', sign_in, name='sign_in'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('threads/<int:thread_id>/', thread_detail, name='thread_detail'),
    path('add_news/', views.add_news, name='add_news'),
    path('news/<int:article_id>/', views.news_detail, name='news_detail'),
    path('delete_article_comment/<int:comment_id>/', delete_article_comment, name='delete_article_comment'),
    path('delete_thread_comment/<int:comment_id>/', delete_thread_comment, name='delete_thread_comment'),
    path('threads/edit/<int:thread_id>/', edit_thread, name='edit_thread'),
    path('comments/edit_thread_comment/<int:comment_id>/', edit_thread_comment, name='edit_thread_comment'),
    path('comments/edit_article_comment/<int:comment_id>/', edit_article_comment, name='edit_article_comment'),
    path('article/edit/<int:article_id>/', edit_article, name='edit_article'),
    path('article/delete/<int:article_id>/', delete_article, name='delete_article'),
    path('threads/delete/<int:thread_id>/', delete_thread, name='delete_thread'),
    path('news/all/', all_news_view, name='all_news'),
    path('search/', views.search_results, name='search_results'),
    path('comments/<int:comment_id>/<str:action>/', views.handle_comment_reaction, name='handle_comment_reaction'),
    path('threads/comments/<int:comment_id>/<str:action>/', views.handle_thread_comment_reaction, name='handle_thread_comment_reaction'),
    path('comments/add/<int:article_id>/', add_comment, name='add_comment'),
    path('threads/<int:thread_id>/add-thread-comment/', add_thread_comment, name='add_thread_comment'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='news_app/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='news_app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='news_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='news_app/password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)