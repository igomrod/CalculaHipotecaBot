from core.application.services import calculate_mortgage_fee


def test_should_calculate_mortgage_fee():
    mortgage_fee = calculate_mortgage_fee(capital=120196.34, rate=0.5150, term=286, max_periods=48)

    print(mortgage_fee)

    #assert mortgage_fee == 100



