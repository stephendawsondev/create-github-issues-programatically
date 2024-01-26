import requests
import env


def get_column_id(project_id, column_name):
    """ Get the column ID for the given project and column name """
    url = f"https://api.github.com/projects/{project_id}/columns"
    headers = {
        "Authorization": f"token {env.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.inertia-preview+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        columns = response.json()
        for column in columns:
            if column['name'] == column_name:
                return column['id']
    return None


def create_issue(title, body=None, labels=[], assignees=[], project_column_id=None):
    """ Create an issue on github.com using the given parameters. """
    url = f"https://api.github.com/repos/{env.REPO}/issues"
    headers = {
        "Authorization": f"token {env.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    issue = {"title": title, "body": body or "",
             "labels": labels, "assignees": assignees}
    response = requests.post(url, json=issue, headers=headers)

    if response.status_code == 201:
        print(f"Issue created successfully: {title}")
        issue_data = response.json()
        if project_column_id:
            add_issue_to_project(issue_data['number'], project_column_id)
        return issue_data
    else:
        print(f"Failed to create issue: {response.content}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Request Payload: {issue}")
        return None


def add_issue_to_project(issue_number, project_column_id):
    """ Add an issue to a project column """
    url = f"https://api.github.com/projects/columns/{project_column_id}/cards"
    headers = {
        "Authorization": f"token {env.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.inertia-preview+json"
    }
    card_content = {
        "content_id": issue_number,
        "content_type": "Issue"
    }
    response = requests.post(url, json=card_content, headers=headers)

    if response.status_code == 201:
        print(f"Issue added to project successfully: {issue_number}")
    else:
        print(f"Failed to add issue to project: {response.content}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Request Payload: {card_content}")


project_column_id = get_column_id(env.PROJECT_ID, env.PROJECT_COLUMN_NAME)

user_stories = [
    # User story dictionaries go here
]


standard_tasks = (
    "- [ ] Reviewed the user story for clarity and completeness.\n"
    "- [ ] Identified and linked related issues or epics.\n"
    "- [ ] Updated the issue with any relevant notes or feedback (to date)."
)

for story in user_stories:
    title = story["title"]
    body = (
        f"### If applicable, add a related Epic.\n\n{story['related_epic']}\n\n"
        f"### User Story\n\n{story['user_story']}\n\n"
        f"### Acceptance Criteria\n\n{story['acceptance_criteria']}\n\n"
        f"### Please ensure you've completed these tasks before marking the issue as done.\n\n{standard_tasks}\n\n"
        f"### Please add any further tasks that need to be completed before the issue can be marked as done.\n\n{story['further_tasks']}"
    )
    labels = story["labels"]
    assignees = env.ASSIGNEES

    create_issue(title, body, labels, assignees, project_column_id)
print("All issues created.")
