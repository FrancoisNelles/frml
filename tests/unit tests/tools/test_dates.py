""" This module is to test the function in tools.dates.py."""

import csv
import pytest
from datetime import (date,
                        datetime)
from frml.tools.dates import (calculate_year_fraction,
                                get_calendar)

def read_csv(file_path):
    """
    Imports a csv file and skips the first row
    """
    with open(file_path, newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            yield row


@pytest.mark.parametrize(
    "country, test_date, holiday_bool",
    [
        ("South Africa", datetime(2019, 1, 1), False),
        ("South Africa", datetime(2019, 1, 2), True),
        ("South Africa", datetime(2019, 3, 21), False),
        ("South Africa", datetime(2019, 4, 27), False),
        ("South Africa", datetime(2019, 5, 1), False),
        ("South Africa", datetime(2019, 6, 16), False),
        ("South Africa", datetime(2019, 8, 9), False),
        ("South Africa", datetime(2019, 9, 24), False),
        ("South Africa", datetime(2019, 12, 16), False),
        ("South Africa", datetime(2019, 12, 25), False),
        ("South Africa", datetime(2019, 12, 26), False),
        ("South Africa", datetime(2019, 12, 27), True),
        ("South Africa", datetime(2019, 12, 28), False),
        ("South Africa", datetime(2019, 12, 29), False),
        ("South Africa", datetime(2019, 12, 30), True),
        ("South Africa", datetime(2019, 12, 31), True),
    ],
)
def test_get_calendar(country, test_date, holiday_bool):
    """Test the calendar objects based on the parametrization above."""
    calendar = get_calendar(country)
    assert calendar.is_on_offset(test_date) == holiday_bool


@pytest.mark.parametrize("index, start_date, end_date, day_count_convention, year_fraction", read_csv('tests/unit tests/tools/day_count_test.csv'))
def test_calculate_year_fraction(index, start_date, end_date, day_count_convention, year_fraction):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    year_fraction = float(year_fraction)
    
    assert calculate_year_fraction(start_date, end_date, day_count_convention) == pytest.approx(year_fraction, rel=1e-7)

def test_calculate_year_fraction_error_catching():

    with pytest.raises(ValueError):

        start_date = date(2022,1,1)
        end_date = date(2022,1,1)
        day_count_convention = 'Actual/366'

        calculate_year_fraction(start_date, end_date, day_count_convention)

    with pytest.raises(TypeError):

        start_date = 1234
        end_date = date(2022,1,1)
        day_count_convention = 'Actual/365'

        calculate_year_fraction(start_date, end_date, day_count_convention)

    with pytest.raises(TypeError):

        start_date = date(2022,1,1)
        end_date = 1234
        day_count_convention = 'Actual/365'

        calculate_year_fraction(start_date, end_date, day_count_convention)

