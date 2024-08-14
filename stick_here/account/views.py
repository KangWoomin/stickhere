from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import *

# Create your views here.
def main(request):
    return render(request,'main.html')

def user_type_create(request):
    return render(request,'user_type_create.html')

def create_user(request):
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    
    else:
        form =CustomUserForm()
    return render(request,'create_user.html',{'form':form})

def login_user_type(request):
    return render(request,'login_user_type.html')

def login_view(request):
    if request.method =='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None,'인증에 실패했습니다. 이메일과 비밀번호를 확인해 주세요')
    else:
        form = AuthenticationForm()

    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('main')


from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile_view(request, pk):
    author = get_object_or_404(User, pk=pk)
    friend_request_sent = False
    
    if request.user.is_authenticated and request.user != author:
        # Check if a friend request has been sent
        friend_request_sent = FriendRequst.objects.filter(
            from_user=request.user,
            to_user=author,
            status='pending'
        ).exists()
    
    return render(request, 'profile_view.html', {
        'author': author,
        'friend_request_sent': friend_request_sent
    })

# @login_required
# def profile(request):
#     user_profile,created = UserProfile.objects.get_or_create(user = request.user)

#     content = {
#         'user_profile':user_profile,
#         'user':request.user
#     }
#     return render(request,'profile_view.html',content)


