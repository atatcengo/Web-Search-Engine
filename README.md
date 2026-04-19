# Mini Search Engine — Web Crawler + PageRank

> **DSAI 301: Introduction to Programming with Python** — Coursework Submission  

---

## What This Is

A dependency-free mini search engine built in Python from scratch. It crawls the web starting from a seed URL, builds an inverted index of every word it finds, and ranks results using the **PageRank** algorithm — the same core idea behind the original Google.

---

## How It Works

**1. Crawling** — `crawl_web(seed)` keeps a queue of URLs to visit. For each page it fetches the HTML, strips the tags to get plain text, and indexes every word. It also records every outbound link to form a graph and adds undiscovered URLs to the queue.

**2. Inverted Index** — Every word is mapped to the list of URLs containing it. `index["python"]` returns every crawled page that mentions the word. This is how all search engines store data internally.

**3. PageRank** — Links between pages are treated as votes. A link from a popular page counts for more than one from an obscure page. Because this is circular (A's rank depends on B's, which depends on A's), it's solved iteratively — starting with uniform ranks and redistributing them across links repeatedly until stable.

The formula for each page `p` per iteration:

```
Rank(p) = (1 - d) / N  +  d × Σ [ Rank(node) / OutLinks(node) ]
```

Where `d = 0.8` is the damping factor (the probability a random surfer follows a link rather than jumping to a random page), and `N` is the total number of pages.

---

## Key Components

| Function | Description |
|---|---|
| `get_page(url)` | Fetches raw HTML from a URL; returns empty string on any error |
| `get_clear_page(content)` | Strips all HTML tags, returning the title + body as plain text |
| `union(p, q)` | Merges list `q` into `p` in-place, skipping duplicates — used to update the crawl queue |
| `get_next_target(page)` | Finds the first `<a href="...">` in a string and returns the URL and scan position |
| `get_all_links(page)` | Calls `get_next_target` in a loop to collect every link on a page |
| `add_to_index(index, keyword, url)` | Appends a URL to `index[keyword]`, creating the entry if it doesn't exist |
| `add_page_to_index(index, url, content)` | Strips a page to plain text and indexes every word |
| `crawl_web(seed)` | Main crawler loop — returns the completed `index` and link `graph` |
| `compute_ranks(graph)` | Runs 10 iterations of PageRank over the link graph |
| `ranked_lookup(index, key, graph)` | Looks up a keyword and sorts matches by PageRank score |
| `lookup(index, key, graph, x)` | Unified interface for both ranked and unranked lookups |

---

## Usage

```python
# Crawl from a seed URL
index, graph = crawl_web("https://example.com/")

# Simple lookup (unranked)
lookup(index, "python")

# PageRank-sorted lookup
lookup(index, "python", graph, compute_ranks)
```

> *The explanation in this README was refined with the assistance of Claude.*
