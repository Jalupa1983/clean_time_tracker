import os 
import random
import calendar
import fitz  # PyMuPDF
from datetime import datetime
from calendar import monthrange
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.image import Image as CoreImage
from io import BytesIO
from storage import save_user_data, load_user_data  # Your JSON storage handlers

# Force working directory to this script's folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))


IMAGE_FOLDER = "images"

motivational_messages = [
    "One day at a time. You’re doing great.",
    "Each clean day is a new beginning.",
    "You're proof that recovery is possible.",
    "You are stronger than your past.",
    "Healing is happening — trust the process.",
    "Every clean day adds strength to your soul.",
    "Every moment clean is a moment won.",
    "Your journey is inspiring, keep moving forward.",
    "You’ve come too far to go back now. Eyes forward.",
    "You don’t need to be perfect — just show up and keep going.",
    "Every day you stay clean is a middle finger to your past.",
    "It’s not about being clean forever. Just today. Win today.",
    "Some people collect stamps — you collect clean days and life lessons.",
    "Sobriety’s wild… suddenly you remember birthdays, appointments, and where your phone is."
]

def calculate_days_clean(clean_date_str):
    try:
        clean_date = datetime.strptime(clean_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        return (today - clean_date).days
    except:
        return 0

def get_random_image():
    if not os.path.exists(IMAGE_FOLDER):
        return None
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(".png")]
    if not images:
        return None
    return os.path.join(IMAGE_FOLDER, random.choice(images))


from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Welcome Message near the top
        welcome_label = Label(
            text=("Welcome!\n\n"
                  "You’ve taken the first step toward healing, and that’s no small thing.\n\n"
                  "Whether this is day one or day one hundred, your commitment to change is a sign of strength — not weakness.\n\n"
                  "This journey isn’t easy, but you’re not alone. Every clean day is a win. Every moment is a victory. "
                  "And this app is here to walk with you, one step at a time."),
            halign="center",
            valign="top",
            font_size=24,
            size_hint=(0.9, None),
            height=Window.height * 0.5,
            pos_hint={"center_x": 0.5, "top": 0.95},
            text_size=(Window.width * 0.9, None)
        )
        layout.add_widget(welcome_label)

        # Serenity Prayer around 3/4 down
        serenity_label = Label(
            text=("[i]God, grant me the serenity\n"
                  "to accept the things I cannot change,\n"
                  "courage to change the things I can,\n"
                  "and wisdom to know the difference.[/i]"),
            halign="center",
            valign="middle",
            font_size=22,
            size_hint=(0.9, None),
            height=150,
            pos_hint={"center_x": 0.5, "top": 0.3},
            text_size=(Window.width * 0.9, None),
            markup=True
        )
        layout.add_widget(serenity_label)

        # Transparent Get Started button at the bottom
        get_started_btn = Button(
            text="Get Started",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "y": 0.05},
            background_normal='',  # This makes the button background transparent
            background_color=(0, 0, 0, 0),  # Fully transparent background
            color=(0.1, 0.5, 0.8, 1),  # Text color (blue-ish)
            font_size=20,
            bold=True,
        )
        get_started_btn.bind(on_press=self.go_to_setup)
        layout.add_widget(get_started_btn)

        self.add_widget(layout)

    def go_to_setup(self, instance):
        self.manager.current = "setup"


