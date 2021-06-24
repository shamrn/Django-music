import requests
import logging
from django.core.exceptions import ValidationError
#logging.basicConfig(filename="sample.log", level=logging.INFO)


def get_iframe(request,link):
    """Получаем iframe с soundcloud
        link - ссылка на трек"""

    data = {
        'format': 'json',
        'url': link
    }
    response = requests.post('https://soundcloud.com/oembed', data=data)
    if response.status_code != 200:
        pass
        #raise ValidationError({'iframe_sound': ''})
    else:
        return response.json()['html']