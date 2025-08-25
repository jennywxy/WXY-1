import os
import requests
import openai
import argparse
import textwrap


HEADERS = {"User-Agent": "video-script-generator/0.1"}


def fetch_reddit_comments(topic: str, post_limit: int = 3, comment_limit: int = 5):
    """Fetch top Reddit comments for a topic.

    Parameters
    ----------
    topic: str
        Search term used on Reddit.
    post_limit: int, optional
        Number of posts to inspect. Defaults to 3.
    comment_limit: int, optional
        Total number of comments to return. Defaults to 5.
    """
    search_url = "https://www.reddit.com/search.json"
    params = {"q": topic, "sort": "top", "limit": post_limit}
    resp = requests.get(search_url, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    comments = []
    for post in data.get("data", {}).get("children", []):
        permalink = post.get("data", {}).get("permalink")
        if not permalink:
            continue
        comments_url = f"https://www.reddit.com{permalink}.json"
        resp_comments = requests.get(comments_url, headers=HEADERS, timeout=10)
        resp_comments.raise_for_status()
        comments_data = resp_comments.json()
        if len(comments_data) < 2:
            continue
        for item in comments_data[1].get("data", {}).get("children", []):
            if item.get("kind") != "t1":
                continue
            body = item.get("data", {}).get("body")
            if body:
                comments.append(body)
            if len(comments) >= comment_limit:
                return comments
    return comments


def build_prompt(topic: str, comments):
    intro = "\n".join(f"- {c}" for c in comments)
    prompt = (
        f"You are a helpful scriptwriter. Using the following user comments from Reddit on the topic '{topic}', "
        "craft a short and engaging video script. The comments can be used as an introduction or inspiration.\n\n"
        f"Comments:\n{intro}\n\nVideo Script:"
    )
    return prompt


def generate_video_script(topic: str, model: str = "gpt-3.5-turbo") -> str:
    comments = fetch_reddit_comments(topic)
    prompt = build_prompt(topic, comments)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"].strip()


def main():
    parser = argparse.ArgumentParser(description="Generate a video script from Reddit comments")
    parser.add_argument("topic", help="Topic to search on Reddit")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model to use")
    args = parser.parse_args()
    script = generate_video_script(args.topic, model=args.model)
    print(textwrap.fill(script, width=80))


if __name__ == "__main__":
    main()
