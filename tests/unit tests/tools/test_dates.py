""" This module is to test the function in tools.dates.py."""

import csv
import pytest
from datetime import (date,
                        datetime)
from frml.tools.dates import (adjust_date,
                                adjust_date_to_business_convention,
                                adjust_date_to_month_end,
                                adjust_date_to_tenor,
                                calculate_year_fraction,
                                generate_dates_list,
                                get_calendar)

def read_csv(file_path):
    """
    Imports a csv file and skips the first row, yields every row in the csv.
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

def test_get_calendar_error_catching():
    with pytest.raises(ValueError):
        calendar = "Test"
        get_calendar(calendar)


@pytest.mark.parametrize("start_date, end_date, day_count_convention, year_fraction", read_csv('tests/unit tests/tools/day_count_test.csv'))
def test_calculate_year_fraction(start_date, end_date, day_count_convention, year_fraction):
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

def test_adjust_date_to_tenor_error_catching():
    with pytest.raises(TypeError):
        base_date = 1234
        adjust_tenor = '1M'
        adjust_date_to_tenor(base_date, adjust_tenor)

    with pytest.raises(TypeError):
        base_date = date(2022,1,1)
        adjust_tenor = 1234
        adjust_date_to_tenor(base_date, adjust_tenor)

    with pytest.raises(ValueError):
        base_date = date(2022,1,1)
        adjust_tenor = '1234'
        adjust_date_to_tenor(base_date, adjust_tenor)

def test_adjust_date_to_month_end_error_catching():
    with pytest.raises(TypeError):
        base_date = 1234
        adjust_date_to_month_end(base_date)

def test_adjust_date_to_business_convention_error_catching():
    with pytest.raises(TypeError):
        base_date = 1234
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        adjust_date_to_business_convention(base_date, calendar, business_day_convention)

    with pytest.raises(ValueError):
        base_date = date(2022,1,1)
        calendar = 'South Africas'
        business_day_convention = 'Unadjusted'
        adjust_date_to_business_convention(base_date, calendar, business_day_convention)
    
    with pytest.raises(ValueError):
        base_date = date(2022,1,1)
        calendar = 'South Africa'
        business_day_convention = 'Unadjusteds'
        adjust_date_to_business_convention(base_date, calendar, business_day_convention)

def test_adjust_date_error_catching():
    with pytest.raises(TypeError):
        base_date = '2022/02/01'
        tenor = '1M'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = True
        adjust_date(base_date, tenor, calendar, business_day_convention, end_of_month)

    with pytest.raises(ValueError):
        base_date = date(2022,1,1)
        tenor = '1Ms'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = True
        adjust_date(base_date, tenor, calendar, business_day_convention, end_of_month)
    
    with pytest.raises(ValueError):
        base_date = date(2022,1,1)
        tenor = '1M'
        calendar = 'South Africas'
        business_day_convention = 'Unadjusted'
        end_of_month = True
        adjust_date(base_date, tenor, calendar, business_day_convention, end_of_month)
    
    with pytest.raises(ValueError):
        base_date = date(2022,1,1)
        tenor = '1M'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusteds'
        end_of_month = True
        adjust_date(base_date, tenor, calendar, business_day_convention, end_of_month)
    
    with pytest.raises(ValueError):
        base_date = date(2022,1,1)
        tenor = '1M'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = 'Trues'
        adjust_date(base_date, tenor, calendar, business_day_convention, end_of_month)


@pytest.mark.parametrize("start_date, end_date, tenor, date_generation_method, calendar, business_day_convention, end_of_month, generated_dates_list", read_csv('tests/unit tests/tools/generate_date_list_test.csv'))
def test_generate_dates_list(start_date, end_date, tenor, date_generation_method, calendar, business_day_convention, end_of_month, generated_dates_list):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    end_of_month = [True if end_of_month == "True" else False][0]
    generated_dates_list = [datetime.strptime(list_date, '%Y-%m-%d').date() for list_date in generated_dates_list.split("|")]
    assert generate_dates_list(start_date, end_date, tenor, date_generation_method, calendar, business_day_convention, end_of_month) == generated_dates_list

def test_generate_dates_list_error_catching():
    with pytest.raises(TypeError):
        start_date = '2022,1,1'
        end_date = date(2022,1,31)
        tenor = '1M'
        date_generation_method = 'Forwards'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = True
        generate_dates_list(start_date,
                                end_date,
                                tenor,
                                date_generation_method,
                                calendar,
                                business_day_convention,
                                end_of_month)
    with pytest.raises(TypeError):
        start_date = date(2022,1,1)
        end_date = 19960326
        tenor = '1M'
        date_generation_method = 'Forwards'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = True

        generate_dates_list(start_date,
                                end_date,
                                tenor,
                                date_generation_method,
                                calendar,
                                business_day_convention,
                                end_of_month)
    with pytest.raises(ValueError):
        start_date = date(2022,1,31)
        end_date = date(2022,1,1)
        tenor = '1M'
        date_generation_method = 'Forwards'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = True

        generate_dates_list(start_date,
                                end_date,
                                tenor,
                                date_generation_method,
                                calendar,
                                business_day_convention,
                                end_of_month)
        
    with pytest.raises(ValueError):
        start_date = date(2022,1,1)
        end_date = date(2022,1,31)
        tenor = '1Ms'
        date_generation_method = 'Forwards'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = True

        generate_dates_list(start_date,
                                end_date,
                                tenor,
                                date_generation_method,
                                calendar,
                                business_day_convention,
                                end_of_month)
        
    with pytest.raises(ValueError):
        start_date = date(2022,1,1)
        end_date = date(2022,1,31)
        tenor = '-1M'
        date_generation_method = 'Forwards'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = True

        generate_dates_list(start_date,
                                end_date,
                                tenor,
                                date_generation_method,
                                calendar,
                                business_day_convention,
                                end_of_month)
        
    with pytest.raises(ValueError):
        start_date = date(2022,1,1)
        end_date = date(2022,1,31)
        tenor = '1M'
        date_generation_method = 'Forward'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = True

        generate_dates_list(start_date,
                                end_date,
                                tenor,
                                date_generation_method,
                                calendar,
                                business_day_convention,
                                end_of_month)
        
    with pytest.raises(ValueError):
        start_date = date(2022,1,1)
        end_date = date(2022,1,31)
        tenor = '1M'
        date_generation_method = 'Forwards'
        calendar = 'South Africas'
        business_day_convention = 'Unadjusted'
        end_of_month = True

        generate_dates_list(start_date,
                                end_date,
                                tenor,
                                date_generation_method,
                                calendar,
                                business_day_convention,
                                end_of_month)
        
    with pytest.raises(ValueError):
        start_date = date(2022,1,1)
        end_date = date(2022,1,31)
        tenor = '1M'
        date_generation_method = 'Forwards'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusteds'
        end_of_month = True

        generate_dates_list(start_date,
                                    end_date,
                                    tenor,
                                    date_generation_method,
                                    calendar,
                                    business_day_convention,
                                    end_of_month)
        
    with pytest.raises(ValueError):
        start_date = date(2022,1,1)
        end_date = date(2022,1,31)
        tenor = '1M'
        date_generation_method = 'Forwards'
        calendar = 'South Africa'
        business_day_convention = 'Unadjusted'
        end_of_month = 'True'

        generate_dates_list(start_date,
                                end_date,
                                tenor,
                                date_generation_method,
                                calendar,
                                business_day_convention,
                                end_of_month)