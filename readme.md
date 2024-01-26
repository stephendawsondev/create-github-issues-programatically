# Github issue creator

## Description

Have you had the situation where you've added all your user stories to the README.md file, but then you have to rewrite them, add the labels and assignee on the project board? Well, this script will do that for you.

## Installation

1. Clone the repository
2. Create a .env file with the following variables:

   - GITHUB_TOKEN = 'your-api-token'
   - REPO = 'your-username'
   - ASSIGNEES = ['your-username']
   - PROJECT_ID = 'your-project-id' (a number in the URL)
   - PROJECT_COLUMN_NAME = 'your-default-column-name'

## Usage

1. Get your GitHub API token from in your GitHub settings:
   - Settings -> Developer settings -> Personal access tokens -> Generate new token -> Select all the repo -> Select issues editing permissions
2. Get your project ID from the URL of your project board and add to your env.py file
3. Get your default column name from the URL of your project board
4. Add your user stories to the user_stories list in the `main.py` file in the following format:

```

user_stories = [
  {
    "title": "<title>",
    "related_epic": "Epic:",
    "user_story": "<user story>",
    "acceptance_criteria": "<acceptance criteria>",
    "further_tasks": "<further tasks>",
    "labels": ["<label1>", "<label2>"]
  }.
  {
    "title": "<title>",
    "related_epic": "Epic:",
    "user_story": "<user story>",
    "acceptance_criteria": "<acceptance criteria>",
    "further_tasks": "<further tasks>",
    "labels": ["<label1>", "<label2>"]
  }
]

```

5. Run the script with `python3 main.py`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Also feel free to create issue templates and add them. 😄
