from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from .models import Profile, MusicalInventory, Song
from .forms import UserUpdateForm, UserInventoryForm
from django.forms import inlineformset_factory
from .check_profile import check_profile
from .api_sound import get_iframe


@login_required
def service(request):
    """Страница личного кабинета"""

    user = request.user
    if not Profile.objects.filter(telegram=user).exists():  # если профиль не создан
        Profile.objects.create(telegram=user)  # создаем профиль , записываем только ник с телеграма
        return redirect('profile_update')  # и перенаправляем пользователя, на заполнение профиля данными

    acces_create_song = check_profile(user)  # Проверяем может ли пользователь добавлять трек
    songs = Song.objects.filter(profile__telegram=user)
    profile = Profile.objects.get(telegram=user)
    context = {'songs': songs, 'acces_create_song': acces_create_song, 'profile': profile}
    return render(request, 'service/service.html', context)


class ProfileUpdateViews(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""

    model = Profile
    form_class = UserUpdateForm
    template_name = 'service/profile_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, telegram=self.request.user)

    def get_success_url(self):
        """Если у пользователя пуст список инвентаря, отправляем его на страницу заполнения"""
        if not MusicalInventory.objects.filter(profile__telegram=self.request.user).exists():
            return reverse_lazy('inventory_update')
        else:
            return reverse_lazy('service')


def inventory_update(request):
    """Редактирование инвентаря"""

    profile = Profile.objects.get(telegram=request.user)
    inventory_formset = inlineformset_factory(Profile, MusicalInventory, form=UserInventoryForm, fields=('name',),
                                              extra=2)
    if request.method == 'POST':
        formset = inventory_formset(request.POST, instance=profile)
        if formset.is_valid():
            try:
                formset.save()
            except:
                formset._errors["name"] = ErrorList([u"Инвентарь добавлен в трек, удаление запрещено"])

        # У пользователя на выбор 2 кнопки 'Сохранить и выйти' и 'сохранить и добавить поле', если пользователь
        # нажимает 'сохранить и выйти' в запрос добавляется exit
        if 'exit' in request.POST:
            return redirect('service')
        else:
            return redirect('inventory_update')
    formset = inventory_formset(instance=profile)
    return render(request, 'service/inventory_update.html', {'formset': formset})


class SongCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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
        # Добавляем профиль к заполненной форме
        profile = Profile.objects.get(telegram=self.request.user)
        instance = form.save(commit=False)
        instance.profile = profile
        # Парсим iframe по ссылке
        instance.iframe_sound = get_iframe(self.request,
                                           instance.link)
        instance.save()
        return super(SongCreateView, self).form_valid(form)


class SongUpdateView(SongCreateView, UpdateView):
    """Редактирование трека, наследуемся от нашего класса SongCreateView"""

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Song.objects.filter(profile__telegram=self.request.user, pk=pk)


def song_delete(request, pk):
    _ = get_object_or_404(Song, profile__telegram=request.user, pk=pk).delete()
    return redirect('service')
