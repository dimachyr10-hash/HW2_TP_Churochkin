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

# ShoppingList
def test_shopping_list_add_recipe():
    "проверка добавления рецепта в список покупок и обработак порций(<=0)"
    recipe = Recipe("Суп", [Ingredient("Картофель", 2.0, "шт")])
    shopping_list = ShoppingList()

    shopping_list.add_recipe(recipe, 3)
    assert len(shopping_list._items) == 1

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, -1)


def test_shopping_list_remove_recipe():
    "проверка удаления ингредиентов из конкретного рецепта"
    r1 = Recipe("Окрошка", [Ingredient("Картошка", 4.0, "шт")])
    r2 = Recipe("Чай", [Ingredient("Сахар", 1.0, "ч.л.")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(r1, 1)
    shopping_list.add_recipe(r2, 1)

    shopping_list.remove_recipe("Окрошка")
    items = shopping_list.get_list()
    assert len(items) == 1
    assert items[0].name == "Сахар"

    shopping_list.remove_recipe("---")
    assert len(shopping_list.get_list()) == 1


def test_shopping_list_get_list_sum_and_sorting():
    "проверка суммирования одинаковых продуктов и сортировки их по алфавиту"
    r1 = Recipe("Борщ", [Ingredient("Свекла", 2.0, "шт"), Ingredient("Вода", 2.0, "л"), Ingredient("Картошка", 2.0, "шт")])
    r2 = Recipe("Салат", [Ingredient("Свекла", 1.0, "шт"), Ingredient("Орешки", 100.0, "гр")])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(r1, 1)
    shopping_list.add_recipe(r2, 1)

    final_list = shopping_list.get_list()

    assert len(final_list) == 4
    assert final_list[0].name == "Вода"
    assert final_list[3].name == "Свекла"
    assert final_list[3].quantity == 3.0


def test_shopping_list_addition():
    "проверка метода __add__ сложения списков продуктов"
    r1 = Recipe("Борщ", [Ingredient("Мясо", 5.0, "кг")])
    r2 = Recipe("Паста", [Ingredient("Макароны", 500.0, "гр")])

    list1 = ShoppingList()
    list1.add_recipe(r1, 1)

    list2 = ShoppingList()
    list2.add_recipe(r2, 1)

    combined = list1 + list2

    assert len(list1.get_list()) == 1
    assert len(list2.get_list()) == 1
    assert len(combined.get_list()) == 2