class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.form_layout = BoxLayout(orientation='vertical', padding=30, spacing=20, size_hint=(None, None))
        self.form_layout.width = 400
        self.form_layout.height = 400

        title_label = Label(
            text="Please Enter Your Info:",
            font_size=28,
            size_hint=(None, None),
            size=(280, 50))
        title_anchor = AnchorLayout(anchor_x='center')
        title_anchor.add_widget(title_label)
        self.form_layout.add_widget(title_anchor)

        self.entered_name = ""
        self.name_input = Button(
            text="Enter Your Name", 
            size_hint=(None, None), 
            size=(280, 60), 
            font_size=22)
        self.name_input.bind(on_release=self.open_name_input)
        name_anchor = AnchorLayout(anchor_x='center')
        name_anchor.add_widget(self.name_input)
        self.form_layout.add_widget(name_anchor)

        # Add label above date spinners
        clean_date_label = Label(
            text="Please enter your clean date:",
            font_size=22,
            size_hint=(None, None),
            size=(280, 40))
        clean_date_anchor = AnchorLayout(anchor_x='center')
        clean_date_anchor.add_widget(clean_date_label)
        self.form_layout.add_widget(clean_date_anchor)

        self.year_spinner = Spinner(
            text='Year',
            values=[str(year) for year in range(datetime.now().year, 1979, -1)],
            size_hint=(None, None),
            size=(100, 60),
            font_size=22)
        self.month_spinner = Spinner(
            text='Month',
            values=[str(m) for m in range(1, 13)],
            size_hint=(None, None),
            size=(80, 60),
            font_size=22)
        self.day_spinner = Spinner(
            text='Day',
            values=[str(d) for d in range(1, 32)],
            size_hint=(None, None),
            size=(80, 60),
            font_size=22)

        date_box = BoxLayout(
            orientation='horizontal', 
            spacing=10, 
            size_hint=(None, None), 
            size=(280, 60))
        date_box.add_widget(self.year_spinner)
        date_box.add_widget(self.month_spinner)
        date_box.add_widget(self.day_spinner)

        date_anchor = AnchorLayout(anchor_x='center')
        date_anchor.add_widget(date_box)
        self.form_layout.add_widget(date_anchor)

        self.message_label = Label(size_hint_y=None, height=40, font_size=20, color=(1, 0, 0, 1))
        self.form_layout.add_widget(self.message_label)

        root = FloatLayout()

        form_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 1), pos_hint={"center_y": 0.75})
        form_anchor.add_widget(self.form_layout)
        root.add_widget(form_anchor)

        self.save_button = Button(
            text="Save and Continue",
            size_hint=(None, None),
            size=(280, 60),
            font_size=24,
            pos_hint={"center_x": 0.5, "y": 0.05})
        self.save_button.bind(on_press=self.save_data)
        root.add_widget(self.save_button)

        self.add_widget(root)

    def open_name_input(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        ti = TextInput(text=self.entered_name, multiline=False, font_size=22, size_hint_y=None, height=60)
        btn = Button(text="OK", size_hint_y=None, height=60, font_size=22)
        content.add_widget(ti)
        content.add_widget(btn)

        popup = Popup(title="Enter Your Name", content=content, size_hint=(0.8, 0.4))

        def on_ok(instance):
            self.entered_name = ti.text.strip()
            self.name_input.text = self.entered_name if self.entered_name else "Enter Your Name"
            popup.dismiss()

        btn.bind(on_press=on_ok)
        popup.open()

    def save_data(self, instance):
        name = self.entered_name.strip()
        year = self.year_spinner.text
        month = self.month_spinner.text
        day = self.day_spinner.text

        if not name:
            self.message_label.text = "X Please enter your name."
            return
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            self.message_label.text = "X Please select a valid date."
            return
        try:
            clean_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            self.message_label.text = "X Invalid date."
            return

        save_user_data(name, clean_date.strftime("%Y-%m-%d"))
        self.manager.transition_to("main")
        self.manager.get_screen("main").update_screen()


import os  # make sure this is at the top of your file

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.top_image = Image(size_hint=(0.3, 0.3), pos_hint={"center_x": 0.5, "top": 1})
        self.label = Label(text="", font_size=24, halign="center", valign="middle",
                           size_hint=(0.9, 0.4), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.label.bind(size=self.label.setter('text_size'))
        self.bottom_image = Image(size_hint=(0.3, 0.3), pos_hint={"center_x": 0.5, "y": 0})
        self.home_button = Button(text="Home", size_hint=(0.15, None), height=60,
                                  background_color=(0, 0, 0, 0), background_normal="",
                                  color=(1, 1, 1, 1), font_size=22, pos_hint={"center_x": 0.83, "y": 0.05})
        self.home_button.bind(on_press=lambda x: self.manager.transition_to("home"))
        self.layout.add_widget(self.top_image)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.bottom_image)
        self.layout.add_widget(self.home_button)
        self.add_widget(self.layout)

    def on_enter(self):
        self.update_screen()

    def update_screen(self):
        data = load_user_data()
        if not data:
            self.label.text = "No user data found."
            return

        try:
            name = data.get("name", "Friend")
            clean_date = data.get("clean_date")
            days = calculate_days_clean(clean_date)
            image_path = get_random_image()

            # Normalize and validate image path
            if image_path:
                image_path = os.path.abspath(os.path.normpath(image_path))

            # Milestone messages
            if days == 30:
                message = "30 days clean! That’s one hell of a month. You’ve just done something most people couldn’t. Respect."
            elif days == 60:
                message = "60 days clean — you're no rookie anymore. Two months of fighting back. Keep killing it."
            elif days == 90:
                message = "90 days! That’s a whole quarter of a year clean. You’re not just surviving — you’re winning."
            elif days == 180:
                message = "Half a freakin’ year clean. That’s strength. That’s growth. That’s you changing your life."
            elif days == 270:
                message = "9 months clean — you've rebuilt more than just habits. You’ve rebuilt *you*."
            elif days == 365:
                message = "1 full year. 365 clean days. A whole revolution around the sun — and you’re still rising. 🎉"
            elif days == 547:
                message = "18 months clean. That’s not luck — that’s you doing the work. Quietly unstoppable."
            elif days >= 730 and days % 365 == 0:
                years = days // 365
                message = f"{years} years clean. You’ve come a long way — and you’re still leveling up."
            else:
                message = random.choice(motivational_messages)

            self.label.text = f"{name}, you have been clean for {days} days!\n\n{message}"

            if image_path and os.path.exists(image_path):
                self.top_image.source = image_path
                self.bottom_image.source = image_path
            else:
                self.top_image.source = ""
                self.bottom_image.source = ""
        except Exception as e:
            self.label.text = "Error loading data."
            print("Exception in update_screen:", e)


from kivy.uix.widget import Widget  # spacer widget
from pathlib import Path

DATA_FILE = Path("JSON_files/user_data.json")

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()

        top_label = Label(
            text="Home Screen",
            font_size=28,
            size_hint=(None, None),
            size=(400, 60),
            pos_hint={"center_x": 0.5, "top": 0.98})
        root.add_widget(top_label)

        na_button = Button(
            text="Narcotics Anonymous Readings",
            size_hint=(None, None),
            size=(310, 60),
            font_size=20,
            pos_hint={"center_x": 0.5, "center_y": 0.65})
        na_button.bind(on_press=lambda x: self.manager.transition_to("na_readings"))
        root.add_widget(na_button)

        aa_button = Button(
            text="Alcoholics Anonymous Readings",
            size_hint=(None, None),
            size=(310, 60),
            font_size=20,
            pos_hint={"center_x": 0.5, "center_y": 0.53})
        aa_button.bind(on_press=lambda x: self.manager.transition_to("aa_readings"))
        root.add_widget(aa_button)

        bottom_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=60,
            padding=[30, 0, 30, 20],
            spacing=20,
            pos_hint={"x": 0, "y": 0}
        )

        back_button = Button(
            text="Back to Message",
            size_hint=(None, None),
            size=(200, 50),
            font_size=20)
        back_button.bind(on_press=lambda x: self.manager.transition_to("main"))

        reset_button = Button(
            text="Reset Clean Date",
            size_hint=(None, None),
            size=(200, 50),
            font_size=20)
        reset_button.bind(on_press=self.reset_clean_date)

        bottom_row.add_widget(back_button)
        bottom_row.add_widget(Widget())
        bottom_row.add_widget(reset_button)

        root.add_widget(bottom_row)
        self.add_widget(root)

    def reset_clean_date(self, instance):
        if DATA_FILE.exists():
            DATA_FILE.unlink()
            print("User data reset.")
        else:
            print("No user data file found to reset.")
        self.manager.transition_to("setup")


