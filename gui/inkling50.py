import flet as ft
from datetime import datetime
import calendar

# Colors
PRIMARY_COLOR = "#B7D4B1"
SIDEBAR_COLOR = "#85A27F"
BACKGROUND_COLOR = "#232b2b"
TEXT_COLOR = "#FFFFFF"

"""Calendar utilities"""
# Create calendar object
cal = calendar.Calendar()

# Constants for date and month
date_class = {0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}
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
    12: "December",
}

# Settings class to navigate between year and month
class Settings:
    # Get system year and month
    year = datetime.now().year
    month = datetime.now().month

    @staticmethod
    def get_year():
        return Settings.year

    @staticmethod
    def get_month():
        return Settings.month

    # Change date and month
    @staticmethod
    def get_date(delta: int):
        # If right arrow is pressed
        if delta == 1:
            if Settings.month + delta > 12:
                Settings.month = 1
                Settings.year += 1
            else:
                Settings.month += 1

        # If left arrow is pressed
        if delta == -1:
            if Settings.month + delta < 1:
                Settings.month = 12
                Settings.year -= 1
            else:
                Settings.month -= 1


# Calendar Classes
class DateGrid(ft.Column):
    # Class constructor
    def __init__(self, year: int, month: int, history_instance: object) -> None:
        super(DateGrid, self).__init__()
        self.year = year
        self.month = month
        self.history_manager = history_instance
        self.date = ft.Text(f"{month_class[self.month]} {self.year}")

        # Controls for the year & month header
        self.year_month = ft.Container(
            bgcolor="#85A27F",
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
            content=ft.Row(
                alignment="center",
                controls=[
                    ft.IconButton(
                        "chevron_left",
                        icon_color="#F4EAD9",
                        on_click=lambda _: self.update_date_grid(-1),
                    ),
                    ft.Container(
                        width=150, content=self.date, alignment=ft.alignment.center
                    ),
                    ft.IconButton(
                        "chevron_right",
                        icon_color="#F4EAD9",
                        on_click=lambda _: self.update_date_grid(1),
                    ),
                ],
            ),
        )

        # Controls for the weekday
        self.controls.insert(1, self.year_month)
        weekday = ft.Row(
            alignment="spaceEvenly",
            controls=[
                ft.Container(
                    content=ft.Text(date_class[i], color="black", text_align="center"),
                    width=30,
                    height=30,
                    bgcolor=BACKGROUND_COLOR,
                )
                for i in range(7)
            ],
        )

        self.controls.insert(1, weekday)
        self.populate_date_grid(self.year, self.month)

    # Controls for date with placement depending on month
    def populate_date_grid(self, year: int, month: int):
        del self.controls[2:]
        for week in cal.monthdayscalendar(year, month):
            row = ft.Row(alignment="spaceEvenly")
            for day in week:
                row.controls.append(
                    ft.Container(
                        content=ft.Text(str(day) if day != 0 else "", color="black"),
                        width=30,
                        height=30,
                        bgcolor=PRIMARY_COLOR if day != 0 else None,
                        border_radius=5,
                    )
                )
            self.controls.append(row)

    # Change placement of date based on month after arrow pressed
    def update_date_grid(self, delta: int):
        Settings.get_date(delta)
        self.update_year_month(Settings.get_year(), Settings.get_month())
        self.populate_date_grid(Settings.get_year(), Settings.get_month())
        self.update()

    # Update year and month
    def update_year_month(self, year: int, month: int):
        self.year = year
        self.month = month
        self.date.value = f"{month_class[self.month]} {self.year}"

# Placeholder for history
class HistoryManager(ft.Column):
    def __init__(self):
        super(HistoryManager, self).__init__()
        self.date = ft.TextField(
            label="Selected Date",
            read_only=True,
            value="",
            height=50,
            border_radius=5,
        )
        self.controls = [self.date]


# Sidebar Application
def main(page: ft.Page):
    page.title = "Inkling50"
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 0

    # Content panel
    content = ft.Container(width=700, bgcolor=BACKGROUND_COLOR, expand=True)

    # Load the calendar
    def load_calendar():
        history_manager = HistoryManager()
        calendar_grid = DateGrid(
            year=Settings.get_year(), month=Settings.get_month(), history_instance=history_manager
        )
        content.content = ft.Container(
            height=800,
            border=ft.border.all(5, "#85A27F"),
            border_radius=20,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=calendar_grid,
        )
        content.update()

    # Load home screen
    def load_home():
        content.content = ft.Text("Welcome to Inkling50! Select an option from the menu.", size=18)
        content.update()

    # Sidebar layout
    sidebar = ft.Container(
        content=ft.Column(
            [
                # App Logo
                ft.Container(
                    content=ft.Image(
                        src="/Users/benraihane/inkling50/gui/inkling.png",
                        width=40,
                        height=40,
                        fit="contain",
                    ),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(bottom=20),
                ),
                # Sidebar Icons
                ft.IconButton("home", icon_color=TEXT_COLOR, on_click=lambda _: load_home()),
                ft.IconButton("calendar_today", icon_color=TEXT_COLOR, on_click=lambda _: load_calendar()),
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor=SIDEBAR_COLOR,
        width=60,
        height=page.height,
        padding=10,
    )

    # Add sidebar and content to the page
    page.add(ft.Row([sidebar, content], expand=True))
    load_home()


# Run the app
ft.app(target=main)
