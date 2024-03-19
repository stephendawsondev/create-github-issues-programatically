import requests
import json
import env
import time

# GraphQL endpoint
GRAPHQL_URL = 'https://api.github.com/graphql'
HEADERS = {
    "Authorization": f"Bearer {env.GITHUB_TOKEN}",
    "Content-Type": "application/json",
}

# User stories and epics to add
user_stories = [

]

epics = [

]


# Queries and Mutations
create_issue_query = """
mutation CreateIssue($input: CreateIssueInput!) {
  createIssue(input: $input) {
    issue {
      id
      number
      title
    }
  }
}
"""

update_field_value_query = """
mutation UpdateProjectV2ItemFieldValue($input: UpdateProjectV2ItemFieldValueInput!) {
  updateProjectV2ItemFieldValue(input: $input) {
    clientMutationId
  }
}
"""


def run_query(query, variables):
    request = requests.post(
        GRAPHQL_URL,
        json={'query': query, 'variables': variables},
        headers=HEADERS
    )
    response = request.json()
    if request.status_code == 200 and 'errors' not in response:
        return response
    else:
        raise Exception(f"""
                        GraphQL query failed: {json.dumps(response, indent=4)}
                        """)


def find_project_item_id(issue_id):
    print(f"Fetching project item for issue: {issue_id}...")
    get_project_item_query = f"""
    {{
      node(id: "{issue_id}") {{
        ... on Issue {{
          projectItems(first: 1) {{
            nodes {{
              id
              estimate: fieldValueByName(name: "Estimate") {{
                ...on ProjectV2ItemFieldNumberValue {{
                  number
                  id
                }}
              }}
              area: fieldValueByName(name: "Area") {{
                ...on ProjectV2ItemFieldTextValue {{
                  text
                  id
                }}
              }}
              importance: fieldValueByName(name: "Importance") {{
                ...on ProjectV2ItemFieldNumberValue {{
                  number
                  id
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """

    result = run_query(get_project_item_query, {})
    if ('data' in result and 'node' in result['data']
            and 'projectItems' in result['data']['node']):
        project_items = result['data']['node']['projectItems']['nodes']
        if project_items:
            project_item = project_items[0]
            return project_item['id']

    print("Error: No matching project item found for the issue.")
    return None, {}


# Create issues and update project fields
for story in user_stories:
    body = f"""
### If applicable, add a related Epic.\n\n{story.get('related_epic', '')}\n
Epic: \n\n
### User Story\n\n{story.get('user_story', story.get('description', ''))}\n\n
### Acceptance Criteria\n\n{story.get('acceptance_criteria', '')}\n
### Please ensure you've completed these tasks before marking the issue as done.\n
- [ ] Reviewed the user story for clarity and completeness.
- [ ] Identified and linked related issues or epics.
- [ ] Updated the issue with any relevant notes or feedback (to date).\n
### Please add any further tasks that need to be completed before the issue can be marked as done.\n
{story.get('further_tasks', '')}
""".strip()

    issue_variables = {
        "input": {
            "repositoryId": env.REPO_ID,
            "title": story["title"],
            "body": body,
            "labelIds": [env.LABEL_IDS[label] for label in story['labels']],
            **({"assigneeIds": story['assignees']} if 'assignees' in story and story['assignees'] else {})
        }
    }
    issue_result = run_query(create_issue_query, issue_variables)
    issue_id = issue_result["data"]["createIssue"]["issue"]["id"]

    # delay for 2 seconds
    time.sleep(2)

    # Fetch the project item ID
    project_item_id = find_project_item_id(issue_id)

    if project_item_id:
        # Mapping for field names to their respective env constants
        field_config_mapping = {
            "Estimate": env.ESTIMATE_FIELD_CONFIG_ID,
            "Area": env.AREA_FIELD_CONFIG_ID,
            "Importance": env.IMPORTANCE_FIELD_CONFIG_ID
        }
        # Update custom fields for the project item
        for field_name, field_value in [("Estimate", story["estimate"]), ("Area", story["area"]), ("Importance", story["importance"])]:
            # Determine the type of value to update based on the field name
            if field_name == "Estimate" or field_name == "Importance":
                value_type = "number"
            else:
                value_type = "text"

            # Format the value correctly based on its type
            formatted_value = {value_type: field_value}

            update_variables = {
                "input": {
                    "projectId": env.PROJECT_ID,
                    "itemId": project_item_id,
                    "fieldId": field_config_mapping[field_name],
                    "value": formatted_value
                }
            }

            run_query(update_field_value_query, update_variables)


for epic in epics:
    body = f"""
{epic.get('description', '')}
""".strip()

    issue_variables = {
        "input": {
            "repositoryId": env.REPO_ID,
            "title": epic["title"],
            "body": body,
            "labelIds": [env.LABEL_IDS[label] for label in epic['labels']],
            **({"assigneeIds": epic['assignees']} if 'assignees' in epic and epic['assignees'] else {})
        }
    }
    issue_result = run_query(create_issue_query, issue_variables)
    # Use issue ID directly
    issue_id = issue_result["data"]["createIssue"]["issue"]["id"]
    issue_number = issue_result["data"]["createIssue"]["issue"]["number"]
    issue_title = issue_result["data"]["createIssue"]["issue"]["title"]

    # delay for 2 seconds
    time.sleep(2)

    # Fetch the project item ID
    project_item_id = find_project_item_id(issue_id)

    if project_item_id:
        # Mapping for field names to their respective env constants
        field_config_mapping = {
            "Estimate": env.ESTIMATE_FIELD_CONFIG_ID,
            "Area": env.AREA_FIELD_CONFIG_ID,
            "Importance": env.IMPORTANCE_FIELD_CONFIG_ID
        }
        # Update custom fields for the project item
        for field_name, field_value in [("Estimate", epic["estimate"]), ("Area", epic["area"]), ("Importance", epic["importance"])]:
            # Determine the type of value to update based on the field name
            if field_name == "Estimate" or field_name == "Importance":
                value_type = "number"
            else:
                value_type = "text"

            # Format the value correctly based on its type
            formatted_value = {value_type: field_value}

            update_variables = {
                "input": {
                    "projectId": env.PROJECT_ID,
                    "itemId": project_item_id,
                    "fieldId": field_config_mapping[field_name],
                    "value": formatted_value
                }
            }
            run_query(update_field_value_query, update_variables)

print("All issues and their project fields have been created and updated.")
