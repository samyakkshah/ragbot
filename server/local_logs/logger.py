import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

from config import config


class AppLogger:
    """
    Lightweight app logger.
    - Writes INFO/DEBUG to server/local_logs/app.log
    - Writes ERROR (and above) to server/local_logs/error.log
    - Also streams to stdout (handy for Docker)
    - Daily rotation, keep 7 days
    """

    def __init__(self, name: str = "eloquent", log_dir: str = "local_logs/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
        self._logger.propagate = False

        if self._logger.handlers:
            for h in list(self._logger.handlers):
                self._logger.removeHandler(h)

        fmt = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File: app.log (INFO+)
        app_handler = TimedRotatingFileHandler(
            filename=str(self.log_dir / "app.log"),
            when="D",
            interval=1,
            backupCount=7,
            encoding="utf-8",
        )
        app_handler.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
        app_handler.setFormatter(fmt)
        self._logger.addHandler(app_handler)

        # File: error.log (ERROR+)
        err_handler = TimedRotatingFileHandler(
            filename=str(self.log_dir / "error.log"),
            when="D",
            interval=1,
            backupCount=14,
            encoding="utf-8",
        )
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(fmt)
        self._logger.addHandler(err_handler)

        # Stdout
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
        console.setFormatter(fmt)
        self._logger.addHandler(console)

    # -- Public convenience methods --
    def info(self, msg: str, **kwargs) -> None:
        self._logger.info(msg, extra=kwargs or None)

    def error(self, msg: str, exc: Exception | None = None, **kwargs) -> None:
        if exc:
            self._logger.exception(msg, extra=kwargs or None)  # includes traceback
        else:
            self._logger.error(msg, extra=kwargs or None)

    # If you need raw logger (rare)
    @property
    def raw(self) -> logging.Logger:
        return self._logger


logger = AppLogger()
