import requests
from flask import current_app


def search_papers(query, per_page=10):
    """
    Search papers from the OpenAlex API.
    Returns a list of dicts with title, authors, doi, and URL.
    """
    base_url = current_app.config["OPENALEX_BASE_URL"]
    params = {
        "search": query,
        "per-page": per_page
    }

    try:
        resp = requests.get(base_url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title"),
                "authors": ", ".join([a["author"]["display_name"] for a in item.get("authorships", [])]),
                "doi": item.get("doi"),
                "url": item.get("id"),
                "abstract": item.get("abstract_inverted_index"),
            })
        return results

    except Exception as e:
        current_app.logger.error(f"OpenAlex search failed: {e}")
        return []
