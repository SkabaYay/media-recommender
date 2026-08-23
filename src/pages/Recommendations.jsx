import { Link } from "react-router-dom";
import { useSearch } from "../context/SearchContext.jsx";
import { useEffect } from "react";
import "../css/Recommendations.css";
import Search from "../components/Search";

function Recommendations() {
  const {
    openSearch,
    setOpenSearch,
    media,
    searchQuery,
    setSearchQuery,
    handleSearch,
    page,
    setPage,
  } = useSearch();

  useEffect(() => {
    setPage("recommendations");
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
        <div className="recommendations-container">
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
        </div>
      </section>
    </>
  );
}

export default Recommendations;