from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class NAReadingsMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Title label centered at the top
        title = Label(
            text="NA Readings",
            font_size='32sp',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        layout.add_widget(title)

        # Just For Today button
        jft_btn = Button(
            text="Just For Today",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.58},
            font_size=18
        )
        jft_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'just_for_today'))
        layout.add_widget(jft_btn)

        #NA Basic Text button
        basic_text_btn = Button(
            text="NA Basic Text",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.47},
            font_size=18
        )
        basic_text_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'na_basic_text'))
        layout.add_widget(basic_text_btn)

        # # It Works How and Why button
        # it_works_btn = Button(
        #     text="It Works How and Why",
        #     size_hint=(None, None),
        #     size=(300, 60),
        #     pos_hint={"center_x": 0.5, "center_y": 0.36},
        #     font_size=18
        # )
        # it_works_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'it_works'))
        # layout.add_widget(it_works_btn)

        # # NA Step Guide button
        # step_guide_btn = Button(
        #     text="NA Step Guide",
        #     size_hint=(None, None),
        #     size=(300, 60),
        #     pos_hint={"center_x": 0.5, "center_y": 0.25},
        #     font_size=18
        # )
        # step_guide_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'na_step_guide'))
        # layout.add_widget(step_guide_btn)

        # Back button bottom right
        back_btn = Button(
            text="Back",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"right": 0.98, "y": 0.02},
            font_size=16
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        self.add_widget(layout)


import os
import json
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from datetime import datetime, timedelta

class JustForTodayScreen(Screen):
    def on_enter(self):
        self.current_date = datetime.now()
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        # Build absolute path to JSON file based on script location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "JSON_files", "Just_For_Today.json")

        # Load the reading from JSON using absolute path
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                readings = json.load(f)
        except Exception as e:
            readings = {}
            print(f"Error loading JSON: {e}")

        # Format the current date string
        today_str = self.current_date.strftime('%B %d').lstrip("0").replace(" 0", " ")
        reading_text = readings.get(today_str, "Sorry, no reading found for today.")

        # Main vertical layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header label
        header = Label(
            text="Just For Today Reading",
            font_size='24sp',
            size_hint_y=None,
            height=dp(40),
            halign='center',
            valign='middle',
        )
        header.bind(size=header.setter('text_size'))
        layout.add_widget(header)

        # Scrollable reading area
        scroll = ScrollView(do_scroll_x=False)

        reading_layout = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        reading_layout.bind(minimum_height=reading_layout.setter('height'))

        reading_label = Label(
            text=f"[b]{today_str}[/b]\n\n{reading_text}",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        reading_label.bind(texture_size=reading_label.setter('size'))
        reading_label.text_size = (self.width - dp(40), None)

        reading_layout.add_widget(reading_label)
        scroll.add_widget(reading_layout)
        layout.add_widget(scroll)

        # Bottom button bar with aligned buttons
        button_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            padding=10,
            spacing=10,
            orientation='horizontal'
        )

        prev_button = Button(
            text="Previous Reading",
            size_hint=(None, None),
            height=dp(40),
        )
        prev_button.bind(on_release=self.previous_reading)
        prev_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        back_button = Button(
            text="Back",
            size_hint=(None, None),
            height=dp(40),
        )
        back_button.bind(on_release=self.go_back)
        back_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        next_button = Button(
            text="Next Reading",
            size_hint=(None, None),
            height=dp(40),
        )
        next_button.bind(on_release=self.next_reading)
        next_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        # Add buttons with spacers for alignment
        button_bar.add_widget(prev_button)
        button_bar.add_widget(Widget())  # spacer pushes the back button toward center
        button_bar.add_widget(back_button)
        button_bar.add_widget(Widget())  # spacer pushes the next button right
        button_bar.add_widget(next_button)

        layout.add_widget(button_bar)
        self.add_widget(layout)

    def go_back(self, *args):
        if 'na_readings' in self.manager.screen_names:
            self.manager.current = 'na_readings'
        else:
            self.manager.current = 'home'

    def previous_reading(self, *args):
        self.current_date -= timedelta(days=1)
        self.build_ui()

    def next_reading(self, *args):
        self.current_date += timedelta(days=1)
        self.build_ui()


