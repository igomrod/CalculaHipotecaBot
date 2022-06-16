from unittest.mock import MagicMock, Mock

from core.application.dtos import CreateLoanRequest
from core.application.services import create_loan


def test_create_loan_from_request():
    request = CreateLoanRequest(capital_as_str="120196.34", rate_as_str="0.5150", term=int(283 / 12), max_periods=48,
                                image_path="path")

    repository = MagicMock()
    repository.save = Mock()

    create_loan(request, repository)

    repository.save.assert_called()
