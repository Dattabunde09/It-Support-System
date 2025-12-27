from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TicketViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]

