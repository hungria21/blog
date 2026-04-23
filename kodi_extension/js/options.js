document.addEventListener('DOMContentLoaded', () => {
  const hostInput = document.getElementById('host');
  const portInput = document.getElementById('port');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const status = document.getElementById('status');

  // Load saved settings
  chrome.storage.sync.get(['kodiHost', 'kodiPort', 'kodiUsername', 'kodiPassword'], (items) => {
    hostInput.value = items.kodiHost || '';
    portInput.value = items.kodiPort || '8080';
    usernameInput.value = items.kodiUsername || '';
    passwordInput.value = items.kodiPassword || '';
  });

  // Save settings
  document.getElementById('save').addEventListener('click', () => {
    const host = hostInput.value;
    const port = portInput.value;
    const username = usernameInput.value;
    const password = passwordInput.value;

    chrome.storage.sync.set({
      kodiHost: host,
      kodiPort: port,
      kodiUsername: username,
      kodiPassword: password
    }, () => {
      status.textContent = 'Settings saved.';
      setTimeout(() => {
        status.textContent = '';
      }, 2000);
    });
  });
});
