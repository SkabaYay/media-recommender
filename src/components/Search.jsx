import "../css/Search.css";
import { useNavigate } from "react-router-dom";
import { useSearch } from "../context/SearchContext.jsx";
import { getAlbumMetadata, getReleaseGroupMetadata } from "../services/api.js";
import Loading from "../assets/Loading.svg";
import Missing from "../assets/Missing.svg";

function Search({ page }) {
  const { setOpenSearch, setSearchQuery, results, loading } = useSearch();
  const navigate = useNavigate();

  async function handleMediaClick(e) {
    setOpenSearch(false);
    setSearchQuery("");

    navigate("/recommendations");

    const release = await getAlbumMetadata(e.currentTarget.id);
    const releaseGroupId = release["release-group"].id;
    const album = await getReleaseGroupMetadata(releaseGroupId);
    e.preventDefault();
    console.log(album);
  }

  return (
    <div className={`search-box-${page}`}>
      <div className="albums">
        {loading ? (
          <p>Loading albums...</p>
        ) : results.length === 0 ? (
          <p>No albums found</p>
        ) : (
          results.map((album) => {
            return (
              <div
                key={album.id}
                className="album"
                id={album.id}
                onClick={handleMediaClick}
              >
                <img
                  src={
                    album.cover === undefined ? Loading : album.cover || Missing
                  }
                  alt={album.title}
                />

                <div className="album-info">
                  <p>{album.title}</p>
                  <p>{album.artist}</p>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default Search;
