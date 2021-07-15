#!/usr/bin/env python3

import py_cui


class PlayerTUI:
    def __init__(self, root: py_cui.PyCUI):
        self.root = root
        self.artist_menu = self._init_artist_menu()
        self.current_audio = self._init_current_audio()

    def _init_artist_menu(self):
        return self.root.add_scroll_menu("Artists", 0, 0, row_span=8, column_span=8)

    def _init_current_audio(self):
        current_audio = self.root.add_label("", 8, 0, column_span=8)
        current_audio.toggle_border()
        return current_audio


if __name__ == "__main__":

    def _init_root():
        root = py_cui.PyCUI(9, 8)
        # root.enable_logging(logging_level=logging.DEBUG)
        root.set_title("CAP - Crappy Audio Player")
        root.toggle_unicode_borders()
        root.set_refresh_timeout(1)
        return root

    def _start():
        root = _init_root()
        wrapper = PlayerTUI(root)
        root.start()

    _start()
