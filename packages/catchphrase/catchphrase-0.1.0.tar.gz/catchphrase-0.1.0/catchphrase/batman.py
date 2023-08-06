import pkg_resources
import json
import random


# List of real quotes provided courtesy of BuzzFeed
# https://www.buzzfeed.com/spenceralthouse/the-definitive-ranking-of-robins-exclamations-from-batma


with open(pkg_resources.resource_filename(__name__, "batman.json")) as f:
    real_holy_phrases = json.load(f)  # type: [str]


def random_holy(suffix=', Batman!'):
    return random.choice(real_holy_phrases) + (suffix or '')


if __name__ == '__main__':
    print(random_holy())
