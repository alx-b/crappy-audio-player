#!/usr/bin/env python3
import pathlib
import pytest
import pygame
import mutagen
import crappy_audio_player.audio as audio


def audio_file(length):
    class Info:
        def __init__(self, length):
            self.length = length

    class MetaData:
        def __init__(self, length):
            self.info = Info(length)

    class File:
        def __init__(self, length):
            self.path = "/random/path"
            self.metadata = MetaData(length)

    return File(length)


def test_get_metadata_succeed(mocker):
    mocker.patch(
        "crappy_audio_player.audio.mutagen.File",
        return_value=mutagen.File,
    )
    assert (
        audio._get_metadata(pathlib.PosixPath("/parameter/is/useless"))
        == mutagen.File()
    )


def test_get_metadata_fail():
    assert (
        audio._get_metadata(pathlib.PosixPath("/filepath/to/nowhere"))
        == "can't read metadata - /filepath/to/nowhere"
    )


def test_get_filepath() -> list:
    assert audio._get_filepaths("/filepath/to/nowhere") == []


def test_get_filepath_return_files(mocker) -> list:
    mocker.patch(
        "crappy_audio_player.audio.pathlib.PosixPath.glob",
        return_value=[
            pathlib.PosixPath("track1.flac"),
            pathlib.PosixPath("track2.flac"),
        ],
    )
    mocker.patch(
        "crappy_audio_player.audio.pathlib.PosixPath.is_file", return_value=True
    )
    assert audio._get_filepaths("/this/parameter/is/useless/for/this/test") == [
        pathlib.PosixPath("track1.flac"),
        pathlib.PosixPath("track2.flac"),
    ]


def test_file_is_not_loadable(mocker) -> False:
    assert audio._is_file_loadable("Not a filepath") == False


def test_file_is_loadable(mocker) -> True:
    mocker.patch("crappy_audio_player.audio.pygame.mixer.music.load", return_value=None)
    assert audio._is_file_loadable("This parameter is useless for testing") == True


def test_get_audio_end_event_returns_true(mocker) -> bool:
    end_event = pygame.event.Event(pygame.USEREVENT, {})
    mocker.patch(
        "crappy_audio_player.audio.pygame.event.get",
        return_value=[end_event],
    )
    assert audio.get_audio_end_event() == True


def test_get_audio_end_event_returns_false(mocker) -> bool:
    mocker.patch("crappy_audio_player.audio.pygame.event.get", return_value=[])
    assert audio.get_audio_end_event() == False


@pytest.mark.parametrize(
    "fake_file, expected",
    [
        (audio_file(20.332), "0:20"),
        (audio_file(65), "1:05"),
        (audio_file("not valid to get an exception"), "can't read length of audio."),
    ],
)
def test_get_audio_length(fake_file, expected) -> str:
    assert audio.get_audio_length(fake_file) == expected
