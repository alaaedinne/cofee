from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from products.models import Product
# Create your views here.

def products(request):
    products = Product.objects.all()
    name = None
    desc = None
    pfrom = None
    pto= None
    cs= None

    if 'cs' in request.GET:
        cs= request.GET['cs']
        print(cs)
        if not cs :
            cs='off'

    if 'searchname' in request.GET:
        name= request.GET['searchname']
        if name:
            if cs =='on':
                products = products.filter(name__contains=name)
            else:
                products = products.filter(name__icontains=name)
    
    if 'searchdesc' in request.GET :
        desc = request.GET['searchdesc']
        if desc:
            if cs=='on':
                products= products.filter(description__contains=desc)
            else:
                products= products.filter(description__icontains=desc)

    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
        pfrom= request.GET['searchpricefrom']
        pto= request.GET['searchpriceto']
        if pfrom and pto:
            if pfrom.isdigit() and pto.isdigit():
                products = products.filter(price__gte=pfrom , price__lte= pto )
    context={
        'products':products,
    }
    return render(request , 'products/products.html', context)

def product(request , pro_id):
    context = {
        'pro': get_object_or_404(Product , pk = pro_id)
    }
    return render(request , 'products/product.html', context)

def search(request):
    return render(request , 'products/search.html')