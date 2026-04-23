class KodiAPI {
  constructor(host, port, username = '', password = '') {
    this.url = `http://${host}:${port}/jsonrpc`;
    this.username = username;
    this.password = password;
  }

  async sendRequest(method, params = {}) {
    const body = {
      jsonrpc: '2.0',
      method: method,
      params: params,
      id: 1
    };

    const headers = {
      'Content-Type': 'application/json'
    };

    if (this.username && this.password) {
      const auth = btoa(`${this.username}:${this.password}`);
      headers['Authorization'] = `Basic ${auth}`;
    }

    try {
      const response = await fetch(this.url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.error) {
        throw new Error(`Kodi API error: ${data.error.message}`);
      }
      return data.result;
    } catch (error) {
      console.error('Kodi request failed:', error);
      throw error;
    }
  }

  // Player Methods
  getActivePlayers() {
    return this.sendRequest('Player.GetActivePlayers');
  }

  playPause(playerId) {
    return this.sendRequest('Player.PlayPause', { playerid: playerId });
  }

  stop(playerId) {
    return this.sendRequest('Player.Stop', { playerid: playerId });
  }

  getItem(playerId) {
    return this.sendRequest('Player.GetItem', {
      playerid: playerId,
      properties: ['title', 'artist', 'album', 'year', 'art', 'duration', 'thumbnail']
    });
  }

  // VideoLibrary Methods
  getMovies() {
    return this.sendRequest('VideoLibrary.GetMovies', {
      properties: ['title', 'year', 'art', 'rating', 'playcount'],
      sort: { method: 'title', order: 'ascending' }
    });
  }

  getTVShows() {
    return this.sendRequest('VideoLibrary.GetTVShows', {
      properties: ['title', 'year', 'art', 'playcount', 'episode'],
      sort: { method: 'title', order: 'ascending' }
    });
  }

  // AudioLibrary Methods
  getAlbums() {
    return this.sendRequest('AudioLibrary.GetAlbums', {
      properties: ['title', 'artist', 'year', 'art', 'rating'],
      sort: { method: 'title', order: 'ascending' }
    });
  }

  // Introspect
  introspect() {
      return this.sendRequest('JSONRPC.Introspect');
  }
}
