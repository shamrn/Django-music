from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView
from .models import Profile, MusicalInventory, Song
from .forms import UserUpdateForm, UserInventaryFormset, UserInventoryForm
from django.forms import inlineformset_factory
from django import forms
from .check_profile import check_profile
from django.forms import formset_factory

@login_required
def service(request):
    """Страница личного кабинета"""

    user = request.user
    if not Profile.objects.filter(telegram=user).exists():  # если профиль не создан
        Profile.objects.create(telegram=user)  # создаем профиль , записываем только ник с телеграма
        return redirect('profile_update')  # и перенаправляем пользователя, на заполнение профиля данными

    acces_create_song = check_profile(user) # Проверяем может ли пользователь добавлять трек
    songs = Song.objects.filter(profile__telegram=user)
    profile = Profile.objects.get(telegram=user)
    context = {'songs': songs,'acces_create_song':acces_create_song,'profile':profile}
    return render(request, 'service/service.html', context)



# @login_required
# def profile_update(request):
#     """Редактирование профиля"""
#
#     profile = Profile.objects.get(telegram=request.user)
#     if request.method == 'POST':
#         update_form = UserUpdateForm(request.POST, instance=profile)
#         if update_form.is_valid():
#             cd = update_form.cleaned_data
#             profile.last_name, profile.first_name, profile.instagram = \
#                 cd['last_name'], cd['first_name'], cd['telegram']
#             profile.save()
#             return redirect('service')
#     else:
#         update_form = UserUpdateForm(instance=profile)
#     context = {'form': update_form}
#     return render(request, 'service/profile_update.html', context)

class ProfileUpdateViews(LoginRequiredMixin,UpdateView):
    """Редактирование профиля"""

    model = Profile
    form_class =  formset_factory(UserUpdateForm)
    template_name = 'service/profile_update.html'
    success_url = reverse_lazy('service')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile,telegram=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileUpdateViews,self).get_context_data(**kwargs)
    #     context['formset'] = UserInventaryFormset(queryset=Profile.objects.none())
    #     return context


class SongCreateView(LoginRequiredMixin, CreateView):
    """Создание трека"""

    model = Song
    fields = ('name', 'link', 'inventory', 'image', 'body')
    template_name = 'service/song_create.html'
    success_url = reverse_lazy('service')

    def get_context_data(self, **kwargs):
        """Фильтруем инвентарь , показываем пользователю тот инвентарь, который он добавил"""
        context = super(SongCreateView, self).get_context_data(**kwargs)
        context['form'].fields['inventory'].queryset = MusicalInventory.objects.filter(
            profile__telegram=self.request.user)
        return context

    def form_valid(self, form):
        """Добавляем профиль к заполненной форме"""
        profile = Profile.objects.get(telegram=self.request.user)
        instance = form.save(commit=False)
        instance.profile = profile
        instance.save()
        return super(SongCreateView, self).form_valid(form)


class SongUpdateView(SongCreateView, UpdateView):
    """Редактирование трека, наследуемся от SongCreateView"""

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Song.objects.filter(profile__telegram=self.request.user, slug=slug)