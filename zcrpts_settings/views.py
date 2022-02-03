from Products.forms import SearchForm
from django.shortcuts import render

def home(request, **kwargs):
    context = {'search_form': SearchForm}
    return render(request, 'home.html', context)