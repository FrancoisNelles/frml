import csv
import pytest
from datetime import (date,
                        datetime)
from frml.tools.dates import calculate_year_fraction

def read_csv(file_path):
    """
    Imports a csv file and skips the first row
    """
    with open(file_path, newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            yield row

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

