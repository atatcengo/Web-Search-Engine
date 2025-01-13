def get_page(url):
    try:
        import urllib.request
        page = urllib.request.urlopen(url).read()
        return page.decode("utf-8")
    except:
        return ""

def get_clear_page(content):
  title = content[content.find("<title>")+7:content.find("</title>")]
  body = content[content.find("<body>")+6:content.find("</body>")]
  while body.find(">") != -1:
    start =  body.find("<")
    end =  body.find(">")
    body = body[:start] + body[end+1:]
  return title + body

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_next_target (page):
    start_link = page.find('<a href')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote +1)
    url = page[start_quote+1:end_quote]
    return url,end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def add_page_to_index(index, url, content):
    content = get_clear_page(content)
    words = content.split()
    for word in words:
        add_to_index(index,word,url)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {}
    while tocrawl:
        pageurl = tocrawl.pop()
        if pageurl not in crawled:
            content = get_page(pageurl)
            add_page_to_index(index, pageurl, content)
            outlinks = get_all_links(content)
            graph[pageurl] = outlinks
            union(tocrawl, get_all_links(content))
            crawled.append(pageurl)
    return index, graph #1-a: We use a "graph" to store and track the nodes (web pages) and edges (links between pages), representing the connections between them. This "graph" structure allows us to assess the popularity of pages more accurately by considering the relationships between them.

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

index, graph = crawl_web("https://searchengineplaces.com.tr/")

def compute_ranks(graph):
    d = 0.8
    N = len(graph)
    numloops = 10
    ranks = {}
    for page in graph:
        ranks[page] = 1/N
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1-d)/N
            for node in graph:
              if page in graph[node]:
                newrank = newrank + d*(ranks[node]/len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return newranks

ranks = compute_ranks(graph)

def ranked_lookup(index, key, graph):
  ranks_sorted = dict(sorted(compute_ranks(graph).items(), key=lambda x: x[1], reverse=True))
  if key in index:
    links = index[key]
  else:
    return None
  results = []
  for e in ranks_sorted:
    if e in links:
        results.append(e)
  return results

def lookup(index, key, graph=None, x=None):
  if graph == None and x == None:
    if key in index:
        return index[key]
    else:
        return None

  elif graph != None and x == compute_ranks:
    return ranked_lookup(index, 'in', graph)

  elif graph != None and x == None:
    return print("""This procedure takes 4 outputs. These are:
                      1-An Index
                      2-A key
                      3-A graph
                      4-A computing procedure
                              respectively.
                You have 2 options to use this lookup procedure: with or without ranking.
                        -If you intend to use it without page rank be sure you have given two inputs: index and key, respectively.
                        -If you intend to use it with page rank be sure you have given all four inputs in the given order.
                INVALID INPUT COMBONATION: Please check the inputs.""")
