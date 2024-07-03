
NOT_ALLOWED_SYMBOLS = "() -+"


def phone_serializer(phone: str) -> str:
    for symbol in NOT_ALLOWED_SYMBOLS:
        phone = phone.replace(symbol, "")

    phone = phone.replace("+7", "")

    if phone[0] == "7" or phone[0] == "8":
        phone = phone[1:]

    return phone


def fcs_serializer(fcs: str) -> str:
    return fcs.lower()
