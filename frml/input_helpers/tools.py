from typing import Literal
from frml.tools.calendars import (
    BotswanaBusinessDays,
    GhanaBusinessDays,
    KenyaBusinessDays,
    MalawiBusinessDays,
    NigeriaBusinessDays,
    NoHolidayBusinessDays,
    SouthAfricaBusinessDays,
    UnitedStatesOfAmerica_NYBusinessDays,
    ZimbabweBusinessDays,
)

class Calendars:
    """
    This class is intended to help populate function inputs with allowable drop down lists.
    """
    calendars = Literal[
        Literal["Botswana"],
        Literal["Ghana"],
        Literal["Kenya"],
        Literal["Malawi"],
        Literal["Nigeria"],
        Literal["No Holidays"],
        Literal["South Africa"],
        Literal["UnitedStatesOfAmerica_NYBusinessDays"],
        Literal["Zimbabwe"],
    ]

    calendar_sets = {
        "Botswana": BotswanaBusinessDays(),
        "Ghana": GhanaBusinessDays(),
        "Kenya": KenyaBusinessDays(),
        "Malawi": MalawiBusinessDays(),
        "Nigeria": NigeriaBusinessDays(),
        "No Holidays": NoHolidayBusinessDays(),
        "South Africa": SouthAfricaBusinessDays(),
        "United States of America - NY": UnitedStatesOfAmerica_NYBusinessDays(),
        "Zimbabwe": ZimbabweBusinessDays(),
    }

class Dates:
    """
    This class is intended to help populate function inputs with allowable drop down lists.
    """

    day_count_conventions = Literal[
                            Literal["Actual/Actual"],
                            Literal["Actual/365"],
                            Literal["Actual/360"],
                            Literal["30/360E"],
                            Literal["30/360A"]
    ]

    day_count_list = ["Actual/Actual",
                        "Actual/365",
                        "Actual/360",
                        "30/360E",
                        "30/360A"]