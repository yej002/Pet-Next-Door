import {
    convertToGeoJson,
    plotPostsOnMap,
    displayPostDetails,
} from './map.js';

/**
 * Fetch list of nearby posts from a given latitude and longitude
 * @param {number} latitude
 * @param {number} longitude
 * @return {Promise<Post[]>} Array of posts
 */
 async function fetchNearbyPosts(longitude, latitude) {
    const response = await fetch(`/posts/?lng=${longitude}&lat=${latitude}`, {
        method: 'GET'
    });
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(Error(response.statusText));
    }
}

/**
 * Fetch and display nearby posts
 * @typedef {import('./map').PostsGeoJSON} PostsGeoJSON
 * @param {Object} map
 * @param {number} latitude
 * @param {number} longitude
 * @return {Promise<PostsGeoJSON>} Posts in GeoJSON
 */
 export async function displayNearbyPosts(map, longitude, latitude) {
    try {
        const posts = await fetchNearbyPosts(longitude, latitude);
        const postsGeoJson = convertToGeoJson(posts);
        plotPostsOnMap(map, postsGeoJson);
        return postsGeoJson;
    } catch(error) {
        console.error(error);
    }
}
