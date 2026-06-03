import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


# Ingredient
def test_ingredient_creation():
    "правильно ли инициализируются атрибуты  ингредиента"
    ing = Ingredient("Мука", 500.0, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"


def test_ingredient_str():
    "проверка метода __str__."
    ing = Ingredient("Мука", 500.0, "г")
    assert str(ing) == "Мука: 500.0 г"


def test_ingredient_equality():
    "проверим логику сравнения __eq__"
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 300.0, "г")  
    ing3 = Ingredient("Сахар", 500.0, "г") 
    ing4 = Ingredient("Мука", 500.0, "кг")

    assert ing1 == ing2
    assert ing1 != ing3
    assert ing1 != ing4

# Recipe
def test_recipe_creation():
    "проверка(конструктора) правильности инициализации класса рецепт"
    ing = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Блины", [ing])
    assert recipe.title == "Блины"
    assert recipe.ingredients == [ing]


def test_recipe_add_new_ingredient():
    "проверка на добавление нового ингредиента"
    recipe = Recipe("Скрэмбл")
    ing = Ingredient("Яйцо", 2.0, "шт")
    recipe.add_ingredient(ing)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Яйцо"


def test_recipe_add_duplicate_ingredient():
    "проверка на правильность добавления дубликата(сумируется)"
    recipe = Recipe("Борщ")
    recipe.add_ingredient(Ingredient("Соль", 1.0, "ч.л."))
    recipe.add_ingredient(Ingredient("Соль", 3.0, "ч.л."))

    assert len(recipe.ingredients) == 1  
    assert recipe.ingredients[0].quantity == 4.0  


def test_recipe_scale():
    "проверка на увелечение количества порций для рецепта"
    ing = Ingredient("Молоко", 200.0, "мл")
    recipe = Recipe("Каша", [ing])

    scaled_recipe = recipe.scale(2.5)

    assert recipe.ingredients[0].quantity == 200.0
    assert scaled_recipe is not recipe
    assert scaled_recipe.ingredients[0].quantity == 500.0


def test_recipe_scale_invalid_ratio():
    "проверка на выброс исключения при увелеяения порций в рецепте на отрицательное число"
    recipe = Recipe("Чай")
    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-1.5)


def test_recipe_len():
    "проверка кол-ва уникальных ингридиентов"
    recipe = Recipe("Салат")
    assert len(recipe) == 0

    recipe.add_ingredient(Ingredient("Помидор", 2.0, "шт"))
    recipe.add_ingredient(Ingredient("Огурец", 2.0, "шт"))
    recipe.add_ingredient(Ingredient("Помидор", 1.0, "шт"))  
    recipe.add_ingredient(Ingredient("Сметана", 1.0, "ст.л."))

    assert len(recipe) == 3