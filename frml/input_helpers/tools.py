from typing import Literal

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