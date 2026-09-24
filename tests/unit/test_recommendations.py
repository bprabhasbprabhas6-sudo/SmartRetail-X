import pandas as pd


def calculate_similarity(
    co_purchase_count,
    product_x_purchases,
    product_y_purchases,
):
    denominator = (
        product_x_purchases
        + product_y_purchases
        - co_purchase_count
    )

    if denominator == 0:
        return 0.0

    return co_purchase_count / denominator


def test_similarity_calculation():
    similarity = calculate_similarity(
        co_purchase_count=43,
        product_x_purchases=100,
        product_y_purchases=80,
    )

    assert similarity > 0
    assert similarity <= 1


def test_similarity_is_zero_when_no_co_purchase():
    similarity = calculate_similarity(
        co_purchase_count=0,
        product_x_purchases=100,
        product_y_purchases=80,
    )

    assert similarity == 0.0


def test_similarity_is_one_for_identical_purchase_sets():
    similarity = calculate_similarity(
        co_purchase_count=100,
        product_x_purchases=100,
        product_y_purchases=100,
    )

    assert similarity == 1.0


def test_recommendations_are_sorted_by_rank():
    recommendations = pd.DataFrame(
        {
            "recommendation_rank": [3, 1, 2],
            "similarity": [0.10, 0.30, 0.20],
        }
    )

    result = recommendations.sort_values(
        "recommendation_rank"
    )

    assert result["recommendation_rank"].tolist() == [1, 2, 3]


def test_recommendation_limit():
    recommendations = pd.DataFrame(
        {
            "product_id": ["A", "B", "C", "D", "E"],
            "similarity": [0.5, 0.4, 0.3, 0.2, 0.1],
        }
    )

    result = recommendations.head(3)

    assert len(result) == 3