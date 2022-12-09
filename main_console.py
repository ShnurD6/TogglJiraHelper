from common import format_time, get_link_by_description, get_key_by_description, get_description_without_jira_key, \
    get_sorted_aggregated_time_points, convert_timestamp_from_toggle_to_jira
from jira_wl_updater import jira_add_wl


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
