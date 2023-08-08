from django.db.models import Q
from django.http import Http404
from django.db import transaction
from rest_framework.response import Response
from rest_framework import generics, permissions, status, filters



from account.models import User
from .models import App, Purchase
from utils.permissions import IsOwner
from .serializers import AppSerializer, AppOwnerSerializer, PurchaseSerializer


# /// App Views ///


class AppListAPIView(generics.ListAPIView):
    serializer_class = AppSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        return App.objects.filter(is_verified=True)
    

class AppRetrieveAPIView(generics.RetrieveAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        obj = super().get_object()
        if obj.is_verified == False:
            raise Http404()
        return obj


class AppOwnerListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AppOwnerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.app_set.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# TODO When app edited change verified false 
class AppOwnerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = App.objects.all()
    serializer_class = AppOwnerSerializer
    permission_classes = [permissions.IsAuthenticated ,IsOwner]


# /// Purchase Views ///


class PurchaseCreateAPIView(generics.CreateAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)

    @transaction.atomic
    def create(self, request, app_id, *args, **kwargs):
        try:
            app = App.objects.get(~Q(owner=request.user), pk=app_id, is_verified=True)
        except App.DoesNotExist:
            raise Http404
        
        try:
            Purchase.objects.get(owner=request.user, app=app)
            return Response({'detail': 'This app has been purchased'}, status=status.HTTP_400_BAD_REQUEST) 
        
        except Purchase.DoesNotExist:
            with transaction.atomic():
                buyer_profile = User.objects.select_for_update().get(id=request.user.id)
                if buyer_profile.credit >= app.price:
                    seller_profile = User.objects.select_for_update().get(id=app.owner.id)

                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(owner=request.user, app=app)

                    # Deduct the app price from the buyer's credit
                    buyer_profile.credit -= app.price
                    buyer_profile.save()

                    # Increase the app price to the seller's credit
                    seller_profile.credit += app.price
                    seller_profile.save()
                    
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'detail': 'Insufficient credit'}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseListAPIView(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Purchase.objects.filter(owner=self.request.user)


class PurchaseRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]