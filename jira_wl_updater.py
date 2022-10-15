import requests

from credentials import JIRA_LOGIN, JIRA_API_KEY, JIRA_DOMAIN


def jira_post_api_request(url, query):
    print(f"Jira API: {url}, Post: {query}")

    response = requests.post(
        url,
        json=query,
        auth=(JIRA_LOGIN, JIRA_API_KEY)
    )

    print(f"Jira API: {response}, Reason: {response.reason}")


def jira_add_wl(key: str, time_seconds: int, begin_time: str, description: str):
    url = f"https://{JIRA_DOMAIN}.atlassian.net/rest/api/3/issue/{key}/worklog"

    query = {
        "timeSpentSeconds": time_seconds,
        "comment": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": f"{description}",
                            "type": "text"
                        }
                    ]
                }
            ]
        },
        "started": begin_time
    }

    jira_post_api_request(url=url, query=query)