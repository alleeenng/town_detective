from game_data import (
    describe, is_valid_room, clue_in_room, has_enough_clues, long_clues, 
    suspect_labels
)
def test_describe():
    assert "Улица" in describe("street")
    assert describe("moon") == "Нет такой локации."

def test_is_valid_room():
    assert is_valid_room("cafe") is True
    assert is_valid_room("moon") is False

def test_clue_in_room():
    assert clue_in_room("street") == "грязные следы"
    assert clue_in_room("flat") is None

def test_has_enough_clues():
    assert has_enough_clues(["a", "b", "c"]) is True
    assert has_enough_clues(["a", "b"]) is False

def test_long_clues():
    # Проверяем генератор с условием (длина > 6)
    # "следы" (5 букв) не пройдет, "перчатка" (8 букв) пройдет
    assert long_clues(["следы", "перчатка"]) == ["перчатка"]

def test_suspect_labels():
    # Проверяем базовый генератор
    assert suspect_labels(["ivanov"]) == ["Подозреваемый: ivanov"]