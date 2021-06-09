from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from service.models import Song, Profile
from .like import proc_like


class SongListView(ListView):
    """Главная страница, список треков"""

    model = Song
    paginate_by = 4
    context_object_name = 'songs'
    template_name = 'pages/song_list.html'

    def get_queryset(self):
        """Фильтрация треков"""

        songs = Song.objects.all()
        if 'get_param' in self.kwargs:
            param = self.kwargs['get_param']
            if param == 'like':
                songs = Song.objects.order_by('-like')
        return songs


def like_song(request, actions, pk):
    """Функция лайков,дизлайков
        actions - действия пользователя, лайк или дизлайк
        pk - id трека"""

    if not request.user.is_authenticated:  # если пользователь не вошел, отправляем его на страницу авторизации
        return redirect('login')
    else:
        profile = Profile.objects.get(telegram=request.user)
        proc_like(profile, actions, pk)
        return redirect('song_list')


def song_detail(request, slug):
    song = get_object_or_404(Song, slug=slug)
    author = Profile.objects.filter(telegram=song.profile)
    context = {'song': song, 'author': author}
    return render(request, 'pages/song_detail.html', context)


def author_detail(request, pk):
    author = Profile.objects.get(pk=pk)
    permission_edit = False
    if author.telegram == str(
            request.user):  # проверяем, если пользователь является автором, добавляем ему кнопки редактирования
        permission_edit = True
    songs = Song.objects.filter(profile=author)
    context = {'author': author, 'songs': songs, 'permission_edit': permission_edit}
    return render(request, 'pages/author_detail.html', context)
