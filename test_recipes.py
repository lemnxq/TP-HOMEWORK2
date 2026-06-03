import pytest
from recipes import Ingredient, Recipe


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