import { useState, useEffect } from "react";
import "../css/Home.css";
import Search from "../components/Search";

function Home() {
  const [openSearch, setOpenSearch] = useState(false);
  const [media, setMedia] = useState("Album");

  function handleMediaClick(e) {
    if (e.target.textContent != media) {
      setMedia(e.target.textContent);
    }
    console.log("Switched to " + e.target.textContent);
  }

  return (
    <>
      <header>
        <nav>
          <a href="#">Media Recommender</a>
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
            <form action="#">
              <input
                type="text"
                placeholder={`Search ${media}...`}
                onChange={(e) => setOpenSearch(e.target.value.length > 0)}
              />
            </form>

            {openSearch && <Search />}
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
