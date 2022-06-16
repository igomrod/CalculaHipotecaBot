from core.application.services import MortgageTableRequest
import numpy_financial as npf
import math


class MortgageTable:
    def __init__(self, request: MortgageTableRequest):
        def format_amount(amount):
            return format(amount, '0,.2f').replace(',', ' ')

        capital = request.capital
        rate = request.rate
        term = request.term
        self._max_periods = request.max_periods

        balance = capital

        fee = npf.pmt(rate / (12 * 100), term, -capital, 0)
        self.monthly_fees = []

        self.total = 0
        self.total_interests = 0

        for i in range(1, term + 1):
            pago_capital = npf.ppmt(rate / (12 * 100), i, term, -capital, 0)
            pago_int = fee - pago_capital
            balance -= pago_capital
            month_fee_line = [f'{math.ceil(i / 12)} / {i}',
                              format_amount(fee),
                              format_amount(pago_capital),
                              format_amount(pago_int),
                              format_amount(balance)]

            self.total += fee
            self.total_interests += pago_int

            self.monthly_fees.append(month_fee_line)

class MortgageTable:
    def __init__(self, request: MortgageTableRequest):
        def format_amount(amount):
            return format(amount, '0,.2f').replace(',', ' ')

        capital = request.capital
        rate = request.rate
        term = request.term
        self._max_periods = request.max_periods

        balance = capital

        fee = npf.pmt(rate / (12 * 100), term, -capital, 0)
        self.monthly_fees = []

        self.total = 0
        self.total_interests = 0

        for i in range(1, term + 1):
            pago_capital = npf.ppmt(rate / (12 * 100), i, term, -capital, 0)
            pago_int = fee - pago_capital
            balance -= pago_capital
            month_fee_line = [f'{math.ceil(i / 12)} / {i}',
                              format_amount(fee),
                              format_amount(pago_capital),
                              format_amount(pago_int),
                              format_amount(balance)]

            self.total += fee
            self.total_interests += pago_int

            self.monthly_fees.append(month_fee_line)