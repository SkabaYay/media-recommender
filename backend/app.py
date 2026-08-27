from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import recommender
import os
import psycopg2
from psycopg2 import pool

load_dotenv()

db_pool = psycopg2.pool.ThreadedConnectionPool(
    1,
    10,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

def getDB():
    return db_pool.getconn()

app = Flask(__name__)
CORS(app)

@app.route("/search-albums", methods=["POST"])
def search():
    conn = getDB()
    cursor = conn.cursor()

    try:
        data = request.json
        queryTitle = data["query"]
        
        cursor.execute(
            """
        SELECT rg.musicbrainz_id, rg.title, a.name
        FROM release_groups rg
        INNER JOIN artists a
        ON a.id = rg.artist_id
        WHERE rg.title ILIKE %s
        LIMIT 20
        """,
            (f"%{queryTitle}%",)
        )
        
        albums = cursor.fetchall()
        return jsonify([
            {
                "id": album[0],
                "title": album[1],
                "artist": album[2],
                "cover": None
            }
            for album in albums
        ])
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        db_pool.putconn(conn)

@app.route("/get-release-group-metadata", methods=["POST"])
def getReleaseGroupMetadata():
    conn = getDB()
    cursor = conn.cursor()

    try:
        data = request.json
        mb_id = data["releaseGroupId"]
        
        cursor.execute(
            """
        SELECT rg.id, rg.musicbrainz_id, rg.title, rg.release_date, a.musicbrainz_id, a.name
        FROM artists a
        INNER JOIN release_groups rg
        ON a.id = rg.artist_id
        WHERE rg.musicbrainz_id = %s
        """,
            (mb_id,)
        )
        
        album = cursor.fetchone()
        
        if album is None:
            return jsonify({"error": "Album not found"}), 404
        
        releaseGroupId = album[0]
        
        cursor.execute(
            """
        SELECT g.name
        FROM genres g
        INNER JOIN release_group_genres rgg
        ON rgg.genre_id = g.id
        WHERE rgg.release_group_id = %s
        """,
            (releaseGroupId,)
        )
        
        genres = [row[0] for row in cursor.fetchall()]
        
        cursor.execute(
            """
        SELECT t.name
        FROM tags t
        INNER JOIN release_group_tags rgt
        ON rgt.tag_id = t.id
        WHERE rgt.release_group_id = %s
        """,
            (releaseGroupId,)
        )
        
        tags = [row[0] for row in cursor.fetchall()]
        
        return jsonify({
            "id": album[1],
            "title": album[2],
            "release_date": album[3],
            "artist": {
                "id": album[4],
                "name": album[5]
            },
            "genres": genres,
            "tags": tags
        })
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        db_pool.putconn(conn)

@app.route("/get-recommendations", methods=["POST"])
def getRecommendations():
    conn = getDB()
    cursor = conn.cursor()

    try:
        data = request.json
        dataReleaseGroupId = data["id"]
        dataTitle = data["title"]
        
        cursor.execute(
            """
        SELECT g.name
        FROM genres g
        INNER JOIN release_group_genres rgg
        ON rgg.genre_id = g.id
        INNER JOIN release_groups rg
        ON rgg.release_group_id = rg.id
        WHERE rg.musicbrainz_id = %s
        """,
            (dataReleaseGroupId,)
        )
        
        genres = [row[0] for row in cursor.fetchall()]
        
        cursor.execute(
            """
        SELECT t.name
        FROM tags t
        INNER JOIN release_group_tags rgt
        ON rgt.tag_id = t.id
        INNER JOIN release_groups rg
        ON rgt.release_group_id = rg.id
        WHERE rg.musicbrainz_id = %s
        """,
            (dataReleaseGroupId,)
        )
        
        tags = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("""
        SELECT
            rg.musicbrainz_id,
            rg.title,
            a.name,
            ARRAY_AGG(DISTINCT g.name) AS genres,
            ARRAY_AGG(DISTINCT t.name) AS tags
        FROM release_groups rg
        
        INNER JOIN artists a
        ON rg.artist_id = a.id
        
        INNER JOIN release_group_genres rgg
            ON rgg.release_group_id = rg.id
        
        INNER JOIN genres g
            ON g.id = rgg.genre_id
        
        LEFT JOIN release_group_tags rgt
            ON rgt.release_group_id = rg.id
        
        LEFT JOIN tags t
            ON t.id = rgt.tag_id
        
        WHERE g.name = ANY(%s)
        
        GROUP BY rg.id, rg.musicbrainz_id, rg.title, a.name
        """, (genres,))
        
        results = cursor.fetchall()
        albums = [
            {
                "id": album[0],
                "title": album[1],
                "artist": album[2],
                "genres": album[3],
                "tags": album[4]
            }
            for album in results
        ]
        
        recommendations = recommender.recommend(dataTitle, albums)
        return jsonify(recommendations)
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        db_pool.putconn(conn)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