from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.resources import resource_find
import json
import os

class NABasicTextScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load JSON file
        self.pages = {}
        try:
            json_path = resource_find("JSON_files/NA_Basic_Text.json")
            if json_path and os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    self.pages = json.load(f)
            else:
                print("⚠️ JSON file not found at:", json_path)
        except Exception as e:
            print("❌ Error loading JSON:", e)

        self.total_pages = len(self.pages)
        self.current_page = 1

        root = FloatLayout()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(1, 1))

        # 🔧 Proper scrollable label with expanding height
        self.text_label = Label(
            text='Loading...',
            font_size=18,
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.text_label.bind(texture_size=self.update_label_height)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.text_label)

        layout.add_widget(scroll)

        # Navigation bar
        nav = BoxLayout(size_hint=(1, None), height=50, spacing=10)

        self.page_input = TextInput(
            text='1',
            multiline=False,
            size_hint=(None, None),
            size=(80, 44),
            input_filter='int'
        )
        go_button = Button(text="Go", size_hint=(None, None), size=(60, 44))
        prev_button = Button(text="Previous", size_hint=(None, None), size=(100, 44))
        next_button = Button(text="Next", size_hint=(None, None), size=(100, 44))

        nav.add_widget(Label(text="Page:", size_hint=(None, None), size=(50, 44)))
        nav.add_widget(self.page_input)
        nav.add_widget(go_button)
        nav.add_widget(prev_button)
        nav.add_widget(next_button)

        layout.add_widget(nav)
        root.add_widget(layout)

        # Back button
        back_button = Button(
            text='Back',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'right': 0.98, 'y': 0.02},
            font_size=16
        )
        back_button.bind(on_press=self.go_back)
        root.add_widget(back_button)

        self.add_widget(root)

        # Bind buttons
        go_button.bind(on_press=self.go_to_page)
        prev_button.bind(on_press=self.prev_page)
        next_button.bind(on_press=self.next_page)

        # Load first page
        self.load_page(self.current_page)

    def update_label_height(self, instance, size):
        instance.height = size[1]
        instance.text_size = (instance.width, None)

    def load_page(self, page_num):
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num
            self.page_input.text = str(page_num)
            content = self.pages.get(str(page_num), "[Page not found]")
            print(f"🔹 Loading page {page_num}")
            self.text_label.text = content
        else:
            self.text_label.text = "[Invalid page number]"

    def go_to_page(self, instance):
        try:
            page = int(self.page_input.text)
            self.load_page(page)
        except ValueError:
            pass

    def next_page(self, instance):
        if self.current_page < self.total_pages:
            self.load_page(self.current_page + 1)

    def prev_page(self, instance):
        if self.current_page > 1:
            self.load_page(self.current_page - 1)

    def go_back(self, instance):
        self.manager.current = 'na_readings'


# from kivy.uix.textinput import TextInput
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.core.image import Image as CoreImage
# from kivy.uix.image import Image
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.screenmanager import Screen
# from io import BytesIO
# import fitz  # PyMuPDF
# import os

# class ItWorksScreen(Screen):
#     OFFSET = 6  # PDF page 7 will be logical page 1

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
    
#         pdf_path = os.path.join(os.path.dirname(__file__), "PDF_files", "It_Works.pdf")
#         self.doc = fitz.open(pdf_path)

#         self.zoom = 1.5
#         self.current_page = 0

#         root = FloatLayout()

#         layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(1, 1))
#         self.image = Image()
#         layout.add_widget(self.image)

#         nav = BoxLayout(size_hint=(1, None), height=50, spacing=10)

#         self.page_input = TextInput(
#             text='1',
#             multiline=False,
#             size_hint=(None, None),
#             size=(80, 44),
#             input_filter='int'
#         )
#         go_button = Button(text="Go", size_hint=(None, None), size=(60, 44))
#         prev_button = Button(text="Previous", size_hint=(None, None), size=(100, 44))
#         next_button = Button(text="Next", size_hint=(None, None), size=(100, 44))

#         nav.add_widget(Label(text="Page:", size_hint=(None, None), size=(50, 44)))
#         nav.add_widget(self.page_input)
#         nav.add_widget(go_button)
#         nav.add_widget(prev_button)
#         nav.add_widget(next_button)

#         layout.add_widget(nav)
#         root.add_widget(layout)

#         # Back button
#         back_button = Button(
#             text='Back',
#             size_hint=(None, None),
#             size=(100, 50),
#             pos_hint={'right': 0.98, 'y': 0.02},
#             font_size=16
#         )
#         back_button.bind(on_press=self.go_back)
#         root.add_widget(back_button)

#         self.add_widget(root)

#         go_button.bind(on_press=self.go_to_logical_page)
#         prev_button.bind(on_press=self.prev_page)
#         next_button.bind(on_press=self.next_page)

#         self.load_page(self.current_page)

#     def load_page(self, page_num):
#         if 0 <= page_num < len(self.doc):
#             self.current_page = page_num
#             page = self.doc.load_page(page_num)
#             mat = fitz.Matrix(self.zoom, self.zoom)
#             pix = page.get_pixmap(matrix=mat)
#             img_data = pix.tobytes("png")
#             data = BytesIO(img_data)
#             core_img = CoreImage(data, ext="png")
#             self.image.texture = core_img.texture

