from django.urls import path, include
from .views import *

urlpatterns = [
    path('products/', ProductAPIView.as_view()),
    path('products/<int:pk>/', ProductAPIView.as_view()),
    path('orders/', OrderAPIView.as_view()),
    path('orders/<int:pk>/', OrderAPIView.as_view()),
    path('health/', HealthBlogAPIView.as_view()),
    path('health/<int:pk>/', HealthBlogAPIView.as_view()),
    path('month/', MonthlyPromotionAPIView.as_view()),
    path('month/<int:pk>/', MonthlyPromotionAPIView.as_view()),
    path('catalogs/', CatalogAPIView.as_view()),
    path('catalogs/<int:pk>/', CatalogAPIView.as_view()),
    path('categories/', CategoryAPIView.as_view()),
    path('categories/<int:pk>/', CategoryAPIView.as_view()),
    path('pop_brands/', PopularBrandAPIView.as_view()),
    path('pop_brands/<int:pk>/', PopularBrandAPIView.as_view()),
    path('persons/', PersonalAccountAPIView.as_view()),
    path('persons/<int:pk>/', PersonalAccountAPIView.as_view()),
    path('auth/', include("rest_framework.urls"))
]
