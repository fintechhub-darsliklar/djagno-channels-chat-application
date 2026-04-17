
from django.contrib import admin
from django.urls import path
from chat.views import index, room, login_page, register_view, start_chat, profile_page
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('chat/<str:room_name>/', room, name='room'),
    path('login/', login_page, name='login_page'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('start-chat/<int:user_id>/', start_chat, name='start_chat'),
    path('profile/page/', profile_page, name='profile_page'),
]
