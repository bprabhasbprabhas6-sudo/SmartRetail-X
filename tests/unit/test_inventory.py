import numpy as np


def calculate_safety_stock(demand_std, service_level_z, lead_time_days):
    return service_level_z * demand_std * np.sqrt(lead_time_days)


def calculate_reorder_point(avg_daily_demand, lead_time_days, safety_stock):
    return (avg_daily_demand * lead_time_days) + safety_stock


def test_safety_stock_calculation():
    demand_std = 20.85
    service_level_z = 1.65
    lead_time_days = 7

    safety_stock = calculate_safety_stock(
        demand_std,
        service_level_z,
        lead_time_days,
    )

    assert safety_stock > 0
    assert round(safety_stock, 2) == 91.02


def test_reorder_point_calculation():
    avg_daily_demand = 22.17
    lead_time_days = 7
    safety_stock = 91.02

    reorder_point = calculate_reorder_point(
        avg_daily_demand,
        lead_time_days,
        safety_stock,
    )

    assert reorder_point > 0
    assert round(reorder_point, 2) == 246.21


def test_recommended_order_quantity_is_non_negative():
    target_inventory = 401.38
    current_inventory = 100.0

    recommended_order_quantity = max(
        target_inventory - current_inventory,
        0,
    )

    assert recommended_order_quantity >= 0
    assert round(recommended_order_quantity, 2) == 301.38


def test_inventory_priority():
    def get_priority(recommended_quantity):
        if recommended_quantity >= 1000:
            return "HIGH"
        elif recommended_quantity >= 500:
            return "MEDIUM"
        elif recommended_quantity >= 100:
            return "LOW"
        return "VERY LOW"

    assert get_priority(1500) == "HIGH"
    assert get_priority(700) == "MEDIUM"
    assert get_priority(250) == "LOW"
    assert get_priority(50) == "VERY LOW"