#             if page_num >= self.OFFSET:
#                 logical_page = page_num - self.OFFSET + 1
#                 self.page_input.text = str(logical_page)
#             else:
#                 self.page_input.text = ""

#     def go_to_logical_page(self, instance):
#         try:
#             logical_page = int(self.page_input.text)
#             if logical_page < 1:
#                 logical_page = 1
#             pdf_page = logical_page + self.OFFSET - 1
#             if pdf_page >= len(self.doc):
#                 pdf_page = len(self.doc) - 1
#             self.load_page(pdf_page)
#         except ValueError:
#             pass

#     def next_page(self, instance):
#         if self.current_page + 1 < len(self.doc):
#             self.load_page(self.current_page + 1)

#     def prev_page(self, instance):
#         if self.current_page > 0:
#             self.load_page(self.current_page - 1)

#     def go_back(self, instance):
#         self.manager.current = 'na_readings'


# from kivy.uix.textinput import TextInput
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.core.image import Image as CoreImage
# from kivy.uix.image import Image
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.screenmanager import Screen
# from io import BytesIO
# import fitz  # PyMuPDF
# import os

# class NAStepGuideScreen(Screen):
#     OFFSET = 3  # PDF page 4 will be logical page 1

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
    
#         pdf_path = os.path.join(os.path.dirname(__file__), "PDF_files", "NA_Step_Guide.pdf")
#         self.doc = fitz.open(pdf_path)

#         self.zoom = 1.5
#         self.current_page = 0

#         root = FloatLayout()

#         layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(1, 1))
#         self.image = Image()
#         layout.add_widget(self.image)

#         nav = BoxLayout(size_hint=(1, None), height=50, spacing=10)

#         self.page_input = TextInput(
#             text='1',
#             multiline=False,
#             size_hint=(None, None),
#             size=(80, 44),
#             input_filter='int'
#         )
#         go_button = Button(text="Go", size_hint=(None, None), size=(60, 44))
#         prev_button = Button(text="Previous", size_hint=(None, None), size=(100, 44))
#         next_button = Button(text="Next", size_hint=(None, None), size=(100, 44))

#         nav.add_widget(Label(text="Page:", size_hint=(None, None), size=(50, 44)))
#         nav.add_widget(self.page_input)
#         nav.add_widget(go_button)
#         nav.add_widget(prev_button)
#         nav.add_widget(next_button)

#         layout.add_widget(nav)
#         root.add_widget(layout)

#         # Back button
#         back_button = Button(
#             text='Back',
#             size_hint=(None, None),
#             size=(100, 50),
#             pos_hint={'right': 0.98, 'y': 0.02},
#             font_size=16
#         )
#         back_button.bind(on_press=self.go_back)
#         root.add_widget(back_button)

#         self.add_widget(root)

#         # Button bindings
#         go_button.bind(on_press=self.go_to_logical_page)
#         prev_button.bind(on_press=self.prev_page)
#         next_button.bind(on_press=self.next_page)

#         self.load_page(self.current_page)

#     def load_page(self, page_num):
#         if 0 <= page_num < len(self.doc):
#             self.current_page = page_num
#             page = self.doc.load_page(page_num)
#             mat = fitz.Matrix(self.zoom, self.zoom)
#             pix = page.get_pixmap(matrix=mat)
#             img_data = pix.tobytes("png")
#             data = BytesIO(img_data)
#             core_img = CoreImage(data, ext="png")
#             self.image.texture = core_img.texture

#             if page_num >= self.OFFSET:
#                 logical_page = page_num - self.OFFSET + 1
#                 self.page_input.text = str(logical_page)
#             else:
#                 self.page_input.text = ""

#     def go_to_logical_page(self, instance):
#         try:
#             logical_page = int(self.page_input.text)
#             if logical_page < 1:
#                 logical_page = 1
#             pdf_page = logical_page + self.OFFSET - 1
#             if pdf_page >= len(self.doc):
#                 pdf_page = len(self.doc) - 1
#             self.load_page(pdf_page)
#         except ValueError:
#             pass

#     def next_page(self, instance):
#         if self.current_page + 1 < len(self.doc):
#             self.load_page(self.current_page + 1)

#     def prev_page(self, instance):
#         if self.current_page > 0:
#             self.load_page(self.current_page - 1)

#     def go_back(self, instance):
#         self.manager.current = 'na_readings'


from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.metrics import dp
from datetime import date
# import fitz  # PyMuPDF
# from io import BytesIO

class AAReadingsMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        title = Label(
            text="AA Readings",
            font_size='32sp',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        layout.add_widget(title)

        btn1 = Button(
            text="Daily Reflections Reading",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.58},
            font_size=18
        )
        btn1.bind(on_press=self.open_daily_reflections_screen)
        layout.add_widget(btn1)

        # btn2 = Button(
        #     text="AA Big Book",
        #     size_hint=(None, None),
        #     size=(300, 60),
        #     pos_hint={"center_x": 0.5, "center_y": 0.26},
        #     font_size=18
        # )
        # btn2.bind(on_press=lambda x: setattr(self.manager, 'current', 'aa_big_book'))
        # layout.add_widget(btn2)

        # btn3 = Button(
        #     text="12 Steps and 12 Traditions",
        #     size_hint=(None, None),
        #     size=(300, 60),
        #     pos_hint={"center_x": 0.5, "center_y": 0.36},
        #     font_size=18
        # )
        # btn3.bind(on_press=lambda x: setattr(self.manager, 'current', 'aa_12_steps'))
        # layout.add_widget(btn3)

        # New 24 Hours a Day button
        btn4 = Button(
            text="24 Hours a Day",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.47},  # Positioned below btn3
            font_size=18
        )
        btn4.bind(on_press=self.open_24_hours_screen)
        layout.add_widget(btn4)

        back_btn = Button(
            text="Back",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"right": 0.98, "y": 0.02},
            font_size=16
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def open_daily_reflections_screen(self, instance):
        self.manager.current = 'aa_daily_reflections'
        self.manager.get_screen('aa_daily_reflections').load_today_reading()

    def open_24_hours_screen(self, instance):
        # You can either switch to a new screen or show a popup here.
        # For example, if you have a screen named 'twenty_four_hours', do:
        self.manager.current = 'aa_24_hours_a_day'

        # If you want to load the readings now or refresh:
        screen = self.manager.get_screen('aa_24_hours_a_day')
        if hasattr(screen, 'load_today_reading'):
            screen.load_today_reading()


import os
import json
from datetime import datetime, timedelta
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import dp

class AADailyReflectionsScreen(Screen):
    def on_enter(self):
        self.current_date = datetime.today()
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        # Build absolute path to JSON file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "JSON_files", "Daily_Reflections.json")

        # Load the daily reflections JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.readings = json.load(f)
        except Exception as e:
            self.readings = {}
            print(f"Error loading Daily Reflections JSON: {e}")

        # Handle leap year for Feb 29 by showing Feb 28 reading instead
        display_date = self.current_date
        if display_date.strftime('%B %d') == "February 29":
            display_date = datetime(display_date.year, 2, 28)

        date_str = display_date.strftime('%B %d').lstrip("0").replace(" 0", " ")
        reflection_text = self.readings.get(date_str, "No reflection found for today.")

        # Main vertical layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header label
        header = Label(
            text="AA Daily Reflections",
            font_size='24sp',
            size_hint_y=None,
            height=dp(40),
            halign='center',
            valign='middle',
        )
        header.bind(size=header.setter('text_size'))
        layout.add_widget(header)

        # Scrollable reading area
        scroll = ScrollView(do_scroll_x=False)

        reading_layout = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        reading_layout.bind(minimum_height=reading_layout.setter('height'))

        reading_label = Label(
            text=f"[b]{date_str}[/b]\n\n{reflection_text}",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        reading_label.bind(texture_size=reading_label.setter('size'))
        reading_label.text_size = (self.width - dp(40), None)

        reading_layout.add_widget(reading_label)
        scroll.add_widget(reading_layout)
        layout.add_widget(scroll)

        # Bottom button bar with alignment spacers
        button_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            padding=10,
            spacing=10,
            orientation='horizontal'
        )

        prev_button = Button(
            text="Previous Reading",
            size_hint=(None, None),
            height=dp(40),
        )
        prev_button.bind(on_release=self.load_previous_reading)
        prev_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        back_button = Button(
            text="Back",
            size_hint=(None, None),
            height=dp(40),
        )
        back_button.bind(on_release=self.go_back)
        back_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        next_button = Button(
            text="Next Reading",
            size_hint=(None, None),
            height=dp(40),
        )
        next_button.bind(on_release=self.load_next_reading)
        next_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        # Add buttons and spacers for alignment
        button_bar.add_widget(prev_button)
        button_bar.add_widget(Widget())  # spacer pushes back_button to center
        button_bar.add_widget(back_button)
        button_bar.add_widget(Widget())  # spacer pushes next_button to right
        button_bar.add_widget(next_button)

        layout.add_widget(button_bar)
        self.add_widget(layout)

    def load_today_reading(self):
        self.current_date = datetime.today()
        self.build_ui()

    def load_previous_reading(self, *args):
        self.current_date -= timedelta(days=1)
        self.build_ui()

    def load_next_reading(self, *args):
        self.current_date += timedelta(days=1)
        self.build_ui()

    def go_back(self, *args):
        self.manager.current = 'aa_readings' if 'aa_readings' in self.manager.screen_names else 'home'


# import os
# import fitz
# from kivy.uix.screenmanager import Screen
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.image import Image
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput
# from kivy.core.image import Image as CoreImage
# from io import BytesIO

# class AABigBookScreen(Screen):
#     OFFSET = 22  # Page number in PDF that corresponds to logical page 1

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         pdf_path = os.path.join(os.path.dirname(__file__), "PDF_files", "AA-BigBook-4th-Edition.pdf")
#         self.doc = fitz.open(pdf_path)
#         self.zoom = 1.5
#         self.current_page = 0

#         root = FloatLayout()
#         layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(1, 1))
#         self.image = Image()
#         layout.add_widget(self.image)

#         nav = BoxLayout(size_hint=(1, None), height=50, spacing=10)
#         self.page_input = TextInput(text='1', multiline=False, size_hint=(None, None), size=(80, 44), input_filter='int')
#         go_button = Button(text="Go", size_hint=(None, None), size=(60, 44))
#         prev_button = Button(text="Previous", size_hint=(None, None), size=(100, 44))
#         next_button = Button(text="Next", size_hint=(None, None), size=(100, 44))

