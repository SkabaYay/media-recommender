import requests

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

    response = requests.get(
        url,
        params=params,
        headers=HEADERS
    )

    response.raise_for_status()

    data = response.json()

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

    response = requests.get(
        url,
        params=params,
        headers=HEADERS
    )

    response.raise_for_status()
    return response.json()


def get_release_group_metadata(release_group_id):
    url = f"{BASE_URL}/release-group/{release_group_id}"

    params = {
        "inc": "tags genres artists",
        "fmt": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers=HEADERS
    )

    response.raise_for_status()
    return response.json()