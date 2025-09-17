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

if __name__ == "__main__":
    print(build_query(["cs.AI","cs.RO"], ["exoskeleton","human-robot interaction"]))




