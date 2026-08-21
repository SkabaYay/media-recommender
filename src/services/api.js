export async function searchAlbums(query) {
  const response = await fetch(
    `https://musicbrainz.org/ws/2/release/?query=${encodeURIComponent(query)}&fmt=json`,
    {
      headers: {
        "User-Agent": "media-recommender/1.0 honng2552@gmail.com",
      },
    },
  );

  const data = await response.json();

  return data.releases.map((release) => ({
    id: release.id,
    title: release.title,
    artist: release["artist-credit"]?.[0]?.name ?? "Unknown Artist",
    cover: undefined,
  }));
}

export async function getAlbumCover(releaseId) {
  const response = await fetch(
    `https://coverartarchive.org/release/${releaseId}`,
  );

  if (!response.ok) {
    return null;
  }

  const data = await response.json();

  const frontCover = data.images.find((image) => image.front);

  return frontCover?.thumbnails?.["500"] ?? null;
}
