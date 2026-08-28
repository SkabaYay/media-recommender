from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import recommender
import os
import psycopg2
from psycopg2 import pool

load_dotenv()

def getDB():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        # sslmode="require"
    )

app = Flask(__name__)
CORS(
    app
    # resources={
    #     r"/*": {
    #         "origins": "*"
    #     }
    # }
)

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
                "artist": album[2]
            }
            for album in albums
        ])
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

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
        conn.close()

@app.route("/get-recommendations", methods=["POST"])
def getRecommendations():
    conn = getDB()
    cursor = conn.cursor()

    try:
        data = request.json
        dataReleaseGroupId = data["id"]
        
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
            WITH genre_matches AS (
                SELECT rgg.release_group_id, COUNT(*) AS shared_genres
                FROM release_group_genres rgg
                INNER JOIN genres g ON g.id = rgg.genre_id
                WHERE g.name = ANY(%s)
                GROUP BY rgg.release_group_id
            ),
            tag_matches AS (
                SELECT rgt.release_group_id, COUNT(*) AS shared_tags
                FROM release_group_tags rgt
                INNER JOIN tags t ON t.id = rgt.tag_id
                WHERE t.name = ANY(%s)
                GROUP BY rgt.release_group_id
            ),
            candidate_scores AS (
                SELECT
                    COALESCE(gm.release_group_id, tm.release_group_id) AS release_group_id,
                    COALESCE(gm.shared_genres, 0) AS shared_genres,
                    COALESCE(tm.shared_tags, 0) AS shared_tags
                FROM genre_matches gm
                FULL OUTER JOIN tag_matches tm
                    ON gm.release_group_id = tm.release_group_id
                ORDER BY shared_genres DESC, shared_tags DESC
                LIMIT 200
            )

            SELECT
                rg.musicbrainz_id,
                rg.title,
                a.name,

                (
                    SELECT ARRAY_AGG(DISTINCT g2.name)
                    FROM release_group_genres rgg2
                    INNER JOIN genres g2
                        ON g2.id = rgg2.genre_id
                    WHERE rgg2.release_group_id = rg.id
                ) AS genres,

                (
                    SELECT ARRAY_AGG(DISTINCT t2.name)
                    FROM release_group_tags rgt2
                    INNER JOIN tags t2
                        ON t2.id = rgt2.tag_id
                    WHERE rgt2.release_group_id = rg.id
                ) AS tags,

                candidate_scores.shared_genres,
                candidate_scores.shared_tags

            FROM candidate_scores

            INNER JOIN release_groups rg
                ON rg.id = candidate_scores.release_group_id

            INNER JOIN artists a
                ON a.id = rg.artist_id

            ORDER BY
                candidate_scores.shared_genres DESC,
                candidate_scores.shared_tags DESC

        """, (genres, tags))
        
        results = cursor.fetchall()
        albums = [
            {
                "id": album[0],
                "title": album[1],
                "artist": album[2],
                "genres": album[3] or [],
                "tags": album[4] or [],
                "shared_genres": album[5],
                "shared_tags": album[6] or 0
            }
            for album in results
        ]
        
        recommendations = recommender.recommend(
            genres,
            tags,
            albums
        )
        return jsonify(recommendations)
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
