import argparse
import unicodedata
import re
import pprint

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

SWGOH_URL = 'https://swgoh.gg/characters/{character}/gear-list/'
REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0'}

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
    full_gear_list = []

    request = Request(character_url, headers=REQUEST_HEADERS)
    response = urlopen(request).read().decode('utf-8')

    soup = BeautifulSoup(response, 'html.parser')
    gear_list = soup.find(attrs={"class": 'media-list-stream'})
    gears = gear_list.find_all(attrs={"class": 'character'})

    header = soup.title.string

    for gear in gears:
        try:
            gear_link = gear.a.get('href')
            gear_quantity_needed = gear.p.string.strip('x')
            gear_name = gear.a.get('title')

            full_gear_list.append({
                'link': gear_link,
                'quantity_needed': gear_quantity_needed,
                'name': gear_name
            })
        except AttributeError:
            continue

    print(header)
    print('=========')
    pprint.pprint(full_gear_list)
    print(len(full_gear_list))


if __name__ == '__main__':
    args = parser.parse_args()
    get_character_gear_list(args.character)
