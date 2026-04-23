let kodi;
let activePlayerId = null;

document.addEventListener('DOMContentLoaded', async () => {
  if (typeof chrome === 'undefined' || !chrome.storage) {
    showMessage('Running outside of Chrome Extension environment.');
    return;
  }

  const settings = await chrome.storage.sync.get(['kodiHost', 'kodiPort', 'kodiUsername', 'kodiPassword']);

  if (!settings.kodiHost) {
    showMessage('Please configure Kodi settings first.');
    return;
  }

  kodi = new KodiAPI(settings.kodiHost, settings.kodiPort, settings.kodiUsername, settings.kodiPassword);

  setupNavigation();
  setupControls();
  loadView('movies');
  startStatusPolling();
});

function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item[data-view]');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      navItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      loadView(item.dataset.view);
    });
  });

  document.getElementById('open-settings').addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });
}

function showMessage(text) {
  const overlay = document.getElementById('message');
  const messageText = document.getElementById('message-text');
  messageText.textContent = text;
  overlay.style.display = 'block';
  document.getElementById('content').style.display = 'none';
}

function hideMessage() {
  document.getElementById('message').style.display = 'none';
  document.getElementById('content').style.display = 'grid';
}

async function loadView(view) {
  const content = document.getElementById('content');
  const title = document.getElementById('view-title');
  content.innerHTML = 'Loading...';
  hideMessage();

  try {
    let data;
    switch (view) {
      case 'movies':
        title.textContent = 'Movies';
        data = await kodi.getMovies();
        renderMedia(data.movies, 'movie');
        break;
      case 'tvshows':
        title.textContent = 'TV Shows';
        data = await kodi.getTVShows();
        renderMedia(data.tvshows, 'tvshow');
        break;
      case 'music':
        title.textContent = 'Albums';
        data = await kodi.getAlbums();
        renderMedia(data.albums, 'album');
        break;
      case 'remote':
        title.textContent = 'Remote Control';
        content.innerHTML = '<div style="grid-column: 1/-1; text-align:center;">Remote UI Coming Soon</div>';
        break;
    }
  } catch (error) {
    showMessage('Error connecting to Kodi. Check your settings.');
  }
}

function renderMedia(items, type) {
  const content = document.getElementById('content');
  content.innerHTML = '';

  if (!items || items.length === 0) {
    content.innerHTML = '<p>No items found.</p>';
    return;
  }

  items.forEach(item => {
    const card = document.createElement('div');
    card.className = 'media-card';

    let thumb = 'https://via.placeholder.com/120x180?text=No+Image';
    if (item.art && (item.art.poster || item.art.thumb)) {
        const artUrl = item.art.poster || item.art.thumb;
        // Kodi image URLs often need decoding if they are image:// format
        thumb = decodeKodiImage(artUrl);
    }

    card.innerHTML = `
      <img class="media-poster" src="${thumb}" onerror="this.src='https://via.placeholder.com/120x180?text=Error'">
      <div class="media-info">
        <div class="media-title">${item.title || item.label}</div>
        <div class="media-year">${item.year || ''}</div>
      </div>
    `;
    content.appendChild(card);
  });
}

function decodeKodiImage(url) {
    if (url.startsWith('image://')) {
        const encoded = url.substring(8, url.length - 1);
        return `${kodi.url.replace('/jsonrpc', '')}/image/${encoded}`;
    }
    return url;
}

function setupControls() {
    document.getElementById('btn-play').addEventListener('click', () => {
        if (activePlayerId !== null) kodi.playPause(activePlayerId);
    });
    document.getElementById('btn-stop').addEventListener('click', () => {
        if (activePlayerId !== null) kodi.stop(activePlayerId);
    });
}

async function startStatusPolling() {
    setInterval(async () => {
        try {
            const players = await kodi.getActivePlayers();
            const playbackBar = document.getElementById('playback-bar');

            if (players && players.length > 0) {
                activePlayerId = players[0].playerid;
                playbackBar.style.display = 'flex';

                const item = await kodi.getItem(activePlayerId);
                if (item && item.item) {
                    const info = item.item;
                    document.getElementById('np-title').textContent = info.title || info.label;
                    document.getElementById('np-subtitle').textContent = info.artist ? info.artist.join(', ') : (info.year || '');

                    if (info.thumbnail) {
                        document.getElementById('np-thumb').src = decodeKodiImage(info.thumbnail);
                    }
                }
            } else {
                activePlayerId = null;
                playbackBar.style.display = 'none';
            }
        } catch (e) {
            console.error('Polling error', e);
        }
    }, 2000);
}
