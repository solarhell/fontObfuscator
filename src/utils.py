from pathlib import Path

import base64
from collections import OrderedDict

import emoji

from fontTools import subset


def str_has_whitespace(s: str) -> bool:
    return ' ' in s


def str_has_emoji(s: str) -> bool:
    for character in s:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False


def deduplicate_str(s: str) -> str:
    return "".join(OrderedDict.fromkeys(s))


def ensure_cmap_has_all_text(cmap: dict, s: str) -> bool:
    for char in s:
        if ord(char) not in cmap:
            raise Exception(f'字库缺少{char}这个字')
    return True


def subset_ttf_font(filepath: str) -> dict:
    options = subset.Options()
    font = subset.load_font(f'{filepath}.ttf', options)
    options.flavor = 'woff'
    subset.save_font(font, f'{filepath}.woff', options)
    options.flavor = 'woff2'
    subset.save_font(font, f'{filepath}.woff2', options)
    return {
        'woff': f'{filepath}.woff',
        'woff2': f'{filepath}.woff2'
    }


def base64_binary(file: str):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_project_root() -> Path:
    return Path(__file__).parent.parent
