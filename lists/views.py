from django.shortcuts import redirect, render, get_object_or_404
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

def view_list(request, pk):
    list_ = get_object_or_404(List, pk=pk)
    return render(request, 'list.html', {'list': list_})

def add_item(request, pk):
    list_ = List.objects.get(pk=pk)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')