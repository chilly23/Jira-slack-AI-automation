import os, sys, json, base64, requests
from slack_sdk import WebClient

slack = WebClient(token="API1")

jira_base = "https://velansworkspace-46333384.atlassian.net"

import base64

email = "mail_id"
token = "API2"

auth_string = f"{email}:{token}"

jira_auth = base64.b64encode(
    auth_string.encode("utf-8")
).decode("utf-8")

jira_headers = {"Authorization": f"Basic {jira_auth}", "Content-Type": "application/json"}
jira_project = "KAN"
slack_channel = "C0B9UNHDDRU"
or_key = "API3"

def ask(messages):
    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {or_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemma-4-31b-it:free",
            "messages": messages
        }
    )

    print("Status:", res.status_code)
    print("Response:", res.text)

    data = res.json()

    if "choices" not in data:
        raise Exception(f"OpenRouter Error: {data}")

    return data["choices"][0]["message"]
def extract_actions(transcript):
    prompt = f"Extract all action items from this meeting transcript. Return ONLY a JSON array, no markdown. Each item: {{\"title\": string, \"assignee\": string or null, \"due\": string or null, \"context\": string}}\n\nTranscript:\n{transcript}"
    msg = ask([{"role": "user", "content": prompt}])
    followup = ask([
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": msg.get("content"), "reasoning_details": msg.get("reasoning_details")},
        {"role": "user", "content": "Make sure you haven't missed any action items and the JSON is valid. Return the final JSON array only."}
    ])
    return json.loads(followup["content"])

def create_jira_ticket(action):
    body = {
        "fields": {
            "project": {"key": jira_project},
            "summary": action["title"],
            "description": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": action.get("context", "")}]}]
            },
            "issuetype": {"name": "Task"}
        }
    }
    res = requests.post(f"{jira_base}/rest/api/3/issue", headers=jira_headers, json=body)
    if not res.ok:
        raise Exception(f"Jira error {res.status_code}: {res.text}")
    return res.json()

def post_slack_summary(actions, tickets):
    lines = []
    for action, ticket in zip(actions, tickets):
        key = ticket.get("key", "ERR")
        url = f"{jira_base}/browse/{key}"
        who = f" → {action['assignee']}" if action.get("assignee") else ""
        due = f" (due: {action['due']})" if action.get("due") else ""
        lines.append(f"• <{url}|{key}>{who}{due}: {action['title']}")
    slack.chat_postMessage(channel=slack_channel, text="*Meeting Action Items*\n" + "\n".join(lines))

def run():
    if len(sys.argv) < 2:
        print("Usage: python main.py transcript.txt")
        sys.exit(1)

    transcript = open(sys.argv[1]).read()
    print("Extracting action items...")
    actions = extract_actions(transcript)
    print(f"Found {len(actions)} action items")

    tickets = []
    for action in actions:
        print(f"Creating ticket: {action['title']}")
        ticket = create_jira_ticket(action)
        tickets.append(ticket)
        print(f"  → {ticket['key']}")

    print("Posting Slack summary...")
    post_slack_summary(actions, tickets)
    print("Done.")

run()