import dataclasses
from datetime import datetime


@dataclasses.dataclass
class CreateLoanCommand:
    loan_id: str
    capital: float
    rate: float
    term: float
    max_periods: int
    image_path: str = None
    amortization_amount: float = None
    amortization_periodicity: int = None

    def __init__(self, owner_id: str, loan_id: str, capital_as_str: str, rate_as_str: str, term: float,
                 max_periods: str, partial_amortizations: str = None):
        self.owner_id = owner_id
        self.loan_id = loan_id
        self.capital = float(capital_as_str.replace(',', '.'))
        self.rate = float(rate_as_str.replace(',', '.'))
        self.term = term
        self.max_periods = int(max_periods) if max_periods else 12

        def parse_partial_amortizations(partial_amortizations_str: str):
            values = partial_amortizations_str.split(" - ")

            return float(values[0].replace(',', '.')), int(values[1])

        if partial_amortizations:
            self.amortization_amount, self.amortization_periodicity = parse_partial_amortizations(partial_amortizations)


@dataclasses.dataclass
class LoanSummary:
    amount: float
    tae: float
    term: int
    pmt: float
    end_date: datetime
    total_payment: float
    total_interests: float


@dataclasses.dataclass
class LoanDTO:
    loan_summary: LoanSummary
    table_image_path: str

