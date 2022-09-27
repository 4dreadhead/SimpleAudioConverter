import threading
import os
import pathlib
import datetime
from time import time

from PyQt6.QtWidgets import QFileDialog, QApplication
from pydub import AudioSegment

from lib import UIMainWindow


class AudioFile:
    def __init__(self, full_path, name, audio_format):
        self.full_path = full_path
        self.name = name
        self.audio_format = audio_format


class Result:
    def __init__(self, status, file_name):
        self.status = status
        self.file_name = file_name


class Converter(UIMainWindow):
    MAX_THREADS = 30

    def __init__(self):
        super().__init__()
        self.setup_ui(self)

        self.files_count = 0
        self.processed_files_count = 0
        self.parsed_files = []
        self.results = []
        self.folder_path = None
        self.mutex = threading.Lock()
        self.thread_limiter = threading.BoundedSemaphore(self.MAX_THREADS)

        self.button_convert.clicked.connect(self.create_threads)
        self.button_select_files.clicked.connect(self.parse_files_list)

        os.environ['PATH'] += str(pathlib.Path("ffmpeg/bin").resolve())

    def select_files(self):
        try:
            files, _ = QFileDialog.getOpenFileNames(self.central_widget, "Open files:")
            return files
        except Exception as error:
            self.files_browser.setPlainText(f"Error during opening files: {error}")
            return []

    def convert(self):
        self.thread_limiter.acquire()
        self.mutex.acquire()
        processing_file = self.parsed_files.pop()
        self.mutex.release()

        try:
            input_file = str(pathlib.Path(processing_file.full_path))

            audio = AudioSegment.from_file(input_file, format=processing_file.audio_format)

            full_file_path = pathlib.Path(f"{self.folder_path}/{processing_file.name}.{self.out_format.currentText()}")
            audio.export(full_file_path, format=self.out_format.currentText())

            self.mutex.acquire()
            self.results.append(Result("OK", f"{processing_file.name}.{processing_file.audio_format}"))

        except Exception:
            self.mutex.acquire()
            self.results.append(Result("FAILED", f"{processing_file.name}.{processing_file.audio_format}"))

        finally:
            self.processed_files_count += 1

            self.mutex.release()
            self.thread_limiter.release()

    def parse_files_list(self):
        files = self.select_files()
        self.parsed_files.clear()

        for selected_file in files:
            self.parsed_files.append(self.parse_file(selected_file))

        files_list_string = ""

        for parsed_file in self.parsed_files:
            files_list_string += f"{parsed_file.name}.{parsed_file.audio_format}\n"

        self.files_browser.setPlainText(files_list_string)
        self.statusbar.showMessage(f"Selected {len(self.parsed_files)} files.")

    @staticmethod
    def parse_file(unparsed_file):
        try:
            file_without_path = unparsed_file.split("/")[-1].split("\\")[-1]

            file_format = file_without_path.split(".")[-1]
            file_name = file_without_path.removesuffix(f".{file_format}")

            return AudioFile(unparsed_file, file_name, file_format)

        except Exception:
            return AudioFile(None, None, None)

    def create_threads(self):
        try:
            start_time = time()
            self.processed_files_count = 0
            self.files_count = len(self.parsed_files)
            self.folder_path = self.create_folder()
            self.results.clear()

            files_list_string = ""

            for parsed_file in self.parsed_files:
                files_list_string += f"{parsed_file.name}.{parsed_file.audio_format}\n"

            self.files_browser.setPlainText(files_list_string)

            threads = []

            for _ in range(self.files_count):
                thread = threading.Thread(target=self.convert)
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
                self.statusbar.showMessage(f"Processed {self.processed_files_count}/{self.files_count} files.")
                QApplication.processEvents()

            results_string = ""
            for result in self.results:
                results_string += f"{result.file_name}\tstatus: {result.status}\n"

            self.status_browser.setPlainText(results_string)
            self.statusbar.showMessage(f"Converting finished in {time() - start_time} seconds.")

        except Exception:
            self.statusbar.showMessage(f"Something went wrong, please try again.")

    def create_folder(self):
        folder_date = datetime.datetime.now().__str__().split(".")[0].replace(":", "-")

        filepath = pathlib.Path(f"results/converting to {self.out_format.currentText()} {folder_date}").resolve()

        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.mkdir(parents=True)

        return filepath
