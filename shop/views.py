from operator import truediv
from unicodedata import category, name
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.


def index(request):
    # products = Product.objects.all()
    # print(products)

    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    # allProds = [[products, range(1, nSlides), nSlides], [
    #     products, range(1, nSlides), nSlides]]
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = ceil(n/4)
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        # print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thankq = True
        return render(request, 'shop/contact.html', {'thankq': thankq})

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(
                        {"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)

                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.sub_category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = ceil(n/4)
        if n != 0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds, 'msg': ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search"}
    return render(request, 'shop/search.html', params)


def productView(request, myid):
    # Fetching product using its id
    product = Product.objects.filter(id=myid)
    # print(product)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Order(items_json=items_json, name=name, email=email,
                      address=address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed")
        update.save()

        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})

    return render(request, 'shop/checkout.html')
