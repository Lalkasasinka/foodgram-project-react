from django.core.validators import MinValueValidator
from django.db import models
from users.models import User
from django.db.models import UniqueConstraint


NAME_LIMIT=150


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=NAME_LIMIT)
    measurement_unit = models.CharField('Единица измерения', max_length=NAME_LIMIT)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField('Название', max_length=NAME_LIMIT, unique=True)
    color = models.CharField('Цветовой HEX-код', unique=True, max_length=7)
    slug = models.SlugField('Уникальный слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', related_name='recipe')
    name = models.CharField('Название', max_length=NAME_LIMIT)
    image = models.ImageField('Изображение рецепта', upload_to='recipes/media/')
    description = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField('Время приготовления', validators=[MinValueValidator(1, 'Минимальное время приготовления 1')])
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInRecipe', verbose_name='Ингредиенты', related_name='recipes')
    tag = models.ManyToManyField(Tag, verbose_name='Теги', related_name='recipe')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.name
    

class  IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='ingredient_list')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField('Количество', validators=[MinValueValidator(1, 'Минимальное количество 1')])

    def __str__(self):
        return f'{self.ingredient} {self.amount}'
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_unique'
            )
        ]


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, verbose_name='Рецпет', related_name='favorite')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='favorite')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('recipe', 'author'),
                name='unique_author_favorite'
            )
        ]

    def __str__(self):
        return f'{self.author} добавил {self.recipe} в избранное!'
