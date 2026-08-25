import "../css/Search.css";
import { useSearch } from "../context/SearchContext.jsx";
import Loading from "../assets/Loading.svg";
import Missing from "../assets/Missing.svg";

function Search({ page }) {
  const { handleMediaClickOnSearch, results, loading } = useSearch();

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
                onClick={handleMediaClickOnSearch}
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
