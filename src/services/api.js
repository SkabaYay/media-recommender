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

export async function getAlbumMetadata(releaseId) {
  const response = await fetch(
    `https://musicbrainz.org/ws/2/release/${releaseId}?inc=release-groups+artists&fmt=json`,
    {
      headers: {
        "User-Agent": "media-recommender/1.0 honng2552@gmail.com",
      },
    },
  );

  const data = await response.json();

  return data;
}

export async function getReleaseGroupMetadata(releaseGroupId) {
  const response = await fetch(
    `https://musicbrainz.org/ws/2/release-group/${releaseGroupId}?inc=tags+genres+artists&fmt=json`,
    {
      headers: {
        "User-Agent": "media-recommender/1.0 honng2552@gmail.com",
      },
    },
  );

  if (!response.ok) {
    throw new Error("Failed to fetch release group");
  }

  const data = await response.json();

  return data;
}

export async function getAlbumCover(releaseId) {
  const response = await fetch(
    `https://coverartarchive.org/release/${releaseId}`,
  );

  if (response.status === 404) {
    return undefined;
  }

  if (!response.ok) {
    return null;
  }

  const data = await response.json();

  const frontCover = data.images.find((image) => image.front);

  return frontCover?.thumbnails?.["500"] ?? null;
}
