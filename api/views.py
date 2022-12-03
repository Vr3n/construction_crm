from django.contrib.auth import get_user_model, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from django.http import JsonResponse
from rest_framework import status
from .models import NseStock, Position, UserBankDetail, UserFund, WatchList, Order, UserKYC, UserDocument, KYCDocumentName
from .serializers import (NseStockSerializer,  ReadOnlyPositionSerializer, ReadOnlyUserFundSerializer, StockCodesSerializer, StockNameSerializer, WatchListSerializer,
                          OrderReadOnlySerializer, OrderSerializer, ReadOnlyWatchListSerializer, UserKYCSerializer, UserDocumentSerializer, KYCDocumentNameSerializer,
                          UserBankDetailSerializer, ReadOnlyUserBankDetailSerializer)

# Create your views here.

User = get_user_model()


class NseStockListView(ListAPIView):
    queryset = NseStock.objects.all()
    serializer_class = NseStockSerializer


class NseStockCodeListView(ListAPIView):
    queryset = NseStock.objects.all()
    serializer_class = StockCodesSerializer


class NseStockNameListView(ListAPIView):
    queryset = NseStock.objects.all()
    serializer_class = StockNameSerializer


class WatchListView(ListAPIView):
    serializer_class = ReadOnlyWatchListSerializer

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


class WatchListCreateView(CreateAPIView):
    serializer_class = WatchListSerializer

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


class WatchListDeleteView(DestroyAPIView):
    serializer_class = WatchListSerializer

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


@api_view(["DELETE"])
def watchlist_item_delete_view(request, code):
    watchlist_qs = WatchList.objects.filter(user=request.user)
    stock = NseStock.objects.get(code=code)

    if watchlist_qs.exists():
        watchlist_obj = watchlist_qs.first()
        watchlist_obj.stocks.remove(stock)
        watchlist_obj.save()
        return Response({"message": "Removed Successfully!"})

    return Response({"message": "The Item was not found!"}, status=status.HTTP_404_NOT_FOUND)


class OrderListView(ListAPIView):
    serializer_class = OrderReadOnlySerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_deleted=False)


class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderUpdateView(UpdateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# class OrderDeleteView(DestroyAPIView):
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)


@api_view(['DELETE'])
def order_delete_view(request, pk):
    order = Order.objects.filter(user=request.user, pk=pk).first()

    order.is_deleted = True
    order.save()
    return Response({"message": f"Order Deleted Successfully"})


def checkUserAuthenticated(request):
    """
    Check if User is Authenticated.
    """
    if request.user.is_authenticated:
        user = request.user
        user_details = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile_number': user.mobile_number,
            'is_authenticated': True,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'available_margin': user.userfunds.available_margin,
        }
        return JsonResponse(user_details)

    user_details = {
        'is_authenticated': False
    }
    return JsonResponse(user_details)


@api_view(["POST"])
def userLogout(request):
    """
    Logout the User.
    """

    logout(request)
    return JsonResponse({
        "is_authenticated": False
    },)


# class OrderHistoryList(ListAPIView):
class UserKYCRetriveAPIView(ListAPIView):
    """
    Readonly api used to send the user kyc instance
    """

    serializer_class = UserKYCSerializer

    def get_queryset(self):
        return UserKYC.objects.filter(user=self.request.user)


class KYCDocumentNameListView(ListAPIView):
    """
    Read only serializer for sending list of kyc documents.
    """

    serializer_class = KYCDocumentNameSerializer

    def get_queryset(self):
        return KYCDocumentName.objects.all()


class PositionListView(ListAPIView):
    """
    Read only serializer for sending list of Postions.
    """

    serializer_class = ReadOnlyPositionSerializer

    def get_queryset(self):
        return Position.objects.filter(user=self.request.user)


class UserFundListView(ListAPIView):
    """
    List of User Funds
    """

    serializer_class = ReadOnlyUserFundSerializer

    def get_queryset(self):
        return UserFund.objects.filter(user=self.request.user)


class UserBankDetailListView(ListAPIView):
    """
    List of User Bank Details.
    """

    serializer_class = ReadOnlyUserBankDetailSerializer

    def get_queryset(self):
        return UserBankDetail.objects.filter(user=self.request.user)


class UserBankDetailCreateView(CreateAPIView):
    """
    Create View for User Banks.
    """

    serializer_class = UserBankDetailSerializer


class UserBankDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Detail, Update, Delete View for API.
    """

    serializer_class = UserBankDetailSerializer

    def get_queryset(self):
        return UserBankDetail.objects.filter(user=self.request.user)
