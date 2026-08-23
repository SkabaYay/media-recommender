from flask import Flask, request, jsonify
from flask_cors import CORS
import musicbrainz

app = Flask(__name__)
CORS(app)

@app.route("/search-albums", methods=["POST"])
def search():
    data = request.json
    albums = musicbrainz.search_albums(data["query"])
    return jsonify(albums)

@app.route("/get-album-metadata", methods=["POST"])
def getMetadata():
    data = request.json
    albums = musicbrainz.get_album_metadata(data["releaseId"])
    return jsonify(albums)

@app.route("/get-release-group-metadata", methods=["POST"])
def getReleaseGroupMetadata():
    data = request.json
    albums = musicbrainz.get_release_group_metadata(data["releaseGroupId"])
    return jsonify(albums)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
