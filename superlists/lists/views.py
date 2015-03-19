from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item, List

# Create your views here.

def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    stupid_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=stupid_list)
    return redirect('/lists/a-silly-list-url/')
