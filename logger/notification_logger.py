# logger/notification_logger.py

import os
import datetime


class NotificationLogger:
    """
    File-based logger that writes every notification event to a .log file.
    Used alongside the Singleton NotificationManager (which holds in-memory logs).
    This class is responsible for persistence — writing logs to disk.

    The Singleton manager calls this after logging to its internal list,
    so both in-memory and on-disk records stay in sync.
    """

    def __init__(self, log_dir: str = "logs") -> None:
        self._log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        date_str      = datetime.datetime.now().strftime("%Y-%m-%d")
        self._log_path = os.path.join(log_dir, f"notifications_{date_str}.log")
        self._write_header()

    def _write_header(self) -> None:
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(
                f"\n{'='*70}\n"
                f"  Notification Log — Session started "
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"{'='*70}\n"
            )

    def write(self, event_type: str, channel: str,
              recipient: str, message: str, status: str) -> None:
        """Append one log entry to the log file."""
        ts    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line  = (
            f"[{ts}]  {status:8}  |  {channel:10}  →  "
            f"{recipient:35}  |  {event_type}  |  {message[:60]}\n"
        )
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(line)

    def get_log_path(self) -> str:
        return self._log_path
