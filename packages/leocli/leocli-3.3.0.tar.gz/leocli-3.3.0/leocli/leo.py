"""
leocli - a console translation script for https://dict.leo.org/ .
"""

# Copyright (c) 2012 Christian Schick
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import subprocess
import sys
from typing import TYPE_CHECKING, Iterable, List, Optional, Tuple, Union

import requests
import termcolor
from bs4 import BeautifulSoup
from tabulate import tabulate

from . import __version__

if TYPE_CHECKING:
    from bs4.element import Tag


try:
    import argcomplete
except ImportError:
    pass

API = "https://dict.leo.org/dictQuery/m-vocab/{lang1}{lang2}/query.xml"
DEFAULTPARAMS = {
    "tolerMode": "nof",
    "rmWords": "off",
    "rmSearch": "on",
    "searchLoc": "0",
    "resultOrder": "basic",
    "multiwordShowSingle": "on",
    "lang": "de",
}
LANGUAGES = {
    "de": {"name": "German", "emoji": "🇩🇪",},
    "en": {"name": "English", "emoji": "🇺🇸",},
    "fr": {"name": "French", "emoji": "🇫🇷",},
    "es": {"name": "Spanish", "emoji": "🇪🇸",},
    "it": {"name": "Italian", "emoji": "🇮🇹",},
    "ch": {"name": "Chinese", "emoji": "🇨🇳",},
    "ru": {"name": "Russian", "emoji": "🇷🇺",},
    "pt": {"name": "Portuguese", "emoji": "🇵🇹",},
    "pl": {"name": "Polish", "emoji": "🇵🇱",},
}
PAGER = "less -R -I -S -X"


def parse_args() -> argparse.Namespace:
    """
    Parse cli arguments.

    Return the parsed arguments
    """
    valid_langs = [lang for lang in LANGUAGES.keys() if lang != "de"]
    valid_langs_str = ", ".join(valid_langs)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "words",
        action="store",
        nargs="+",
        metavar="word",
        type=str,
        help="the words you want to translate",
    )
    parser.add_argument(
        "-l",
        "--lang",
        action="store",
        dest="language",
        metavar="lang",
        type=str,
        default="en",
        choices=valid_langs,
        help=f"the languagecode to translate to or from {valid_langs_str}",
    )
    parser.add_argument(
        "-e",
        "--emojis",
        action="store_true",
        dest="emojis",
        default=False,
        help="Use emoji language flags for languages. Your terminal font must support this feature.",
    )
    parser.add_argument(
        "--pager",
        action="store",
        dest="pager",
        metavar="pagercmd",
        type=str,
        default=PAGER,
        help=f"The pager command to use. Default: '{PAGER}'. Use `--pager=` to disable the pager.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}",
    )

    if "argcomplete" in globals():
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    return args


def get(search: Iterable[str], language1: str = "en", language2: str = "de",) -> str:
    """Querie the API and returns a lists of result string pairs."""
    params = {"search": "+".join(search), "lp": f"{language1}{language2}"}
    params.update(DEFAULTPARAMS)
    try:
        res = requests.get(API.format(lang1=language1, lang2=language2), params=params,)
        res.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as err:
        print("[!]", str(err), file=sys.stderr)
        sys.exit(1)

    return res.text


class Text(str):
    """Represent a text node received from API."""


class Attribute(str):
    """Represent a <small> or <domain> attribute received from API."""


APITag = Union[Text, Attribute]
APIText = List[APITag]
APITranslation = Tuple[APIText, APIText]
APISection = List[APITranslation]


def simplify_repr(root: "Tag") -> APIText:
    """Simplify the XML representation of a ``repr`` tag in API."""
    result: APIText = []

    for node in root:
        if node.name in ("domain", "small"):
            result.append(Attribute(node.getText()))
        else:
            if node.name is None:
                result.append(Text(node))
            else:
                result.append(Text(node.getText()))

    return result


def parse_api(
    api_res: str, language1: str = "en", language2: str = "de",
) -> List[APISection]:
    """Parse the API response and return the results list."""
    content = BeautifulSoup(api_res, "xml")
    results = []

    for api_section in content.sectionlist.findAll("section"):
        if int(api_section["sctCount"]) > 0:
            section: APISection = []

            for entry in api_section.findAll("entry"):
                res0 = entry.find("side", attrs={"lang": language1})
                res1 = entry.find("side", attrs={"lang": language2})

                if res0 and res1:
                    res0_text = simplify_repr(res0.repr)
                    res1_text = simplify_repr(res1.repr)
                    section.append((res0_text, res1_text))

            if section:
                results.append(section)

    return results


def print_result(
    results: List[APISection],
    language1: str = "en",
    language2: str = "de",
    pager: Optional[str] = PAGER,
    with_emojis: bool = False,
) -> None:
    """Print the result to stdout."""

    def format_api_text(text: APIText, normal_is_bold: bool = False) -> str:
        return "".join(
            termcolor.colored(part, color="green")
            if isinstance(part, Attribute)
            else termcolor.colored(part, attrs=["bold"] if normal_is_bold else [])
            for part in text
        )

    def format_translation(translation: APITranslation) -> Tuple[str, str]:
        return (
            format_api_text(translation[0], True),
            format_api_text(translation[1], False),
        )

    def format_section(section: APISection) -> List[Tuple[str, str]]:
        return [format_translation(translation) for translation in section]

    def format_header(lang: str, with_emoji: bool = False) -> str:
        lang_name = LANGUAGES[lang]["name"]
        lang_emoji = LANGUAGES[lang]["emoji"]
        header_str = lang_name

        if with_emoji:
            header_str += " " + lang_emoji

        return termcolor.colored(header_str, attrs=["bold"])

    output = "\n\n".join(
        tabulate(
            format_section(section),
            headers=(
                format_header(language1, with_emoji=with_emojis),
                format_header(language2, with_emoji=with_emojis),
            ),
            #  tablefmt="presto",
            tablefmt="fancy_grid",
        )
        for section in results
    )

    if not pager:
        print(output)
    else:
        subprocess.run(
            pager.split(), input=output, check=True, encoding=sys.stdout.encoding,
        )


def main() -> None:
    """The main function."""
    args = parse_args()
    # The second language must be 'de'
    language2 = "de"
    api_res = get(args.words, args.language, language2)
    words = parse_api(api_res, args.language, language2)

    if words:
        print_result(
            words, args.language, language2, pager=args.pager, with_emojis=args.emojis
        )
    else:
        print(
            "[!] No matches found for '{}'".format("', '".join(args.words)),
            file=sys.stderr,
        )
        sys.exit(1)
