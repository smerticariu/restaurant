from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Menu, ORDER_SHIPPING, ORDER_PROCESSING,ORDER_ENDED
from .forms import MenuForm, OrderForm
from django.shortcuts import render
from django.contrib import messages
from restaurant.models import Menu, Order
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from restaurant.serializers import MenuSerializer, OrderSerializer,InfoSerializer
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework import status




def index(request):
    all_menus=Menu.objects.all().order_by('-date_day')
    template=loader.get_template('restaurant/menu_list.html')
    context={
        "all_menus":all_menus,
    }
    return HttpResponse(template.render(context, request))

def detail(request, menu_id):
    #import ipdb; ipdb.set_trace();
    menu=Menu.objects.get(pk=menu_id)
    order_list=Order.objects.filter(title__pk=menu_id)
    template=loader.get_template('restaurant/view_menu.html')
    total=0
    count=0
    average=0
    for order in order_list:
        if order.raiting != 0:
            total+= order.raiting
            count+=1
    try:
        average=total/count
    except:
        average=0
    context={
        "menu":menu,
        "order_list":order_list,
        "average":average
    }
    return HttpResponse(template.render(context, request))

def index_o(request):
    all_orders_list=Order.objects.all()
    paginator = Paginator(all_orders_list, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        all_orders = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        all_orders = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        all_orders = paginator.page(paginator.num_pages)
    template=loader.get_template('restaurant/order_list.html')
    context={
        "all_orders":all_orders,
    }
    return HttpResponse(template.render(context, request))


def detail_o(request, order_id):
    #import ipdb; ipdb.set_trace();
    order=Order.objects.get(pk=order_id)
    template=loader.get_template('restaurant/view_order.html')
    context={
        "order":order,
    }
    return HttpResponse(template.render(context, request))

def index_t(request):
    all_menus=Menu.objects.filter(date_day=datetime.today().date())
    template=loader.get_template('restaurant/todays_menu.html')
    context={
        "all_menus":all_menus,
    }
    return HttpResponse(template.render(context, request))

def post_new(request):
    if request.method == 'GET':
        form = MenuForm()
    elif request.method == 'POST':
        form = MenuForm(data=request.POST)
        # import ipdb; ipdb.set_trace();
        if form.is_valid():
            form.save()
            messages.success(request, "Success!")
        # else:
        #     # pass
        #     messages.error(request, "Error 411: Length Required")
    return render(request, 'restaurant/post_edit.html', {'form': form})



def change(request, order_id):
    u = Order.objects.get(pk=order_id)
    if u.status == ORDER_PROCESSING:
        u.status=ORDER_SHIPPING
        u.save()
        messages.success(request, "The order was sent!")
    else:
        messages.error(request, "Nu se poate ")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# sandru
def post_order(request):

    if request.method == 'GET':
        form = OrderForm()
    elif request.method == 'POST':
        # orders = Order.objects.all()
        #data = request.data
        form = OrderForm(data=request.POST)
        if form.is_valid():
            # import  ipdb; ipdb.set_trace();
            order = form.save()

            send_m(order)
        else:
            # pass
            messages.error(request, "Error la scriere")
    return render(request, 'restaurant/post_order.html', {'form': form})

@api_view(['GET', 'POST'])
def MenuViewSet(request):
    if request.method == 'GET':
        menus = Menu.objects.filter(date_day=datetime.today().date())
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def OrderViewSet(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order=serializer.save()
            # import ipdb; ipdb.set_trace();
            send_m(order)

            return Response("Comanda realizata de succes!", status=status.HTTP_201_CREATED)
        return Response("Comanda esuata!", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def InfoViewSet(request):
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace();
        data=request.data
        sir=data['sir']
        ids = sir.split("-")
        menu_id=ids[0]
        order_id=ids[1]
        try:
            if len(data['sir'])>=3 and ('-' in data['sir']) and len(ids)==2 and menu_id.isnumeric() and order_id.isnumeric() :

                order= Order.objects.get(id=order_id)
                serializer = InfoSerializer(order)
                # import ipdb; ipdb.set_trace();
                menu= Menu.objects.get(id=serializer.data['title'])
                if str(menu.id)==str(menu_id):
                    informatii ={
                    'dish1':menu.dish1,
                    'dish2':menu.dish2,
                    'desert':menu.desert,
                    'status': serializer.data['status']
                    }
                else:
                    return Response("Meniul dat nu corespunde", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Meniul dat nu corespunde", status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"details":str(err)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(informatii,status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
def RaitingViewSet(request):
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace();
        data=request.data
        sir=data['sir']
        ids = sir.split("-")
        menu_id=ids[0]
        order_id=ids[1]
        try:
            if len(data['sir'])>=3 and ('-' in data['sir']) and float(data['rating'])>0 and float(data['rating'])<=5.0 and len(ids)==2 and menu_id.isnumeric() and order_id.isnumeric():
                order= Order.objects.get(id=    order_id)
                if str(order_id)==str(order.id):
                    order.raiting=data['rating']
                    order.status=ORDER_ENDED
                    order.save()
                else:
                    return Response("Rating invalid", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Rating invalid", status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
             return Response({"details":str(err)}, status=status.HTTP_400_BAD_REQUEST)
        return Response("Comanda finalizata cu succes",status=status.HTTP_200_OK)





def send_m(order):
    subject = "Order confirmation"
    msg = "Va multumim pentru comanda facuta " + order.name + ". Ati comandat urmatorul meniu :" + order.title.title + " si contine: Felul 1 - " + order.title.dish1 + ", Felul 2 - " + order.title.dish2 +", Desert - " + order.title.desert + ". Numarul dvs de comanda este :" + str(order.title.pk) +"-" + str(order.pk)
    send_mail(subject, msg, "testlunch72@gmail.com", [order.email])
