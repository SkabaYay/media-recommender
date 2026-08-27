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

export function getReleaseGroupMetadata(releaseGroupId) {
  return post("http://localhost:5000/get-release-group-metadata", {
    releaseGroupId,
  });
}

export function getRecommendations(title, id) {
  return post("http://localhost:5000/get-recommendations", {
    title,
    id,
  });
}

export async function getAlbumCover(releaseGroupId) {
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
