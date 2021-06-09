
import requests
from django.contrib import messages
from django.http import HttpResponseRedirect


def get_iframe(request,link):
    """Получаем iframe с soundcloud
        link - ссылка на трек"""

    data = {
        'format': 'json',
        'url': link
    }
    response = requests.post('https://soundcloud.com/oembed', data=data)
    if response.status_code != 200:
        messages.error(request,'Ссылка некорректна')
        return 'error in the link'
    else:
        return response.json()['html']