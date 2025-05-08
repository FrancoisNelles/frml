import calendar
import pandas as pd
from typing import Union
from datetime import date 
from dateutil.relativedelta import relativedelta
from frml.tools.calendars import CalendarMemory
from frml.input_helpers.tools import (Calendars,
                                        Dates)

def get_calendar(calendar: Calendars.calendars) -> pd.offsets.CustomBusinessDay:
    """
    Function returns a calendar object for the calendar specified.

    Parameters:
        - calendar (Calendars.calendars): The calendar for which the calendar is required.

    returns:
        - created_calendar (pd.offsets.CustomBusinessDay): A calendar object for the calendar
            specified.

    Notes:
        - calendar objects only take into account holidays not based on the lunar calendar except for easter.

    See Also:
        - Calendars class to view the countries and which holidays they have.
        - CalendarMemory class to view the calendars that have been created.
    """
    if (calendar not in Calendars.calendar_list):
        raise ValueError(f"Calendar {calendar} not recognized. Use any of {Calendars.calendar_list}.")

    calendar_memory = CalendarMemory()
    created_calendar = calendar_memory.calendar_instance_dictionary.get(calendar)
    if created_calendar is None:
        created_calendar = pd.offsets.CustomBusinessDay(
            calendar=Calendars.calendar_sets[calendar]
        )
        calendar_memory.calendar_instance_dictionary[calendar] = created_calendar
    return created_calendar

def calculate_year_fraction(start_date: date,
                            end_date: date,
                            day_count: Dates.day_count_conventions) -> float:
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
    if day_count not in Dates.day_count_conventions_list:
        valid_conventions = ', '.join(Dates.day_count_conventions_list)
        raise ValueError(f"DayCountConventions {day_count} does not exist. Use any of the following: {valid_conventions}")
    if not isinstance(start_date, date):
        raise TypeError(f"Start date {start_date} of type {type(start_date)} is not of type datetime.date.")
    if not isinstance(end_date, date):
        raise TypeError(f"End date {end_date} of type {type(end_date)} is not of type datetime.date.")

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

def adjust_date_to_tenor(base_date: date,
                            adjust_tenor: str) -> date:
    """
    This function adjusts a single date with a frequency and period being the tenor.

    Parameters:
        - base_date (date): The selected date to be adjusted.
        - adjust_tenor (str): The tenor the date should be adjusted by.

    Returns:
        - adjusted_date (date): Returns the tenor adjusted date.

    Usage:
        - The tenor convention is dictated by any amount of numbers followed by a single letter,
            the letter dictates the period of the tenor, and the number dictates the frequency.

    Notes:
        - The tenor convention is as follows:
            1D denotes 1 day
            1W denotes 1 week
            1M denotes 1 month
            1Y denotes 1 year
    """
    if not isinstance(base_date, date):
        raise TypeError(f"Base date was not of type datetime.date, but rather of {type(base_date)}.")
    if not isinstance(adjust_tenor, str):
        raise TypeError(f"Adjust tenor was not of type string, but rather of {type(base_date)}.")
    if adjust_tenor[-1] not in ["D", "W", "M", "Y"]:
        raise ValueError(
            f"Tenor {adjust_tenor} not recognized. Please provide a valid tenor value."
        )

    frequency = int(adjust_tenor[0:-1])
    tenor = adjust_tenor[-1]

    if tenor == "D":
        delta = relativedelta(days=frequency)
    if tenor == "W":
        delta = relativedelta(weeks=frequency)
    if tenor == "M":
        delta = relativedelta(months=frequency)
    if tenor == "Y":
        delta = relativedelta(years=frequency)

    adjusted_date = base_date + delta
    return adjusted_date

def adjust_date_to_month_end(base_date: date) -> date:
    """
    This function adjusts a single date to the month end.

    Parameters:
        - base_date (date): The selected date to be adjusted.

    Returns:
        - adjusted_date (date): Returns the month end adjusted date.
    """
    if not isinstance(base_date, date):
        raise TypeError(f"Base date was not of type datetime.date, but rather of {type(base_date)}.")
    
    adjusted_date = pd.to_datetime(base_date)
    month_end_offset = pd.offsets.MonthEnd()

    if not adjusted_date.is_month_end:
        adjusted_date = adjusted_date + month_end_offset
    
    adjusted_date = adjusted_date.date()
    return adjusted_date

