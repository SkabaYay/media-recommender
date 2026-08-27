import { createContext, useContext, useState } from "react";
import {
  getAlbumCover,
  searchAlbums,
  getReleaseGroupMetadata,
  getRecommendations,
} from "../services/api";
import { useNavigate } from "react-router-dom";

const SearchContext = createContext();

export function SearchProvider({ children }) {
  const [openSearch, setOpenSearch] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState();
  const [recommendations, setRecommendations] = useState([]);
  const [chosenMedia, setChosenMedia] = useState();
  const [loadingRec, setLoadingRec] = useState(true);
  const [loadingChosenMed, setLoadingChosenMed] = useState(true);

  const navigate = useNavigate();

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

  async function handleMediaClickOnSearch(e) {
    const currentAlbumId = e.currentTarget.id;

    setOpenSearch(false);
    setSearchQuery("");
    setRecommendations([]);

    setLoadingRec(true);
    setLoadingChosenMed(true);

    navigate("/recommendations");

    const release = await getReleaseGroupMetadata(currentAlbumId);
    setChosenMedia(release);

    const releaseTitle = release["title"];
    const releaseId = release["id"];
    const newRecommmendations = await getRecommendations(
      releaseTitle,
      releaseId,
    );
    setRecommendations(newRecommmendations);

    return recommendations;
  }

  return (
    <SearchContext.Provider
      value={{
        openSearch,
        setOpenSearch,
        searchQuery,
        setSearchQuery,
        results,
        setResults,
        error,
        loading,
        handleSearch,
        page,
        setPage,
        handleMediaClickOnSearch,
        recommendations,
        chosenMedia,
        loadingRec,
        setLoadingRec,
        loadingChosenMed,
        setLoadingChosenMed,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
}

export function useSearch() {
  return useContext(SearchContext);
}
