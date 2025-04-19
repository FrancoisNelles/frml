import calendar
from datetime import date
from frml.input_helpers.tools import Dates

def calculate_year_fraction(
    start_date: date,
    end_date: date,
    day_count: Dates.day_count_conventions
) -> float:
    """
    This function calculates the year fraction between two dates given a day count convention.

    Parameters:
        - start_date (date): Start date
        - end_date (date): End date
        - day_count (Dates.day_count_conventions): Day count convention. The following are applicable day count conventions:
            Actual/Actual
            Actual/365
            Actual/360
            30/360E
            30/360A

    Returns:
        - year_fraction (float): The year fraction for the given dates.

    Notes:
        - The calculations follow ISDA conventions.
        - The 30/360 conventions rely on the following rulesets:
            - 30/360E: European method, where the last day of February is always considered to be the 30th.
            - 30/360A: American method, where the last day of February is considered to be the 30th only if the start date is on or after the 30th.

    """
    if day_count not in Dates.day_count_list:
        raise ValueError(f"DayCountConventions {day_count} does not exist!")

    if start_date > end_date:
        sign = -1
        start_date, end_date = end_date, start_date
    else:
        sign = 1

    if day_count == "Actual/Actual":
        
        day_counts = []
        date_1 = start_date

        for i in range(start_date.year, end_date.year + 1):
            date_2 = date(i+1, 1, 1)
            
            if end_date < date_2:
                date_2 = end_date
            
            days = (date_2 - date_1).days
            
            if calendar.isleap(date_1.year):
                day_counts.append(days / 366)
            else:
                day_counts.append(days / 365)
            
            date_1 = date_2
        year_fraction =  sign * sum(day_counts)

    if day_count == "Actual/365":
        year_fraction =  sign * (end_date - start_date).days / 365.0

    if day_count == "Actual/360":
        year_fraction =  sign * (end_date - start_date).days / 360.0

    if day_count == "30/360E":
        y1, m1, d1 = start_date.year, start_date.month, start_date.day
        y2, m2, d2 = end_date.year, end_date.month, end_date.day

        if d1 == 31:
            d1 = 30
        if d2 == 31:
            d2 = 30

        year_fraction = sign * (360*(y2 - y1) + 30*(m2 - m1) + (d2 - d1))/360

    if day_count == "30/360A":
        y1, m1, d1 = start_date.year, start_date.month, start_date.day
        y2, m2, d2 = end_date.year, end_date.month, end_date.day

        if d1 == 31 or (m1 == 2 and d1 == 29):
            d1 = 30
        if d2 == 31 and d1 > 29:
            d2 = 30

        year_fraction = sign * (360*(y2 - y1) + 30*(m2 - m1) + (d2 - d1))/360

    return year_fraction