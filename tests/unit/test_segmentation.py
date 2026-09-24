import pandas as pd


def calculate_rfm_scores(df):
    df = df.copy()

    df["r_score"] = pd.qcut(
        df["recency"],
        5,
        labels=[5, 4, 3, 2, 1],
        duplicates="drop",
    ).astype(int)

    df["f_score"] = pd.qcut(
        df["frequency"],
        5,
        labels=[1, 2, 3, 4, 5],
        duplicates="drop",
    ).astype(int)

    df["m_score"] = pd.qcut(
        df["monetary"],
        5,
        labels=[1, 2, 3, 4, 5],
        duplicates="drop",
    ).astype(int)

    return df


def assign_segment(r_score, f_score, m_score):
    if r_score >= 4 and f_score >= 4 and m_score >= 4:
        return "Champions"

    if r_score >= 3 and f_score >= 4:
        return "Loyal Customers"

    if r_score >= 4 and f_score <= 3:
        return "Potential Loyalists"

    if r_score <= 2 and f_score >= 3:
        return "At Risk"

    return "Lost Customers"


def test_rfm_scores_are_between_one_and_five():
    df = pd.DataFrame(
        {
            "recency": [5, 10, 20, 30, 40],
            "frequency": [1, 2, 3, 4, 5],
            "monetary": [100, 200, 300, 400, 500],
        }
    )

    result = calculate_rfm_scores(df)

    assert result["r_score"].between(1, 5).all()
    assert result["f_score"].between(1, 5).all()
    assert result["m_score"].between(1, 5).all()


def test_champions_segment():
    assert assign_segment(5, 5, 5) == "Champions"


def test_loyal_customers_segment():
    assert assign_segment(3, 5, 3) == "Loyal Customers"


def test_potential_loyalists_segment():
    assert assign_segment(5, 2, 3) == "Potential Loyalists"


def test_at_risk_segment():
    assert assign_segment(2, 4, 3) == "At Risk"


def test_lost_customers_segment():
    assert assign_segment(1, 1, 1) == "Lost Customers"