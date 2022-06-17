import pytest

from core.infrastructure import loan_repository
from tests.core.domain.loan_builder import LoanMother


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    loan_repository.clear()


def test_save_should_not_fail():
    loan = LoanMother().build()
    owner_id = '1'

    loan_repository.save(owner_id, loan)


def test_get_all_saved_loans():
    owner_id = '1'

    loan_1 = LoanMother().with_field(field_name="loan_id", value="1").build()
    loan_2 = LoanMother().with_field(field_name="loan_id", value="2").build()

    loan_repository.save(owner_id=owner_id, loan=loan_1)
    loan_repository.save(owner_id=owner_id, loan=loan_2)

    assert loan_repository.get_all(owner_id) == [loan_1, loan_2]


def test_get_by_owner_and_id():
    owner_id = "1"

    loan_1 = LoanMother().with_field(field_name="loan_id", value="ANOTHER_ID").build()
    loan_2 = LoanMother().with_field(field_name="loan_id", value="2").build()

    loan_repository.save(owner_id=owner_id, loan=loan_1)
    loan_repository.save(owner_id=owner_id, loan=loan_2)

    assert loan_repository.get(owner_id=owner_id, loan_id="2") == loan_2


def test_delete_loan():
    owner_id = '1'

    loan_1 = LoanMother().with_field(field_name="loan_id", value="1").build()
    loan_2 = LoanMother().with_field(field_name="loan_id", value="2").build()

    loan_repository.save(owner_id=owner_id, loan=loan_1)
    loan_repository.save(owner_id=owner_id, loan=loan_2)

    assert loan_repository.get_all(owner_id) == [loan_1, loan_2]

    loan_repository.delete(owner_id, loan_1.loan_id)

    assert loan_repository.get_all(owner_id) == [loan_2]

    loan_repository.delete(owner_id, loan_2.loan_id)

    assert loan_repository.get_all(owner_id) == []
