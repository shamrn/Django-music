from django import forms
from .models import Profile,MusicalInventory

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('telegram','first_name','last_name','instagram')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telegram'].widget.attrs.update({'class': 'input-update', 'placeholder': 'Telegram'})
        self.fields['telegram'].widget.attrs['readonly'] = True  # убираем изменение поля telegram
        self.fields['first_name'].widget.attrs.update({'class': 'input-update', 'placeholder': 'Имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'input-update', 'placeholder': 'Фамилия'})
        self.fields['instagram'].widget.attrs.update({'class': 'input-update', 'placeholder': 'Instagram'})


