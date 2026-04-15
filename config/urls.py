
from django.contrib import admin
from django.urls import path
from chat.views import index, room, MyLoginView, register_view, start_chat
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', index, name='index'),
    path('chat/<str:room_name>/', room, name='room'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('start-chat/<int:user_id>/', start_chat, name='start_chat'),
]
