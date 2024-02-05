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
There is a config file for customizing the script: config.json. The file contains two key elements:

teams: a list of commands used to generate a search pattern for tasks in JIRA.
patterns: an array of objects, each of which contains a key (task key in JIRA) and a regex (regular expression for searching in the description).

Examples of parsing descriptions from Toggle to Jira key are provided in the tests.py file. Don't forget to update it after editing the config!