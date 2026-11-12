"""Refresh the deployed metadata of a curated feed; keep its offers unchanged.

The workflow runs this before tests and packaging, not on clients, once per
renewed feed (Mar and Folclore). The source feed is a curated seed;
revision/valid_until in the deployed artifact are renewed.
"""
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

MAX_REVISION = 2**31 - 1
SITE = 'https://vcdevelopstudio.github.io/tico-e-lili-legal/'
RENEWED_FEEDS = ('catalogo/mar/v1/jogos.json', 'catalogo/folclore/v1/jogos.json')
PUBLIC = SITE + RENEWED_FEEDS[0]


def public_url(path):
    """Public URL of a renewed feed; unknown paths are refused, never guessed."""
    relative = Path(path).as_posix()
    if relative not in RENEWED_FEEDS:
        raise ValueError(f'Not a renewed feed: {relative}')
    return SITE + relative


def valid_revision(value):
    if type(value) is not int or not 0 <= value < MAX_REVISION:
        raise ValueError('Revision must be a non-negative integer below the increment limit')
    return value


def refresh(path, now=None, previous_revision=0):
    path = Path(path)
    document = json.loads(path.read_text(encoding='utf-8'))
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('UTC-aware time required')
    revision = max(valid_revision(document['revision']),
                   valid_revision(previous_revision), int(now.timestamp())) + 1
    if revision > MAX_REVISION:
        raise ValueError('Revision would exceed supported range')
    document['revision'] = revision
    document['valid_until'] = (now.astimezone(timezone.utc) + timedelta(hours=23)).strftime('%Y-%m-%dT%H:%M:%SZ')
    content = json.dumps(document, ensure_ascii=False, indent=2) + '\n'
    if len(content.encode('utf-8')) > 65536:
        raise ValueError('Feed exceeds the client byte limit')
    path.write_text(content, encoding='utf-8')
    return document


def published_revision(url=PUBLIC, allow_bootstrap=False):
    try:
        with urlopen(url, timeout=20) as response:
            if response.geturl() != url:
                raise ValueError('Unexpected redirect')
            content = response.read(65537)
            if len(content) > 65536:
                raise ValueError('Published feed exceeds byte limit')
            return valid_revision(json.loads(content)['revision'])
    except HTTPError as error:
        if error.code == 404 and allow_bootstrap:
            return 0  # Explicit first publication of this endpoint.
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='catalogo/mar/v1/jogos.json')
    parser.add_argument('--bootstrap', action='store_true', help='Allow HTTP 404 only for an explicit first publication')
    args = parser.parse_args()
    url = public_url(args.path)
    result = refresh(args.path, previous_revision=published_revision(url, allow_bootstrap=args.bootstrap))
    print(f"{args.path} revision {result['revision']}; valid until {result['valid_until']}")
