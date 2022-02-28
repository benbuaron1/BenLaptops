import datetime

from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .custom_queries import top_laptops, score_by_manu, cheap_but_rate
from .models import *
from .serializers import LaptopSerializer, OrderSerializer, CustomerSerializer, OrderItemSerializer, ReviewSerializer, \
    ReviewUpdateSerializer


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
        with transaction.atomic():
            for cus in Customer.objects.all():
                if cus.id == request.data['customer']['id']:
                    customer = cus
                else:
                    customer = Customer(
                        id=request.data['customer']['id'],
                        name=request.data['customer']['name'],
                        address=request.data['customer']['address'])
                    customer.save()
            new_order = Order.objects.create(customer=customer, order_date=datetime.date.today())
            new_order.save()


            items = request.data['items']
            for item in items:
                laptop = Laptop.objects.get(id=item['id'])
                if item['amount'] <= int(laptop.stock_amount):
                    laptop.stock_amount -= item['amount']
                    laptop.save()
                else:
                    return Response(status.HTTP_400_BAD_REQUEST)
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


@api_view(['GET','POST'])
def review(request):
    if request.method == 'GET':
        all_revs = Review.objects.all()
        serializer = ReviewSerializer(all_revs,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        new_rev = ReviewSerializer(data=request.data)
        if new_rev.is_valid():
            new_rev.save()
            return Response(new_rev.data,status=status.HTTP_201_CREATED)
        return Response(new_rev.errors,status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PATCH','DELETE'])
def review_by_id(request,pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ReviewUpdateSerializer(review,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def best_laptops(request):
    limit = 2
    result = top_laptops(limit)
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET'])
def reviews_manufactorer(request):
    result = score_by_manu()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET'])
def cheap_rate(request):
    limit = 5
    result = cheap_but_rate(limit)
    return Response(result,status=status.HTTP_200_OK)