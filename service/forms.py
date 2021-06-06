from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from .models import Profile,MusicalInventory,Song


class UserUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telegram'].widget.attrs.update({'class': 'input-update', 'placeholder': 'Telegram'})
        self.fields['telegram'].widget.attrs['readonly'] = True  # отключаем изменение поля telegram
        self.fields['first_name'].widget.attrs.update({'class': 'input-update', 'placeholder': 'Имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'input-update', 'placeholder': 'Фамилия'})
        self.fields['instagram'].widget.attrs.update({'class': 'input-update', 'placeholder': 'Instagram'})

    class Meta:
        model = Profile
        fields = ('telegram','first_name','last_name','instagram')

class UserInventoryForm(forms.ModelForm):

    class Meta:
        model = MusicalInventory
        fields = ('name',)


UserInventaryFormset = modelformset_factory(Profile,extra=1,form=UserUpdateForm,fields = ('telegram','first_name','last_name','instagram'))
