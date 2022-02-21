from itertools import product
import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializer

from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer, MyOrderSerializer


@api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(item.get(
            'quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='USD',
                description='Charge from Djackets',
                source=serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, paid_amount=paid_amount)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def checkout_order(request):
#     orderItem = OrderItem(request)
#     for item in orderItem:
#         OrderItem.objects


class OrdersList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = OrderItem.objects.all()
        serializer = OrderItemSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():

            # orders = OrderItem.objects.all()

            product_quantity = Product.quantity
            # product_quantity  = product_quantity - OrderItem.quantity
            serializer.save()
            print(serializer.data["quantity"])
            print(product_quantity)
            order_product_quantity = serializer.data["quantity"]
            order_product_quantity = serializer.data["product"]
            product = request.data.get('product')
            print(product)

            quantity_product = request.data.get('quantity')
            print(quantity_product)  # legit

            products = Product.objects.filter(id=product)
            print(products)

            stock = products.first()
            print(stock)

            in_stock = stock.quantity
            # serializer2 = ProductSerializer(stock, many=True)
            print(in_stock)

            if(quantity_product > in_stock):
                return Response("Out of stock", status=status.HTTP_201_CREATED)

            in_stock = in_stock - quantity_product

            p = Product.objects.get(id=product)
            p.quantity = in_stock
            print(in_stock)
            # p.save(['quantity'])

            print(in_stock)

            stock_to_update = {'quantity': in_stock}
            print(stock_to_update)

            serializer_class = ProductSerializer

            serializer_stock = serializer_class(p,
                                                data=stock_to_update, partial=True)
            print(serializer_stock)

            # update = Product.objects.filter(
            #     quantity=in_stock).update(quantity=in_stock)
            # # update= Product.objects.filter(id=product).first().quantity.update(quantity=in_stock)

            # print(update)
            if serializer_stock.is_valid():
                # print(serializer_stock.is_valid())
                # serializer_stock.save()
                # self.perform_update(serializer_stock)

                # return Response(serializer_stock.data)
                serializer_stock.save()

                print(serializer_stock)

                print(in_stock)
            # print(serializer2.data[quantity])
            # serializer = ProductSerializer(products, many=True)

            # Product.quantity = product_quantity - order_product_quantity
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList1(APIView):
    """
    List all Orders, or create a new Order.
    """

    def get(self, request, format=None):
        orders = OrderItem.objects.all()
        serializer = OrderItemSerializer(orders, many=True)

        print(serializer.data)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    Retrieve, update or delete a Product instance.
    """

    def get_object(self, pk):
        try:
            return OrderItem.objects.filter(pk=pk)
        except OrderItem.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     serializer = ProductSerializer(product)

    #     print(serializer.data["quantity"])

    #     return Response(serializer.data)

    def put(self, request, format=None):
        # product = request.data.get('product')
        # myproduct = OrderItem.objects.filter(id=product)

        # # product = request.data.get('product')
        # print("HERE")
        # print(product)
        # product = self.get_object(pk)
        data = {

            "quantity": 8
        }
        serializer = ProductSerializer(id=2, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            print(serializer.data)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
