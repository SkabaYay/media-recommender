from time import sleep
import musicbrainz
import json

with open("backend/dataset/album_ids.json", "r") as file:
    albums = json.load(file)

album_ids = []

for album in albums:
    title = album["title"]
    release_id = album["release_group_id"]

    print(f"Getting metadata for: {title}")

    metadata = musicbrainz.get_release_group_metadata(release_id)

    genres = []
    tags = []

    for genre in metadata.get("genres", []):
        genres.append(genre["name"])

    for tag in metadata.get("tags", []):
        tags.append(tag["name"])

    album_ids.append({
        "title": title,
        "genres": genres,
        "tags": tags
    })

    print(f"Finished: {title}")

    sleep(10)

print(album_ids)

with open("backend/dataset/albums.json", "w") as file:
    json.dump(album_ids, file, indent=4)