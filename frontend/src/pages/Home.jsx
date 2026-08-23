import { Link } from "react-router-dom";
import { useSearch } from "../context/SearchContext.jsx";
import { useEffect } from "react";
import "../css/Home.css";
import Search from "../components/Search.jsx";

function Home() {
  const {
    openSearch,
    setOpenSearch,
    media,
    searchQuery,
    setSearchQuery,
    handleSearch,
    handleMediaClick,
    page,
    setPage,
  } = useSearch();

  useEffect(() => {
    setPage("home");
  }, []);

  return (
    <>
      <header>
        <nav>
          <Link to="/">Media Recommender</Link>

          <a
            href="https://github.com/SkabaYay/media-recommender"
            target="_blank"
            rel="noopener noreferrer"
          >
            <i className="fa-brands fa-github"></i>
          </a>
        </nav>
      </header>

      <section>
        <div className="home-container">
          <p>{media} Recommender</p>

          <div className="search-container">
            <form onSubmit={handleSearch} className="search-bar-form">
              <input
                type="text"
                placeholder={`Search ${media}...`}
                onChange={(e) => {
                  setOpenSearch(e.target.value.length > 0);
                  setSearchQuery(e.target.value);
                }}
                value={searchQuery}
                id="search-bar"
                name="search-bar"
              />
            </form>

            {openSearch && <Search page={page} />}
          </div>

          <div className="media-buttons">
            <button className="album-button" onClick={handleMediaClick}>
              Album
            </button>

            <button className="anime-button" onClick={handleMediaClick}>
              Anime
            </button>
          </div>
        </div>
      </section>
    </>
  );
}

export default Home;
