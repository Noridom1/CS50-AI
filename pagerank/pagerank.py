import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    #orpus = crawl(sys.argv[1])
    corpus = {
        '1': {'2'}, '2': {'1', '3'}, '3': {'2', '4'}, '4': {'2'}
    }
    print(f"corpus: {corpus}")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    """trans_model = transition_model(corpus, "2.html" ,DAMPING)
    print(f"trans_model: {trans_model}")"""


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if page not in corpus:
        return None
    cur_page_links = corpus[page]
    prob_distribution = {}
    num_pages_corpus = len(corpus)
    num_pages_curpage = len(cur_page_links)
    if cur_page_links == None:
        for page in corpus:
            prob_distribution[page] = 1.0 / num_pages_corpus
        return prob_distribution
    for page in corpus:
        prob_distribution[page] = (1 - damping_factor) / num_pages_corpus
        if page in cur_page_links:
            prob_distribution[page] += damping_factor / num_pages_curpage
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = {}
    for page in corpus.keys():
        page_rank[page] = int(0)
    cur_page = random.choice(list(corpus.keys()))
    page_rank[cur_page] += 1

    n -= 1
    for i in range(n):
        prob_distribution = transition_model(corpus, cur_page, damping_factor)
        keys_list = prob_distribution.keys()
        values_list = prob_distribution.values()
        cur_page = random.choices(list(keys_list), values_list, k = 1)[0]
        page_rank[cur_page] += 1

    for page in page_rank.keys():
        page_rank[page] = (1.0 * page_rank[page]) / n
    return page_rank


def calculate_pagerank(corpus, damping_factor, page, pagerank):
    corpus_size = len(corpus)
    cum_rank = (1 - damping_factor) / corpus_size
    for corpus_page in corpus:
        if not corpus[corpus_page]:
            cum_rank += damping_factor * (pagerank[corpus_page] / corpus_size)
        elif page in corpus[corpus_page]:
            cum_rank += damping_factor * (pagerank[corpus_page] / len(corpus[corpus_page]))
    return cum_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus_size = len(corpus)
    pagerank = {page : 1 / corpus_size for page in corpus}

    diff = 1e6
    MAX_DIFF = 0.001
    while diff >= MAX_DIFF:
        new_pagerank = {page: calculate_pagerank(corpus, damping_factor, page, pagerank) for page in pagerank}
        diff = max(abs(new_pagerank[page] - pagerank[page]) for page in corpus)
        pagerank = new_pagerank
    return pagerank
    #raise NotImplementedError


if __name__ == "__main__":

    main()
