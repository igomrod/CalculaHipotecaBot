from core.application.services import CreateLoanRequest


def validate_user_data(user_data):
    return {"Capital", "TAE", "Años"}.issubset(user_data) or {"Capital", "TAE", "Meses"}.issubset(user_data)


def parse_user_data(user_data, chat_id):
    if 'Años' in user_data:
        term = int(user_data['Años'])
    else:
        term = int(int(user_data['Meses']) / 12)

    return CreateLoanRequest(capital_as_str=user_data["Capital"],
                             rate_as_str=user_data["TAE"],
                             term=term,
                             max_periods=user_data.get("Cuantos meses mostrar? (por defecto 12)", None),
                             partial_amortizations=user_data.get("Amortizaciones Parciales", None),
                             image_path=f'/tmp/{chat_id}.png')