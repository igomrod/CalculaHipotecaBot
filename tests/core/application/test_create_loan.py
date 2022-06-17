from unittest.mock import MagicMock, Mock

from core.application.dtos import CreateLoanCommand
from core.application.services import create_loan


def test_create_loan_from_request():
    request = CreateLoanCommand(owner_id="OWNER_ID",
                                loan_id="ID",
                                capital_as_str="120196.34",
                                rate_as_str="0.5150",
                                term=int(283 / 12),
                                max_periods="48")

    repository = MagicMock()
    repository.save = Mock()

    save_as_image_service_mock = Mock()

    create_loan(request, repository=repository, save_as_image_service=save_as_image_service_mock)

    repository.save.assert_called()
    save_as_image_service_mock.assert_called()
