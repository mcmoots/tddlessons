from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from lists.models import Item, List

# Create your views here.

def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    the_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': the_list})


def new_list(request):
    the_list = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=the_list)
    try:
        item.full_clean()
    except ValidationError:
        the_list.delete()
        error = '🐬 No empty sea creatures allowed!'
        return render(request, 'home.html', {"error": error})
    return redirect('/lists/%d/' % (the_list.id,))


def add_item(request, list_id):
    the_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=the_list)
    return redirect('/lists/%d/' % (the_list.id,))
