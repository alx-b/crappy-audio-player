#!/usr/bin/env python3
import threading
import time

import py_cui

import audio


class PlayerTUI:
    def __init__(self, root: py_cui.PyCUI):
        self.root = root
        self.artist_menu = self._init_artist_menu()
        self.current_audio_label = self._init_current_audio_label()
        self.status_label = self._init_status_label()
        self.playtime_label = self._init_playtime_label()
        self._get_playlist()
        self._init_global_keybindings()
        self.thread_is_alive = False
        self.thread1 = threading.Thread(
            target=self.loop_play_audio_files,
            args=[self.artist_menu.get_selected_item_index()],
        )

    def _init_global_keybindings(self) -> None:
        self.root.add_key_command(py_cui.keys.KEY_P_LOWER, self.toggle_pause_audio_file)

    def _init_artist_menu(self) -> py_cui.widgets.ScrollMenu:
        menu = self.root.add_scroll_menu("Artists", 0, 0, row_span=8, column_span=8)
        menu.add_key_command(py_cui.keys.KEY_ENTER, self.play_selected_audio_file)
        menu.add_key_command(py_cui.keys.KEY_P_LOWER, self.toggle_pause_audio_file)
        return menu

    def _init_current_audio_label(self) -> py_cui.widgets.Label:
        current_audio = self.root.add_label("", 8, 1, column_span=6)
        current_audio.toggle_border()
        return current_audio

    def _init_status_label(self) -> py_cui.widgets.Label:
        label = self.root.add_label("", 8, 0, column_span=1)
        label.toggle_border()
        return label

    def _init_playtime_label(self) -> py_cui.widgets.Label:
        label = self.root.add_label("", 8, 7, column_span=1)
        label.toggle_border()
        return label

    # !! might put this in init_artist_menu instead !!
    def _get_playlist(self) -> None:
        self.artist_menu.add_item_list(audio.get_supported_audio_files())

    def play_selected_audio_file(self) -> None:
        song = audio.play_audio(self.artist_menu.get())
        self.current_audio_label._title = str(song)
        self.playtime_label._title = audio.get_audio_length(song)
        # self.current_audio_label._title = audio.play_audio(self.artist_menu.get())
        self.status_label._title = "[PLAYING]"
        if self.thread1.is_alive():
            self.kill_thread()
        self.create_and_start_new_thread()

    def loop_play_audio_files(self, current_idx: int) -> None:
        for audio_file in self.artist_menu.get_item_list()[current_idx + 1 : -1]:
            while self.thread_is_alive:
                time.sleep(1)
                if audio.get_audio_end_event():
                    song = audio.play_audio(audio_file)
                    self.current_audio_label._title = str(song)
                    self.playtime_label._title = audio.get_audio_length(song)
                    # self.current_audio_label._title = str(audio.play_audio(audio_file))
                    break

    def toggle_pause_audio_file(self) -> None:
        self.status_label._title = audio.toggle_pause_audio()

    def create_and_start_new_thread(self) -> None:
        self.thread1 = threading.Thread(
            target=self.loop_play_audio_files,
            args=[self.artist_menu.get_selected_item_index()],
        )
        # print("START THREAD")
        self.thread_is_alive = True
        self.thread1.start()

    def kill_thread(self) -> None:
        # print("KILL THREAD")
        self.thread_is_alive = False
        if self.thread1.is_alive():
            self.thread1.join()

    # def reset_labels(self):
    #    self.current_audio_label._title = ""
    #    self.status_label._title = ""


if __name__ == "__main__":

    def _init_root() -> py_cui.PyCUI:
        root = py_cui.PyCUI(9, 8)
        # root.enable_logging(logging_level=logging.DEBUG)
        root.set_title("CAP - Crappy Audio Player")
        root.toggle_unicode_borders()
        root.set_refresh_timeout(1)
        return root

    def _start() -> None:
        root = _init_root()
        wrapper = PlayerTUI(root)
        root.start()
        root.run_on_exit(wrapper.kill_thread())

    _start()
