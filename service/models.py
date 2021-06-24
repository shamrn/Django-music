from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    """Таблица профиля"""
    telegram = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    instagram = models.CharField(max_length=150, null=True, blank=True)


class MusicalInventory(models.Model):
    """Таблица инвентаря пользователя"""
    profile = models.ForeignKey(Profile, related_name='inventory', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Название инвентаря')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.song_set.count() > 0:
            raise ValidationError({'name': 'Инвентарь добавлен в трек, удаление запрещено'})
        else:
            super(MusicalInventory, self).delete(*args, **kwargs)

class Song(models.Model):
    """Таблица трека"""
    profile = models.ForeignKey(Profile, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Название трека')
    slug = models.SlugField()
    link = models.URLField(verbose_name='Ссылка на трек')
    inventory = models.ManyToManyField(MusicalInventory,verbose_name='Инвентарь')
    image = models.ImageField(upload_to=f'image/', blank=True, verbose_name='Изображение')
    body = models.TextField(blank=True, null=True, verbose_name='Описание')
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    iframe_sound = models.TextField()
    like = models.SmallIntegerField(default=0)
    dislike = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ('-date_created',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Song, self).save(*args, **kwargs)


class Like(models.Model):
    """Таблица лайков"""
    CHOICES_ACTIONS = (
        ('like', 'like'),
        ('dislike', 'dislike'),
    )

    profile = models.ForeignKey(Profile, related_name='like', blank=True, null=True, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='song', on_delete=models.CASCADE)
    actions = models.CharField(max_length=50, blank=True, null=True, choices=CHOICES_ACTIONS)
