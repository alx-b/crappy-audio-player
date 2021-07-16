#!/usr/bin/env python3
import py_cui

import audio


class PlayerTUI:
    def __init__(self, root: py_cui.PyCUI):
        self.root = root
        self.artist_menu = self._init_artist_menu()
        self.current_audio = self._init_current_audio()
        self._get_playlist()

    def _init_artist_menu(self) -> py_cui.widgets.ScrollMenu:
        menu = self.root.add_scroll_menu("Artists", 0, 0, row_span=8, column_span=8)
        menu.add_key_command(py_cui.keys.KEY_ENTER, self.play_selected_audio_file)
        return menu

    def _init_current_audio(self) -> py_cui.widgets.Label:
        current_audio = self.root.add_label("", 8, 0, column_span=8)
        current_audio.toggle_border()
        return current_audio

    # !! might put this in init_artist_menu instead !!
    def _get_playlist(self):
        self.artist_menu.add_item_list(audio.get_supported_audio_files())

    def play_selected_audio_file(self) -> None:
        # !! return into some info display ? !!
        audio.play_audio(self.artist_menu.get())


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

    _start()
