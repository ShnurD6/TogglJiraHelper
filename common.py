import re
from base64 import b64encode
from datetime import datetime, timedelta
from http import HTTPStatus

import requests

from credentials import JIRA_DOMAIN, TOGGL_LOGIN, TOGGL_PASSWORD

jira_team_pattern = r'((?:COR|CON|FRONT|WEB|SUP|BUS|TESTS|ORG|AGG|ARC).\d{1,6})'


class Worklog:
    def __init__(self, description, duration, last_time):
        self.description = description
        self.duration = duration
        self.last_time = last_time

    def __add__(self, other):
        assert self.description == other.description
        return Worklog(
            description=self.description,
            duration=self.duration + other.duration,
            last_time=max(self.last_time, other.last_time))

    def __repr__(self):
        return f"WlObj[" \
               f"Description:{self.description}, " \
               f"Duration:{self.duration}, " \
               f"LastTime:{self.last_time}" \
               f"]"


def format_time(sum_time_in_seconds):
    result = ""
    seconds = sum_time_in_seconds % 60
    if seconds:
        result += f"{seconds}s"
    minutes = (sum_time_in_seconds // 60) % 60
    if minutes:
        result = f"{minutes}m " + result
    hours = (sum_time_in_seconds // 60 // 60) % 60
    if hours:
        result = f"{hours}h " + result
    return result if result else "0s"


def get_sorted_aggregated_time_points(
        start=datetime.today().date(),
        end=(datetime.today() + timedelta(days=1)).date()):
    data = requests.get(
        'https://api.track.toggl.com/api/v9/me/time_entries',
        headers={
            'content-type': 'application/json',
            'Authorization': 'Basic %s' % b64encode(bytes(f"{TOGGL_LOGIN}:{TOGGL_PASSWORD}", 'utf-8')).decode("ascii")},
        params={
            'start_date': start,
            'end_date': end
        })

    if data.status_code != 200:
        raise Exception(f"Code: {data.status_code} ({HTTPStatus(data.status_code).phrase}), "
                        f"Error: {data.json() if data.text else None}")

    sorted_aggregated_wls = {}
    for worklog in data.json():
        wl_class = Worklog(
            description=worklog['description'],
            duration=int(worklog['duration']),
            last_time=worklog['stop'])

        if wl_class.last_time is None:
            continue

        if wl_class.description in sorted_aggregated_wls.keys():
            sorted_aggregated_wls[wl_class.description] += wl_class
        else:
            sorted_aggregated_wls[wl_class.description] = wl_class

    return sorted(sorted_aggregated_wls.values(), key=lambda wl: wl.last_time, reverse=True)


def get_description_without_jira_key(description: str):
    return re.sub(jira_team_pattern, "", description)


def get_key_by_description(description: str):
    # Try search task number
    match = re.search(jira_team_pattern, description)
    if match is not None:
        return f"{match.group(0)}"
    # Try search StandUps / Retro / DEMO / Backlog / 1n1
    if re.search(
            r'(standup|retro|status|ретро|организационные|demo|демо|backlog|беклог|1n1)',
            description.lower()) is not None:
        return f"ORG-7"
    # Try search Interview
    if re.search(r'(собеседование|собес|кандидат|тестов|отклик)', description.lower()) is not None:
        return f"ORG-2"


def get_link_by_description(description: str):
    parsed_key = get_key_by_description(description)
    if parsed_key:
        return f"https://{JIRA_DOMAIN}.atlassian.net/browse/{parsed_key}"


def convert_timestamp_from_toggle_to_jira(ts: str) -> str:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M:%S.000+0000")
