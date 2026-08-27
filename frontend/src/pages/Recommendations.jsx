import { Link } from "react-router-dom";
import { getAlbumCover, getReleaseGroupMetadata } from "../services/api.js";
import { useSearch } from "../context/SearchContext.jsx";
import { useEffect, useState } from "react";
import "../css/Recommendations.css";
import Search from "../components/Search.jsx";
import Loading from "../assets/Loading.svg";
import Missing from "../assets/Missing.svg";

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
    recommendations,
    chosenMedia,
    loadingRec,
    setLoadingRec,
    loadingChosenMed,
    setLoadingChosenMed,
  } = useSearch();
  const [cover, setCover] = useState(undefined);
  const [results, setResults] = useState([]);

  useEffect(() => {
    setPage("recommendations");
  }, []);

  useEffect(() => {
    if (recommendations.length === 0) return;

    setResults([]);

    async function getRecommendationInfo() {
      const promiseResults = await Promise.all(
        recommendations.map(async (album) => {
          const searchResult = await getReleaseGroupMetadata(album["id"]);
          const searchResultCover = await getAlbumCover(album["id"]);

          return {
            title: searchResult["title"],
            id: searchResult["id"],
            artist: searchResult["artist"]["name"],
            cover: searchResultCover,
          };
        }),
      );

      setResults(promiseResults);
      setLoadingRec(false);
    }

    getRecommendationInfo();
  }, [recommendations]);

  useEffect(() => {
    if (chosenMedia === null || typeof chosenMedia !== "object") return;

    setCover(undefined);
    setLoadingChosenMed(false);

    async function getTheAlbumCover() {
      const newCover = await getAlbumCover(chosenMedia["id"]);
      setCover(newCover);
    }
    getTheAlbumCover();
  }, [chosenMedia]);

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
            <form
              onChange={handleSearch}
              onSubmit={(e) => e.preventDefault()}
              className="search-bar-form"
            >
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

          <div className="chosen-album">
            {loadingChosenMed ? (
              <p>Loading album...</p>
            ) : (
              <>
                <img src={cover} alt={chosenMedia["title"]} />
                <div className="chosen-album-info">
                  <p>{chosenMedia["title"]}</p>
                  <p>{chosenMedia["artist"]["name"]}</p>
                </div>
              </>
            )}
          </div>

          <div className="recommendations">
            <p>Similar To</p>
            <div className="container">
              {loadingRec ? (
                <p>Loading recommendations...</p>
              ) : (
                results.map((album) => {
                  return (
                    <div
                      className="recommended-album"
                      key={album.id}
                      id={album.id}
                    >
                      <img
                        src={
                          album.cover === undefined
                            ? Loading
                            : album.cover || Missing
                        }
                        alt={album.title}
                      />

                      <div className="recommended-album-info">
                        <p>{album.title}</p>
                        <p>{album.artist}</p>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default Recommendations;
