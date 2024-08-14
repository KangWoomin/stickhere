from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, nickname, number,gender,birth,hoby,password=None, **extra):
        email = self.normalize_email(email)
        user= self.model(
                email=email,
                nickname = nickname,
                number = number,
                gender = gender,
                birth = birth,
                hoby = hoby,
                **extra
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,nickname ,password=None, **extra):
        extra.setdefault('is_active', True)
        extra.setdefault('is_admin', True)
        extra.setdefault('birth','2000-01-01')
        extra.setdefault('number','01000000000')
        extra.setdefault('lat',0.0)
        extra.setdefault('lnt',0.0)
        extra.setdefault('gender', '남성')
        extra.setdefault('user_type','일반')

        return self.create_user(email,nickname,password=password,**extra)

class User_gender(models.TextChoices):
    male = '남성','남성'
    female = '여성','여성'
class User_type(models.TextChoices):
    일반 = '일반','일반'
    기업 = '기업','기업'

class Hobby_choices(models.TextChoices):
    기타 = '기타','기타'
    테니스 = '테니스','테니스'
    헬스 = '헬스','헬스'
    골프 = '골프','골프'
    풋살 = '풋살','풋살'
    축구 = '축구','축구'
    수영 = '수영','수영'
    요리 = '요리','요리'
    농구 = '농구','농구'
    야구 = '야구','야구'
    독서 = '독서','독서'
    탁구 = '탁구','탁구'
    양궁 = '양궁','양궁'
    사격 = '사격','사격'
    프라모델 = '프라모델','프라모델'

from multiselectfield import MultiSelectField

class User(AbstractBaseUser):

    email = models.EmailField(verbose_name='email', max_length=80, unique=True)
    nickname = models.CharField(verbose_name='닉네임', max_length=100)
    lat = models.FloatField(verbose_name='위도', max_length=10, default=33.450701)
    lnt = models.FloatField(verbose_name='경도', max_length=10, default=126.570667)
    gender= models.CharField(verbose_name='성별',max_length=50, choices=User_gender.choices, default=User_gender.male)
    number = models.CharField(verbose_name='연락처', max_length=50)
    birth = models.DateField()
    hobbies = MultiSelectField(choices=Hobby_choices.choices, verbose_name='취미', default=Hobby_choices.기타, null=True,help_text='다중선택 가능')
    user_type = models.CharField(verbose_name='유저타입',max_length=50, choices=User_type.choices, default=User_type.일반)
    img = models.ImageField(upload_to='uploads/', blank=True, null=True, default='uploads/logo.png')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname','number']

    def __str__(self):
        return self.nickname
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
from django.conf import settings
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    location = models.CharField(verbose_name='활동지역', max_length=100)

    def __str__(self):
        return self.user.nickname
    


class HobbyCategory(models.Model):
    name = models.CharField(verbose_name='카테고리 이름', max_length=50)
    

    def __str__(self):
        return self.name


class UserHobby_click(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobby_category = models.ForeignKey(HobbyCategory, on_delete=models.CASCADE)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.nickname} - {self.hobby_category.name} - {self.click_count}"
    

# from ckeditor.fields import RichTextField
class TextBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=100)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    ##위치 관련된 컬럼
    lat = models.FloatField(verbose_name='위도', max_length=10, default=33.450701)
    lnt = models.FloatField(verbose_name='경도', max_length=10, default=126.570667)
    hobby_category = models.ForeignKey(HobbyCategory, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.title

class ShortMovieBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=100)
    content = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    ##위치 관련된 컬럼
    lat = models.FloatField(verbose_name='위도',  default=33.450701)
    lnt = models.FloatField(verbose_name='경도',  default=126.570667)
    

    def __str__(self):
        return self.title
    


class Dm_table(models.Model):
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    create_dt = models.DateTimeField(auto_now_add=True)
    modify_dt = models.DateTimeField(auto_now=True)

    


    def __str__(self):
       return f"Message from {self.sender_id.nickname} to {self.receiver_id.nickname}"
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(sender_id=models.F('receiver_id')), name='no_self_messaging'),
        ]


class FriendRequst(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.from_user.nickname} -> {self.to_user.nickname} ({self.status})"
    


class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendship_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendship_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f'{self.user1} - {self.user2}'
