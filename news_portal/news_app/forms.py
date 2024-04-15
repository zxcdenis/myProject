from django import forms
from .models import Thread, Comment, Article, ArticleComment,Tag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_select2.forms import Select2MultipleWidget




class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['text', 'parent_id']
        

class NewsForm(forms.ModelForm):
    delete_image = forms.BooleanField(required=False, label='Удалить изображение')

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'tags': Select2MultipleWidget(attrs={
                'class': 'select2', 
                'style': 'width: 100%;', 
                'data-placeholder': 'Выберите теги...'
            }),
        }
    def save(self, commit=True):
        if self.cleaned_data.get('delete_image'):
            self.instance.image.delete()
        return super().save(commit=commit)  


        
        
class ArticleCommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = ArticleComment
        fields = ['text', 'parent_id']
