import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False)



from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from datetime import datetime
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import NumericProperty



class DateSelector(Button):
    value = NumericProperty(1)
    def __init__(self, label, min_value, max_value, initial_value, update_callback, **kwargs):
        super().__init__(**kwargs)

        self.value = initial_value
        self.label_text = label
        self.update_callback = update_callback
        self.min_value = min_value
        self.max_value = max_value
        self.text = f"{self.label_text}: {self.value}"
        self.width = 140
        self.height = 25
        self.dropdown = DropDown()

        self.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.on_select)

        self.update_dropdown()

    def update_dropdown(self):
        self.dropdown.clear_widgets()
        for value in range(self.min_value, self.max_value + 1):
            btn = Button(text=str(value), size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

    def on_select(self, instance, x):
        self.value = int(x)
        self.text = f"{self.label_text}: {self.value}"
        self.update_callback()


    def update_range(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.update_dropdown()


class DateCodeApp(App):
    def build(self):
        # Configuration de la fenêtre
        Window.size = (426, 190)

        # Création d'un BoxLayout principal avec orientation verticale
        main_layout = BoxLayout(orientation='vertical', padding=1, spacing=10)

        # Création d'un BoxLayout pour les sélecteurs de date
        self.layout_select = BoxLayout(orientation='horizontal', padding=1, spacing=1, size_hint_y=None, height=30)

        Window.bind(on_request_close=self.end_func)
        current_date = datetime.now()

        self.year_selector = DateSelector("Year", current_date.year - 5, current_date.year + 2, current_date.year, update_callback=self.update_result)
        self.month_selector = DateSelector("Month", 1, 12, current_date.month, update_callback=self.update_result)
        self.day_selector = DateSelector("Day", 1, 31, current_date.day, update_callback=self.update_result)

        self.layout_select.add_widget(self.day_selector)
        self.layout_select.add_widget(self.month_selector)
        self.layout_select.add_widget(self.year_selector)

        # Ajout du layout_select au début du main_layout
        main_layout.add_widget(self.layout_select)

        # Création d'un BoxLayout pour centrer le résultat
        result_layout = BoxLayout(orientation='vertical')

        date_en = datetime.now().strftime("%A, %B %d, %Y")
        self.date_English_label = Label(text=f'{date_en}', font_size=20, color=(0, 1, 0.5, 1))
        self.date_English_label.font_name ='DejaVuSans'

        self.result_label = Label(text='DateCode:    ', color=(0.4, 1, 0.8, 1))
        self.result_label.font_size = 25
        self.result_label.font_name = "Comic"
        result_layout.add_widget(self.date_English_label)
        result_layout.add_widget(self.result_label)

        # Ajout du result_layout au main_layout
        main_layout.add_widget(result_layout)

        self.update_result()

        return main_layout


    def is_leap_year(self, annee):
        if (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0):
            return True
        else:
            return False

    def update_result(self, *args):
        try:
            date = datetime(self.year_selector.value, self.month_selector.value, self.day_selector.value)

            year = date.year % 100  # Get last two digits of the year
            week_number = date.isocalendar()[1]

            self.date_English_label.text = date.strftime("%A, %B %d, %Y")
            date_code = f"{year:02d}{week_number:02d}"
            self.result_label.text = f'DateCode:    {date_code}'


            # Update year range dynamically
            if self.month_selector.value == 2 and not(self.is_leap_year(self.year_selector.value)):
                self.day_selector.update_range(1, 28)

            if self.month_selector.value == 2 and self.is_leap_year(self.year_selector.value):
                self.day_selector.update_range(1, 29)

            if self.month_selector.value in [1,3,5,7,8,10,12]:
                self.day_selector.update_range(1, 31)

            if self.month_selector.value in [4,6,9,11]:
                self.day_selector.update_range(1, 30)

            if self.year_selector.value == self.year_selector.max_value:
                self.year_selector.update_range(self.year_selector.min_value + 4, self.year_selector.max_value + 4)

            if self.year_selector.value == self.year_selector.min_value:
                self.year_selector.update_range(self.year_selector.min_value - 4, self.year_selector.max_value - 4)

        except ValueError:
            self.day_selector.value-=1
            self.day_selector.on_select(self,self.day_selector.value)
            self.update_result()

    def end_func(self, *args):
        Window.close()


if __name__ == '__main__':
    DateCodeApp().run()