from pathlib import Path
import urllib.request as request
from urllib.error import HTTPError
import yaml


def test_registry():
    """Test that all files in the registry are available at the expected URLs"""

    registry = Path(__file__).parent.parent / 'registry.yaml'
    with open(registry, 'r') as f:
        registry = yaml.safe_load(f)

    # Get download url for each mapping set
    urls = []
    for i in registry['mapping_set_references']:
        try:
            urls.append(i['mirror_from'])
        except KeyError:
            urls.append(i['mapping_set_id'])

    missing = []
    for url in urls:
        try:
            r = request.urlopen(url)
        except HTTPError:
            missing.append(url)
    if len(missing) > 0:
        print('The following urls are not available:')
        for url in missing:
            print(url)
        raise Exception

if __name__ == '__main__':
    test_registry()