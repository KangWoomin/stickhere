from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User


class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호 입력', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=['email','nickname','number','gender','birth','user_type','hobbies']

    def clear_date(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 일치 하지 않습니다.')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'nickname', 'number', 'gender', 'birth', 'user_type')


from .models import TextBoard
class PostForm(forms.ModelForm):
    class Meta:
        model = TextBoard
        fields = ['title', 'content','lat','lnt']
        # widgets = {
        #     'content': forms.Textarea(attrs={'id':'content'})
        # }


from django import forms
from .models import ShortMovieBoard

class ShortVideo(forms.ModelForm):
    class Meta:
        model = ShortMovieBoard
        fields = ['title', 'content', 'video', 'lat', 'lnt']
