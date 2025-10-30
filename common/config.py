from datetime import datetime, timedelta, timezone

# Fuso horário GMT-3 (Horário de Brasília)
GMT_MINUS_3 = timezone(timedelta(hours=-3))

DATE_FORMAT = "%d/%m/%Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

def agora_datetime():
    return datetime.now(GMT_MINUS_3)

def agora_formatado() -> str:
    return agora_datetime().strftime(DATETIME_FORMAT)