def adjust_date_to_business_convention(base_date: date,
                                        calendar: Calendars.calendars = "South Africa",
                                        business_day_convention: Dates.business_day_convention = "Modified Following") -> date:
    """
    The function adjust_date_to_business_convention adjusts a single date to the business
    day convention of the calendar selected.

    Parameters:
        - base_date (date): The selected date to be adjusted.
        - calendar (Calendars.calendars): The calendar for which the calendar is required.
        - business_day_convention (Dates.business_day_convention): The business day convention of the date list.
            The inputs are as follows:
            Modified Following
            Following
            Modified Preceding
            Preceding
            Unadjusted

    Returns:
        - adjusted_date (date): Returns the business day convention adjusted date.

    Notes:
        - Modified Following: The dates will be adjusted to the next business day if the
            date falls on a weekend or holiday unless the adjusted date would fall in
            another month, then it would use preceding.
        - Following: The dates will be adjusted to the next business day if the date falls
            on a weekend.
        - Modified Preceding: The dates will be adjusted to the previous business day if
            the date falls on a weekend or holiday unless the adjusted date would fall in
            another month, then it would use following.
        - Preceding: The dates will be adjusted to the previous business day if the date
            falls on a weekend.
        - Unadjusted: The dates will not be adjusted if the date falls on a weekend.

    See also:
        - The 'DateGenerationConventions' class to view the business day conventions.
        - The 'Calendars' class to view the countries and which holidays they have.
    """
    if not isinstance(base_date, date):
        raise TypeError(f"Base date was not of type datetime.date, but rather of {type(base_date)}.")
    if (calendar not in Calendars.calendar_list):
        raise ValueError(f"Calendar {calendar} not recognized. Use any of {Calendars.calendar_list}.")
    if (business_day_convention not in Dates.business_day_convention_list):
        raise ValueError(f"Business day convention {business_day_convention} not recognized. Use any of {Dates.business_day_convention_list}.")

    business_day_offset = get_calendar(calendar)
    adjusted_date = pd.to_datetime(base_date)

    if business_day_convention == "Modified Following":
        adjusted_date = [
            (
                business_day_offset.rollforward(adjusted_date)
                if business_day_offset.rollforward(adjusted_date).month == adjusted_date.month
                else business_day_offset.rollback(adjusted_date)
            )
        ][0]
    if business_day_convention == "Following":
        adjusted_date = [business_day_offset.rollforward(adjusted_date)][0]
    if business_day_convention == "Modified Preceding":
        adjusted_date = [
            (
                business_day_offset.rollback(adjusted_date)
                if business_day_offset.rollback(adjusted_date).month == adjusted_date.month
                else business_day_offset.rollforward(adjusted_date)
            )
        ][0]
    if business_day_convention == "Preceding":
        adjusted_date = [business_day_offset.rollback(adjusted_date)][0]
    
    adjusted_date = pd.to_datetime(adjusted_date).date()
    return adjusted_date

def adjust_date(base_date: date,
                adjust_tenor: str,
                calendar: Calendars.calendars = "South Africa",
                business_day_convention: Dates.business_day_convention = "Modified Following",
                end_of_month: bool = False) -> date:
    """
    Adjust a single date with a frequency and period being the tenor,
    a month end adjustment and a business day convention.

    Parameters:
        - base_date (date): The selected date to be adjusted.
        - adjust_tenor (str): The tenor the date should be adjusted by.
        - calendar (Calendars.calendars): The calendar for which the calendar is required.
        - business_day_convention (Dates.business_day_convention): The business day convention of the date list.
            The inputs are as follows:
            Modified Following
            Following
            Modified Preceding
            Preceding
            Unadjusted
        - end_of_month (boolean): True or False. If True, the dates will be adjusted to the
            last day of the month.

    Returns:
        - adjusted_date (date): Returns the tenor adjusted date.

    Usage:
        - The tenor convention is dictated by any amount of numbers followed by a single letter,
            the letter dictates the period of the tenor, and the number dictates the frequency.

    Notes:
        - The tenor convention is as follows:
            1D denotes 1 day
            1W denotes 1 week
            1M denotes 1 month
            1Y denotes 1 year
        - Modified Following: The dates will be adjusted to the next business day if the
            date falls on a weekend or holiday unless the adjusted date would fall in
            another month, then it would use preceding.
        - Following: The dates will be adjusted to the next business day if the date falls
            on a weekend.
        - Modified Preceding: The dates will be adjusted to the previous business day if
            the date falls on a weekend or holiday unless the adjusted date would fall in
            another month, then it would use following.
        - Preceding: The dates will be adjusted to the previous business day if the date
            falls on a weekend.
        - Unadjusted: The dates will not be adjusted if the date falls on a weekend.

        See also:
        - The 'Dates' class to view the business day conventions.
        - The 'Calendars' class to view the countries and which holidays they have.
        - The 'adjust_date_to_tenor' function for the tenor adjustment.
        - The 'adjust_date_to_month_end' function for the month end adjustment.
        - The 'adjust_date_to_business_convention' function for the business day convention
            adjustment.
    """
    if not isinstance(base_date, date):
        raise TypeError(f"Base date was not of type datetime.date, but rather of {type(base_date)}.")
    if adjust_tenor[-1] not in ["D", "W", "M", "Y"]:
        raise ValueError(f"Tenor {adjust_tenor} not recognized. Please provide a valid tenor value.")
    if (calendar not in Calendars.calendar_list):
        raise ValueError(f"Calendar {calendar} not recognized. Use any of {Calendars.calendar_list}.")
    if (business_day_convention not in Dates.business_day_convention_list):
        raise ValueError(f"Business day convention {business_day_convention} not recognized. Use any of {Dates.business_day_convention_list}.")
    if (end_of_month not in [True, False]):
        raise ValueError(f"End of the month setting {end_of_month} not recognized. It must be set to True or False.")

    adjusted_date = adjust_date_to_tenor(base_date,
                                            adjust_tenor)
    if end_of_month:
        adjusted_date = adjust_date_to_month_end(adjusted_date)
    
    adjusted_date = adjust_date_to_business_convention(adjusted_date,
                                                        calendar,
                                                        business_day_convention)
    return adjusted_date

