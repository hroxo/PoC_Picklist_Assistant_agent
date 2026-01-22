import os
import time
from typing import Optional


class FileService:
    """
    Service for monitoring file system events.
    """

    def __init__(self, directory: str):
        """
        Initializes the service with a directory to watch.

        Args:
            directory: Path to the directory.
        """
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def watch_for_new_file(self) -> Optional[str]:
        """
        Blocks until a new file appears in the directory.

        Returns:
            The full path of the new file, or None if interrupted.
        """
        previous_files = set()
        try:
            if os.path.exists(self.directory):
                previous_files = set(os.listdir(self.directory))

            while True:
                time.sleep(1)
                current_files = set(os.listdir(self.directory))
                new_files = current_files - previous_files

                for file_name in new_files:
                    full_path = os.path.abspath(os.path.join(self.directory,
                                                             file_name))
                    if os.path.isfile(full_path):
                        return full_path

                previous_files = current_files

        except KeyboardInterrupt:
            return None
