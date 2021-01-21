import pytest

from main import *

# How to execute: 
# $ python -m pytest
# $ python -m pytest -v --disable-pytest-warnings

@pytest.fixture
def FXTrade_prep(): # FXTrade prepare
    hist = HistData()
    mean = np.mean(hist.list())
    hist_list = hist.list() - mean 
    hist_list = hist_list[200:1200]
    hist_list = hist_list.tolist()
    fxt = FXTrade(hist_list)
    return fxt


def test_FXTrade_is_valid_action_01(FXTrade_prep):
    FXTrade_prep._trading._position = Position.SQUARE.value
    assert FXTrade_prep.is_valid_action(Action.WAIT.value)      == True
    assert FXTrade_prep.is_valid_action(Action.SHORT.value)     == True
    assert FXTrade_prep.is_valid_action(Action.LONG.value)      == True
    assert FXTrade_prep.is_valid_action(Action.LIQUIDATE.value) == False
    FXTrade_prep._trading._position = Position.SHORT.value
    assert FXTrade_prep.is_valid_action(Action.WAIT.value)      == True
    assert FXTrade_prep.is_valid_action(Action.SHORT.value)     == False
    assert FXTrade_prep.is_valid_action(Action.LONG.value)      == False
    assert FXTrade_prep.is_valid_action(Action.LIQUIDATE.value) == True
    FXTrade_prep._trading._position = Position.LONG.value
    assert FXTrade_prep.is_valid_action(Action.WAIT.value)      == True
    assert FXTrade_prep.is_valid_action(Action.SHORT.value)     == False
    assert FXTrade_prep.is_valid_action(Action.LONG.value)      == False
    assert FXTrade_prep.is_valid_action(Action.LIQUIDATE.value) == True


@pytest.fixture
def Trading_prep(): # Trading prepare
    trd = Trading()
    return trd


def test_Trading_reset_01(Trading_prep):
    Trading_prep.change(Action.LONG.value, 1.0)
    assert Trading_prep._pos_rate == 1.0
    Trading_prep.reset()
    assert Trading_prep.is_square() == True
    Trading_prep.change(Action.SHORT.value, 0.1)
    assert Trading_prep._pos_rate == 0.1


def test_Trading_is_square_01(Trading_prep):
    assert Trading_prep.is_square() == True  # When intilizing
    Trading_prep._position = Position.SQUARE.value
    assert Trading_prep.is_square() == True
    Trading_prep._position = Position.SHORT.value
    assert Trading_prep.is_square() == False
    Trading_prep._position = Position.LONG.value
    assert Trading_prep.is_square() == False
    Trading_prep._position = Position.SQUARE.value
    assert Trading_prep.is_square() == True


def test_Trading_change_01(Trading_prep):
    # When intilizing
    with pytest.raises(TypeError):
        Trading_prep.change(Action.LONG.value, None)
    with pytest.raises(TypeError):
        Trading_prep.change(Action.SHORT.value, "str_input") 
    with pytest.raises(ValueError):
        Trading_prep.change(Action.WAIT.value, 0.98)
    with pytest.raises(ValueError):
        Trading_prep.change(Action.LIQUIDATE.value, 0.98)


def test_Trading_change_02(Trading_prep):
    # When intilizing
    Trading_prep.change(Action.SHORT.value, 0.98)
    assert Trading_prep._pos_rate == 0.98


def test_Trading_change_03(Trading_prep):
    # When intilizing
    Trading_prep.change(Action.LONG.value, -0.13)
    assert Trading_prep._pos_rate == -0.13


def test_Trading_change_04(Trading_prep):
    Trading_prep.change(Action.LONG.value, 0)
    assert Trading_prep._pos_rate == 0
    with pytest.raises(ValueError):
        Trading_prep.change(Action.LONG.value, 0.98)


def test_Trading_liquidate_01(Trading_prep):
    Trading_prep._position = Position.SQUARE.value
    with pytest.raises(ValueError):
        Trading_prep.liquidate(0.98)

def test_Trading_liquidate_02(Trading_prep):
    Trading_prep.change(Action.LONG.value, 0.98)
    pl = Trading_prep.liquidate(0.99)
    assert pl == 100.00000000000009 

def test_Trading_liquidate_03(Trading_prep):
    Trading_prep.change(Action.SHORT.value, 0.98)
    pl = Trading_prep.liquidate(0.99)
    assert pl == -100.00000000000009 

def test_Trading_liquidate_04(Trading_prep):
    Trading_prep.change(Action.LONG.value, 0.99)
    pl = Trading_prep.liquidate(0.98)
    assert pl == -100.00000000000009 

def test_Trading_liquidate_05(Trading_prep):
    Trading_prep.change(Action.SHORT.value, 0.99)
    pl = Trading_prep.liquidate(0.98)
    assert pl == 100.00000000000009 

def test_Trading_liquidate_07(Trading_prep):
    Trading_prep.change(Action.LONG.value, -0.10)
    pl = Trading_prep.liquidate(0.10)
    assert pl == 2000.0

def test_Trading_liquidate_08(Trading_prep):
    Trading_prep.change(Action.SHORT.value, -0.10)
    pl = Trading_prep.liquidate(0.10)
    assert pl == -2000.0

def test_Trading_liquidate_09(Trading_prep):
    Trading_prep.change(Action.LONG.value, 0.10)
    pl = Trading_prep.liquidate(-0.10)
    assert pl == -2000.0

def test_Trading_liquidate_10(Trading_prep):
    Trading_prep.change(Action.SHORT.value, 0.10)
    pl = Trading_prep.liquidate(-0.10)
    assert pl == 2000.0


