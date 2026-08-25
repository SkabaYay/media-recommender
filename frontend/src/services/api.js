async function post(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return await response.json();
}

export function searchAlbums(query) {
  return post("http://localhost:5000/search-albums", {
    query,
  });
}

export function getAlbumMetadata(releaseId) {
  return post("http://localhost:5000/get-album-metadata", {
    releaseId,
  });
}

export function getReleaseGroupMetadata(releaseGroupId) {
  return post("http://localhost:5000/get-release-group-metadata", {
    releaseGroupId,
  });
}

export function getRecommendations(title) {
  return post("http://localhost:5000/get-recommendations", {
    title,
  });
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

export async function getAlbumCoverWithReleaseGroup(releaseGroupId) {
  const response = await fetch(
    `https://coverartarchive.org/release-group/${releaseGroupId}`,
  );

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    return null;
  }

  const data = await response.json();

  const frontCover = data.images?.find((image) => image.front);

  return frontCover?.thumbnails?.["500"] ?? frontCover?.image ?? null;
}