#         nav.add_widget(Label(text="Page:", size_hint=(None, None), size=(50, 44)))
#         nav.add_widget(self.page_input)
#         nav.add_widget(go_button)
#         nav.add_widget(prev_button)
#         nav.add_widget(next_button)

#         layout.add_widget(nav)
#         root.add_widget(layout)

#         back_button = Button(
#             text='Back',
#             size_hint=(None, None),
#             size=(100, 50),
#             pos_hint={'right': 0.98, 'y': 0.02},
#             font_size=16
#         )
#         back_button.bind(on_press=self.go_back)
#         root.add_widget(back_button)

#         self.add_widget(root)

#         go_button.bind(on_press=self.go_to_logical_page)
#         prev_button.bind(on_press=self.prev_page)
#         next_button.bind(on_press=self.next_page)

#         self.load_page(self.current_page)

#     def load_page(self, page_num):
#         if 0 <= page_num < len(self.doc):
#             self.current_page = page_num
#             page = self.doc.load_page(page_num)
#             mat = fitz.Matrix(self.zoom, self.zoom)
#             pix = page.get_pixmap(matrix=mat)
#             img_data = pix.tobytes("png")
#             data = BytesIO(img_data)
#             core_img = CoreImage(data, ext="png")
#             self.image.texture = core_img.texture

#             if page_num >= self.OFFSET:
#                 logical_page = page_num - self.OFFSET + 1
#                 self.page_input.text = str(logical_page)
#             else:
#                 self.page_input.text = ""

#     def go_to_logical_page(self, instance):
#         try:
#             logical_page = int(self.page_input.text)
#             if logical_page < 1:
#                 logical_page = 1
#             pdf_page = logical_page + self.OFFSET - 2
#             if pdf_page >= len(self.doc):
#                 pdf_page = len(self.doc) - 1
#             self.load_page(pdf_page)
#         except ValueError:
#             pass

#     def next_page(self, instance):
#         if self.current_page + 1 < len(self.doc):
#             self.load_page(self.current_page + 1)

#     def prev_page(self, instance):
#         if self.current_page > 0:
#             self.load_page(self.current_page - 1)

#     def go_back(self, instance):
#         self.manager.current = 'aa_readings'


# import os
# import fitz
# from kivy.uix.screenmanager import Screen
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.image import Image
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput
# from kivy.core.image import Image as CoreImage
# from io import BytesIO

# class AA12StepsScreen(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         pdf_path = os.path.join(os.path.dirname(__file__), "PDF_files", "AA-12-Steps-12-Traditions.pdf")
#         self.doc = fitz.open(pdf_path)
#         self.zoom = 1.5
#         self.current_page = 0

#         root = FloatLayout()
#         layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(1, 1))
#         self.image = Image()
#         layout.add_widget(self.image)

#         nav = BoxLayout(size_hint=(1, None), height=50, spacing=10)
#         self.page_input = TextInput(text='1', multiline=False, size_hint=(None, None), size=(80, 44), input_filter='int')
#         go_button = Button(text="Go", size_hint=(None, None), size=(60, 44))
#         prev_button = Button(text="Previous", size_hint=(None, None), size=(100, 44))
#         next_button = Button(text="Next", size_hint=(None, None), size=(100, 44))

#         nav.add_widget(Label(text="Page:", size_hint=(None, None), size=(50, 44)))
#         nav.add_widget(self.page_input)
#         nav.add_widget(go_button)
#         nav.add_widget(prev_button)
#         nav.add_widget(next_button)

#         layout.add_widget(nav)
#         root.add_widget(layout)

#         back_button = Button(
#             text='Back',
#             size_hint=(None, None),
#             size=(100, 50),
#             pos_hint={'right': 0.98, 'y': 0.02},
#             font_size=16
#         )
#         back_button.bind(on_press=self.go_back)
#         root.add_widget(back_button)

#         self.add_widget(root)

#         go_button.bind(on_press=self.go_to_logical_page)
#         prev_button.bind(on_press=self.prev_page)
#         next_button.bind(on_press=self.next_page)

#         self.load_page(self.current_page)

#     def load_page(self, page_num):
#         if 0 <= page_num < len(self.doc):
#             self.current_page = page_num
#             page = self.doc.load_page(page_num)
#             mat = fitz.Matrix(self.zoom, self.zoom)
#             pix = page.get_pixmap(matrix=mat)
#             img_data = pix.tobytes("png")
#             data = BytesIO(img_data)
#             core_img = CoreImage(data, ext="png")
#             self.image.texture = core_img.texture

#             # Show user-facing page number (1-indexed)
#             self.page_input.text = str(page_num + 1)

#     def go_to_logical_page(self, instance):
#         try:
#             user_page = int(self.page_input.text)
#             if user_page < 1:
#                 user_page = 1
#             pdf_page = user_page - 1  # zero-based page index directly
#             if pdf_page >= len(self.doc):
#                 pdf_page = len(self.doc) - 1
#             self.load_page(pdf_page)
#         except ValueError:
#             pass

#     def next_page(self, instance):
#         if self.current_page + 1 < len(self.doc):
#             self.load_page(self.current_page + 1)

#     def prev_page(self, instance):
#         if self.current_page > 0:
#             self.load_page(self.current_page - 1)

