mapboxgl.accessToken = 'pk.eyJ1IjoieWVqMDAyIiwiYSI6ImNsMmNiM3RrZjBubDUzY3BkeDBjZWU1aTUifQ.S_KG7tc8i-osS3CZOA4D_g';

/**
 * create a map instance and place it in 'map'
 */
export function addMap() {
    const map = new mapboxgl.Map({
        container: 'map', // map DOM id
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [-122.41735985586202, 37.78091127755505], // NEU-SF [longitude, latitude]
        zoom: 13 // initial zoom
    });
    map.addControl(new mapboxgl.NavigationControl()); // general navigation
    return map;
}

/**
 * add a mapCallback function to the geocoder location search
 */
export function addMapCallback(map, mapCallback) {
    // add geocoder to search for places
    let geocoder = new MapboxGeocoder(
    {
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl
    }).on('result', (data) => { //upon search result returns
        mapCallback(data);
    });

    map.addControl(geocoder);
}

/**
 * GeoJson is the standard way to transfer location-based info
 * hence converting the post data into GeoJson format
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
                    creator: post.creator,
                    updated_at: post.updated_at,
                    likes: post.liked_count,
                }
            }
        })
    }
}

/**
* Mark posts on the Map using GeoJson data
*/
export function plotPostsOnMap(map, postsGeoJson) {
    for (let post of postsGeoJson.features) {
        // create a HTML element for each feature
        let postEl = document.createElement('div');
        postEl.className = 'post-pin';
        postEl.id = `post-${post.properties.id}`;

        // make a marker for each feature and add to the map
        new mapboxgl.Marker(postEl)
        .setLngLat(post.geometry.coordinates)
        .addTo(map);

        postEl.addEventListener('click', function(e) {
            flyToPost(map, post); // Move to Post location
            displayPostDetails(map, post); // opens post details popup
        });
    }
}

/**
* Move to the post location and zoom in
*/
export function flyToPost(map, point) {
    map.flyTo({
        center: point.geometry.coordinates,
        zoom: 17
    });
}

/**
* Open up the popup containing the selected post's details
*/
export function displayPostDetails(map, point) {
    const popUps = document.getElementsByClassName('mapboxgl-popup');
    if (popUps[0]){
        popUps[0].remove();
    }
    const popup = new mapboxgl.Popup({ closeOnClick: true })
    .setLngLat(point.geometry.coordinates)
    .setHTML(`
        <div class="card bg-light mb-3" style="max-width: 18rem;">
        <img class="card-img-top" src="..." alt="Pet Picture">
        <div class="card-body">
        <h5 class="card-title">${point.properties.title}</h5>
        <p class="card-text">${point.properties.content || 'N/A'}</p>
        </div>
        <ul class="list-group list-group-flush">
        <li class="list-group-item">Tags: ${point.properties.tags || 'N/A'}</li>
        <li class="list-group-item">Likes: ${point.properties.likes}</li>
        <li class="list-group-item">By ${point.properties.creator}</li>
        </ul>
        <div class="card-footer">
        <small class="text-muted">Last updated at ${point.properties.updated_at}</small>
        </div>
        </div>
        `)
    .addTo(map);
    return popup;
}