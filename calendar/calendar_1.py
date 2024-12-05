import flet as ft
import calendar
from datetime import datetime

cal = calendar.Calendar()

date_class = {
    0: "Mo",
    1: "Tu",
    2: "We",
    3: "Th",
    4: "Fr",
    5: "Sa",
    6: "Su"
}

month_class = {
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

    @staticmethod
    def get_year() -> int:
        return Settings.year
    
    @staticmethod
    def get_month() -> int:
        return Settings.month
    
    @staticmethod
    def get_date(delta: int):
        if delta == 1:
            if Settings.month + delta > 12:
                Settings.month = 1
                Settings.year += 1
            else:
                Settings.month += 1
        if delta == -1:
            if Settings.month + delta < 1:
                Settings.month = 12
                Settings.year -= 1
            else:
                Settings.month -= 1
    

date_box_style = {
    "width": 30, "height": 30,
    "alignment": ft.alignment.center, 
    "shape": ft.BoxShape("rectangle"),
    "animate": ft.Animation(400, "ease"),
    "border_radius": 5
}

class DateBox(ft.Container):
    def __init__(self,
                 day: int,
                 date: str = None,
                 date_instance: ft.Column = None,
                 history_instance: ft.Column = None,
                 opacity_: float | int = None,
                 ) -> None:
        super(DateBox, self).__init__(**date_box_style,
                                      data = date,
                                      opacity = opacity_,
                                      on_click = self.selected
                                      )
        
        self.day = day
        self.date_instance = date_instance
        self.history_instance = history_instance

        self.content = ft.Text(self.day, text_align="center")
    
    def selected(self, event: ft.TapEvent):
        if self.date_instance:
            for row in self.date_instance.controls[1:]:
                for date in row.controls:
                    date.bgcolor = "#85A27F" if date == event.control else None
                    date.border = (ft.border.all(0.5, "#85A27F")) if date == event.control else None
            
                    if date == event.control:
                        self.history_instance.date.value = event.control.data

            self.date_instance.update()
            self.history_instance.update()

class DateGrid(ft.Column):
    def __init__(self, year: int, month: int, history_instance: object) -> None:
        super(DateGrid, self).__init__()
        
        self.year = year
        self.month = month
        self.history_manager = history_instance

        self.date = ft.Text(f"{month_class[self.month]} {self.year}")

        self.year_month = ft.Container(
            bgcolor = "#85A27F",
            border_radius = ft.border_radius.only(top_left = 10, top_right = 10),
            content = ft.Row(alignment = "center",
                             controls = [ft.IconButton("chevron_left", icon_color = "#F4EAD9", on_click = lambda event: self.update_date_grid(event, -1)
                                                        ),
                                         ft.Container(width = 150, content = self.date, alignment = ft.alignment.center),
                                         ft.IconButton("chevron_right", icon_color = "#F4EAD9", on_click = lambda event: self.update_date_grid(event, 1))]
                            )
        )

        self.controls.insert(1, self.year_month)

        weekday = ft.Row(
            alignment="spaceEvenly",
            controls = [DateBox(day = date_class[i], opacity_ = 0.80) for i in range(7)]
        )

        self.controls.insert(1, weekday)
        self.populate_date_grid(self.year, self.month)
    
    def populate_date_grid(self, year: int, month: int):
        del self.controls[2:]

        for week in cal.monthdayscalendar(year, month):
            row = ft.Row(alignment = "spaceEvenly")
            for day in week:
                if day != 0:
                    row.controls.append(
                        DateBox(day, self.format_date(day), self, self.history_manager))
                else:
                    row.controls.append(DateBox(" "))
            
            self.controls.append(row)

    def update_date_grid(self, event: ft.TapEvent, delta: int):
        Settings.get_date(delta)

        self.update_year_month(Settings.get_year(), Settings.get_month())
        self.populate_date_grid(Settings.get_year(), Settings.get_month())
        self.update()
    
    def update_year_month(self, year: int, month: int) -> None:
        self.year = year
        self.month = month
        self.date.value = f"{month_class[self.month]} {self.year}"
        
    def format_date(self, day: int):
        return f"{month_class[self.month]} {day}, {self.year}"

def history_style(height: int):
    return {
        "height": height,
        "focused_border_color": "#F4EAD9",
        "border_radius": 5,
        "cursor_height": 16,
        "cursor_color": "white",
        "content_padding": 10,
        "border_width": 1.5,
        "text_size": 12
    }

class HistoryManager(ft.Column):
    def __init__(self):
        super(HistoryManager, self).__init__()

        self.date = ft.TextField(
            label = "Date", read_only = True, value = " ", **history_style(50)
        )

        self.controls = [self.date]

def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.SYSTEM
    
    history_manager = HistoryManager()

    grid = DateGrid(
        year = Settings.get_year(),
        month = Settings.get_month(),
        history_instance = history_manager
    )
    page.add(
        ft.Container(
            height = 350,
            border = ft.border.all(0.75, "#85A27F"),
            border_radius = 10,
            clip_behavior = ft.ClipBehavior.HARD_EDGE,
            content = grid
        ),
        ft.Divider(color = "transparent", height = 20), 
        history_manager
    )
    page.update()
    
ft.app(main)