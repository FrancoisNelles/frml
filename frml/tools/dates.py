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
        - Year fraction convention 30/360E follows the European convention. This
            convention applies bigger weights to the 1st day of a month depending on how many
            days were in the previous month. The 31st counts as a 0 day weight. The American
            convention allocates weights to the days slightly differently.
        - Year fraction convention 30/360A follows the European convention. This
            convention applies bigger weights to the 1st day of a month depending on how many
            days were in the previous month. The 31st counts as a 0 day weight. The American
            convention allocates weights to the days slightly differently.
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
            date_2 = date(i + 1, 1, 1)
            if end_date < date_2:
                date_2 = end_date
            days = (date_2 - date_1).days
            if calendar.isleap(date_1.year):
                day_counts.append(days / 366)
            else:
                day_counts.append(days / 365)
            date_1 = date_2
        return sign * sum(day_counts)

    if day_count == "Actual/365":
        return sign * (end_date - start_date).days / 365.0

    if day_count == "Actual/360":
        return sign * (end_date - start_date).days / 360.0

    if day_count == "30/360E":
        # Matches European convention
        years = end_date.year - start_date.year
        months = end_date.month - start_date.month
        calculated_months = (12 * years + months) * 30
        days = min(30, end_date.day) - min(30, start_date.day)
        return sign * (calculated_months + days) / 360