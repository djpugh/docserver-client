from datetime import datetime

from docsclient.client import Client  # noqa F401
from ._version import get_versions


__version__ = get_versions()['version']
del get_versions

start_year = 2019
end_year = datetime.now().year
del datetime
if end_year > start_year:
    __copyright__ = f"David Pugh, {start_year} - {end_year}"
else:
    __copyright__ = f'David Pugh, {start_year}'
del start_year
del end_year
