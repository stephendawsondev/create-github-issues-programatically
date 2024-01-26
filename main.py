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


# User story mapping to labels
priority_mapping = {
    "won't have": "wont-have",
    "could have": "could-have",
    "should have": "should-have",
    "must have": "must-have",
}

# Your GitHub username
username = "your_github_username"

# Your project column ID
project_column_id = "your_project_column_id"

# List of user stories
user_stories = [
    {"summary": "Account creation", "description": "As a user, I can create an account so that I can access personalized features and save my preferences.", "priority": "must have"},
    # Add all your user stories here...
]

for story in user_stories:
    title = f"USER STORY: {story['summary']}"
    body = story['description']
    labels = [priority_mapping[story['priority']], "user story"]
    assignees = [username]

    create_issue(title, body, labels, assignees, project_column_id)

print("All issues created.")
