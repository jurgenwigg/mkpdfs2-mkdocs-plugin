"""Transforms HTML links to the PDF equivalent."""
import os

from .util import is_doc, normalize_href


def transform_href(href: str, rel_url: str) -> str:
    """Normalize href to #foo/bar/section:id"""
    if not is_doc(href):
        return href
    if "#" not in href:
        href += "#"
    return "#" + normalize_href(href, rel_url).replace("#", ":", 1)


def transform_id(ident: str, rel_url: str) -> str:
    """Normalize id to foo/bar/section:id"""
    head, section = os.path.split(rel_url)

    if len(head) > 0:
        head += "/"

    return f"{head}{section}:{ident}"
