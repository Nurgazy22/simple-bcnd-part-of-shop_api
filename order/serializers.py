from rest_framework import serializers
from .models import Order, OrderItem, Favorite


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_sum', 'items']

    def create(self, validated_data):
        items = validated_data.pop('items')
        validated_data['author'] = self.context.get('user')
        order = super().create(validated_data)
        total_sum = 0
        order_items = []
        for item in items:
            print(item)
            order_items.append(OrderItem(order=order, product=item['product'], quantity=item['quantity']))
            total_sum += item['product'].price * item['quantity']
        OrderItem.objects.bulk_create(order_items)
        order.total_sum = total_sum
        order.save()
        return order
    

class FavoriteSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')
    product = serializers.ReadOnlyField()

    class Meta:
        model = Favorite
        fields = '__all__'
    









