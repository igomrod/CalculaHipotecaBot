from core.application.dtos import LoanSummary
from tabulate import tabulate


def loan_summary_to_table_string(loan: LoanSummary) -> str:
    table = [
        ["Total solicitado:", f"{loan.amount:.2f}"],
        ["Cuota:", f"{loan.pmt:.2f}"],
        ["Fecha fin:", f"{loan.end_date}"],
        ["Total pagado:", f"{loan.total_payment:.2f}"],
        ["Intereses totales:", f"{loan.total_interests:.2f}"],
    ]

    return f"""```
{tabulate(table, tablefmt='plain')}
```"""
