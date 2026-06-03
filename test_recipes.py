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