import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
# Create your views here.
from .serializers import LaptopSerializer, OrderSerializer, CustomerSerializer, OrderItemSerializer


@api_view(['GET','POST'])
def laptops_list(request):
    if request.method == 'GET':
        all_laptops = Laptop.objects.all()
        if 'sort' in request.GET and request.GET['sort']:
            all_laptops = all_laptops.order_by(request.GET['sort'])

        serializer = LaptopSerializer(all_laptops,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LaptopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE','PATCH'])
def laptop_details(request,pk):
        try:
            laptop = Laptop.objects.get(pk=pk)
        except Laptop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = LaptopSerializer(laptop)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = LaptopSerializer(laptop,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PATCH':
            serializer = LaptopSerializer(laptop,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        elif request.method == 'DELETE':
            laptop.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def orders_list(request):
    if request.method == 'GET':
        all_orders = Order.objects.all()
        serializer = OrderSerializer(all_orders,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        for cus in Customer.objects.all():
            if cus.id == request.data['customer']['id']:
                customer = cus
            else:
                customer = Customer(id=request.data['customer']['id'],name=request.data['customer']['name'],address=request.data['customer']['address'])
                customer.save()
        new_order = Order.objects.create(customer=customer, order_date=datetime.date.today())
        new_order.save()


        items = request.data['items']
        for item in items:
            laptop = Laptop.objects.get(id=item['id'])
            new_orderItems = OrderItems.objects.create(
            laptop=laptop,
            order=new_order,
            item_price=item['price'],
            amount=item['amount'])
            new_orderItems.save()

        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def customers(request):
    if request.method == 'GET':
        all_custs = Customer.objects.all()
        serializer = CustomerSerializer(all_custs,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        new_cust = CustomerSerializer(data=request.data)
        if new_cust.is_valid():
            new_cust.save()
            return Response(new_cust.data,status=status.HTTP_201_CREATED)
        return Response(new_cust.errors,status=status.HTTP_400_BAD_REQUEST)

