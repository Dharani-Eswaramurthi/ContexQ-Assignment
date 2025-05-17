import feedparser
import pandas as pd
import logging
from typing import List, Dict

def fetch_feeds(feed_urls: List[str]) -> pd.DataFrame:
    """
    Fetch and parse multiple RSS feeds into a deduplicated DataFrame.

    Args:
        feed_urls (List[str]): List of RSS feed URLs.

    Returns:
        pd.DataFrame: DataFrame with columns ['id', 'title', 'summary', 'date', 'source', 'url'].
    """
    rows = []
    for url in feed_urls:
        logging.info(f"Parsing feed: {url}")
        try:
            feed = feedparser.parse(url)
            if feed.bozo:
                logging.warning(f"Feed parsing error for {url}: {feed.bozo_exception}")
            for entry in feed.entries:
                # Use robust extraction with fallback keys
                entry_id = entry.get("id") or entry.get("link") or None
                if not entry_id:
                    logging.warning(f"Skipping entry without ID or link in feed {url}")
                    continue
                rows.append({
                    "id": entry_id,
                    "title": entry.get("title", "").strip(),
                    "summary": entry.get("summary", entry.get("description", "")).strip(),
                    "date": entry.get("published", entry.get("updated", "")).strip(),
                    "source": feed.feed.get("title", "").strip(),
                    "url": entry.get("link", "").strip()
                })
        except Exception as e:
            logging.error(f"Failed to parse feed {url}: {e}")

    df = pd.DataFrame(rows)
    df.drop_duplicates(subset=["id", "url"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    logging.info(f"Fetched {len(df)} unique feed entries.")
    return df
