import math

import dataframe_image as dfi
import numpy_financial as npf
import pandas as pd


def format_amount(amount):
    return format(amount, '0,.2f').replace(',', ' ')


def calculate_mortgage_fee(capital, rate, term, max_periods=None, image_path='/tmp/dataframe.png'):
    balance = capital

    fee = npf.pmt(rate/(12*100), term, -capital, 0)
    monthly_fees = []

    if not max_periods:
        max_periods = term

    total = 0
    total_interests = 0

    for i in range(1, term + 1):
        pago_capital = npf.ppmt(rate/(12*100), i, term, -capital, 0)
        pago_int = fee - pago_capital
        balance -= pago_capital
        month_fee_line = [f'{math.ceil(i/12)} / {i}',
                          format_amount(fee),
                          format_amount(pago_capital),
                          format_amount(pago_int),
                          format_amount(balance)]

        total += fee
        total_interests += pago_int

        monthly_fees.append(month_fee_line)

    df = pd.DataFrame(monthly_fees, columns=['Año/Mes', 'Cuota', 'Capital', 'Intereses', 'saldo']).round(2)

    df_to_show = df.head(max_periods).style.hide_index()

    print(df)

    dfi.export(df_to_show, image_path)

    return total, total_interests



