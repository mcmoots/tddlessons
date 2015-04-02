from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from lists.models import Item, List

# Create your views here.

def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    the_list = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=the_list)
            item.full_clean()
            item.save()
            return redirect('/lists/%d/' % (the_list.id,))
        except ValidationError:
            error = '🐬 No empty sea creatures allowed!'

    return render(request, 'list.html', {'list': the_list, 'error': error})


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

