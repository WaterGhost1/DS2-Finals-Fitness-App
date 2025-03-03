"""This module contains the custom Activity Dialog class."""

# pylint: disable=no-name-in-module
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.material_resources import DEVICE_TYPE
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import BaseDialog


class ActivityDialog(BaseDialog):
    """Custom Dialog for picking a new activity."""

    current_activity = StringProperty("Sedentary")

    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.view = view
        self.selected_activity = self.current_activity
        self.radius = [dp(10), dp(10), dp(10), dp(10)]
        self.size_hint = (None, None)

        # adjust the width according to the device
        if DEVICE_TYPE in ("desktop", "tablet"):
            self.width = min(dp(560), Window.width - dp(50))
        elif DEVICE_TYPE == "mobile":
            self.width = min(dp(280), Window.width - dp(50))

    def on_pre_open(self):
        """Called before opening the dialog."""
        for activity_item in self.ids.activity_items.children:
            if (
                isinstance(activity_item, ActivityItem)
                and activity_item.activity_type == self.current_activity
            ):
                activity_item.ids.checkbox.active = True

    def _on_confirm_selection(self):
        self.dismiss()
        self.current_activity = self.selected_activity
        self.view.controller.update_all_calorie_goal(self.current_activity)


class ActivityItem(MDBoxLayout):
    """Activity Dialog checkbox items."""

    activity_type = StringProperty()
    description = StringProperty()

    def _on_active(self, instance_checkbox, value: bool):
        """Called when an `ActivityItem` checkbox is clicked."""
        if value:
            self.ids.description.opacity = 1.0
            self.ids.description.height = self.ids.description.texture_size[1]
            self.parent.selected_activity = self.activity_type
        else:
            self.ids.description.opacity = 0.0
            self.ids.description.height = 0
        instance_checkbox.disabled = value
