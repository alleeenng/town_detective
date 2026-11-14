import game_data as gd
def test_describe():
    assert "Улица" in gd.describe("street")
    assert gd.describe("moon") == "Нет такой локации."

def test_is_valid_room():
    assert gd.is_valid_room("cafe") is True
    assert gd.is_valid_room("moon") is False

def test_clue_in_room():
    assert gd.clue_in_room("street") == "грязные следы"
    assert gd.clue_in_room("flat") is None

def test_has_enough_clues():
    assert gd.has_enough_clues(["a", "b", "c"]) is True
    assert gd.has_enough_clues(["a", "b"]) is False

def test_long_clues():
    # Проверяем генератор с условием (длина > 6)
    # "следы" (5 букв) не пройдет, "перчатка" (8 букв) пройдет
    assert gd.long_clues(["следы", "перчатка"]) == ["перчатка"]

def test_suspect_labels():
    # Проверяем базовый генератор
    assert gd.suspect_labels(["ivanov"]) == ["Подозреваемый: ivanov"]