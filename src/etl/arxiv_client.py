import time, requests, feedparser
from urllib.parse import quote_plus

BASE = "http://export.arxiv.org/api/query"
USER_AGENT = "TA-dashboard (lino.zurmuehl@web.de)"

def build_query(categories=None, terms=None):
    """
    categories: list like ["cs.AI","cs.RO"] -> "(cat:cs.AI OR cat:cs.RO)"
    terms: list like ["exoskeleton","human-robot interaction"]
           -> '(ti:"exoskeleton" OR abs:"exoskeleton" OR ti:"human-robot interaction" OR abs:"human-robot interaction")'
    Return: join with " AND " if both parts exist, else the one part, else "all:*"
    """
    parts = []
    if categories:
        parts.append("(" + " OR ".join(f"cat:{c}" for c in categories) + ")")
    
    if terms:
        parts.append("(" + " OR ".join(f"ti:\"{t}\"" for t in terms)+ " OR " + " OR ".join(f"abs:\"{t}\"" for t in terms) + ")")
    
    return " AND ".join(parts) if parts else "all:*"

def fetch_arxiv(search_query, start=0, max_results=50,
                sort_by="submittedDate", sort_order="descending"):
    """
    Call arXiv API and return a list[dict] of entries with keys:
      arxiv_id, title, summary, published, updated, authors(list[str]),
      categories(list[str]), link_abs, link_pdf
    Raise for HTTP errors. No sleeping needed here (paging comes next).
    """
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(BASE, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    feed = feedparser.parse(r.text)
    rows = []
    for e in feed.entries:
        rows.append({
            "arxiv_id": e.id.split("/abs/")[-1],
            "title": e.title,
            "summary": e.summary,
            "published": e.published,
            "updated": e.updated,
            "authors": [a.name for a in getattr(e, "authors", [])],
            "categories": [t["term"] for t in getattr(e, "tags", [])],
            "link_abs": next((l.href for l in e.links if getattr(l, "rel", "") == "alternate"), None),
            "link_pdf": next((l.href for l in e.links if getattr(l, "title", "") == "pdf"), None),
        })

    return rows



if __name__ == "__main__":
    q = build_query(["cs.AI","cs.RO"], ["exoskeleton","human-robot interaction"])
    rows = fetch_arxiv(q, max_results=5)
    print(len(rows), "entries")
    print(rows[0]["title"])
    print(rows[0]["arxiv_id"], rows[0]["link_abs"])




