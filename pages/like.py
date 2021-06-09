from service.models import Profile, Like, Song


def proc_like(user, actions, pk):
    """Функция лайков, 1 пользователь может поставить 1 лайк или дизлайк
    user - пользователь
    actions - действие(лайк/дизлайк)
    pk - id трека"""

    song_obj = Song.objects.get(pk=pk)
    if not Like.objects.filter(profile=user,song=song_obj).exists():  # Если пользователь еще не ставил лайк/дизлайк,
        # создаем новое поле с пользователем, и треком.
        like_obj = Like(profile=user, song=song_obj)
    else:
        like_obj = Like.objects.get(profile=user, song=song_obj)
    # Если пользователь еще не ставил лайк/дизлайк, исходя из его действия(actions) добавляем к полю трека ,лайк или дизлайк
    if not like_obj.actions:
        if actions == 'like':
            like_obj.actions = 'like'  # указываем какое действие было у пользователя
            song_obj.like += 1
        elif actions == 'dislike':
            like_obj.actions = 'dislike'
            song_obj.dislike += 1
    else:
        if actions == 'like' and like_obj.actions == 'like':  # если пользователь ставит еще один лайк , убираем лайк
            song_obj.like -= 1
            like_obj.actions = ''
        elif actions == 'dislike' and like_obj.actions == 'dislike':
            song_obj.dislike -= 1
            like_obj.actions = ''

        elif actions == 'like' and like_obj.actions == 'dislike':  # меняем местами лайк/дизлайк
            song_obj.like += 1
            song_obj.dislike -= 1
            like_obj.actions = 'like'

        elif actions == 'dislike' and like_obj.actions == 'like':
            song_obj.like -= 1
            song_obj.dislike += 1
            like_obj.actions = 'dislike'

    song_obj.save()
    like_obj.save()
