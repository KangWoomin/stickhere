from django.urls import path
from .views import *


urlpatterns =[
    path('',view=index, name='main'),
    # path('index/',view=index, name='index'),
    path('user_type_create/',view=user_type_create, name='user_type_create'),
    path('create_user/',view=create_user, name='create_user'),
    path('login/',view=login_view, name='login'),
    path('login_user_type/',view=login_user_type, name='login_user_type'),
    path('logout/',view=logout_view, name='logout'),

    # path('user_profile/',view=profile, name='user_profile'),
    path('profile/<int:pk>/', view=profile_view, name='profile_view'),
    path('profile_edit/',view=profile_modify, name='profile_edit'),


    path('boart_type/',view=board_type, name='board_type'),
    path('create_board_text/',view=create_board_text, name='create_board_text'),
    path('text_board_list/',view=post_list, name='text_board_list'),
    path('text_board/<int:post_id>/edit',view=edit_post, name='text_board_edit'),
    path('text_board_delete/<int:post_id>/', view=delete_post, name='text_board_delete'),
    path('text_board/<int:pk>/',view=text_detail, name='text_detail'),

    path('increase_hobby_click/',view=increase_hobby_click, name='increase_hobby_click'),

    path('movie_board/',view=movie_board, name='movie_board'),
    path('main_map/',view=main_map, name='main_map'),
    
    
    path('short_create/',view=create_shorts, name='shorts_board_create'),
    path('short/',view=short_movie_list, name='shorts_board_list'),
    path('short/<int:pk>/',view=short_movie_detail, name='shorts_board_detail'),
    path('short/<int:pk>/edit/',view=short_movie_edit, name='shorts_board_edit'),
    path('short/<int:pk>/delete/',view=short_movie_delete, name='shorts_board_delete'),
    
    path('delete_message/<int:message_id>/', view=delete_message, name='delete_message'),
    path('direct_message/<int:friend_id>/', view=direct_message, name='direct_message'),

    
    path('send_friend_request/<int:to_user_id>/', view=send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', view=accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', view=reject_friend_request, name='reject_friend_request'),
    path('friend_requests/', view=friend_request_list, name='friend_request_list'),
    path('friend-requests/', view=friend_requests_view, name='friend_requests'),

    
    path('dm/<int:friend_id>/', view=dm_view, name='dm_view'),
    path('delete_message/<int:message_id>/', view=delete_dm, name='delete_dm'),
    
    # 다른 URL 패턴들...
    path('user_hobby_click/',view=user_hobby_click, name='user_hobby_click'),

]


