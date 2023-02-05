from rest_framework import serializers
from logistic.models import Product, Stock,StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

    


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'price', 'quantity']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id','address', 'positions']
    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        for position in positions:
            position['stock'] = stock
            StockProduct.objects.create(**position)
        
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for position in positions:
            try:
                position_product = position.get('product')
                stock_item = StockProduct.objects.get(stock=stock, product=position_product)
                stock_item.quantity = position.get('quantity', stock_item.quantity)
                stock_item.price = position.get('price', stock_item.price)
                stock_item.save()
            except StockProduct.DoesNotExist:
                StockProduct.objects.create(stock=stock, **position)
        

        return stock
