"""Main preprocessor module."""
import os

from bs4 import BeautifulSoup
from weasyprint import urls

from .links import (
    get_body_id,
    rel_pdf_href,
    replace_asset_hrefs,
    transform_href,
    transform_id,
)


def get_combined(soup: BeautifulSoup, base_url: str, rel_url: str):
    """Returns combined href."""
    for entry in soup.find_all(id=True):
        entry["id"] = transform_id(entry["id"], rel_url)

    for link in soup.find_all("a", href=True):
        if urls.url_is_absolute(link["href"]) or os.path.isabs(link["href"]):
            link["class"] = "external-link"
            continue

        link["href"] = transform_href(link["href"], rel_url)

    soup.attrs["id"] = get_body_id(rel_url)
    soup = replace_asset_hrefs(soup, base_url)
    return soup


def get_separate(soup: BeautifulSoup, base_url: str):
    """Transforms relative hrefs into PDF href.

    Transforms all relative hrefs pointing to other html docs
    into relative pdf hrefs.
    """
    for link in soup.find_all("a", href=True):
        link["href"] = rel_pdf_href(link["href"])

    soup = replace_asset_hrefs(soup, base_url)
    return soup
