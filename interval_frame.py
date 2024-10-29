import tkinter

import customtkinter

from integer_entry import IntegerEntry
from label_variables import LabelVariables, detranslate_scale, translate_scale


class ClickIntervalFrame(customtkinter.CTkFrame):

    def __init__(self, master: customtkinter.CTk, label_variables: LabelVariables):
        super().__init__(master)
        self.label_variables = label_variables

        item_padding = master.getvar(name="ITEM_PADDING")

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.interval_label = customtkinter.CTkLabel(self, text=label_variables.CLICK_INTERVAL_LABEL)
        self.interval_label.grid(row=0, column=0, padx=item_padding, pady=item_padding, sticky="ew")

        self.interval_entry = IntegerEntry(self, variable_name="CLICK_INTERVAL", max_length=master.getvar(name="MAX_CLICK_INTERVAL_DIGITS"),
                                           min_value=master.getvar(name="MIN_CLICK_INTERVAL"))
        self.interval_entry.grid(row=0, column=1, padx=item_padding, pady=item_padding, sticky="ew")

        self.interval_timescale_dropdown = (customtkinter.CTkOptionMenu(self, values=[label_variables.MILLISECONDS_CHOICE, label_variables.SECONDS_CHOICE, label_variables.MINUTES_CHOICE, label_variables.HOURS_CHOICE], command=self.interval_timescale_callback))
        self.interval_timescale_dropdown.configure(variable=tkinter.StringVar(value=translate_scale(label_variables=label_variables, scale=master.getvar(name="CLICK_INTERVAL_SCALE"))))
        self.interval_timescale_dropdown.grid(row=0, column=2, padx=item_padding, pady=item_padding, sticky="ew")

    def interval_timescale_callback(self, option_value: str) -> None:
        self.master.setvar(name="CLICK_INTERVAL_SCALE", value=detranslate_scale(label_variables=self.label_variables, scale=option_value))
