from typing import List

import pytest

from apps.telegram_bot.user_data import parse_user_data
from core.application.dtos import CreateLoanCommand
from tests.core.domain.loan_builder import LoanMother

valid_user_data = {
    "Años": "10",
    "Meses": "100",
    "Capital": "100000",
    "TAE": "1.2",
    "Cuantos meses mostrar? (por defecto 12)": "24",
    "Amortizaciones Parciales": "10000 - 12"
}


def remove_fields(original_dict, fieldnames: List[str]) -> dict:
    return {k: v for k, v in original_dict.items() if k not in fieldnames}


def test_should_return_filled_request():
    request: CreateLoanCommand = parse_user_data(valid_user_data, chat_id="1111")

    assert request.capital == 100000
    assert request.term == 10
    assert request.rate == 1.2
    assert request.max_periods == 24
    assert request.amortization_periodicity == 12
    assert request.amortization_amount == 10000


def test_should_return_filled_request_when_only_mandatory_fields_present():
    user_data = remove_fields(valid_user_data, ["Cuantos meses mostrar? (por defecto 12)",
                                                "Amortizaciones Parciales"])

    request: CreateLoanCommand = parse_user_data(user_data, chat_id="1111")

    assert request.capital == 100000
    assert request.term == 10
    assert request.rate == 1.2
    assert request.max_periods == 12
    assert request.amortization_periodicity is None
    assert request.amortization_amount is None


@pytest.mark.parametrize(
    "user_data",
    [
        dict(valid_user_data, **{"Años": "NOTANUMBER"}),
        dict(remove_fields(valid_user_data, ["Años"]), **{"Meses": "NOTANUMBER"}),
        dict(valid_user_data, **{"Capital": "NOTANUMBER"}),
        dict(valid_user_data, **{"TAE": "NOTANUMBER"}),
        dict(valid_user_data, **{"Cuantos meses mostrar? (por defecto 12)": "NOTANUMBER"}),
        dict(valid_user_data, **{"Amortizaciones Parciales": "10000 X 12"})
    ]
)
def test_should_raise_error_is_value_is_not_valid(user_data):
    with pytest.raises(ValueError) as e:
        parse_user_data(user_data, "111")
