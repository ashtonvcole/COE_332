#!/usr/bin/env python3



from analyze_water import turbidity_of, turbidity_min_time
import pytest



def test_turbidity_of():
    # a0 * abs(I90)
    assert turbidity_of(0, 0) == 0
    assert turbidity_of(0, 1) == 0
    assert turbidity_of(1, 0) == 0
    assert turbidity_of(1, 1) == 1
    assert turbidity_of(1, -1) == 1
    assert turbidity_of(-1, 1) == -1
    assert abs(turbidity_of(0.1, -0.9) - 0.09) <= 0.000001
    assert abs(turbidity_of(-1.5, 1.2) == -1.8) <= 0.000001



def test_turbidity_min_time():
    # ln(Ts / T0) / ln(1 - d)
    assert turbidity_min_time(5.2, 5.2, 0) == 0
    assert turbidity_min_time(3.9182, 2.1, 354) == 0
    assert abs(turbidity_min_time(9.8, 10, 0.02) - 1) <= 0.000001
    assert abs(turbidity_min_time(2, 32, 0.5) - 4) <= 0.000001
