import os
import time


class FileHandler:
    """
    Handles file system operations such as watching a directory for new files.
    """

    def __init__(self, dir: str):
        """
        Initializes the FileHandler with a specific directory.

        If the directory does not exist, it is created.

        Args:
            dir (str): The path to the directory to be watched.
        """
        self.dir = dir

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def watch_dir(self) -> str | None:
        """
        Monitors the directory for new files and returns the directory path.

        This method runs an infinite loop, checking for new files every second.
        When a new file is detected, it returns the
                            absolute path of the directory.

        return:
            str: The absolute directory path where the new file was found.
        """
        ficheiros_anteriores = set()
        try:
            ficheiros_anteriores = set(os.listdir(self.dir))
            while True:
                time.sleep(1)
                ficheiros_atuais = set(os.listdir(self.dir))
                novos_ficheiros = ficheiros_atuais - ficheiros_anteriores

                for ficheiro in novos_ficheiros:

                    caminho_completo = os.path.abspath(os.path.join(self.dir,
                                                                    ficheiro))
                    if caminho_completo is not None:
                        # print(f"DEBUG: {caminho_completo}")
                        return caminho_completo

                ficheiros_anteriores = ficheiros_atuais

        except KeyboardInterrupt:
            return None
