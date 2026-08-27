# import os
# import json
# import psycopg2
# from dotenv import load_dotenv

# load_dotenv()

# path = "/mnt/c/Users/Skaba/Downloads/release-group/mbdump/release-group"

# conn = psycopg2.connect(
#     dbname=os.getenv("DB_NAME"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     host=os.getenv("DB_HOST"),
#     port=os.getenv("DB_PORT")
# )

# cursor = conn.cursor()

# with open(path, "r", encoding="utf-8") as file:
#     line = file.readline()
#     album = json.loads(line)

#     artist = album["artist-credit"][0]["artist"]

#     cursor.execute(
#         """
#         INSERT INTO artists(musicbrainz_id, name)
#         VALUES(%s, %s)
#         ON CONFLICT (musicbrainz_id) DO NOTHING
#         """,
#         (artist["id"], artist["name"])
#     )

#     cursor.execute(
#         """
#         SELECT id
#         FROM artists
#         WHERE musicbrainz_id = %s
#         """,
#         (artist["id"])
#     )

#     artist_id = cursor.fetchone()[0]

#     cursor.execute(
#         """INSERT INTO release_groups
#         (musicbrainz_id, title, artist_id, release_date)
#         VALUES(%s, %s, %s, %s)
#         """,

#         (
#             album["id"],
#             album["title"],
#             artist_id, 
#             album["first-release-date"]
#         )
#     )

# conn.commit()

# cursor.close()
# conn.close()

# print("Successfully imported:", album["title"])