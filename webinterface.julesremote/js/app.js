let kodi;
let activePlayerId = null;

document.addEventListener('DOMContentLoaded', async () => {
  // In a web interface hosted by Kodi, we can often assume the host is the same as the one serving the file
  const host = window.location.hostname;
  const port = window.location.port || '8080';

  kodi = new KodiAPI(host, port);

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

  // Settings button can be hidden or changed for the web interface version
  const settingsBtn = document.getElementById('open-settings');
  if (settingsBtn) settingsBtn.style.display = 'none';
}

function showMessage(text) {
  const overlay = document.getElementById('message');
  const messageText = document.getElementById('message-text');
  if (messageText) messageText.textContent = text;
  if (overlay) overlay.style.display = 'block';
  const content = document.getElementById('content');
  if (content) content.style.display = 'none';
}

function hideMessage() {
  const overlay = document.getElementById('message');
  if (overlay) overlay.style.display = 'none';
  const content = document.getElementById('content');
  if (content) content.style.display = 'grid';
}

async function loadView(view) {
  const content = document.getElementById('content');
  const title = document.getElementById('view-title');
  if (!content) return;
  content.innerHTML = 'Loading...';
  hideMessage();

  try {
    let data;
    switch (view) {
      case 'movies':
        if (title) title.textContent = 'Movies';
        data = await kodi.getMovies();
        renderMedia(data.movies, 'movie');
        break;
      case 'tvshows':
        if (title) title.textContent = 'TV Shows';
        data = await kodi.getTVShows();
        renderMedia(data.tvshows, 'tvshow');
        break;
      case 'music':
        if (title) title.textContent = 'Albums';
        data = await kodi.getAlbums();
        renderMedia(data.albums, 'album');
        break;
      case 'remote':
        if (title) title.textContent = 'Remote Control';
        content.innerHTML = '<div style="grid-column: 1/-1; text-align:center;">Remote UI Coming Soon</div>';
        break;
    }
  } catch (error) {
    showMessage('Error connecting to Kodi API.');
  }
}

function renderMedia(items, type) {
  const content = document.getElementById('content');
  if (!content) return;
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
    const playBtn = document.getElementById('btn-play');
    const stopBtn = document.getElementById('btn-stop');
    if (playBtn) {
        playBtn.addEventListener('click', () => {
            if (activePlayerId !== null) kodi.playPause(activePlayerId);
        });
    }
    if (stopBtn) {
        stopBtn.addEventListener('click', () => {
            if (activePlayerId !== null) kodi.stop(activePlayerId);
        });
    }
}

async function startStatusPolling() {
    setInterval(async () => {
        try {
            const players = await kodi.getActivePlayers();
            const playbackBar = document.getElementById('playback-bar');

            if (players && players.length > 0) {
                activePlayerId = players[0].playerid;
                if (playbackBar) playbackBar.style.display = 'flex';

                const item = await kodi.getItem(activePlayerId);
                if (item && item.item) {
                    const info = item.item;
                    const npTitle = document.getElementById('np-title');
                    const npSubtitle = document.getElementById('np-subtitle');
                    const npThumb = document.getElementById('np-thumb');

                    if (npTitle) npTitle.textContent = info.title || info.label;
                    if (npSubtitle) npSubtitle.textContent = info.artist ? info.artist.join(', ') : (info.year || '');

                    if (info.thumbnail && npThumb) {
                        npThumb.src = decodeKodiImage(info.thumbnail);
                    }
                }
            } else {
                activePlayerId = null;
                if (playbackBar) playbackBar.style.display = 'none';
            }
        } catch (e) {
            console.error('Polling error', e);
        }
    }, 2000);
}
