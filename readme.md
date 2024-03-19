# Github issue creator

## Description

Have you had the situation where you've added all your user stories to the README.md file, but then you have to rewrite them, add the labels and assignee on the project board? Well, this script will do that for you.

## Getting started (REST API)

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

```python
user_stories = [
  {
    "title": "<title>",
    "related_epic": "Epic:",
    "user_story": "<user story>",
    "acceptance_criteria": "<acceptance criteria>",
    "further_tasks": "<further tasks>",
    "labels": ["user story", "<label2>"],
  }.

]

```

5. Add your epics to the epics list in the `main.py` file in the following format:

```python
epics = [
  {
    "title": "<title>",
    "description": "<description>",
    "labels": ["epic", "<label2>"]
  }
]
```

5. Run the script with `python3 main.py`

## Getting started (GraphQL)

There is also an option to use the GraphQL API. The benefit of using this API is that you can also interact more with the project board, like updating the custom fields on issues, which had been added to the project board.

### Personal Access Token

To use this API, you need to [create a personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) and add it to the .env file. At the time of writing this, [fine-grained personal access tokens](https://github.blog/2022-10-18-introducing-fine-grained-personal-access-tokens-for-github/) can not yet permit you to update projects, so the please use a classic personal access token instead. The permissions needed are:

- repo
- workflow
- admin:org
- user
- project

### Environment Variables

There are a number of environment variables that you need to set in order to use the GraphQL API. You can find the values for these variables using the [GitHub GraphQL API Explorer](https://docs.github.com/en/graphql/overview/explorer). Here are the queries you can use:

#### Query to get the Repo ID

```graphql
{
  repository(owner: "<your-github-username>", name: "<your-repo-name>") {
    ... on Repository {
      id
    }
  }
}
```

#### Query to get the Project ID

This query outputs the first 10 projects in the repository. You can change the `first` argument to get more projects. The number of the project from the URL is the `number` field in the query.

```graphql
{
  viewer {
    projectsV2(first: 10) {
      ... on ProjectV2Connection {
        nodes {
          number
          id
        }
      }
    }
  }
}
```

#### Query to get the Label IDs

> [!TIP]
> The `first` argument is set to 20. You can change this to get more labels. You labels may also differ from the ones in the same env file below.

```graphql
{
  repository(owner: "<your-github-username>", name: "<your-repo-name>") {
    labels(first: 20) {
      nodes {
        name
        id
      }
    }
  }
}
```

#### Query to get the Field Config ID

> [!WARNING]
> You will need to run this query for each custom field you want to get the ID for.

```graphql
{
  node(id: "<your-project-id>") {
    ... on ProjectV2 {
      field(name: "<your-field-name>") {
        ... on ProjectV2Field {
          name
          id
        }
      }
    }
  }
}
```

Create a .env file with the following variables:

```
GITHUB_TOKEN = "<your-personal-access-token>"

PROJECT_ID = "<your-project-id>"
REPO_ID = "<your-repo-id>"
LABEL_IDS = {
    "bug": "<your-label-id>",
    "documentation": "<your-label-id>",
    "duplicate": "<your-label-id>",
    "enhancement": "<your-label-id>",
    "user story": "<your-label-id>",
    "epic": "<your-label-id>",
    "must have": "<your-label-id>",
    "should have": "<your-label-id>",
    "won't have": "<your-label-id>",
    "could have": "<your-label-id>",
    "pull request": "<your-label-id>"
}

ESTIMATE_FIELD_CONFIG_ID = "<your-field-config-id>"
AREA_FIELD_CONFIG_ID = "<your-field-config-id>"
IMPORTANCE_FIELD_CONFIG_ID = "<your-field-config-id>"
```

### Query to get the project ID

Command to GPT:

```
For **User Stories**, use the following structure:

{
    "title": "User story: [Title of the User Story]",
    "user_story": "As a [type of user], I want [feature/desire] so that [rationale/outcome].",
    "acceptance_criteria": "- [Criteria 1]\n- [Criteria 2]\n- [Criteria 3]",
    "further_tasks": "- [ ] [Task 1]\n- [ ] [Task 2]\n- [ ] [Task 3]",
    "labels": ["user story"],
    "importance": [Importance Level],
    "estimate": [Time Estimate],
    "area": "[Area of development] [Corresponding emoji]"
}

-   Replace `[Title of the User Story]` with the feature's title.
-   Fill in the `[type of user]`, `[feature/desire]`, and `[rationale/outcome]` based on the feature details.
-   Add the specific `[Criteria 1/2/3]` that define the completion of the user story.
-   Specify the `[Task 1/2/3]` as actionable steps required to achieve the user story.
-   Set `[Importance Level]` and `[Time Estimate]` based on the details provided.
-   `[Area of development]` should be replaced with `Frontend`, `Backend`, or `Fullstack`. Use `🖥️` for Frontend, `🦾` for Backend, and `🌐` for Fullstack.

For **Epics**, format them as follows:

{
    "title": "Epic: [Title of the Epic]",
    "description": "[Brief description of the epic's purpose and scope]",
    "labels": ["epic"],
    "estimate": [Time Estimate],
    "importance": "[Importance Level]",
    "area": "[Area of development] [Corresponding emoji]"
}

-   Replace `[Title of the Epic]` with the epic's title.
-   Fill in the `[Brief description of the epic's purpose and scope]`.
-   Set `[Time Estimate]` and `[Importance Level]` based on the details provided.
-   `[Area of development]` should be replaced with `Frontend`, `Backend`, or `Fullstack`. Use `🖥️` for Frontend, `🦾` for Backend, and `🌐` for Fullstack.
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Also feel free to create issue templates and add them. 😄
