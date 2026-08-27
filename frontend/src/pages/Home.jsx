import { Link } from "react-router-dom";
import { useSearch } from "../context/SearchContext.jsx";
import { useEffect } from "react";
import "../css/Home.css";
import Search from "../components/Search.jsx";

function Home() {
  const {
    openSearch,
    setOpenSearch,
    searchQuery,
    setSearchQuery,
    handleSearch,
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
          <p>Album Recommender</p>

          <div className="search-container">
            <form
              onChange={handleSearch}
              onSubmit={(e) => e.preventDefault()}
              className="search-bar-form"
            >
              <input
                type="text"
                placeholder={`Search album...`}
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
            <button className="album-button">Album</button>
          </div>
        </div>
      </section>
    </>
  );
}

export default Home;
