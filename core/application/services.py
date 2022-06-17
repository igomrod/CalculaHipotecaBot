from typing import Callable

from pandas import DataFrame

from core.application.dtos import CreateLoanCommand, LoanSummary, LoanDTO
from core.domain.loan import Loan


def create_loan(request: CreateLoanCommand, repository, save_as_image_service: Callable[[DataFrame, int, str], None]):
    loan = Loan(owner_id=request.owner_id,
                loan_id=request.loan_id,
                rate=request.rate,
                term=request.term,
                loan_amount=request.capital)

    repository.save(request.owner_id, loan)

    save_as_image_service(mortgage_table=loan.loan_table(),
                          max_periods=request.max_periods,
                          image_path=_loan_table_image_path(loan))


def get_loans(owner_id: str, repository):
    return [
        LoanDTO(loan_summary=loan.summary(),
                table_image_path=_loan_table_image_path(loan))
        for loan in repository.get_all(owner_id)
    ]


def _loan_table_image_path(loan):
    return f'/tmp/{loan.owner_id}_{loan.loan_id}.png'
