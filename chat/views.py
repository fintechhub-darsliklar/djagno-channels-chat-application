from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, models
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegisterForm
from .models import Chat, Messages
from django.db.models import Q


# Login View (Tayyor klassdan foydalanamiz)
class MyLoginView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('index') # Login bo'lgach qayerga o'tish


# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Ro'yxatdan o'tgach darhol login qilish
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    chats = Chat.objects.filter(Q(owner_user=request.user) | Q(friend_user=request.user))
    
    # 2. Qidiruvni tekshirish
    search_query = request.GET.get('username')
    searched_users = None
    if search_query:
        searched_users = models.User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
    chats = Chat.objects.filter(
        Q(owner_user=request.user) | Q(friend_user=request.user)
    ).order_by('-created_at') # Oxirgi xabar kelgan vaqti bo'yicha tartiblash
    content = {
        "chats": chats,
        'searched_users': searched_users
    }
    print(content)
    return render(request, "index.html", context=content)


def room(request, room_name):
    chat = Chat.objects.get(id=room_name)
    messages = Messages.objects.filter(chat=chat)
    if request.user == chat.owner_user:
        firend_user = chat.friend_user
    else:
        firend_user = chat.owner_user
    context = {
        "messages": messages,
        "room_name": room_name,
        "friend_user": firend_user
    }
    return render(request, "room.html", context=context)



def start_chat(request, user_id):
    # Suhbatdoshni bazadan topamiz
    friend = models.User.objects.get(id=user_id)
    
    # O'z-o'zi bilan chat qilishni oldini olish
    if friend == request.user:
        return redirect('index')

    # Oldin bu ikki foydalanuvchi o'rtasida chat bo'lganmi?
    # Q() orqali ikki xil holatni ham tekshiramiz:
    # 1. Men owner, u friend
    # 2. U owner, men friend
    chat = Chat.objects.filter(
        (Q(owner_user=request.user) & Q(friend_user=friend)) |
        (Q(owner_user=friend) & Q(friend_user=request.user))
    ).first()

    # Agar chat mavjud bo'lmasa, yangi chat yaratamiz
    if not chat:
        chat = Chat.objects.create(
            owner_user=request.user,
            friend_user=friend
        )

    # Chat xonasiga yo'naltiramiz
    return redirect('room', room_name=chat.id)