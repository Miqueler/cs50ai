import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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
    prob_distr = {}
    links = corpus[page]
    pages = {key: 0 for key, value in corpus.items()}
    
    for link in links:
        for item in pages:
            if item == link:
                pages[link] += 1

    if len(links) == 0:
        for single in pages:
                prob_distr[single] = 1 / len(pages)
    else:
        for single in pages:
            prob_distr[single] = (1 - damping_factor)/len(pages) + damping_factor * pages[single] / len(links)
    return prob_distr


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    next_distr = {}
    pages = {key: 0 for key, value in corpus.items()}

    page = random.choice(list(pages.keys()))
    pages[page] += 1
    for i in range(n - 1):
        next_distr = transition_model(corpus, page, damping_factor)
        page = random.choices(list(next_distr.keys()), list(next_distr.values()))[0]
        pages[page] += 1

    prob_distr = {key: value/n for key, value in pages.items()}
    return prob_distr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    flag = True
    pages = {key: 1/len(corpus) for key, value in corpus.items()}

    while flag:
        old_pages = pages.copy()
        for page in list(pages.keys()):
            pages[page] = (1 - damping_factor)/ len(corpus)
            linking_prob = 0
            for linker in pages.keys():
                if page in corpus[linker] and corpus[linker] != set():
                    linking_prob += pages[linker] / len(corpus[linker])
            pages[page] += damping_factor * linking_prob
        
        for key in list(old_pages.keys()):
            flag = False
            if abs(old_pages[key] - pages[key]) > .001: 
                flag = True
                break
    return pages


if __name__ == "__main__":
    main()
