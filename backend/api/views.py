from rest_framework import viewsets
from recipes.models import (Ingredient, Tag, Recipes)
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from .serializers import (IngredientSerializer, TagSerializer, RecipeReadSerializer, UserSerializer, RecipeCreateSerializer) 
from .mixins import ListRetrieve, CreateDestroy
from .permissions import IsAdminOrReadOnly, SAFE_METHODS
from .pagination import LimitPagination
from .filters import RecipeFilter, IngredientFilter


User = get_user_model()


class IngredientViewSet(ListRetrieve):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ['^name', ]
    

class TagViewSet(ListRetrieve):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitPagination