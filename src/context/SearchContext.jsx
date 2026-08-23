import { createContext, useContext, useState } from "react";
import { getAlbumCover, searchAlbums } from "../services/api";

const SearchContext = createContext();

export function SearchProvider({ children }) {
  const [openSearch, setOpenSearch] = useState(false);
  const [media, setMedia] = useState("Album");
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState();

  function handleMediaClick(e) {
    setMedia(e.currentTarget.textContent);
  }

  async function handleSearch(e) {
    e.preventDefault();

    if (!searchQuery.trim()) return;
    if (loading) return;

    setResults([]);
    setLoading(true);

    try {
      const searchResults = await searchAlbums(searchQuery);

      setResults(searchResults);
      setError(null);

      searchResults.forEach(async (album) => {
        try {
          const cover = await getAlbumCover(album.id);

          setResults((currentResults) =>
            currentResults.map((currentAlbum) =>
              currentAlbum.id === album.id
                ? { ...currentAlbum, cover }
                : currentAlbum,
            ),
          );
        } catch {
          // Album has no cover / cover request failed
        }
      });
    } catch (err) {
      console.log(err);
      setError("Failed to search albums");
    } finally {
      setLoading(false);
    }
  }

  return (
    <SearchContext.Provider
      value={{
        openSearch,
        setOpenSearch,
        media,
        setMedia,
        searchQuery,
        setSearchQuery,
        results,
        setResults,
        error,
        loading,
        handleMediaClick,
        handleSearch,
        page,
        setPage,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
}

export function useSearch() {
  return useContext(SearchContext);
}
