import sqlite3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle


DATABASE_NAME = "students.db"


# =========================================================
# DATABASE
# =========================================================

def initialize_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            branch TEXT,
            semester INTEGER,
            phone TEXT
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# MODERN BUTTON
# =========================================================

class ModernButton(Button):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:

            Color(0.12, 0.16, 0.22, 1)

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[12]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(self, *args):

        self.rect.pos = self.pos
        self.rect.size = self.size


# =========================================================
# MAIN APPLICATION
# =========================================================

class StudentManagementApp(App):

    def build(self):

        initialize_database()

        # -------------------------------------------------
        # MAIN LAYOUT
        # -------------------------------------------------

        self.main_layout = BoxLayout(
            orientation="horizontal",
            padding=15,
            spacing=15
        )

        with self.main_layout.canvas.before:

            Color(0.04, 0.06, 0.09, 1)

            self.background = RoundedRectangle(
                pos=self.main_layout.pos,
                size=self.main_layout.size
            )

        self.main_layout.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # =================================================
        # SIDEBAR
        # =================================================

        sidebar = BoxLayout(
            orientation="vertical",
            size_hint_x=0.25,
            spacing=10,
            padding=10
        )

        with sidebar.canvas.before:

            Color(0.07, 0.09, 0.13, 1)

            self.sidebar_rect = RoundedRectangle(
                pos=sidebar.pos,
                size=sidebar.size,
                radius=[18]
            )

        sidebar.bind(
            pos=lambda instance, value:
            setattr(self.sidebar_rect, "pos", value),

            size=lambda instance, value:
            setattr(self.sidebar_rect, "size", value)
        )

        logo = Label(
            text="[b]STUDENT[/b]\n[b]MANAGER[/b]",
            markup=True,
            font_size=22,
            size_hint_y=None,
            height=90
        )

        sidebar.add_widget(logo)

        dashboard_button = ModernButton(
            text="Dashboard",
            font_size=17,
            size_hint_y=None,
            height=55
        )

        add_button = ModernButton(
            text="+   Add Student",
            font_size=17,
            size_hint_y=None,
            height=55
        )

        view_button = ModernButton(
            text="Students",
            font_size=17,
            size_hint_y=None,
            height=55
        )

        search_button = ModernButton(
            text="Search",
            font_size=17,
            size_hint_y=None,
            height=55
        )

        edit_button = ModernButton(
            text="Edit Student",
            font_size=17,
            size_hint_y=None,
            height=55
        )

        delete_button = ModernButton(
            text="Delete Student",
            font_size=17,
            size_hint_y=None,
            height=55
        )

        sidebar.add_widget(dashboard_button)
        sidebar.add_widget(add_button)
        sidebar.add_widget(view_button)
        sidebar.add_widget(search_button)
        sidebar.add_widget(edit_button)
        sidebar.add_widget(delete_button)

        sidebar.add_widget(Label())

        footer = Label(
            text="Student Management\nSystem v1.0",
            font_size=12,
            size_hint_y=None,
            height=60
        )

        sidebar.add_widget(footer)

        # =================================================
        # CONTENT
        # =================================================

        content = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=10
        )

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=90
        )

        title = Label(
            text="[b]Dashboard[/b]",
            markup=True,
            font_size=30
        )

        subtitle = Label(
            text="Manage your students efficiently",
            font_size=15,
            color=(0.6, 0.65, 0.72, 1)
        )

        header.add_widget(title)
        header.add_widget(subtitle)

        content.add_widget(header)

        # =================================================
        # DASHBOARD CARDS
        # =================================================

        cards = GridLayout(
            cols=3,
            spacing=15,
            size_hint_y=None,
            height=130
        )

        total_students = self.get_student_count()

        cards.add_widget(
            self.create_card(
                "TOTAL STUDENTS",
                str(total_students),
                ""
            )
        )

        cards.add_widget(
            self.create_card(
                "ACTIVE RECORDS",
                str(total_students),
                ""
            )
        )

        cards.add_widget(
            self.create_card(
                "SYSTEM",
                "ONLINE",
                ""
            )
        )

        content.add_widget(cards)

        # =================================================
        # QUICK ACTIONS
        # =================================================

        quick_title = Label(
            text="[b]Quick Actions[/b]",
            markup=True,
            font_size=21,
            size_hint_y=None,
            height=50
        )

        content.add_widget(quick_title)

        actions = GridLayout(
            cols=2,
            spacing=15,
            size_hint_y=None,
            height=90
        )

        quick_add = ModernButton(
            text="+   ADD NEW STUDENT",
            font_size=18,
            size_hint_y=None,
            height=70
        )

        quick_view = ModernButton(
            text="VIEW STUDENTS",
            font_size=18,
            size_hint_y=None,
            height=70
        )

        actions.add_widget(quick_add)
        actions.add_widget(quick_view)

        content.add_widget(actions)

        # =================================================
        # BUTTON EVENTS
        # =================================================

        add_button.bind(
            on_press=self.show_add_student
        )

        quick_add.bind(
            on_press=self.show_add_student
        )

        view_button.bind(
            on_press=self.show_students
        )

        quick_view.bind(
            on_press=self.show_students
        )

        # =================================================
        # ADD TO MAIN LAYOUT
        # =================================================

        self.main_layout.add_widget(sidebar)
        self.main_layout.add_widget(content)

        return self.main_layout

    # =====================================================
    # BACKGROUND
    # =====================================================

    def update_background(self, instance, value):

        self.background.pos = instance.pos
        self.background.size = instance.size

    # =====================================================
    # DASHBOARD CARD
    # =====================================================

    def create_card(self, title, value, icon):

        card = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=5
        )

        with card.canvas.before:

            Color(0.08, 0.11, 0.16, 1)

            card_rect = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[15]
            )

        card.bind(
            pos=lambda instance, value:
            setattr(card_rect, "pos", value),

            size=lambda instance, value:
            setattr(card_rect, "size", value)
        )

        top = Label(
            text=title,
            font_size=13,
            color=(0.6, 0.65, 0.72, 1)
        )

        number = Label(
            text="[b]" + value + "[/b]",
            markup=True,
            font_size=28
        )

        card.add_widget(top)
        card.add_widget(number)

        return card

    # =====================================================
    # DATABASE COUNT
    # =====================================================

    def get_student_count(self):

        connection = sqlite3.connect(DATABASE_NAME)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        count = cursor.fetchone()[0]

        connection.close()

        return count

    # =====================================================
    # ADD STUDENT
    # =====================================================

    def show_add_student(self, instance):

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20
        )

        student_id = TextInput(
            hint_text="Student ID",
            multiline=False,
            font_size=16,
            size_hint_y=None,
            height=50
        )

        name = TextInput(
            hint_text="Student Name",
            multiline=False,
            font_size=16,
            size_hint_y=None,
            height=50
        )

        branch = TextInput(
            hint_text="Branch",
            multiline=False,
            font_size=16,
            size_hint_y=None,
            height=50
        )

        semester = TextInput(
            hint_text="Semester",
            multiline=False,
            input_filter="int",
            font_size=16,
            size_hint_y=None,
            height=50
        )

        phone = TextInput(
            hint_text="Phone Number",
            multiline=False,
            font_size=16,
            size_hint_y=None,
            height=50
        )

        save_button = ModernButton(
            text="SAVE STUDENT",
            font_size=17,
            size_hint_y=None,
            height=52
        )

        layout.add_widget(student_id)
        layout.add_widget(name)
        layout.add_widget(branch)
        layout.add_widget(semester)
        layout.add_widget(phone)
        layout.add_widget(save_button)

        popup = Popup(
            title="Add New Student",
            content=layout,
            size_hint=(0.85, 0.65)
        )

        save_button.bind(
            on_press=lambda instance:
            self.save_student(
                student_id.text,
                name.text,
                branch.text,
                semester.text,
                phone.text,
                popup
            )
        )

        popup.open()

    # =====================================================
    # SAVE STUDENT
    # =====================================================

    def save_student(
        self,
        student_id,
        name,
        branch,
        semester,
        phone,
        popup
    ):

        if not student_id or not name:

            self.show_message(
                "Error",
                "Student ID and Name are required."
            )

            return

        try:

            connection = sqlite3.connect(
                DATABASE_NAME
            )

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO students
                (student_id, name, branch, semester, phone)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student_id,
                name,
                branch,
                semester if semester else None,
                phone
            ))

            connection.commit()
            connection.close()

            popup.dismiss()

            self.show_message(
                "Success",
                "Student added successfully!"
            )

        except sqlite3.IntegrityError:

            self.show_message(
                "Error",
                "Student ID already exists."
            )

    # =====================================================
    # VIEW STUDENTS
    # =====================================================

    def show_students(self, instance):

        connection = sqlite3.connect(
            DATABASE_NAME
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id, name, branch, semester, phone
            FROM students
            ORDER BY id DESC
        """)

        students = cursor.fetchall()

        connection.close()

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=15
        )

        title = Label(
            text="[b]REGISTERED STUDENTS[/b]",
            markup=True,
            font_size=21,
            size_hint_y=None,
            height=45
        )

        layout.add_widget(title)

        scroll = ScrollView(
            do_scroll_x=True,
            do_scroll_y=True
        )

        table = GridLayout(
            cols=5,
            spacing=2,
            padding=5,
            size_hint_y=None,
            size_hint_x=None
        )

        table.bind(
            minimum_height=table.setter("height")
        )

        table.width = 700

        headers = [
            "Student ID",
            "Name",
            "Branch",
            "Semester",
            "Phone"
        ]

        for text in headers:

            label = Label(
                text="[b]" + text + "[/b]",
                markup=True,
                font_size=13,
                size_hint=(None, None),
                width=140,
                height=45
            )

            table.add_widget(label)

        for student in students:

            values = [
                str(student[0]),
                str(student[1]),
                str(student[2] or "-"),
                str(student[3] or "-"),
                str(student[4] or "-")
            ]

            for value in values:

                label = Label(
                    text=value,
                    font_size=13,
                    size_hint=(None, None),
                    width=140,
                    height=45
                )

                table.add_widget(label)

        if not students:

            empty = Label(
                text="No students registered yet.",
                font_size=16,
                size_hint=(None, None),
                width=700,
                height=60
            )

            table.add_widget(empty)

        scroll.add_widget(table)

        layout.add_widget(scroll)

        close_button = ModernButton(
            text="CLOSE",
            font_size=16,
            size_hint_y=None,
            height=50
        )

        layout.add_widget(close_button)

        popup = Popup(
            title="Students",
            content=layout,
            size_hint=(0.95, 0.8)
        )

        close_button.bind(
            on_press=popup.dismiss
        )

        popup.open()

    # =====================================================
    # MESSAGE
    # =====================================================

    def show_message(self, title, message):

        popup = Popup(
            title=title,
            content=Label(
                text=message,
                font_size=17
            ),
            size_hint=(0.75, 0.3)
        )

        popup.open()


# =========================================================
# START APP
# =========================================================

if __name__ == "__main__":

    StudentManagementApp().run()