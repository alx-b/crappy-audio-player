#!/usr/bin/env python3
import pathlib
import dataclasses

import pygame
import mutagen


@dataclasses.dataclass
class File:
    path: pathlib.PosixPath or str
    metadata: dict

    def __str__(self) -> str:
        new_meta = {}
        for data in self.metadata:
            new_meta.update({data: "".join(self.metadata[data])})

        return (
            f"{new_meta.get('artist', '')} - {new_meta.get('date', '')}"
            + f" - {new_meta.get('album', '')} - {new_meta.get('tracknumber', '')}"
            + f" - {new_meta.get('title', '')}"
        )


def play_audio(audio_file: File) -> str:
    try:
        pygame.mixer.music.load(audio_file.path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        return audio_file
        # return str(audio_file)
    except Exception:
        return "File not supported (pygame & mp3 don't go along)"


def toggle_pause_audio() -> str:
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        return "[PAUSED]"
    else:
        pygame.mixer.music.unpause()
        return "[PLAYING]"


def get_supported_audio_files() -> list[File]:
    try:
        return _sort_audio_files(
            [
                File(filepath, _get_metadata(filepath))
                for filepath in _get_filepaths(f"{pathlib.Path.home()}/Music")
                if _is_file_loadable(filepath)
            ]
        )
    except Exception:
        return "Something went wrong"


def _sort_audio_files(files: list[File]) -> list[File]:
    # Sort by Artist, date, and then tracknumber.
    return sorted(
        files,
        key=lambda file: (
            "".join(file.metadata.get("artist")).lower(),
            "".join(file.metadata.get("date")),
            int("".join(file.metadata.get("tracknumber", "0"))),
        ),
    )


def _get_metadata(filepath: pathlib.PosixPath or str) -> mutagen.File or str:
    try:
        return mutagen.File(filepath, options=None, easy=True)
    except Exception:
        return f"cant read metadata - {filepath}"


def _get_filepaths(main_path: str) -> list[pathlib.PosixPath]:
    music_path = pathlib.Path(main_path)
    return [path for path in list(music_path.glob("**/*")) if path.is_file()]


def _is_file_loadable(filepath: pathlib.PosixPath or str) -> bool:
    try:
        pygame.mixer.music.load(filepath)
        return True
    except Exception:
        return False


def get_audio_end_event() -> bool:
    if [event for event in pygame.event.get() if event.type == pygame.USEREVENT]:
        return True
    return False


def get_audio_length(audio_file: File) -> str:
    try:
        length = int(audio_file.metadata.info.length)
        if length > 59:
            return f"{int(length / 60)}:{str(int(length % 60)).zfill(2)}"
        else:
            return f"0:{str(length).zfill(2)}"
    except Exception:
        return "cant read length of audio."


pygame.init()
pygame.mixer.init()
