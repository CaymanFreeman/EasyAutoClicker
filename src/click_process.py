import time
from dataclasses import dataclass
from multiprocessing import Process, Event
from typing import Optional, Tuple, List

from pynput.mouse import Button


@dataclass
class ClickProcessInputs:
    is_advanced: bool = False
    click_interval: int = 100
    click_interval_scale_index: int = 0
    click_length: int = 0
    click_length_scale_index: int = 0
    clicks_per_event: int = 1
    click_events: Optional[int] = None
    click_location: Optional[Tuple[int, int]] = None
    mouse_button_index: int = 0

    @staticmethod
    def timescale_from_index(index: int) -> float:
        match index:
            case 0:  # Milliseconds
                return 0.001
            case 1:  # Seconds
                return 1.0
            case 2:  # Minutes
                return 60.0
            case 3:  # Hours
                return 3600.0

    @property
    def click_interval_scale(self) -> float:
        return self.timescale_from_index(self.click_interval_scale_index)

    @property
    def click_length_scale(self) -> float:
        return self.timescale_from_index(self.click_length_scale_index)

    @property
    def scaled_click_interval(self) -> float:
        return self.click_interval * self.click_interval_scale

    @property
    def scaled_click_length(self) -> float:
        return self.click_length * self.click_length_scale

    @property
    def has_location(self) -> bool:
        return self.click_location is not None

    @property
    def location_x(self) -> int:
        return self.click_location[0] if self.has_location else None

    @property
    def location_y(self) -> int:
        return self.click_location[1] if self.has_location else None

    @property
    def mouse_button_str(self):
        match self.mouse_button_index:
            case 0:
                return Button.left
            case 1:
                return Button.right
            case 2:
                return Button.middle


class ClickProcess:

    _active_processes: List[Process] = []

    def __init__(self, inputs: ClickProcessInputs, logger, mouse_controller):
        self.logger = logger
        self.mouse_controller = mouse_controller
        self.click_interval = inputs.scaled_click_interval
        self.mouse_button = inputs.mouse_button_str
        self.location_x = inputs.location_x
        self.location_y = inputs.location_y
        self.finished = Event()

    @classmethod
    def get_appropriate(cls, inputs: ClickProcessInputs, logger, mouse_controller):
        return (
            AdvancedClickProcess(inputs, logger, mouse_controller)
            if inputs.is_advanced
            else cls(inputs, logger, mouse_controller)
        )

    @classmethod
    def terminate_all(cls, logger):
        if len(cls._active_processes) == 0:
            return
        for process in cls._active_processes:
            try:
                if process.is_alive():
                    logger.info(f"Terminating process {process.pid}")
                    process.terminate()
            except Exception as e:
                logger.error("Error while terminating process: %s", e)
        logger.info("Terminated all click processes")
        cls._active_processes.clear()

    def start_process_str(self, pid: int):
        if isinstance(self, AdvancedClickProcess):
            return (
                f"Started advanced click process with PID {pid}:"
                f" click_interval={self.click_interval}s"
                f" mouse_button={self.mouse_button}"
                f" location={f"({self.location_x}, {self.location_y})" if self.location_x is not None and self.location_y is not None else None}"
                f" click_length={self.click_length}"
                f" clicks_per_event={self.clicks_per_event}"
                f" click_events={self.click_events}"
            )
        else:
            return (
                f"Started click process with PID {pid}:"
                f" click_interval={self.click_interval}s"
                f" mouse_button={self.mouse_button}"
                f" location={f"({self.location_x}, {self.location_y})" if self.location_x is not None and self.location_y is not None else None}"
            )

    def start(self) -> Process:
        process_type = (
            self.location_click_process
            if self.location_x is not None and self.location_y is not None
            else self.click_process
        )
        process = Process(target=process_type, daemon=True)
        self.__class__._active_processes.append(process)
        process.start()
        self.logger.info(self.start_process_str(process.pid))
        return process

    def click_process(self) -> None:
        while True:
            self.run_click_event()

    def location_click_process(self) -> None:
        while True:
            self.mouse_controller.position = (self.location_x, self.location_y)
            self.run_click_event()

    def run_click_event(self) -> None:
        start_time = time.perf_counter()
        next_click_time = start_time + self.click_interval
        self.mouse_controller.click(self.mouse_button)
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)


class AdvancedClickProcess(ClickProcess):

    def __init__(self, inputs: ClickProcessInputs, logger, mouse_controller):
        super().__init__(inputs, logger, mouse_controller)
        self.click_length = inputs.scaled_click_length
        self.clicks_per_event = inputs.clicks_per_event
        self.click_events = inputs.click_events

    def click_process(self) -> None:
        click_event = (
            self.run_held_click_event if self.click_length > 0 else self.run_click_event
        )

        if self.click_events is None:
            while True:
                click_event()
        else:
            for _ in range(self.click_events):
                click_event()
            self.finished.set()

    def location_click_process(self) -> None:
        click_event = (
            self.run_held_click_event if self.click_length > 0 else self.run_click_event
        )

        if self.click_events is None:
            while True:
                self.mouse_controller.position = (self.location_x, self.location_y)
                click_event()
        else:
            for _ in range(self.click_events):
                self.mouse_controller.position = (self.location_x, self.location_y)
                click_event()
            self.finished.set()

    def run_click_event(self) -> None:
        start_time = time.perf_counter()
        next_click_time = start_time + self.click_interval
        for _ in range(self.clicks_per_event):
            self.mouse_controller.click(self.mouse_button)
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)

    def run_held_click_event(self) -> None:
        start_time = time.perf_counter()
        next_click_time = start_time + self.click_interval
        self.mouse_controller.press(self.mouse_button)
        time.sleep(self.click_length)
        self.mouse_controller.release(self.mouse_button)
        remaining_time = max(0.0, next_click_time - time.perf_counter())
        if remaining_time > 0:
            time.sleep(remaining_time)