import urllib.request
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage,FileSystemStorage
@login_required
def profile_modify(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        text = request.POST.get('text')
        location = request.POST.get('location')
        new_image = request.FILES.get('new_profile_image')

        if nickname and nickname != request.user.nickname:
            request.user.nickname = nickname
            request.user.save()

        if text and text != user_profile.text:
            user_profile.text = text

        if new_image:
            # 새로 업로드된 이미지 처리
            request.user.img = new_image
        elif request.POST.get('existing_profile_image'):
            # 기존 이미지 경로 처리
            selected_image = request.POST.get('existing_profile_image')
            if selected_image.startswith('/media/'):
                # '/media/' 제거
                request.user.img = selected_image.replace('/media/', '')
            else:
                request.user.img = selected_image

        if location and location != user_profile.location:
            user_profile.location = location

        user_profile.save()

        return redirect('profile_view', pk=request.user.pk)

    return render(request, 'profile_edit.html', {'user_profile': user_profile})

# def profile_modify(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     if request.method =='POST':
#         nickname = request.POST.get('nickname')
#         text = request.POST.get('text')
#         location = request.POST.get('location')
#         selected_image = request.POST.get('existing_profile_image')  # 선택한 이미지 URL
#         new_image = request.FILES.get('new_profile_image')
   
#         if nickname and nickname != request.user.nickname:
#             request.user.nickname = nickname
#             request.user.save()
            
#         if text and text != user_profile.text:
#             user_profile.text = text
        

#         if new_image:
#             fs = FileSystemStorage()
#             filename = fs.save(new_image.name, new_image)
#             request.user.img = filename
#             request.user.save()
#         elif selected_image != 'upload':
#             if selected_image.startswith('/static/'):
#                 # 기본 이미지의 경우 경로만 저장
#                 request.user.img = selected_image.replace('/static/', '')
#             else:
#                 request.user.img = selected_image
#             request.user.save()
       
#         if location and location != user_profile.location:
#             user_profile.location = location

#         user_profile.save()
        
        
#         return redirect('profile_view')

        
#     return render(request,'profile_edit.html',{'user_profile':user_profile})


from django.shortcuts import get_object_or_404

@login_required
def increase_hobby_click (request, category_id):
    hobby_category = get_object_or_404(HobbyCategory, id=category_id)
    user_hobby_click, created = UserHobby_click.objects.get_or_create(user=request.user)
    user_hobby_click.click_count +=1
    user_hobby_click.save()
    
    hobby_category.click_count +=1
    hobby_category.save()
    return redirect('main')


@login_required
def board_type(request):
    return render(request,'board_type.html')


from .forms import PostForm

@login_required
def create_board_text(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.user = request.user  # 현재 로그인한 사용자 설정
            new_entry.save()
            return redirect('text_board_list')
    else:
        form = PostForm()

    return render(request, 'create_board_text.html', {'form': form})




def post_list(request):
    posts = TextBoard.objects.all()
    return render(request, 'text_board_list.html', {'posts': posts})

def text_detail(request, pk):
    text = get_object_or_404(TextBoard, pk=pk)
    
    return render(request,'text_board_detail.html',{'text':text})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(TextBoard, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('text_board_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'text_board_edit.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(TextBoard, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('text_board_list')
    return render(request, 'text_board_delete.html', {'post': post})


def movie_board(request):
    return render(request,'movie_board.html')


def main_map(request):
    
    text = TextBoard.objects.all()
    shorts = ShortMovieBoard.objects.all()

    content = {
        'text':text,    
        'shorts':shorts
    }
    
    return render(request,'main_map.html',content)


from django.shortcuts import render, redirect
from .models import ShortMovieBoard
from .forms import PostForm

def create_shorts(request):
    if request.method == 'POST':
        form = ShortVideo(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('main')
    else:
        form = ShortVideo()
    return render(request, 'shorts_board_create.html', {'form': form})

def short_movie_list(request):
    movies = ShortMovieBoard.objects.all()
    return render(request, 'shorts_board_list.html', {'movies': movies})

def short_movie_detail(request, pk):
    movie = get_object_or_404(ShortMovieBoard, pk=pk)
    author = movie.user
   # 사용자가 작성자에게 이미 친구 요청을 보냈는지 확인
    friend_request_sent = False
    if request.user.is_authenticated:
        friend_request_sent = request.user.friend_requests_sent.filter(to_user=author, status='pending').exists()
    
    content = {
        'movie': movie,
        'author': author,
        'friend_request_sent': friend_request_sent,  # 결과를 템플릿에 전달
    }
    return render(request, 'shorts_board_detail.html', content)

def short_movie_edit(request, pk):
    movie = get_object_or_404(ShortMovieBoard, pk=pk)
    if request.method == 'POST':
        form = ShortVideo(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('shorts_board_detail', pk=movie.pk)
    else:
        form = ShortVideo(instance=movie)
    return render(request, 'shorts_board_edit.html', {'form': form, 'movie': movie})

def short_movie_delete(request, pk):
    movie = get_object_or_404(ShortMovieBoard, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('shords_board_list')
    return render(request, 'shorts_board_delete.html', {'movie': movie})

@login_required
def user_hobby_click(request):
    user_click, created = UserHobby_click.objects.get_or_create(
        user_name = UserHobby_click.user,
        hobby_category = request.POST.get('hobby_category'),
        )
    
    user_click.click_count +=1
    return HttpResponse(f'{user_click.user.nickname}-{user_click.hobby_category.name} - {user_click.click_count}')
    



from django.http import JsonResponse
from .models import Dm_table
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_message(request, message_id):
    if request.method == 'POST':
            message = get_object_or_404(Dm_table, id=message_id)

            # 메시지 삭제는 메시지의 발신자만 가능하게 할 수 있음
            if message.sender == request.user:
                message.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': '권한이 없습니다.'})

    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


from django.http import HttpResponseForbidden

@login_required
def direct_message(request, friend_id):
    # 메시지를 주고받을 친구 유저를 찾음
    friend = get_object_or_404(User, id=friend_id)

    # GET 요청: 해당 친구와의 DM 기록을 보여줌
    if request.method == 'GET':
        dms = Dm_table.objects.filter(
            (Q(sender=request.user) & Q(receiver=friend)) |
            (Q(sender=friend) & Q(receiver=request.user))
        ).order_by('create_dt')

        return render(request, 'direct_message.html', {
            'friend': friend,
            'dms': dms
        })

    # POST 요청: 새로운 메시지를 전송
    elif request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            Dm_table.objects.create(
                sender=request.user,
                receiver=friend,
                message=message_content
            )
            return redirect('direct_message', friend_id=friend.id)
        else:
            return HttpResponseForbidden("메시지 내용이 비어있습니다.")

    # GET과 POST가 아닌 다른 요청은 금지
    return HttpResponseForbidden("잘못된 요청입니다.")

from .models import User, FriendRequst

@login_required
def send_friend_request(request, to_user_id):
    to_user = get_object_or_404(User, id=to_user_id)
    
    # Create a friend request
    FriendRequst.objects.create(from_user=request.user, to_user=to_user, status='pending')
    
    return redirect('profile_view', pk=to_user_id)

# @login_required
# def send_friend_request(request, user_id):
#     to_user = get_object_or_404(User, id=user_id)
#     friend_request, created = FriendRequst.objects.get_or_create(from_user=request.user, to_user=to_user)
    
#     if not created:
#         # 이미 요청이 존재하는 경우
#         return redirect('user_profile', user_id=to_user.id)

#     return redirect('friend_request_list')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequst, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.status = 'accepted'
        friend_request.save()
        return redirect('friend_request_list')
    return redirect('home')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequst, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.status = 'rejected'
        friend_request.save()
        return redirect('friend_request_list')
    return redirect('home')

@login_required
def friend_request_list(request):
    received_requests = FriendRequst.objects.filter(to_user=request.user, status='pending')
    sent_requests = FriendRequst.objects.filter(from_user=request.user, status='pending')
    return render(request, 'friend_requests.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })




@login_required
def friend_requests_view(request):
    # 현재 사용자가 받은 친구 요청
    received_requests = FriendRequst.objects.filter(to_user=request.user)

    # 현재 사용자의 친구 목록
    friendships = Friendship.objects.filter(models.Q(user1=request.user) | models.Q(user2=request.user))
    friends = set()
    for friendship in friendships:
        if friendship.user1 == request.user:
            friends.add(friendship.user2)
        else:
            friends.add(friendship.user1)

    return render(request, 'friend_requests.html', {
        'received_requests': received_requests,
        'friends': friends,
    })

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequst, id=request_id)
    
    if friend_request.to_user == request.user:
        # Create a Friendship record
        Friendship.objects.get_or_create(
            user1=friend_request.from_user,
            user2=friend_request.to_user
        )
        # Update the request status
        friend_request.status = 'accepted'
        friend_request.save()

    return redirect('friend_requests')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequst, id=request_id)
    
    if friend_request.to_user == request.user:
        # Update the request status
        friend_request.status = 'rejected'
        friend_request.save()

    return redirect('friend_requests')


from django.http import JsonResponse

def dm_view(request, friend_id):
    friend = get_object_or_404(User, pk=friend_id)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        Dm_table.objects.create(
            sender_id=request.user,
            receiver_id=friend,
            message=message
        )
        return redirect('dm_view', friend_id=friend_id)

    # 사용자와 친구 간의 대화 내역 조회
    dms = Dm_table.objects.filter(
        (models.Q(sender_id=request.user) & models.Q(receiver_id=friend)) |
        (models.Q(sender_id=friend) & models.Q(receiver_id=request.user))
    ).order_by('create_dt')
    
    return render(request, 'dms.html', {
        'friend': friend,
        'dms': dms
    })

@login_required
def delete_dm(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Dm_table, id=message_id)
        if message.sender_id == request.user or message.receiver_id == request.user:
            message.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    return JsonResponse({'success': False})


def index(request):
    
    shorts = ShortMovieBoard.objects.all()
    texts = TextBoard.objects.all()

    content = {
        'shorts':shorts,
        'texts':texts
    }
    
    return render(request,'index.html',content)

