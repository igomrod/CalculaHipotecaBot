from unittest.mock import MagicMock, Mock

from core.application.dtos import LoanDTO
from core.application.services import get_loans
from tests.core.domain.loan_builder import LoanMother


def test_should_return_created_loans_dtos():
    repository_mock = MagicMock()
    created_loan = \
        LoanMother() \
            .with_field("owner_id", "OWNER_VALID_ID") \
            .with_field("loan_id", "LOAN_VALID_ID") \
            .build()
    repository_mock.get_all = Mock(return_value=[created_loan])

    expected_image_path = f'/tmp/OWNER_VALID_ID_LOAN_VALID_ID.png'
    expected_loan_dto = LoanDTO(loan_summary=created_loan.summary(),
                                table_image_path=expected_image_path)

    assert get_loans(owner_id="owner_id", repository=repository_mock) == [expected_loan_dto]
