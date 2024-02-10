import re

MAX_SQLITE_INT = 2**63 - 1


def search_domain(link):
    domain = None
    if isinstance(link, str):
        searched_domain = re.search(r"https?://([^/]*)", link)
        if searched_domain:
            domain = searched_domain.group(1)

    return domain