def generate_dates_list(start_date: date,
                        end_date: date,
                        tenor: str,
                        date_generation_method: Dates.date_generation_method = "Backwards",
                        calendar: Calendars.calendars = "South Africa",
                        business_day_convention: Dates.business_day_convention = "Modified Following",
                        end_of_month: bool = False) -> list[date]:
    """
    This function creates a list of dates with a frequency and period being the tenor, with optional adjustments like a
    a month end adjustment and a business day convention adjustment.

    Parameters:
        - start_date (date): The date at which the list should start.
        - end_date (date): The date at which the list should end.
        - tenor (str): The tenor the dates should be adjusted by.
        - date_generation_method (Dates.date_generation_method): The date generation method of the date list.
            The inputs are as follows:
            Backwards
            Forwards
        - calendar (Calendars.calendars): The calendar for which the calendar is required.
        - business_day_convention (Dates.business_day_convention): The business day convention of the date list.
            The inputs are as follows:
            Modified Following
            Following
            Modified Preceding
            Preceding
            Unadjusted
        - end_of_month (boolean): True or False. If True, the dates will be adjusted to the
            last day of the month.

    Returns:
        - adjusted_date (list[date]): Returns a list of dates.

    Usage:
        - The list of dates generated follow the input ruleset.

    Notes:
        - Start date should be less than End date, for Date Generation logic.
        - The tenor convention is as follows:
            1D denotes 1 day
            1W denotes 1 week
            1M denotes 1 month
            1Y denotes 1 year
        - Forward denotes a short stub at the end of the list if start date and end date are not multiples of the tenor apart.
        - Backward denotes a short stub at the beginning of the list if start date and end date are not multiples of the tenor apart.
        - Modified Following: The dates will be adjusted to the next business day if the
            date falls on a weekend or holiday unless the adjusted date would fall in
            another month, then it would use preceding.
        - Following: The dates will be adjusted to the next business day if the date falls
            on a weekend.
        - Modified Preceding: The dates will be adjusted to the previous business day if
            the date falls on a weekend or holiday unless the adjusted date would fall in
            another month, then it would use following.
        - Preceding: The dates will be adjusted to the previous business day if the date
            falls on a weekend.
        - Unadjusted: The dates will not be adjusted if the date falls on a weekend.

    See also:
        - The 'Calendars' class to view the countries and which holidays they have.
        - The 'Date' class to view the date generation method.
        - The 'Date' class to view the business day conventions.
        - The 'adjust_date' function for the adjustment calculation.
    """
    if not isinstance(start_date, date):
        raise TypeError(f"Start date was not of type datetime.date, but rather of {type(start_date)}.")
    if not isinstance(end_date, date):
        raise TypeError(f"End date was not of type datetime.date, but rather of {type(end_date)}.")
    if start_date > end_date:
        raise ValueError(f"Start date, {start_date}, cannot be after end date, {end_date}.")
    if tenor[-1] not in ["D", "W", "M", "Y"]:
        raise ValueError(f"Tenor {tenor} not recognized. Please provide a valid tenor value.")
    if tenor[0] == '-':
        raise ValueError(f"Tenor {tenor} cannot be negative. Please provide a valid tenor value.")
    if (date_generation_method not in Dates.date_generation_method_list):
        raise ValueError(f"Date generation method, {date_generation_method}, not recognized. Use any of {Dates.date_generation_method}.")
    if (calendar not in Calendars.calendar_list):
        raise ValueError(f"Calendar {calendar} not recognized. Use any of {Calendars.calendar_list}.")
    if (business_day_convention not in Dates.business_day_convention_list):
        raise ValueError(f"Business day convention {business_day_convention} not recognized. Use any of {Dates.business_day_convention_list}.")
    if (end_of_month not in [True, False]):
        raise ValueError(f"End of the month setting {end_of_month} not recognized. It must be set to True or False.")

    dates_list = []

    if date_generation_method == "Backwards":
        start_date, end_date = end_date, start_date
        tenor = '-'+tenor

    list_date = start_date

    if date_generation_method == "Backwards":
        while list_date > end_date:
            dates_list.append(list_date)
            list_date = adjust_date(list_date,
                                    tenor,
                                    calendar,
                                    business_day_convention,
                                    end_of_month)
            
    if date_generation_method == "Forwards":
        while list_date < end_date:
            dates_list.append(list_date)
            list_date = adjust_date(list_date,
                                    tenor,
                                    calendar,
                                    business_day_convention,
                                    end_of_month)

    dates_list.append(end_date)

    if date_generation_method == "Backwards":
        dates_list.reverse()

    dates_list = list(dict.fromkeys(dates_list))

    return dates_list

