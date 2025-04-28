""" This module is to create calendars for any country."""

from dataclasses import dataclass
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    Holiday,
    EasterMonday,
    GoodFriday,
    sunday_to_monday,
    MO,
    TU,
    TH,
    FR,
)
from pandas.tseries.offsets import Day, Easter, DateOffset


@dataclass
class CalendarMemory:
    """
    This class is a holder for initialized calendars, such that they can be referenced without
    having to reinitialize them on each query.
    """

    calendar_instance_dictionary = {}


class BotswanaBusinessDays(AbstractHolidayCalendar):
    """Botswana Business Day Calendar
    Create an offset with offset = pd.offsets.CustomBusinessDay(calendar=BWBusinessDays)
    You can also use offset.rollforward(date) and offset.rollback(date)
    to get the next and previous"""

    rules = [
        Holiday("New Year", month=1, day=1, observance=sunday_to_monday),
        GoodFriday,
        EasterMonday,
        Holiday("Ascencion Day", month=1, day=1, offset=[Easter(), Day(39)]),
        Holiday("Labour Day", month=5, day=1, observance=sunday_to_monday),
        Holiday("Sir Seretse Khama Day", month=7, day=1, observance=sunday_to_monday),
        # Presidents' Day as the third Monday in July
        Holiday("Presidents Day", month=7, day=1, offset=DateOffset(weekday=MO(3))),
        # The Day after Presidents' Day as the Tuesday after Presidents' Day
        Holiday(
            "Day after Presidents Day", month=7, day=1, offset=DateOffset(weekday=TU(3))
        ),
        Holiday("Democracy Day", month=6, day=12, observance=sunday_to_monday),
        Holiday("Botswana Day", month=9, day=30, observance=sunday_to_monday),
        Holiday("Independence Day", month=10, day=1, observance=sunday_to_monday),
        Holiday("Christmas Day", month=12, day=25, observance=sunday_to_monday),
        Holiday("Boxing Day", month=12, day=26, observance=sunday_to_monday),
    ]


class GhanaBusinessDays(AbstractHolidayCalendar):
    """Ghana Business Day Calendar
    Create an offset with offset = pd.offsets.CustomBusinessDay(calendar=GhanaBusinessDays)
    You can also use offset.rollforward(date) and offset.rollback(date)
    to get the next and previous"""

    rules = [
        Holiday("New Year", month=1, day=1, observance=sunday_to_monday),
        Holiday("Constitution Day", month=1, day=7, observance=sunday_to_monday),
        GoodFriday,
        EasterMonday,
        Holiday("Independence Day", month=3, day=6, observance=sunday_to_monday),
        Holiday("Labour Day", month=5, day=1, observance=sunday_to_monday),
        Holiday("Founders Day", month=8, day=4, observance=sunday_to_monday),
        Holiday(
            "Kwame Nkrumah Memorial Day", month=9, day=21, observance=sunday_to_monday
        ),
        # Farmer's Day (first Friday in December) for the given year
        Holiday("Farmer's Day", month=12, day=1, offset=DateOffset(weekday=FR(1))),
        Holiday("Christmas Day", month=12, day=25, observance=sunday_to_monday),
        Holiday("Day of Goodwill", month=12, day=26, observance=sunday_to_monday),
    ]


class KenyaBusinessDays(AbstractHolidayCalendar):
    """Kenya Business Day Calendar
    Create an offset with offset = pd.offsets.CustomBusinessDay(calendar=KenyaBusinessDays)
    You can also use offset.rollforward(date) and offset.rollback(date)
    to get the next and previous"""

    rules = [
        Holiday("New Year", month=1, day=1, observance=sunday_to_monday),
        GoodFriday,
        EasterMonday,
        Holiday("Labour Day", month=5, day=1, observance=sunday_to_monday),
        Holiday("Madaraka Day", month=6, day=1, observance=sunday_to_monday),
        Holiday("Huduma Day", month=10, day=10, observance=sunday_to_monday),
        Holiday("Mashujaa Day", month=10, day=20, observance=sunday_to_monday),
        Holiday("Jamhuri Day", month=12, day=12, observance=sunday_to_monday),
        Holiday("Christmas Day", month=12, day=25, observance=sunday_to_monday),
        Holiday("Day of Goodwill", month=12, day=26, observance=sunday_to_monday),
    ]


class MalawiBusinessDays(AbstractHolidayCalendar):
    """Malawi Business Day Calendar
    Create an offset with offset = pd.offsets.CustomBusinessDay(calendar=MalawiBusinessDays)
    You can also use offset.rollforward(date) and offset.rollback(date)
    to get the next and previous"""

    rules = [
        Holiday("New Year", month=1, day=1, observance=sunday_to_monday),
        Holiday("John Chilembwe Day", month=1, day=15, observance=sunday_to_monday),
        GoodFriday,
        EasterMonday,
        Holiday("Martyrs Day", month=3, day=3, observance=sunday_to_monday),
        Holiday("Labour Day", month=5, day=1, observance=sunday_to_monday),
        Holiday("Kamuzu Day", month=5, day=14, observance=sunday_to_monday),
        Holiday("Independence Day", month=7, day=6, observance=sunday_to_monday),
        Holiday("Mothers Day", month=10, day=16, observance=sunday_to_monday),
        Holiday("Christmas Day", month=12, day=25, observance=sunday_to_monday),
        Holiday("Day of Goodwill", month=12, day=26, observance=sunday_to_monday),
    ]


