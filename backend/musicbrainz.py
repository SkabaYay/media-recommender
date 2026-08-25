import requests
from time import sleep

BASE_URL = "https://musicbrainz.org/ws/2"

HEADERS = {
    "User-Agent": "media-recommender/1.0 honng2552@gmail.com"
}

def search_albums(query):
    url = f"{BASE_URL}/release/"
    params = {
        "query": query,
        "fmt": "json"
    }

    for attempt in range(5):
        try:
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=30
            )

            if response.status_code == 503:
                wait = 10 * (2 ** attempt)
                print(f"MusicBrainz busy. Retrying in {wait}s...")
                sleep(wait)
                continue

            response.raise_for_status()
            data = response.json()
            break

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        ):
            wait = 10 * (2 ** attempt)
            print(f"Request failed. Retrying in {wait}s...")
            sleep(wait)

    else:
        print(f"Failed to retrieve {query} after 5 attempts.")
        return []

    albums = []

    for release in data["releases"]:
        artist = "Unknown Artist"

        if release.get("artist-credit"):
            artist = release["artist-credit"][0]["name"]

        albums.append({
            "id": release["id"],
            "title": release["title"],
            "artist": artist,
            "cover": None
        })

    return albums


def get_album_metadata(release_id):
    url = f"{BASE_URL}/release/{release_id}"

    params = {
        "inc": "release-groups artists",
        "fmt": "json"
    }

    for attempt in range(5):
        try:
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=30
            )

            if response.status_code == 503:
                wait = 10 * (2 ** attempt)
                print(f"MusicBrainz busy. Retrying in {wait}s...")
                sleep(wait)
                continue

            response.raise_for_status()
            return response.json()

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        ):
            wait = 10 * (2 ** attempt)
            print(f"Request failed. Retrying in {wait}s...")
            sleep(wait)

    raise Exception(
        f"Failed to get metadata for release {release_id} after 5 attempts"
    )


def get_release_group_metadata(release_group_id):
    url = f"{BASE_URL}/release-group/{release_group_id}"

    params = {
        "inc": "artists genres tags releases",
        "fmt": "json"
    }

    for attempt in range(5):
        try:
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=30
            )

            if response.status_code == 503:
                wait = 10 * (2 ** attempt)
                print(f"MusicBrainz busy. Retrying in {wait}s...")
                sleep(wait)
                continue

            response.raise_for_status()
            return response.json()

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        ):
            wait = 10 * (2 ** attempt)
            print(f"Request failed. Retrying in {wait}s...")
            sleep(wait)

    raise Exception(
        f"Failed to get release-group metadata for "
        f"{release_group_id} after 5 attempts"
    )