#     def go_back(self, instance):
#         self.manager.current = 'aa_readings'


import os
import json
from datetime import datetime, timedelta, date
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import dp

class AA24HoursaDayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.readings = {}
        self.current_date = datetime.today()
        self.reading_layout = None

    def on_enter(self):
        self.current_date = datetime.today()
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        # Absolute path for JSON file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "JSON_files", "24hoursaday.json")

        # Load the daily reflections JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.readings = json.load(f)
        except Exception as e:
            self.readings = {}
            print(f"Error loading 24 Hours a Day JSON: {e}")

        # Handle leap year for Feb 29 by showing Feb 28 reading instead
        display_date = self.current_date
        if display_date.strftime('%B %d') == "February 29":
            display_date = datetime(display_date.year, 2, 28)

        date_str = display_date.strftime('%B %d').lstrip("0").replace(" 0", " ")
        meditation_text = self.readings.get(date_str, "No meditation found for today.")

        # Main vertical layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header label
        header = Label(
            text="AA Twenty-Four Hours a Day",
            font_size='24sp',
            size_hint_y=None,
            height=dp(40),
            halign='center',
            valign='middle',
        )
        header.bind(size=header.setter('text_size'))
        layout.add_widget(header)

        # Scrollable reading area
        scroll = ScrollView(do_scroll_x=False)

        self.reading_layout = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        self.reading_layout.bind(minimum_height=self.reading_layout.setter('height'))

        reading_label = Label(
            text=f"[b]{date_str}[/b]\n\n{meditation_text}",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        reading_label.bind(texture_size=reading_label.setter('size'))
        reading_label.text_size = (self.width - dp(40), None)

        self.reading_layout.add_widget(reading_label)
        scroll.add_widget(self.reading_layout)
        layout.add_widget(scroll)

        # Bottom button bar with alignment spacers
        button_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            padding=10,
            spacing=10,
            orientation='horizontal'
        )

        prev_button = Button(
            text="Previous Reading",
            size_hint=(None, None),
            height=dp(40),
        )
        prev_button.bind(on_release=self.load_previous_reading)
        prev_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        back_button = Button(
            text="Back",
            size_hint=(None, None),
            height=dp(40),
        )
        back_button.bind(on_release=self.go_back)
        back_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        next_button = Button(
            text="Next Reading",
            size_hint=(None, None),
            height=dp(40),
        )
        next_button.bind(on_release=self.load_next_reading)
        next_button.bind(texture_size=lambda inst, size: setattr(inst, 'width', size[0] + dp(20)))

        # Add buttons and spacers for alignment
        button_bar.add_widget(prev_button)
        button_bar.add_widget(Widget())  # spacer pushes back_button to center
        button_bar.add_widget(back_button)
        button_bar.add_widget(Widget())  # spacer pushes next_button to right
        button_bar.add_widget(next_button)

        layout.add_widget(button_bar)
        self.add_widget(layout)

    def load_today_reading(self):
        if not self.reading_layout:
            self.build_ui()

        self.reading_layout.clear_widgets()

        today = date.today()
        date_str = today.strftime("%B %d").lstrip("0").replace(" 0", " ")
        meditation_text = self.readings.get(date_str, "Reading not found.")

        reading_label = Label(
            text=f"[b]{date_str}[/b]\n\n{meditation_text}",
            markup=True,
            font_size=18,
            size_hint_y=None,
            text_size=(dp(320), None)
        )
        reading_label.bind(texture_size=reading_label.setter('size'))
        self.reading_layout.add_widget(reading_label)

    def load_previous_reading(self, *args):
        self.current_date -= timedelta(days=1)
        self.build_ui()

    def load_next_reading(self, *args):
        self.current_date += timedelta(days=1)
        self.build_ui()

    def go_back(self, *args):
        self.manager.current = 'aa_readings' if 'aa_readings' in self.manager.screen_names else 'home'


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(WelcomeScreen(name="welcome"))
        self.add_widget(SetupScreen(name="setup"))
        self.add_widget(MainScreen(name="main"))
        self.add_widget(HomeScreen(name="home"))
        self.add_widget(NAReadingsMenuScreen(name="na_readings"))
        self.add_widget(AAReadingsMenuScreen(name="aa_readings"))
        self.add_widget(JustForTodayScreen(name="just_for_today"))
        self.add_widget(NABasicTextScreen(name="na_basic_text"))
        #self.add_widget(ItWorksScreen(name="it_works"))
        #self.add_widget(NAStepGuideScreen(name="na_step_guide"))
        self.add_widget(AADailyReflectionsScreen(name="aa_daily_reflections"))
        #self.add_widget(AABigBookScreen(name="aa_big_book"))
        #self.add_widget(AA12StepsScreen(name="aa_12_steps"))
        self.add_widget(AA24HoursaDayScreen(name="aa_24_hours_a_day"))
    

    def transition_to(self, screen_name):
        self.transition = SlideTransition(direction="left")
        self.current = screen_name


class CleanTimeApp(App):
    def build(self):
        self.title = "From Darkness We Climb"  # <-- Add this line

        self.sm = MyScreenManager()
        # Load user data and decide where to go:
        user_data = load_user_data()
        if user_data:
            self.sm.current = "main"
        else:
            self.sm.current = "welcome"
        return self.sm


if __name__ == "__main__":
    CleanTimeApp().run()

