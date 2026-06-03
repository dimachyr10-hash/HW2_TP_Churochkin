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
    
    
