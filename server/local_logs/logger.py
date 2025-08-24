import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Optional, Tuple

from config import config


class AppLogger:
    """
    Lightweight app logger with duplicate-stack suppression.

    - Use error(..., basic=True) for short one-line errors (no stack).
    - Use error(..., exc=e, once=config.DEBUG) exactly ONCE at the boundary to log full traceback.
    - Any later calls with the same exception info will be downshifted to a basic line.
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

        # very small, process-lifetime cache of already-logged exceptions
        self._seen_exc_fingerprints: set[Tuple[str, str]] = set()

    # ---- Public convenience methods ----
    def info(self, msg: Any, **kwargs) -> None:
        self._logger.info(msg, extra=kwargs or None)

    def warning(self, msg: str, **kwargs) -> None:
        self._logger.warning(msg, extra=kwargs or None)

    def error(
        self,
        msg: str,
        exc: Optional[BaseException] = None,
        *,
        once: bool = False,
        basic: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Log an error.

        - basic=True: one-line error (no stack).
        - exc and once=config.DEBUG: log full stack ONCE per (type, str(exc)); subsequent calls
          with the same fingerprint will log a short one-liner instead.
        - exc and once=False: log a short one-liner (no stack), assuming someone above
          will log the stack with once=config.DEBUG.
        """
        if basic or exc is None:
            self._logger.error(msg, exc_info=False, extra=kwargs or None)
            return

        # we have an exception
        fp = (type(exc).__name__, str(exc)[:500])

        if once:
            if fp in self._seen_exc_fingerprints:
                # already logged with stack; keep it short now
                self._logger.error(msg, exc_info=False, extra=kwargs or None)
            else:
                self._seen_exc_fingerprints.add(fp)
                # full traceback exactly once
                self._logger.exception(msg, exc_info=True, extra=kwargs or None)
        else:
            # inner layer: short line, no traceback; boundary logs stack
            self._logger.error(msg, exc_info=False, extra=kwargs or None)


logger = AppLogger()
