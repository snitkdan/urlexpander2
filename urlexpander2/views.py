from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from .models import Url
from .forms import UrlForm

import requests, bs4

class IndexView(generic.ListView):
    template_name = 'index'
    context_object_name = 'all_urls'
    def get_queryset(self):
        return Url.objects.all()

class DetailView(generic.DetailView):
    model = Url
    template_name = 'detail'

def add_url(request):
    new_url = Url()
    shortened_url = request.POST['new_url']
    r = requests.get(shortened_url)
    beautiful = bs4.BeautifulSoup(r.text)
    new_url.shortened = shortened_url
    new_url.title = beautiful.title.text
    new_url.destination = r.url
    new_url.status = r.status_code
    new_url.save()
    return render(request, 'detail', {'url':new_url})

class UrlUpdate(UpdateView):
    model = Url
    fields = ['shortened', 'destination', 'status', 'title']

class UrlDelete(DeleteView):
    model = Url
    success_url = reverse_lazy('index')











