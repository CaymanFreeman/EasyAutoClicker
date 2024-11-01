import locale
import os
from configparser import ConfigParser
from os.path import isfile

import customtkinter

ROOT_PATH = os.path.abspath("")
CONFIG_PATH = os.path.join(ROOT_PATH, "config.ini")
THEME_PATH = os.path.join(ROOT_PATH, "assets", "easy_auto_clicker_theme.json")
LANGUAGES_PATH = os.path.join(ROOT_PATH, "assets", "languages")
ICON_PATH = os.path.join(ROOT_PATH, "assets", "icon.ico")


class ConfigHandler:

    @staticmethod
    def save_config_and_exit(app: customtkinter.CTk) -> None:
        config = ConfigParser()

        config["LANGUAGE"] = {}
        config["APPEARANCE"] = {}
        config["HOTKEY"] = {}
        config["CLICK_PROCESS"] = {}
        config["LOCATION"] = {}
        config["INPUT_VALIDATION"] = {}

        config["LANGUAGE"]["LANGUAGE_CODE"] = app.getvar(name="LANGUAGE_CODE")

        config["APPEARANCE"]["APPEARANCE_MODE"] = customtkinter.get_appearance_mode()
        config["APPEARANCE"]["FRAME_PADDING"] = app.getvar(name="FRAME_PADDING")
        config["APPEARANCE"]["ITEM_PADDING"] = app.getvar(name="ITEM_PADDING")
        config["APPEARANCE"]["RESIZABLE_WIDTH"] = app.getvar(name="RESIZABLE_WIDTH")
        config["APPEARANCE"]["RESIZABLE_HEIGHT"] = app.getvar(name="RESIZABLE_HEIGHT")

        config["HOTKEY"]["HOTKEY"] = app.getvar(name="HOTKEY")

        config["CLICK_PROCESS"]["CLICK_EVENTS"] = app.getvar(name="CLICK_EVENTS")
        config["CLICK_PROCESS"]["CLICKS_PER_EVENT"] = app.getvar(
            name="CLICKS_PER_EVENT"
        )
        config["CLICK_PROCESS"]["CLICK_INTERVAL"] = app.getvar(name="CLICK_INTERVAL")
        config["CLICK_PROCESS"]["CLICK_INTERVAL_SCALE"] = app.getvar(
            name="CLICK_INTERVAL_SCALE"
        )
        config["CLICK_PROCESS"]["CLICK_LENGTH"] = app.getvar(name="CLICK_LENGTH")
        config["CLICK_PROCESS"]["CLICK_LENGTH_SCALE"] = app.getvar(
            name="CLICK_LENGTH_SCALE"
        )
        config["CLICK_PROCESS"]["MOUSE_BUTTON"] = app.getvar(name="MOUSE_BUTTON")
        config["CLICK_PROCESS"]["CLICK_LOCATION"] = app.getvar(name="CLICK_LOCATION")

        config["LOCATION"]["CANCEL_LOCATION_PICK_KEY"] = app.getvar(
            name="CANCEL_LOCATION_PICK_KEY"
        )
        config["LOCATION"]["LOCATION_UPDATE_INTERVAL_SECONDS"] = app.getvar(
            name="LOCATION_UPDATE_INTERVAL_SECONDS"
        )

        config["INPUT_VALIDATION"]["MAX_HOTKEY_KEYS"] = app.getvar(
            name="MAX_HOTKEY_KEYS"
        )
        config["INPUT_VALIDATION"]["MAX_CLICK_EVENTS_DIGITS"] = app.getvar(
            name="MAX_CLICK_EVENTS_DIGITS"
        )
        config["INPUT_VALIDATION"]["MAX_CLICKS_PER_EVENT_DIGITS"] = app.getvar(
            name="MAX_CLICKS_PER_EVENT_DIGITS"
        )
        config["INPUT_VALIDATION"]["MAX_CLICK_INTERVAL_DIGITS"] = app.getvar(
            name="MAX_CLICK_INTERVAL_DIGITS"
        )
        config["INPUT_VALIDATION"]["MIN_CLICK_INTERVAL"] = app.getvar(
            name="MIN_CLICK_INTERVAL"
        )

        try:
            with open(CONFIG_PATH, "w") as file:
                config.write(file)
        except Exception as error:
            print(f"Can't write config: {error}")
        finally:
            app.quit()
            app.destroy()
            exit(0)

    @staticmethod
    def read_config_values(app: customtkinter.CTk) -> None:
        config = ConfigParser()
        config.read(CONFIG_PATH)
        for section in config.sections():
            for name, value in config.items(section):
                if (
                    section.upper() == "LANGUAGE"
                    and name.upper() == "LANGUAGE_CODE"
                    and value == "system"
                ):
                    value = locale.getdefaultlocale()[0].lower().replace("-", "_")
                app.setvar(name.upper(), value)

    @staticmethod
    def read_config(app: customtkinter.CTk) -> None:
        try:
            ConfigHandler.read_config_values(app)
        except FileNotFoundError:
            try:
                ConfigHandler.create_defaults()
                ConfigHandler.read_config_values(app)
            except Exception as error:
                print(f"Could not read config: {error}")
                exit(0)
        except Exception as error:
            print(f"Could not read config and default could not be created: {error}")
            exit(0)

    @staticmethod
    def create_defaults() -> None:
        if isfile(CONFIG_PATH):
            return

        default_config = ConfigParser()

        default_config["LANGUAGE"] = {"LANGUAGE_CODE": "system"}

        default_config["APPEARANCE"] = {
            "APPEARANCE_MODE": "Dark",
            "FRAME_PADDING": "3",
            "ITEM_PADDING": "5",
            "RESIZABLE_WIDTH": "False",
            "RESIZABLE_HEIGHT": "False",
        }

        default_config["HOTKEY"] = {"HOTKEY": "ctrl+f8"}

        default_config["CLICK_PROCESS"] = {
            "CLICK_EVENTS": "0",
            "CLICKS_PER_EVENT": "1",
            "CLICK_INTERVAL": "100",
            "CLICK_INTERVAL_SCALE": "1",
            "CLICK_LENGTH": "0",
            "CLICK_LENGTH_SCALE": "1",
            "MOUSE_BUTTON": "1",
            "CLICK_LOCATION": "none",
        }

        default_config["LOCATION"] = {
            "CANCEL_LOCATION_PICK_KEY": "escape",
            "LOCATION_UPDATE_INTERVAL_SECONDS": "0.05",
        }

        default_config["INPUT_VALIDATION"] = {
            "MAX_HOTKEY_KEYS": "3",
            "MAX_CLICK_EVENTS_DIGITS": "6",
            "MAX_CLICKS_PER_EVENT_DIGITS": "3",
            "MAX_CLICK_INTERVAL_DIGITS": "6",
            "MIN_CLICK_INTERVAL": "0",
        }

        with open(CONFIG_PATH, "w") as file:
            try:
                default_config.write(file)
            except Exception as error:
                print(f"Can't write config: {error}")
