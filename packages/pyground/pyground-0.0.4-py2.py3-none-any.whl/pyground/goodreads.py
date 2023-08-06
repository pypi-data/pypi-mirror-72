"""
Tools for extracting useful data from the Goodreads API.
See https://www.goodreads.com/api for documentation.
"""
from operator import itemgetter
from typing import Iterable, Iterator
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree
import os
import statistics
import time

import cytoolz as toolz
import requests


class Client:
    scheme = "https"
    netloc = "www.goodreads.com"

    def __init__(self, key: str, secret: str = None):
        self.key = key
        self.secret = secret

    @classmethod
    def from_env(cls, key: str = "GOODREADS_KEY", secret: str = "GOODREADS_SECRET"):
        """
        Load credentials from environment variables.
        """
        return cls(os.getenv(key), os.getenv(secret))

    @classmethod
    def from_vault(cls, path: str = "goodreads"):
        """
        Load credentials from Hashicorp Vault
        """
        import hvac  # pylint: disable=import-outside-toplevel

        vault = hvac.Client()
        data = vault.secrets.kv.v1.read_secret(path=path).get("data", {})
        key, secret = toolz.get(["key", "secret"], data)
        return cls(key, secret)

    def request(self, url: str, method: str = "GET", **params) -> requests.Response:
        params.setdefault("key", self.key)
        # split the URL, fill in defaults, then unsplit (join)
        scheme, netloc, path, query, fragment = urlsplit(url)
        url = urlunsplit(
            (scheme or self.scheme, netloc or self.netloc, path, query, fragment)
        )
        return requests.request(method, url, params=params)

    def search(self, q: str):
        """
        Find books by title, author, or ISBN
        """
        return self.request("/search/index.xml", q=q)

    def book(self, identifier: str):
        """
        Get the reviews for a book given a Goodreads book id
        """
        return self.request(f"/book/show/{identifier}.xml")

    def editions(self, identifier: str):
        """
        > This API requires extra permission please contact us
        All calls return "Invalid API permissions" with a 401 status code.
        """
        return self.request(f"/work/editions/{identifier}", format="xml")


# Data extraction


def extract_book_metadata(GoodreadsResponse_element):
    book_element = GoodreadsResponse_element.find("book")
    num_pages = int(book_element.find("num_pages").text)
    return dict(num_pages=num_pages)


def extract_search_results(GoodreadsResponse_element):
    work_elements = (
        GoodreadsResponse_element.find("search").find("results").findall("work")
    )
    for work_element in work_elements:
        best_book_element = work_element.find("best_book")
        # return
        yield dict(
            # work data
            work_id=work_element.find("id").text,
            ratings_count=int(work_element.find("ratings_count").text),
            average_rating=float(work_element.find("average_rating").text),
            # book data
            book_id=best_book_element.find("id").text,
            title=best_book_element.find("title").text,
            author=best_book_element.find("author").find("name").text,
        )


# Filtering and Ranking


def filter_by_limit_and_ratings_count(
    works: Iterable[dict], limit: int = 5
) -> Iterator[dict]:
    works = list(works)
    # of the first N results
    top_works = works[:limit]
    # find the most-rated
    return sorted(top_works, key=itemgetter("ratings_count"), reverse=True)


def filter_by_quantile_ratings_count(works: Iterable[dict]) -> Iterator[dict]:
    works = list(works)
    ratings_counts = [work["ratings_count"] for work in works]
    # find the 5 works with the most ratings
    highest_ratings_counts = sorted(ratings_counts, reverse=True)[:5]
    # set the threshold to the lowest of those
    minimum_rating_count = highest_ratings_counts[-1]
    for work in works:
        if work["ratings_count"] >= minimum_rating_count:
            yield work


def filter_by_median_ratings_count(works: Iterable[dict]) -> Iterator[dict]:
    works = list(works)
    ratings_counts = [work["ratings_count"] for work in works]
    median_ratings_count = statistics.median(ratings_counts)
    # set the threshold to the median
    for work in works:
        if work["ratings_count"] >= median_ratings_count:
            yield work


def filter_by_dummies_and_mean(works: Iterable[dict]) -> Iterator[dict]:
    works = list(works)
    ratings_counts = [work["ratings_count"] for work in works]
    # pad ratings_counts out with zeroes if shorter than 20
    ratings_counts_with_dummies = ratings_counts + [0] * (20 - len(ratings_counts))
    mean_ratings_count = statistics.mean(ratings_counts_with_dummies)
    # set the threshold to the mean
    for work in works:
        if work["ratings_count"] >= mean_ratings_count:
            yield work


def fetch_best_result(client: Client, q: str) -> dict:
    best_work = toolz.thread_first(
        q,
        (client.search),  # -> search_response
        (getattr, "content"),
        (ElementTree.XML),  # -> search_root
        (extract_search_results),  # -> works
        (filter_by_dummies_and_mean),  # -> best_works
        (toolz.first),  # -> best_work
    )
    # sleep for 1 second, as per API restrictions
    time.sleep(1)
    # get page count
    book_response = client.book(best_work["book_id"])
    book_root = ElementTree.XML(book_response.content)
    book_metadata = extract_book_metadata(book_root)
    return dict(best_work, **book_metadata)
