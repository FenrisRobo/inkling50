import flet as ft
import calendar
from datetime import datetime

cal = calendar.Calendar()

date_class: dict[int, str] = {
    0: "Mo",
    1: "Tu",
    2: "We",
    3: "Th",
    4: "Fr",
    5: "Sa",
    6: "Su"
}

month_class: dict[int, str] = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

class Settings:
    year = datetime.now().year
    month = datetime.now().month
    

date_box_style: dict[str, Any] = {
    "width": 30, "height": 30, "alignment": ft.alignment.center, 
    "shape": ft.BoxShape("rectangle"), "animate": ft.Animation(400, "ease"),
    "border_radius": 5
}

class DateBox(ft.Container):
    def __init__(self,
                 day: int,
                 date: str = None,
                 date_instance: ft.Column = None,
                 opacity1: float | int = None,
                 ) -> None:
        super(DateBox, self).__init__(**date_box_style,
                                      data = date,
                                      opacity = opacity1,
                                      )
        
        self.day = day
        self.date_instance = date_instance
        self.content = ft.Text(self.day, text_align="center")

class DateGrid(ft.Column):
    def __init__(self, year: int, month: int) -> None:
        super(DateGrid, self).__init__()
        
        self.year = year
        self.month = month
        
        

def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.SYSTEM
    grid = DateGrid()
    page.update()
    
ft.app(main)