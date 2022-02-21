from itertools import product
from rest_framework import serializers

from .models import Order, OrderItem

from product.serializers import ProductSerializer

class MyOrderItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer()


    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )

    def validate(self, data):
        # validates the data passed to the order item

        product = data['product']
        quantity = data['quantity']
        if not product.is_available:  # may be out of order
            raise serializers.ValidationError("this product is not available right now")
        for item in data["quantity"]:
            pass


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "place",
            "phone",
            "stripe_token",
            "items",
            "paid_amount"
        )

class OrderItemSerializer(serializers.ModelSerializer):   
    # product = ProductSerializer(many = True) 
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )
    # def create(self, validated_data):
    #     prod = validated_data.pop('product')
    #     order = OrderItem.objects.create(**validated_data)
    #     # for i in prod:
    #     #     Album.objects.create(artist=order, **i)
    #     return order

    # def update(self, instance, validated_data):
    #     prod = validated_data.pop('product')
    #     prods = (instance.product).all()
    #     prods = list(prods)
    #     instance.quantity = validated_data.get('quantity', instance.quantity)
        
    #     instance.save()

    #     for i in prod:
    #         album = prods.pop(0)
    #         album.quantity = i.get('quantity', album.quantity)
           
    #         album.save()
    #     return instance
    


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "place",
            "phone",
            "stripe_token",
            "items",
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order