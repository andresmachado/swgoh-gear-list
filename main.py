import argparse
import unicodedata
import re

from bs4 import BeautifulSoup

SWGOH_URL = 'https://swgoh.gg/characters/{character}/gear-list/'

parser = argparse.ArgumentParser(description='Collect information about gear '
                                             'list for given character of '
                                             'Star Wars Galaxy of Heroes')
parser.add_argument('-c',
                    '--character',
                    help='Name of the character you wish to get info.')


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize(
            'NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def get_character_gear_list(character):
    character_url = SWGOH_URL.format(character=slugify(character))
    print(character_url)


if __name__ == '__main__':
    args = parser.parse_args()
    get_character_gear_list(args.character)
