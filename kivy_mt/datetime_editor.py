'''
DatetimeEditor
==============

.. versionadded:: 1.10.0

DatetimeEditor is a widget that provides a quick way to edit both
date and time. It is essentially a text input but when focused, will
open a popup where you can pick date and time interactively. At the
bottom of the popup, there is a real text input where you can manually
enter date and time in the standard format. The datetime is precised
up to second level and is represented by Python's `datetime` class.

Example::

    from kivy.base import runTouchApp
    from kivy_mt.datetime_editor import DatetimeEditor
    from datetime import datetime

    dt_editor = DatetimeEditor(
        dt=datetime.now(), # input/output datetime
        pHint=(0.8,0.4) # popup size hint
        # just for positioning in our example
        size_hint=(None, None),
        size=(100, 44),
        pos_hint={'center_x': .5, 'center_y': .5})

    def show_selected_value(dt_editor, dt):
        print('The dt_editor', spinner, 'has datetime', dt)

    dt_editor.bind(dt=show_selected_value)

    runTouchApp(dt_editor)

'''

__all__ = ('DatetimeEditor',)

from datetime import datetime

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ListProperty, ReferenceListProperty, ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy_mt.image_btn import ImageButton
from kivy_mt.calendar import CalendarWidget
from kivy_mt.circulardatetimepicker import CircularTimeWidget


# ---------- DatetimeEditorPopup ----------


Builder.load_string("""
#:import CalendarWidget      kivy_mt.calendar.CalendarWidget
#:import CircularTimeWidget  kivy_mt.circulardatetimepicker.CircularTimeWidget

<DatetimeEditorPopup@Popup>:
    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 6

            CalendarWidget:
                id: wdg_date
                size_hint_x: 1

            CircularTimeWidget:
                id: wdg_time
                size_hint_x: 1

        TextInput:
            id: wdg_text
            size_hint_y: 1
            multiline: False
            on_text_validate: root.on_text_validate()

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 1

            Button:
                id: wdg_ok
                text: "OK"
                size_hint_x: 1
                on_release: root.on_ok()

            Button:
                id: wdg_cancel
                text: "Cancel"
                size_hint_x: 1
                on_release: root.on_cancel()
""")


class DatetimeEditorPopup(Popup):

    dt = ObjectProperty(None, allownone=True)
    format = StringProperty("%Y-%m-%d %H:%M:%S")

    def __init__(self, *args, **kwargs):
        super(DatetimeEditorPopup, self).__init__(*args, **kwargs)

        self.old_dt = self.dt

        if not self.dt:
            self.dt = datetime.now()

        self.ids.wdg_date.active_date = [self.dt.day, self.dt.month, self.dt.year]
        self.ids.wdg_time.time = self.dt.time()
        self.ids.wdg_text.text = self.dt.strftime(self.format)

        self.ids.wdg_date.bind(active_date=self.on_update_text_date)
        self.ids.wdg_time.bind(time=self.on_update_text_time)

    def on_text_validate(self):
        '''Handles the case when the new text needs validation.'''
        try:
            dt = datetime.strptime(self.ids.wdg_text.text, self.format)
            if self.ids.wdg_date.active_date != [dt.day, dt.month, dt.year]:
                self.ids.wdg_date.active_date = [dt.day, dt.month, dt.year]
            if self.ids.wdg_time.time != dt.time():
                self.ids.wdg_time.time = dt.time()
            self.dt = dt
        except:
            return

    def on_update_text_date(self, instance, value):
        '''Handles the case when the date widget has a new date.'''
        self.dt = datetime(value[2], value[1], value[0], self.dt.hour, self.dt.minute, self.dt.second)
        self.ids.wdg_text.text = self.dt.strftime(self.format)

    def on_update_text_time(self, instance, value):
        '''Handles the case when the time widget has a new time.'''
        self.dt = datetime(self.dt.year, self.dt.month, self.dt.day, value.hour, value.minute, value.second)
        self.ids.wdg_text.text = self.dt.strftime(self.format)

    def on_ok(self):
        '''Handles the case when the user clicks OK.'''
        self.on_text_validate()
        print("ok",self.dt)
        self.dismiss()

    def on_cancel(self):
        '''Handles the case when the user clicks Cancel.'''
        self.dt = self.old_dt
        print("cancel",self.dt)
        self.dismiss()


# ---------- DatetimeEditor ----------


class DatetimeEditor(TextInput):
    """A TextInput but when focused, shows popup with a CalendarWidget and
    a CircularTimeWidget and a text input to enter date and time. You can
    define the popup dimensions using  pHint_x, pHint_y, and the pHint lists. 
    The `format` property formats the date and time to string using strftime() 
    and strptime(). The `dt` property can be used to initialise date and time.
    It is an ObjectProperty holding a Python datetime object.

    For example in kv:
    DatetimeEditor:
        dt: datetime(2017, 3, 2, 11, 22, 33)
        pHint: 0.7,0.4
        format: "%H:%M:%S"
    would result in a size_hint of 0.7,0.4 being used to create the popup
    """

    # ----- properties -----

    dt = ObjectProperty(None, allownone=True)
    '''Datetime that can be edited by the user. Must be None or of class datetime.

    :attr:`dt` is a :class:`~kivy.properties.ObjectProperty` and defaults to None.
    '''

    pHint_x = NumericProperty(0.8)
    pHint_y = NumericProperty(0.6)
    pHint = ReferenceListProperty(pHint_x ,pHint_y)

    format = StringProperty("%Y-%m-%d %H:%M:%S")

    # ----- initialisation -----

    def __init__(self, *args, **kwargs):
        super(CircularTimePicker, self).__init__(*args, **kwargs)

        self.init_ui()

    def init_ui(self):

        if not self.dt:
            self.dt = datetime.datetime.now()

        # CircularTimeWidget
        self.ctw = CircularTimeWidget()

        # Popup
        self.popup = Popup(content=self.ctw, on_dismiss=self.update_value, title="")
        self.ctw.parent_popup = self.popup

        self.bind(focus=self.show_popup)

    def show_popup(self, isnt, val):
        """
        Open popup if textinput focused,
        and regardless update the popup size_hint
        """
        self.popup.size_hint=self.pHint
        if val:
            # Automatically dismiss the keyboard
            # that results from the textInput
            Window.release_all_keyboards()
            self.ctw.time = datetime.datetime.strptime(self.text, self.format)
            self.popup.open()

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = self.ctw.time.strftime(self.format)
        self.focus = False


Factory.register("DatetimeEditor", cls=DatetimeEditor)

