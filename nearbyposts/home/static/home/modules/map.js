mapboxgl.accessToken = 'pk.eyJ1IjoieWVqMDAyIiwiYSI6ImNsMmNiM3RrZjBubDUzY3BkeDBjZWU1aTUifQ.S_KG7tc8i-osS3CZOA4D_g';

export function addMap() {
    const map = new mapboxgl.Map({
        container: 'map', // container ID
        style: 'mapbox://styles/mapbox/streets-v11', // style URL
        center: [-122.41735985586202,37.78091127755505], // starting position [lng, lat]
        zoom: 13 // starting zoom
    });

    map.addControl(new mapboxgl.NavigationControl());

    return map;
}

export function addMapCallback(map, mapCallback) {
    let geocoder = new MapboxGeocoder(
    {
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl
    }).on('result', (data) => {
        mapCallback(data);
    });

    map.addControl(geocoder);
}

/**
 * Converts array of posts to GeoJSON format
 * @param {Post[]} posts
 * @return {PostsGeoJSON} Posts in GeoJSON
 */
 export function convertToGeoJson(posts) {
    return {
        type: 'FeatureCollection',
        features: posts.map(post => {
            return {
                type: 'Feature',
                geometry: {
                    type: 'Point',
                    coordinates: [post.longitude, post.latitude]
                },
                properties: {
                    id: post.id,
                    title: post.title,
                    content: post.content,
                    tags: post.tags,
                    distance: post.distance,
                }
            }
        })
    }
}

/**
 * Display posts on map
 * @param {Object} map
 * @param {PostsGeoJSON} postsGeoJson
 */

 export function plotPostsOnMap(map, postsGeoJson) {
    for (let post of postsGeoJson.features) {
        // create a HTML element for each feature
        let el = document.createElement('div');
        el.className = 'post-pin';
        el.id = `post-${post.properties.id}`;

        // make a marker for each feature and add to the map
        new mapboxgl.Marker(el)
        .setLngLat(post.geometry.coordinates)
        .addTo(map);

        el.addEventListener('click', function(e) {
            /* Fly to the point */
            flyToPost(map, post);
            // Close all other popups and display popup for clicked post 
            displayPostDetails(map, post);
            // updateSelectedPost(post.properties.id);
        });
    }
}

/**
 * Zoom in-to a specific point on a map
 * @param {Object} map
 * @param {PostFeatureObject} point
 */
 export function flyToPost(map, point) {
    map.flyTo({
        center: point.geometry.coordinates,
        zoom: 17
    });
}

/**
 * Display post info on the map using a popup
 * @param {Object} map
 * @param {PostFeatureObject} point
 */
 export function displayPostDetails(map, point) {
    const popUps = document.getElementsByClassName('mapboxgl-popup');
    /** Check if there is already a popup on the map and if so, remove it */
    if (popUps[0]){
        popUps[0].remove();
    }

    const popup = new mapboxgl.Popup({ closeOnClick: false })
    .setLngLat(point.geometry.coordinates)
    .setHTML(`
        <details>
        <summary><h4>${point.properties.title}</h4></summary>
        <dl>
        <dt>Content</dt>
        <dd>${point.properties.content || 'N/A'}</dd>
        <dt>Tags</dt>
        <dd>${point.properties.tags || 'N/A'}</dd>
        </dl>
        </details>
        `)
    .addTo(map);
    return popup;
}