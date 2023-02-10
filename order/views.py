
from .permissions import IsAuthorOrReadOnly, PermissionMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order
from rest_framework.viewsets import ModelViewSet
from .serializers import OrderSerializer



class OrderView(PermissionMixin, ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request,
                'user': self.request.user
            } 
    

    