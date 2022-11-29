import re
from datetime import datetime, timedelta

import requests
from base64 import b64encode

from credentials import TOGGL_LOGIN, TOGGL_PASSWORD, JIRA_DOMAIN
from jira_wl_updater import jira_add_wl


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
    return result


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
        raise Exception(f"Code: {data.status_code}, Error: {data.json()}")

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


def get_key_by_description(description: str):
    # Try search task number
    match = re.search(r'((?:COR|CON|FRONT|WEB|SUP|BUS|TESTS|ORG|AGG|ARC).\d{1,6})', description)
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


def run():
    for wl in get_sorted_aggregated_time_points():
        print(f"{format_time(wl.duration)}\t"
              f"|\tLink: {get_link_by_description(wl.description)}\t"
              f"| {wl.description} \t "
              f"| {wl.last_time}")
        key = get_key_by_description(wl.description)
        if key is None:
            key = input(f"Input key (predicted: {key}): ")
        jira_add_wl(
            key,
            time_seconds=wl.duration,
            begin_time=convert_timestamp_from_toggle_to_jira(wl.last_time),
            description=input("Input WL:"))


if __name__ == "__main__":
    run()
