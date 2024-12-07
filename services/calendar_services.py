import calendar

def get_days_in_month(ano, mes):
    # Retorna o número de dias no mês
    return calendar.monthrange(ano, mes)[1]
