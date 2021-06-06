from django.shortcuts import render
from django.views.generic import ListView
from service.models import Song



class SongListView(ListView):
    model = Song
    paginate_by = 7
    context_object_name = 'songs'
    template_name = 'pages/song_list.html'
