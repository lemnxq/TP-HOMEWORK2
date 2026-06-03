import pytest
from recipes import Ingredient, Recipe, ShoppingList


def test_ingredient_init():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Сахар", 100, "г")
    ing2 = Ingredient("Сахар", 300, "г")
    assert ing1 == ing2

    ing3 = Ingredient("Креветка", 100, "г")
    assert ing1 != ing3

    ing4 = Ingredient("Сахар", 100, "кг")
    assert ing1 != ing4


def test_recipe_init():
    ing = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [ing])
    
    assert recipe.title == "Пицца"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"

def test_recipe_add_ingredient():
    recipe = Recipe("Пицца")
    
    ing1 = Ingredient("Сыр", 100, "г")
    recipe.add_ingredient(ing1)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 100
    
    ing2 = Ingredient("Сыр", 50, "г")
    recipe.add_ingredient(ing2)
    
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 150

def test_recipe_scale():
    ing = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [ing])
    
    scaled_recipe = recipe.scale(2)
    
    assert scaled_recipe is not recipe
    assert recipe.ingredients[0].quantity == 500
    assert scaled_recipe.ingredients[0].quantity == 1000
    
    with pytest.raises(ValueError):
        recipe.scale(0)
        
    with pytest.raises(ValueError):
        recipe.scale(-1)

def test_recipe_len():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Вода", 200, "мл"))
    recipe.add_ingredient(Ingredient("Мука", 100, "г")) 
    
    assert len(recipe) == 2


def test_shopping_list_add_recipe():
    sl = ShoppingList()
    recipe = Recipe("Блины", [Ingredient("Мука", 100, "г")])
    
    sl.add_recipe(recipe, 2)
    assert len(sl._items) == 1
    assert sl._items[0][0].quantity == 200
    assert sl._items[0][1] == "Блины"
    
    with pytest.raises(ValueError):
        sl.add_recipe(recipe, 0)
    with pytest.raises(ValueError):
        sl.add_recipe(recipe, -2)

def test_shopping_list_remove_recipe():
    sl = ShoppingList()
    r1 = Recipe("Блины", [Ingredient("Мука", 100, "г")])
    r2 = Recipe("Омлет", [Ingredient("Яйца", 2, "шт")])
    
    sl.add_recipe(r1, 1)
    sl.add_recipe(r2, 1)
    

    sl.remove_recipe("Блины")
    assert len(sl._items) == 1
    assert sl._items[0][1] == "Омлет"
    
    sl.remove_recipe("что-то")
    assert len(sl._items) == 1

def test_shopping_list_get_list():
    sl = ShoppingList()
    r1 = Recipe("Блины", [Ingredient("Мука", 100, "г"), Ingredient("Яйца", 2, "шт")])
    r2 = Recipe("Хлеб", [Ingredient("Мука", 300, "г"), Ingredient("Вода", 100, "мл")])
    
    sl.add_recipe(r1, 1)
    sl.add_recipe(r2, 1)
    
    final_list = sl.get_list()
    
    assert len(final_list) == 3
    assert final_list[0].name == "Вода"
    
    assert final_list[1].name == "Мука"
    assert final_list[1].quantity == 400
    
    assert final_list[2].name == "Яйца"

def test_shopping_list_add_magic():
    sl1 = ShoppingList()
    sl1.add_recipe(Recipe("Чай", [Ingredient("Вода", 200, "мл")]), 1)
    
    sl2 = ShoppingList()
    sl2.add_recipe(Recipe("Кофе", [Ingredient("Молоко", 50, "мл")]), 1)
    
    sl3 = sl1 + sl2
    
    assert len(sl3._items) == 2
    assert len(sl1._items) == 1
    assert len(sl2._items) == 1