import requests
from bs4 import BeautifulSoup
from imdb import Cinemagoer


def fetch_top_10_movies():
    url = "https://www.imdb.com/chart/top/"
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to access IMDb page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []

    movie_items = soup.select("li.ipc-metadata-list-summary-item")[:10]

    for item in movie_items:

        title_element = item.select_one("h3.ipc-title__text")
        if title_element:
            full_text = title_element.text.strip()
            title = '.'.join(full_text.split('.')[1:]).strip()
            link_element = item.select_one("a.ipc-title-link-wrapper")
            if link_element and 'href' in link_element.attrs:
                link = "https://www.imdb.com" + link_element['href'].split("?")[0]
                movies.append((title, link))

    return movies


def get_movie_summary(imdb_url):
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(imdb_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        details = {}

        # Try to find the short plot summary (usually at the top of the page)
        summary_elem = soup.find("span", {"data-testid": "plot-l"})
        if not summary_elem:
            summary_elem = soup.find("div", class_="summary_text")

        if summary_elem:
            details["summary"] = summary_elem.text.strip()
        else:
            details["summary"] = "No summary available."

        return details

    except Exception as e:
        return {
            "summary": "Error fetching details",
            "storyline": f"Exception occurred: {str(e)}"
        }


def get_movie_storyline(title):
    try:
        ia = Cinemagoer()
        results = ia.search_movie(title)

        if not results:
            return f"No results found for title: {title}"

        movie_id = results[0].movieID
        movie = ia.get_movie(movie_id)

        if 'plot outline' in movie:
            return movie['plot outline']

        elif 'plot' in movie and movie['plot']:
            return movie['plot'][0].split("::")[0]

        return "No plot information found in Cinemagoer."

    except Exception as e:
        return f"Error using Cinemagoer: {str(e)}"


def main():
    print("Fetching top 10 movies from IMDb...")
    top_movies = fetch_top_10_movies()

    for title, link in top_movies:
        print("TİTLE", title)
        print("<SUMMARY>", get_movie_summary(link))
        print("LINK", link)

        print("\n📖 Storyline (Cinemagoer):")
        storyline = get_movie_storyline(title)
        print(storyline)
        print("=" * 80)


if __name__ == "__main__":
    main()

