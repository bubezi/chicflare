from django.http import HttpResponseBadRequest
from django.shortcuts import render
from manageOrders.models import SpecialOrder
from store.models import Customer
import os
import random
from django.shortcuts import redirect


# Create your views here.
def all_games(request):
    context = {}
    if request.user.is_authenticated:
        return render(request, 'games/games.html', context)
    else:
        return redirect('login')


items = {'easy':'Blunt', 'medium':'Cookie', 'hard':'Bag'}
item_types = {'spaceship1': 'Normal', 'spaceship2': 'Foreign', 'spaceship3': 'Purple'}
items_price = {'easy': 50, 'medium': 100, 'hard': 500}
item_types_price = {'spaceship1': 1, 'spaceship2': 1, 'spaceship3': 1}

def no_money(request):
    context = {}
    if request.user.is_authenticated:
        return render(request, 'games/no_money.html', context)
    else:
        return redirect('login')


def game1_intro(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get(user=user)
        context = {'customer': customer}
        if request.method == 'POST':
            amount = int(request.POST['target'])
            area = request.POST['area']
            item = request.POST['level']
            item_type = request.POST['character']
            price = items_price[item] * item_types_price[item_type] * amount
            if customer.balance < price:
                return redirect('recharge')
            else:
                customer.balance -= price
                customer.save()
                new_oder = SpecialOrder(user=user)
                new_oder.amount = amount
                new_oder.area = area
                new_oder.item = items[item]
                new_oder.item_type = item_types[item_type]
                new_oder.save()
            return redirect('game1')

        return render(request, 'games/game1intro.html', context)
    else:
        return redirect('login')


def game1_view(request):
    try:
        music_list = os.listdir('static/audio/game_music/')
        if len(music_list) > 0:
            song_path = music_list[random.randint(0, len(music_list) - 1)]
            context = {'song_path': song_path}
    except Exception as e:
        context = {}

    if request.user.is_authenticated:
        return render(request, 'games/game1.html', context)

    else:
        return redirect('login')


def game2_view(request):
    try:
        music_list = os.listdir('static/audio/game_music/')
        if len(music_list) > 0:
            song_path = music_list[random.randint(0, len(music_list) - 1)]
            context = {'song_path': song_path}
    except Exception as e:
        context = {}

    if request.user.is_authenticated:
        return render(request, 'games/game2.html', context)

    else:
        return redirect('login')


def game3_view(request):
    try:
        music_list = os.listdir('static/audio/game_music/')
        if len(music_list) > 0:
            song_path = music_list[random.randint(0, len(music_list) - 1)]
            context = {'song_path': song_path}
    except Exception as e:
        context = {}

    if request.user.is_authenticated:
        return render(request, 'games/game3.html', context)

    else:
        return redirect('login')


def game5_view(request):
    try:
        music_list = os.listdir('static/audio/game_music/')
        if len(music_list) > 0:
            song_path = music_list[random.randint(0, len(music_list) - 1)]
            context = {'song_path': song_path}
    except Exception as e:
        context = {}

    if request.user.is_authenticated:
        return render(request, 'games/game5.html', context)

    else:
        return redirect('login')


