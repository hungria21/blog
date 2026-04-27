import json
import requests

def test_details():
    res = requests.get('https://api.telegra.ph/createAccount', params={
        'short_name': 'Tester',
        'author_name': 'Tester'
    }).json()
    access_token = res['result']['access_token']

    content = [
        {
            "tag": "details",
            "children": [
                {"tag": "summary", "children": ["Click me"]},
                {"tag": "p", "children": ["Hidden content"]}
            ]
        }
    ]

    res = requests.post('https://api.telegra.ph/createPage', data={
        'access_token': access_token,
        'title': 'Test Details Tag',
        'content': json.dumps(content),
        'return_content': 'true'
    }).json()

    print(res)

if __name__ == "__main__":
    test_details()
