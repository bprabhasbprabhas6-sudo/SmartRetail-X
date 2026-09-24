import pandas as pd


def test_revenue_calculation():
    df = pd.DataFrame(
        {
            "quantity": [10, 5, 2],
            "unit_price": [2.0, 4.0, 10.0],
        }
    )

    df["revenue"] = df["quantity"] * df["unit_price"]

    assert df["revenue"].tolist() == [20.0, 20.0, 20.0]


def test_negative_quantity_represents_return():
    df = pd.DataFrame(
        {
            "quantity": [10, -5, 3]
        }
    )

    returns = df[df["quantity"] < 0]

    assert len(returns) == 1
    assert returns.iloc[0]["quantity"] == -5


def test_positive_quantity_represents_sale():
    df = pd.DataFrame(
        {
            "quantity": [10, -5, 3]
        }
    )

    sales = df[df["quantity"] > 0]

    assert len(sales) == 2