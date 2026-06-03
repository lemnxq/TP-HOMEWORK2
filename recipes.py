class Ingredient:
    def __init__(self,name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        try:
            walue = float(value)
        except TypeError:
            raise TypeError('value должно быть float')  # noqa: B904
        
        if walue <= 0:
            raise ValueError('Количество должно быть положительным')
        
        self._quantity = walue

    def __str__(self):
        return f'{self.name}: {self.quantity} {self.unit}'
    
    def __repr__(self):
        f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"  # noqa: B021

    def __eq__(self, other):
        return isinstance(other, Ingredient) and other.name == self.name and other.unit == self.unit


class Recipe:
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        self.ingredients = []
        if ingredients:
            for ing in ingredients:
                self.add_ingredient(ing)

    def add_ingredient(self, ingredient: Ingredient):
        for ing in self.ingredients:
            if ing == ingredient:
                ing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if isinstance(ratio, (int, float)) and not isinstance(ratio, bool):
            return ratio > 0
        return False

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        
        new_ingredients = []
        for ing in self.ingredients:
            new_ing = Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            new_ingredients.append(new_ing)
            
        return Recipe(self.title, new_ingredients)

    def __len__(self) -> int:
        return len(self.ingredients)

    def __str__(self) -> str:
        result = f"Рецепт - {self.title}\nИнгредиенты:\n"
        for ing in self.ingredients:
            result += f"-{ing}\n"
        return result.strip()
    


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        new_items = []
        for item in self._items:
            if item[1] != title:
                new_items.append(item)
        self._items = new_items

    def get_list(self) -> list:
        dictres = {}
        
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            dictres[key] = dictres.get(key, 0) + ingredient.quantity
                
        listres = []
        for (name, unit), quantity in dictres.items():
            listres.append(Ingredient(name, quantity, unit))

        listres.sort(key=lambda x: x.name)

        return listres

    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            raise TypeError("Список можно объединить только со списком")
            
        new_list = ShoppingList()
        new_list._items.extend(self._items)
        new_list._items.extend(other._items)
        
        return new_list
    

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled_recipe.ingredients)

    def __str__(self) -> str:
        parent_str = super().__str__()
        return parent_str.replace(f"Рецепт: {self.title}", f"Рецепт: [{self.diet_type}] {self.title}")