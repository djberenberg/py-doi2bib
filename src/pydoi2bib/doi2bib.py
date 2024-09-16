import sys
import re
from io import StringIO
import requests

BASE_URL = "https://doi.org/"
HEADERS = {
    "Accept": 'application/x-bibtex; charset=utf-8'
}

def get_bibtex_from_doi(doi: str) -> str:
    url = BASE_URL + doi
    req = requests.get(url, headers=HEADERS)
    if req.ok:
        return parse_bib(req.text)
    else:
        raise RuntimeError("Could not process request!")

def _parse_bib(text: str) -> dict[str, str]:
    regex = r"@(\w+)\{([^,]+),\s*|(\w+)\s*=\s*\{([^}]*)\}"
    matches = re.findall(regex, text)
    bibtex_dict = {'type': matches[0][0], "ref": matches[0][1]} | {key: value for *_, key, value in matches[1:]}
    return bibtex_dict


def _prettify_bib(bibtex_dict: dict[str, str]) -> str:
    sio = StringIO()

    citation_type = bibtex_dict.pop("type")
    ref = bibtex_dict.pop("ref")

    sio.write(f"@{citation_type}")
    sio.write("{")
    sio.write(f"{ref},\n")
    for key, value in bibtex_dict.items():
        sio.write(f"\t{key}=")
        sio.write("{")
        sio.write(value)
        sio.write("},")
        sio.write("\n")
    sio.write("}\n")

    return sio.getvalue()

def doi2bib():
    try:
        doi = sys.argv[1]
        print(prettify_bib(get_bibtex_from_doi(doi)))
    except IndexError:
        print("Usage: doi2bib DOI_STRING")
        sys.exit(1)
    except RuntimeError as e:
        raise e
