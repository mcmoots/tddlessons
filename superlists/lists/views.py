from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item

# Create your views here.

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/a-silly-list-url/')
    
    items = Item.objects.all()
    return render(request, 'home.html', {
        'items': items, 
    })

def view_list(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

