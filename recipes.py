class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.unit = unit
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        if float(value) <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)
    
    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit
    

class Recipe:
    def __init__(self, title, ingredients = None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []

    def add_ingredient(self, ingredient):
        for exist_ing in self.ingredients:
            if exist_ing == ingredient:
                exist_ing.quantity += ingredient.quantity
                return
        self.ingredients.append(
            Ingredient(ingredient.name, ingredient.quantity, ingredient.unit)
        )

    @staticmethod
    def is_valid_ratio(ratio):
        if isinstance(ratio, (int, float)) and not isinstance(ratio, bool):
            return ratio > 0
        return False

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент для увелечения порций должен быть больше нуля")
        
        scaled_ing = [
            Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            for ing in self.ingredients
        ]
        return Recipe(self.title, scaled_ing)
    
    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        lines = [self.title]
        for ing in self.ingredients:
            lines.append(f"  - {ing}")
        return "\n".join(lines)
    

class ShoppingList:
    def __init__(self):
        # внутренний список для хранения кортежей (ingredient, recipe_title)
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
    
        scaled_recipe = recipe.scale(portions)
        for ing in scaled_recipe.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title: str):
    # временный пустой список для оставшихся рецептов
        clean_items = []
        for ingredient, recipe_title in self._items:
            if recipe_title != title:
                clean_items.append((ingredient, recipe_title))
        self._items = clean_items

    def get_list(self):
        # ключ (name, unit) => количество
        totals = {}
        for ing, _ in self._items:
            key = (ing.name, ing.unit)
            if key in totals:
                totals[key] += ing.quantity
            else:
                totals[key] = ing.quantity
        
        # преобразую словарь обратно в список объектов Ingredient
        result_list = [
            Ingredient(name, quantity, unit) 
            for (name, unit), quantity in totals.items()
        ]
        def get_name(item):
            return item.name  
        result_list.sort(key=get_name)
        return result_list
    
    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            return NotImplemented
        
        combo_list = ShoppingList()
        
        for ing, title in self._items:
            combo_list._items.append((Ingredient(ing.name, ing.quantity, ing.unit), title))
            
        for ing, title in other._items:
            combo_list._items.append((Ingredient(ing.name, ing.quantity, ing.unit), title))
            
        return combo_list
    
class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients = None):
        # конструктор родительского класса Recipe
        super().__init__(title, ingredients)
        self.diet_type = diet_type
    
    def scale(self, ratio):
        scaled_parent = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled_parent.ingredients)
    
    def __str__(self):
        # префикс диетической категории к строке родителя
        return f"[{self.diet_type}] {super().__str__()}"