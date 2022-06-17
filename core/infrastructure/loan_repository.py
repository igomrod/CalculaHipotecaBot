from core.domain.loan import Loan

_loans = {}


def save(owner_id: str, loan: Loan):
    if owner_id in _loans:
        _loans[owner_id] = dict(_loans[owner_id], **{loan.loan_id: loan})
    else:
        _loans[owner_id] = {loan.loan_id: loan}


def get_all(owner_id: str):
    if owner_id not in _loans:
        return []

    return list(_loans[owner_id].values())


def get(owner_id, loan_id: str):
    if owner_id not in _loans:
        return None

    if loan_id not in _loans[owner_id]:
        return None

    return _loans[owner_id][loan_id]


def delete(owner_id, loan_id: str):
    if owner_id in _loans and loan_id in _loans[owner_id]:
        del _loans[owner_id][loan_id]


def clear():
    _loans.clear()
