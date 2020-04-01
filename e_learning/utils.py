import math
import re
import secrets
import string

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import slugify

chars_string = string.ascii_lowercase + string.digits + string.ascii_uppercase


def random_string(
    *,
    size: int = getattr(settings, "CODE_SIZE", 4),
    chars: str = getattr(settings, "RANDOM_CHARS", chars_string),
) -> str:
    """This function generate random string."""
    return "".join(secrets.choice(chars) for _ in range(size))


def unique_slug(*, title: str, new_slug: str = None) -> str:
    """This is will create unique slug for the instance of the model"""

    if new_slug is not None:
        return new_slug

    else:

        slug = slugify(title)

        new_slug = f"{slug}-{random_string()}"

        return new_slug


def get_read_time(*, words: str) -> int:

    word = strip_tags(value=words)

    count = len(re.findall(r"\w+", word))

    read_time = math.ceil(count / 200)

    return read_time
