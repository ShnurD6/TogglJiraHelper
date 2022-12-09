from common import format_time, get_link_by_description, get_key_by_description, get_description_without_jira_key, \
    get_sorted_aggregated_time_points, convert_timestamp_from_toggle_to_jira
from jira_wl_updater import jira_add_wl

import PySimpleGUI as sg

font = ("Helvetica", 20)


def get_current_layout(current_wl, entered_key=None):
    print(f"Current element: {format_time(current_wl.duration)}\t"
          f"|\tLink: {get_link_by_description(current_wl.description)}\t"
          f"| {current_wl.description} \t "
          f"| {current_wl.last_time}")

    if entered_key is not None:
        key = entered_key
    else:
        key = get_key_by_description(current_wl.description)

    result = [[sg.Text(f'Toggle WL: {current_wl.description}', font=font)],
              [sg.Text(f'Time: {format_time(current_wl.duration)}', font=font)]]

    if key:
        result += [[sg.Text(f'Key: {key}', font=font)],
                [sg.Text('Enter WL:', font=font), sg.InputText(
                    default_text=get_description_without_jira_key(current_wl.description), font=font)],
                [sg.Button('Re-enter key', font=font), sg.Button('Log', bind_return_key=True, font=font)]]
    else:
        result += [[sg.Text(f'Cannot parse key :(', font=font)],
                [sg.Text('Enter Key:', font=font), sg.InputText(font=font)],
                [sg.Button('Save key', font=font, bind_return_key=True)]]

    return result


def run():
    sg.theme('DarkAmber')

    wl_iter = iter(get_sorted_aggregated_time_points())
    current_wl = next(wl_iter)
    entered_key = None
    current_layout = get_current_layout(current_wl)

    while True:
        window = sg.Window('Toggle Jira Helper', current_layout)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            # if user closes window or clicks cancel
            break
        if event == 'Save key':
            entered_key = values[0]
            current_layout = get_current_layout(current_wl, entered_key)
        elif event == 'Re-enter key':
            current_layout = get_current_layout(current_wl, "")
        elif event == 'Log':
            jira_add_wl(
                entered_key or get_key_by_description(current_wl.description),
                time_seconds=current_wl.duration,
                begin_time=convert_timestamp_from_toggle_to_jira(current_wl.last_time),
                description=values[0])
            entered_key = None
            current_wl = next(wl_iter)
            current_layout = get_current_layout(current_wl, entered_key)
        window.close()


if __name__ == "__main__":
    run()
