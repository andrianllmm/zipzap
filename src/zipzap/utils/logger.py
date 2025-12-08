import logging

from rich.console import Console
from rich.logging import RichHandler


class Logger:
    """Convenience wrapper for colored logging."""

    COLORS = {
        "debug": "dim",
        "info": "white",
        "warning": "yellow",
        "error": "red",
        "critical": "bold red",
    }

    def __init__(self, name: str = "zipzap", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        if not self.logger.handlers:
            console_handler = RichHandler(
                console=Console(),
                markup=True,
                show_path=False,
                show_level=False,  # remove level name
                show_time=False,  # remove timestamp
            )
            console_handler.setLevel(level)
            # Formatter is ignored, RichHandler handles markup
            self.logger.addHandler(console_handler)

    def _log(self, level: str, msg: str, **kwargs):
        color = self.COLORS.get(level, "white")
        self.logger.log(
            getattr(logging, level.upper()), f"[{color}]{msg}[/{color}]", **kwargs
        )

    def debug(self, msg: str, **kwargs):
        self._log("debug", msg, **kwargs)

    def info(self, msg: str, **kwargs):
        self._log("info", msg, **kwargs)

    def warning(self, msg: str, **kwargs):
        self._log("warning", msg, **kwargs)

    def error(self, msg: str, **kwargs):
        self._log("error", msg, **kwargs)

    def critical(self, msg: str, **kwargs):
        self._log("critical", msg, **kwargs)
