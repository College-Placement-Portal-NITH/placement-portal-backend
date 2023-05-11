from django.urls import path
from . import views
urlpatterns = [
    path('', views.TPRListView.as_view(), name="TPR"),
    path('<int:pk>/', views.TPRView.as_view(), name="TPR"),
]