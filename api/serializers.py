import pdb
from rest_framework import serializers
from .models import NseStock, OrderProduct, Position, WatchList, Order, OrderAction, OrderStatus, OrderType, UserKYC, UserDocument, KYCDocumentName, UserFund, UserBankDetail
from django.contrib.auth import get_user_model


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


class NseStockSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = NseStock
        fields = "__all__"


class StockCodesSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = NseStock
        fields = ('id', 'code', )


class StockNameSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = NseStock
        fields = ('id', 'name', )


class ReadOnlyWatchListSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = WatchList
        fields = (
            'stocks',
        )
        depth = 1


class WatchListSerializer(serializers.ModelSerializer):

    stocks = serializers.PrimaryKeyRelatedField(
        many=True, queryset=NseStock.objects.all())

    class Meta:
        model = WatchList
        fields = (
            'id',
            'user',
            'stocks',
        )

    def create(self, validated_data, *args, **kwargs):
        stocks = validated_data.pop("stocks")
        user = validated_data.get('user')

        watchlist_qs = WatchList.objects.filter(
            user=user)

        if watchlist_qs.exists():
            watchlist_obj = watchlist_qs.first()
            for stock in stocks:
                watchlist_obj.stocks.add(stock)
            return watchlist_obj

        created_obj = WatchList.objects.create(**validated_data)

        created_obj.stocks.set(stocks)
        return created_obj

    def update(self, instance, validated_data):
        stocks = validated_data.pop('stocks')
        instance = super(WatchListSerializer, self).update(
            instance, validated_data)

        for stock in stocks:
            stock_qs = NseStock.objects.filter(id=stock.id)

            if stock_qs.exists():
                stock = stock_qs.first()

            instance.stocks.add(stock)

        return instance


class OrderReadOnlySerializer(ReadOnlyModelSerializer):

    order_type = serializers.ReadOnlyField(source="order_type.name")
    action = serializers.ReadOnlyField(source="action.action")
    status = serializers.ReadOnlyField(source="status.status")
    stock = serializers.ReadOnlyField(source="stock.name")
    stock_code = serializers.ReadOnlyField(source="stock.code")
    product = serializers.ReadOnlyField(source="product.product")

    class Meta:
        model = Order
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    action = serializers.SlugRelatedField(
        queryset=OrderAction.objects.all(), slug_field="action")
    status = serializers.SlugRelatedField(
        queryset=OrderStatus.objects.all(), slug_field="status")
    order_type = serializers.SlugRelatedField(
        queryset=OrderType.objects.all(), slug_field="name")
    stock = serializers.SlugRelatedField(
        queryset=NseStock.objects.all(), slug_field="code")
    product = serializers.SlugRelatedField(
        queryset=OrderProduct.objects.all(), slug_field="product")

    class Meta:
        model = Order
        fields = (
            'user',
            'order_id',
            'stock',
            'quantity',
            'order_type',
            "action",
            "status",
            "margin",
            'price',
            'stop_loss',
            'product',
            'leverage',
            'created_on',
            'updated_on',
        )

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Quantity cannot be a negative number!")

        return value

    def validate_price(self, value):
        if value < float(0):
            raise serializers.ValidationError('Price cannot be less than 0')

        if value == float(0):
            raise serializers.ValidationError('Price cannot be 0.')

        return value


class KYCDocumentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCDocumentName
        fields = "__all__"


class UserDocumentSerializer(serializers.ModelSerializer):

    doc_name = serializers.ReadOnlyField(source="document_name.name")

    class Meta:
        model = UserDocument
        fields = "__all__"


class UserKYCSerializer(serializers.ModelSerializer):

    documents = UserDocumentSerializer(
        source='userkycdocuments', many=True, read_only=True)

    class Meta:
        model = UserKYC
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = "__all__"


class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderStatus
        fields = "__all__"


class OrderActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAction
        fields = "__all__"


class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = "__all__"


class OrderReadOnlyPositionSerializer(ReadOnlyModelSerializer):

    action = OrderActionSerializer(read_only=True)
    status = OrderStatusSerializer(read_only=True)
    order_type = OrderTypeSerializer(read_only=True)
    stock = serializers.SlugRelatedField(
        queryset=NseStock.objects.all(), slug_field="name")
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = ["user"]


class ReadOnlyPositionSerializer(ReadOnlyModelSerializer):
    order = OrderReadOnlyPositionSerializer(read_only=True)

    class Meta:
        model = Position
        exclude = ["user"]
        depth = 1


class ReadOnlyUserFundSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = UserFund
        fields = "__all__"


class UserBankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBankDetail
        fields = "__all__"


class ReadOnlyUserBankDetailSerializer(ReadOnlyModelSerializer):

    class Meta:
        model = UserBankDetail
        fields = "__all__"
