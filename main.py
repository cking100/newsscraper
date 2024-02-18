import requests
import argparse

def get_hackernews_links(num_links, filter_computers, filter_technology, min_points):
    api_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(api_url)

    if response.status_code == 200:
        top_stories_ids = response.json()[:num_links]
        links = []

        for story_id in top_stories_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
            story_response = requests.get(story_url)

            if story_response.status_code == 200:
                story_data = story_response.json()

                if 'url' in story_data and 'score' in story_data and story_data['score'] >= min_points:
                    if (not filter_computers or any(keyword in story_data['title'].lower() or keyword in story_data.get('text', '').lower() for keyword in ['computer', 'programming', 'coding'])) and \
                       (not filter_technology or any(keyword in story_data['title'].lower() or keyword in story_data.get('text', '').lower() for keyword in ['technology', 'tech', 'innovation'])):
                        links.append(story_data['url'])

        return links
    else:
        print(f"Failed to fetch top stories. Status code: {response.status_code}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Retrieve links of top articles from Hacker News.")
    parser.add_argument("num_links", type=int, help="Number of links to retrieve")
    parser.add_argument("-c", "--filter_computers", action="store_true", help="Filter articles related to computers")
    parser.add_argument("-t", "--filter_technology", action="store_true", help="Filter articles related to technology")
    parser.add_argument("-p", "--min_points", type=int, default=0, help="Minimum number of points to include a link (default is 0)")

    args = parser.parse_args()
    num_links = args.num_links
    filter_computers = args.filter_computers
    filter_technology = args.filter_technology
    min_points = args.min_points

    links = get_hackernews_links(num_links, filter_computers, filter_technology, min_points)

    if links:
        print(f"\nTop {num_links} Hacker News Article Links{' (Computers Related)' if filter_computers else ''}{' (Technology Related)' if filter_technology else ''} with {min_points}+ points:\n")
        for idx, link in enumerate(links, start=1):
            print(f"{idx}. {link}")
    else:
        print("No links found.")

if __name__ == "__main__":
    main()
