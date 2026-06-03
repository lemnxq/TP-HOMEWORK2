import pytest
from recipes import Ingredient


def test_ingredient_init():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Пицца", 100, "г")
    ing2 = Ingredient("Пицца", 300, "г")
    assert ing1 == ing2

    ing3 = Ingredient("Креветка", 100, "г")
    assert ing1 != ing3

    ing4 = Ingredient("Пицца", 100, "кг")
    assert ing1 != ing4