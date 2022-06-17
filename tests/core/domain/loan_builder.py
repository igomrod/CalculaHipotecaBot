import dataclasses

from core.domain.loan import Loan


@dataclasses.dataclass
class LoanMother:
    owner_id: str = "1"
    loan_id: str = "1"
    rate: float = 0.5150
    term: int = int(283 / 12)
    loan_amount: float = 120196.34

    def build(self):
        return Loan(owner_id=self.owner_id, loan_id=self.loan_id,
                    rate=self.rate, term=self.term, loan_amount=self.loan_amount)

    def with_field(self, field_name: str, value):
        setattr(self, field_name, value)
        return self