class NigeriaBusinessDays(AbstractHolidayCalendar):
    """Nigeria Business Day Calendar
    Create an offset with offset = pd.offsets.CustomBusinessDay(calendar=NigeriaBusinessDays)
    You can also use offset.rollforward(date) and offset.rollback(date)
    to get the next and previous"""

    rules = [
        Holiday("New Year", month=1, day=1, observance=sunday_to_monday),
        Holiday(
            "Armed Forces Remembrance Day", month=1, day=15, observance=sunday_to_monday
        ),
        GoodFriday,
        EasterMonday,
        Holiday("Workers Day", month=5, day=1, observance=sunday_to_monday),
        Holiday("Democracy Day", month=6, day=12, observance=sunday_to_monday),
        Holiday("Independence Day", month=10, day=1, observance=sunday_to_monday),
        Holiday("Christmas Day", month=12, day=25, observance=sunday_to_monday),
        Holiday("Day of Goodwill", month=12, day=26, observance=sunday_to_monday),
    ]


class NoHolidayBusinessDays(AbstractHolidayCalendar):
    """
    No Holiday Business Day Calendar
    This calendar is to support only weekend and month end roll overs. This Calendar does
    not contain any holidays
    """

    rules = []


class SouthAfricaBusinessDays(AbstractHolidayCalendar):
    """South African Business Day Calendar
    Create an offset with offset = pd.offsets.CustomBusinessDay(calendar=SouthAfricaBusinessDays)
    You can also use offset.rollforward(date) and offset.rollback(date)
    to get the next and previous"""

    rules = [
        Holiday("New Year", month=1, day=1, observance=sunday_to_monday),
        Holiday("Human Rights Day", month=3, day=21, observance=sunday_to_monday),
        GoodFriday,
        EasterMonday,
        Holiday("Freedom Day", month=4, day=27, observance=sunday_to_monday),
        Holiday("Workers Day", month=5, day=1, observance=sunday_to_monday),
        Holiday("Youth Day", month=6, day=16, observance=sunday_to_monday),
        Holiday("National Women Day", month=8, day=9, observance=sunday_to_monday),
        Holiday("Heritage Day", month=9, day=24, observance=sunday_to_monday),
        Holiday("Reconciliation Day", month=12, day=16, observance=sunday_to_monday),
        Holiday("Christmas Day", month=12, day=25, observance=sunday_to_monday),
        Holiday("Day of Goodwill", month=12, day=26, observance=sunday_to_monday),
    ]


class UnitedStatesOfAmerica_NYBusinessDays(AbstractHolidayCalendar):
    rules = [
        Holiday("New Year", month=1, day=1, observance=sunday_to_monday),
        Holiday("Martin Luther King Jr. Day", month=1, day=1, offset=DateOffset(weekday=MO(3))),
        Holiday("Presidents' Day", month=2, day=1, offset=DateOffset(weekday=MO(3))),
        GoodFriday,
        Holiday("Memorial Day", month=5, day=31, offset=DateOffset(weekday=MO(-1))),
        Holiday("Independence Day", month=7, day=4, observance=sunday_to_monday),
        Holiday("Labor Day", month=9, day=1, offset=DateOffset(weekday=MO(1))),
        Holiday("Columbus Day", month=10, day=1, offset=DateOffset(weekday=MO(2))),
        Holiday("Veterans Day", month=11, day=11, observance=sunday_to_monday),
        Holiday("Thanksgiving Day", month=11, day=1, offset=DateOffset(weekday=TH(2))),
        Holiday("Christmas Day", month=12, day=25, observance=sunday_to_monday),
    ]


class ZimbabweBusinessDays(AbstractHolidayCalendar):
    """Zimbabwe Business Day Calendar
    Create an offset with offset = pd.offsets.CustomBusinessDay(calendar=ZimbabweBusinessDays)
    You can also use offset.rollforward(date) and offset.rollback(date)
    to get the next and previous"""

    rules = [
        Holiday("New Year", month=1, day=1, observance=sunday_to_monday),
        Holiday(
            "Robert Gabriel Mugabe National Youth Day",
            month=2,
            day=21,
            observance=sunday_to_monday,
        ),
        GoodFriday,
        EasterMonday,
        Holiday("Independence Day", month=4, day=18, observance=sunday_to_monday),
        Holiday("Labour Day", month=5, day=1, observance=sunday_to_monday),
        Holiday("Africa Day", month=5, day=25, observance=sunday_to_monday),
        Holiday("Unity Day", month=12, day=22, observance=sunday_to_monday),
        # Heroes' Day as the second Monday in August
        Holiday("Heroes Day", month=8, day=1, offset=DateOffset(weekday=MO(2))),
        # The Defence Forces Day as the Tuesday after Heroes' Day
        Holiday("Defence Forces Day", month=8, day=1, offset=DateOffset(weekday=TU(2))),
        Holiday("Christmas Day", month=12, day=25, observance=sunday_to_monday),
        Holiday("Day of Goodwill", month=12, day=26, observance=sunday_to_monday),
    ]