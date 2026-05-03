from django.http import Http404, JsonResponse, HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.paginator import Paginator
from ..payments.stripe_service import stripe_service
from ..models import Item, Order

def index(request: HttpRequest):
    items = Item.objects.all()
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    return render(request, "paymentsystem/index.html", {"items": page_data})

def item(request: HttpRequest, id):
    try:
        item = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404("Item does not exists!")
    return render(request, "paymentsystem/item.html", {"item": item, "stripe_api_key": settings.STRIPE_API_KEY_PUBLISH})

def buy_order(request: HttpRequest, id):
    try:
        order = Order.objects.get(pk=id)
        session = stripe_service.create_checkout_session_order(order)
        return redirect(session.url)
    except Order.DoesNotExist:
        raise Http404("Order does not exists")
    except Exception as error:
        return HttpResponse(str(error))


def buy(request: HttpRequest, id):
    try:
        item = Item.objects.get(pk=id)
        session = stripe_service.create_checkout_session_product(item)
        return JsonResponse({"url": session.url})
    except Item.DoesNotExist:
        raise Http404("Item does not exists!")
    except Exception as error:
        return HttpResponse(str(error))
    

def success(request: HttpRequest):
    return render(request, "paymentsystem/success.html")

def cancel(request: HttpRequest):
    return render(request, "paymentsystem/cancel.html")
        