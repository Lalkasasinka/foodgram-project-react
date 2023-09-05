from django.contrib import admin

from .models import (Ingredient, Tag, Recipes, IngredientInRecipe)


class RecipeIngredintInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = (RecipeIngredintInline, )