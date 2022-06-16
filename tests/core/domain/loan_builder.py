import dataclasses

from core.domain.loan import Loan


@dataclasses.dataclass
class LoanMother:
    loan_id: str = "1"
    rate: float = 0.5150
    term: int = int(283 / 12)
    loan_amount: float = 120196.34

    def build(self):
        return Loan(loan_id=self.loan_id, rate=self.rate, term=self.term, loan_amount=self.loan_amount)

    def with_field(self, fieldName: str, value):
        self[fieldName] = value
