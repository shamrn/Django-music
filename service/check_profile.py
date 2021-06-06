from .models import Profile, MusicalInventory

def check_profile(user):
    """Функция проверяет, какие поля не заполнил пользователь,
    и в дальнейшем выдаем подсказки в шаблоне"""

    profile = Profile.objects.values('first_name', 'last_name').filter(telegram=user)
    inventory = MusicalInventory.objects.values('name').filter(profile__telegram=user)

    result = []
    for data in profile:
        if data['first_name'] == None:
            result.append('заполнить имя')
        if data['last_name'] == None:
            result.append('указать вашу фамилию')
    if len(inventory) == 0:
        result.append('добавить инвентарь')

    result = ' | '.join(result)  # для читабельности разделяем сообщения
    return result