def generate_dates_list_with_stubs(start_date: date,
                                    end_date: date,
                                    tenor: str,
                                    front_stub_tenor_or_end_date: Union[str, date, None] = None,
                                    end_stub_tenor_or_start_date: Union[str, date, None] = None,
                                    date_generation_method: Dates.date_generation_method = "Backwards",
                                    calendar: Calendars.calendars = "South Africa",
                                    business_day_convention: Dates.business_day_convention = "Modified Following",
                                    end_of_month: bool = False) -> list[date]:
    """
    This function creates a list of dates with a frequency and period being the tenor, with optional adjustments like a
    a month end adjustment and a business day convention adjustment.

    Parameters:
        - start_date (date): The date at which the list should start.
        - end_date (date): The date at which the list should end.
        - tenor (str): The tenor the dates should be adjusted by.
        - front_stub_tenor_or_end_date (str|date|None): A tenor or date which indicates the end of the front stub. If None stub is ignored.
        - end_stub_tenor_or_start_date (str|date|None): A tenor or date which indicates the start of the end stub. If None stub is ignored.
        - date_generation_method (Dates.date_generation_method): The date generation method of the date list.
            The inputs are as follows:
            Backwards
            Forwards
        - calendar (Calendars.calendars): The calendar for which the calendar is required.
        - business_day_convention (Dates.business_day_convention): The business day convention of the date list.
            The inputs are as follows:
            Modified Following
            Following
            Modified Preceding
            Preceding
            Unadjusted
        - end_of_month (boolean): True or False. If True, the dates will be adjusted to the
            last day of the month.
        

    Returns:
        - adjusted_date (list[date]): Returns a list of dates.

    Usage:
        - The list of dates generated follow the input ruleset.

    Notes:
        - Start date should be less than End date, for Date Generation logic.
        - The tenor convention is as follows:
            1D denotes 1 day
            1W denotes 1 week
            1M denotes 1 month
            1Y denotes 1 year
        - Forward denotes a short stub at the end of the list if start date and end date are not multiples of the tenor apart.
        - Backward denotes a short stub at the beginning of the list if start date and end date are not multiples of the tenor apart.
        - front_stub_tenor_or_end_date determines the interval of the first accrual period as the difference between the start date 
            and the front stub end date.  If None, front stub is ignored. If tenor is used, it should be a positive tenor.
        - end_stub_tenor_or_start_date determines the interval of the first accrual period as the difference between the end stub 
            start date and the end date.  If None end stub is ignored. If tenor is used, it should be a positive tenor.
        - Modified Following: The dates will be adjusted to the next business day if the
            date falls on a weekend or holiday unless the adjusted date would fall in
            another month, then it would use preceding.
        - Following: The dates will be adjusted to the next business day if the date falls
            on a weekend.
        - Modified Preceding: The dates will be adjusted to the previous business day if
            the date falls on a weekend or holiday unless the adjusted date would fall in
            another month, then it would use following.
        - Preceding: The dates will be adjusted to the previous business day if the date
            falls on a weekend.
        - Unadjusted: The dates will not be adjusted if the date falls on a weekend.

    See also:
        - The 'Calendars' class to view the countries and which holidays they have.
        - The 'Date' class to view the date generation method.
        - The 'Date' class to view the business day conventions.
        - The 'generate_dates_list' function for date list generation.
    """
    if not isinstance(start_date, date):
        raise TypeError(f"Start date was not of type datetime.date, but of type {type(start_date)}.")
    if not isinstance(end_date, date):
        raise TypeError(f"End date was not of type datetime.date, but of type {type(end_date)}.")
    if start_date > end_date:
        raise ValueError(f"Start date, {start_date}, cannot be after end date, {end_date}.")
    if not isinstance(front_stub_tenor_or_end_date, (str, date, type(None))):
        raise TypeError(f"Front stub input was not the correct type, but of type {type(front_stub_tenor_or_end_date)}.")
    if isinstance(front_stub_tenor_or_end_date, str) and front_stub_tenor_or_end_date[0] == '-':
        raise TypeError(f"Front stub tenor input was negative, use a positive tenor, {front_stub_tenor_or_end_date[1:]}.")
    if isinstance(front_stub_tenor_or_end_date, date) and front_stub_tenor_or_end_date < start_date:
        raise ValueError(f"Start date, {start_date}, cannot be before front stub end date, {front_stub_tenor_or_end_date}.")
    if isinstance(front_stub_tenor_or_end_date, str) and front_stub_tenor_or_end_date[0] == '-':
        raise TypeError(f"End stub tenor input was negative, use a positive tenor, {front_stub_tenor_or_end_date[1:]}.")
    if not isinstance(end_stub_tenor_or_start_date, (str, date, type(None))):
        raise TypeError(f"Front stub input was not the correct type, but of type {type(end_stub_tenor_or_start_date)}.")
    if isinstance(end_stub_tenor_or_start_date, date) and end_stub_tenor_or_start_date > end_date:
        raise ValueError(f"End date, {end_date}, cannot be after end stub start date, {end_stub_tenor_or_start_date}.")
    if tenor[-1] not in ["D", "W", "M", "Y"]:
        raise ValueError(f"Tenor {tenor} not recognized. Please provide a valid tenor value.")
    if tenor[0] == '-':
        raise ValueError(f"Tenor {tenor} cannot be negative. Please provide a valid tenor value.")
    if (date_generation_method not in Dates.date_generation_method_list):
        raise ValueError(f"Date generation method, {date_generation_method}, not recognized. Use any of {Dates.date_generation_method}.")
    if (calendar not in Calendars.calendar_list):
        raise ValueError(f"Calendar {calendar} not recognized. Use any of {Calendars.calendar_list}.")
    if (business_day_convention not in Dates.business_day_convention_list):
        raise ValueError(f"Business day convention {business_day_convention} not recognized. Use any of {Dates.business_day_convention_list}.")
    if (end_of_month not in [True, False]):
        raise ValueError(f"End of the month setting {end_of_month} not recognized. It must be set to True or False.")
    
    front_stub_end_date = False
    end_stub_start_date = False

    if isinstance(front_stub_tenor_or_end_date, str):
        front_stub_end_date = adjust_date(start_date,
                                            front_stub_tenor_or_end_date,
                                            calendar,
                                            business_day_convention,
                                            False)    
    elif isinstance(front_stub_tenor_or_end_date, date):
        front_stub_end_date = front_stub_tenor_or_end_date

    if isinstance(end_stub_tenor_or_start_date, str):
        end_stub_start_date = adjust_date(end_date,
                                            '-'+end_stub_tenor_or_start_date,
                                            calendar,
                                            business_day_convention,
                                            False)    
    elif isinstance(end_stub_tenor_or_start_date, date):
        end_stub_start_date = end_stub_tenor_or_start_date

    list_start_date = [front_stub_end_date if front_stub_end_date else start_date][0]
    list_end_date = [end_stub_start_date if end_stub_start_date else end_date][0]

    list_dates = generate_dates_list(list_start_date,
                                        list_end_date,
                                        tenor,
                                        date_generation_method,
                                        calendar,
                                        business_day_convention,
                                        end_of_month)

    if front_stub_end_date:
        list_dates.insert(0, start_date)
    if end_stub_start_date:
        list_dates.append(end_date)

    return list_dates