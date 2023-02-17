# Toggle Jira Helper

## Description
The program takes the time logs from the Toggle API for the last day and logs them to the Jira API.

## Install requirements
`pip3 install -r requirements.txt`

## Launch console version
JIRA_DOMAIN=X JIRA_LOGIN=X TOGGL_LOGIN=X TOGGL_PASSWORD=X JIRA_API_KEY=X python3 main_console.py

## Launch GUI version
JIRA_DOMAIN=X JIRA_LOGIN=X TOGGL_LOGIN=X TOGGL_PASSWORD=X JIRA_API_KEY=X python3 main_gui.py

## Customization
Find the `get_key_by_description` function in common.py and customize it for your needs if necessary.
Don't forget to add the test to test.py!

The teams are listed in the jira_team_pattern variable in the same common.py file.