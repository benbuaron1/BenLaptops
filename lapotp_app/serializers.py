from rest_framework import serializers
from .models import *

class LaptopSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    inches = serializers.IntegerField(read_only=True)
    screen_width = serializers.IntegerField(read_only=True)
    screen_height = serializers.IntegerField(read_only=True)
    cpu = serializers.CharField(read_only=True)
    ram = serializers.IntegerField(read_only=True)
    memory1_storage = serializers.CharField(read_only=True)
    memory1_type = serializers.CharField(read_only=True)
    memory1_GOT = serializers.CharField(read_only=True)
    memory2_storage = serializers.CharField(read_only=True)
    memory2_type = serializers.CharField(read_only=True)
    memory2_GOT = serializers.CharField(read_only=True)
    os = serializers.CharField(read_only=True)
    weight_kg = serializers.CharField(read_only=True)
    manufacturer = serializers.CharField(read_only=True)

    class Meta:
        model = Laptop
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        # depth = 1

class OrderItemSerializer(serializers.ModelSerializer):
    # order = OrderSerializer(many=True)
    # laptop = LaptopSerializer(many=True)
    class Meta:
        model = OrderItems
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AddOrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    laptop = serializers.PrimaryKeyRelatedField(queryset=Laptop.objects.all())
    amount = serializers.IntegerField(required=True)
    item_price = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    class Meta:
        model = Order
        fields = '__all__'