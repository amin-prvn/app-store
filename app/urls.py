from django.urls import path

from .views import (
    AppListAPIView, 
    AppRetrieveAPIView, 
    AppOwnerListCreateAPIView, 
    AppOwnerRetrieveUpdateDestroyAPIView, 
    PurchaseCreateAPIView,
    PurchaseListAPIView,
    PurchaseRetrieveAPIView,
    )


urlpatterns = [
    path('app/', AppListAPIView.as_view()),
    path('app/<int:pk>/', AppRetrieveAPIView.as_view()),
    
    path('user/app/', AppOwnerListCreateAPIView.as_view()),
    path('user/app/<int:pk>/', AppOwnerRetrieveUpdateDestroyAPIView.as_view()),
    path('user/app/<int:app_id>/purchase/', PurchaseCreateAPIView.as_view()),
    path('user/purchase/', PurchaseListAPIView.as_view()),
    path('user/purchase/<int:pk>/', PurchaseRetrieveAPIView.as_view()),
]