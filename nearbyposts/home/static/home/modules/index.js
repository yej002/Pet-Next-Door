import {
    displayNearbyPosts,
} from './posts.js';

import {
    addMap,
    addMapCallback,
} from './map.js';

export const USERNAME = document.body.getAttribute("data-username");

const map = addMap();

addMapCallback(map, (data) => {
    displayNearbyPosts(map, data.result.center[0], data.result.center[1]);
});