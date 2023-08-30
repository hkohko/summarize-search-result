from os import listdir
from typing import Generator
from app._locations import Directories

def get_sample_text() -> Generator[str, None, None]:
    texts = listdir(Directories.SAMPLE_TEXT)
    for text in texts:
        with open(Directories.SAMPLE_TEXT.joinpath(text), encoding="utf-8") as file:
            sample_text = file.read()
            yield sample_text