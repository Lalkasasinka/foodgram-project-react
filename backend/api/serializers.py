from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField
from recipes.models import (Ingredient, Tag, Recipes, IngredientInRecipe, Favorite)
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer, UserSerializer as DjoserUserSerializer
from users.models import User


class UserCreateSerializer(DjoserUserCreateSerializer):
    
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            'password', 
        )
    

class UserSerializer(DjoserUserSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

     class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    ingredients = IngredientInRecipeReadSerializer(many=True, source='ingredient_list')
    author = UserSerializer()

    class Meta:
        model = Recipes
        fields = ('id', 'tag', 'author', 'ingredients', 'name', 'description', 'cooking_time')


class IngredientInRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')

class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipeCreateSerializer(many=True) 
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipes
        fields = ('id', 'tag', 'author', 'ingredients', 'name', 'description', 'cooking_time')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tag = validated_data.pop('tag')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tag.set(tag)
        for i in ingredients:
            ingredient = Ingredient.objects.get(id=i['id'])
            IngredientInRecipe.objects.create(
                ingredient=ingredient, recipe=recipe, amount=i['amount']
            )
        return recipe
    
    def to_representation(self, instance):
        return RecipeReadSerializer(instance).data