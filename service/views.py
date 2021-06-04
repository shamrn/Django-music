from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from .models import Profile, MusicalInventory
from .forms import UserUpdateForm
from django.forms import inlineformset_factory

@login_required
def service(request):
    user = request.user
    if not Profile.objects.filter(telegram=user).exists():   # если профиль не создан
        Profile.objects.create(telegram=user)                # создаем профиль , записываем только ник с телеграма
        return redirect('profile_update')                    # и перенаправляем пользователя, на заполнение профиля данными
    return render(request,'service/service.html')


def login(request): # это нужно убрать и добавить в urls
    return render(request,'service/login.html')


@login_required
def profile_update(request):
    profile = Profile.objects.get(telegram=request.user)
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=profile)
        if update_form.is_valid():
            cd = update_form.cleaned_data
            profile.last_name, profile.first_name, profile.instagram = \
                cd['last_name'], cd['first_name'], cd['telegram']
            profile.save()
    else:
        update_form = UserUpdateForm(instance=profile)
    context = {'form':update_form}
    return render(request,'service/profile_update.html',context)