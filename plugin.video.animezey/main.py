import sys
import json
from urllib import request, parse
import xbmcgui
import xbmcplugin
import xbmcaddon

# Get addon handle and base URL
ADDON_HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]
SITE_URL = "https://1.animezey23112022.workers.dev"
DOWNLOAD_DOMAIN = "https://animezey16082023.animezey16082023.workers.dev"

# Drive names as seen on the site
DRIVE_NAMES = ["AnimeZeY - Animes e Desenhos", "AnimeZeY - Filmes e Séries"]

def build_url(query):
    return BASE_URL + "?" + parse.urlencode(query)

def get_api_data(path, page_index=0, page_token=None):
    url = f"{SITE_URL}/{path}"
    payload = {"page_index": page_index, "password": ""}
    if page_token:
        payload["page_token"] = page_token

    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = request.Request(url, data=data, headers=headers)
    try:
        with request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        xbmcgui.Dialog().notification("Erro", str(e), xbmcgui.NOTIFICATION_ERROR)
        return None

def list_drives():
    xbmcplugin.setContent(ADDON_HANDLE, 'videos')
    for i, name in enumerate(DRIVE_NAMES):
        url = build_url({"action": "list_path", "path": f"{i}:/"})
        li = xbmcgui.ListItem(label=name)
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(ADDON_HANDLE)

def list_path(path, page_index=0, page_token=None):
    xbmcplugin.setContent(ADDON_HANDLE, 'videos')
    result = get_api_data(path, page_index, page_token)
    if not result:
        xbmcplugin.endOfDirectory(ADDON_HANDLE, False)
        return

    files = result.get("data", {}).get("files", [])

    for f in files:
        name = f.get("name")
        mime_type = f.get("mimeType")

        if mime_type == "application/vnd.google-apps.folder":
            url = build_url({"action": "list_path", "path": f"{path}{parse.quote(name)}/"})
            li = xbmcgui.ListItem(label=name)
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)
        elif "video" in mime_type:
            link = f.get("link")
            if link:
                video_url = f"{DOWNLOAD_DOMAIN}{link}"
            else:
                video_url = f"{SITE_URL}/{path}{parse.quote(name)}"

            url = build_url({"action": "play", "video_url": video_url})
            li = xbmcgui.ListItem(label=name)
            li.setInfo("video", {"title": name})
            li.setProperty("IsPlayable", "true")
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=False)

    # Check for next page
    next_page_token = result.get("nextPageToken")
    if next_page_token:
        url = build_url({
            "action": "list_path",
            "path": path,
            "page_index": page_index + 1,
            "page_token": next_page_token
        })
        li = xbmcgui.ListItem(label=">> Próxima Página")
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(ADDON_HANDLE)

def router(paramstring):
    params = dict(parse.parse_qsl(paramstring[1:]))
    if not params:
        list_drives()
    else:
        action = params.get("action")
        if action == "list_path":
            list_path(
                params.get("path"),
                int(params.get("page_index", 0)),
                params.get("page_token")
            )
        elif action == "play":
            play_video(params.get("video_url"))

def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem=play_item)

if __name__ == "__main__":
    router(sys.argv[2])
