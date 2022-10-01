from datetime import datetime, timedelta

import requests
from base64 import b64encode

from credentials import TOGGL_LOGIN, TOGGL_PASSWORD


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

    sorted_aggregated_wls = {}
    for worklog in data.json():
        wl_class = Worklog(
            description=worklog['description'],
            duration=int(worklog['duration']),
            last_time=worklog['stop'])

        if wl_class.description in sorted_aggregated_wls.keys():
            sorted_aggregated_wls[wl_class.description] += wl_class
        else:
            sorted_aggregated_wls[wl_class.description] = wl_class

    return sorted(sorted_aggregated_wls.values(), key=lambda wl: wl.last_time, reverse=True)


def run():
    for wl in get_sorted_aggregated_time_points():
        print(f"Description: {wl.description}, Duration: {format_time(wl.duration)}")


if __name__ == "__main__":
    run()
