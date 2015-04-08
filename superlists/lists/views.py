from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from lists.forms import ItemForm
from lists.models import Item, List

# Create your views here.

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    the_list = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=the_list)
            return redirect(the_list)
    return render(request, 'list.html', {'list': the_list, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        the_list = List.objects.create()
        form.save(for_list=the_list)
        return redirect(the_list)
    else:
        return render(request, 'home.html', {"form": form})

