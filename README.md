# Jira‑Slack AI Automation

Automate notifications and simple issue actions between Jira and Slack using AI-driven routing and message parsing.

## Overview
This repository provides a lightweight bridge between Jira and Slack that uses AI to:
- Parse and summarize Slack messages mentioning issues.
- Create and update Jira issues from Slack.
- Route notifications to the right Slack channels or users based on issue content and context.

It is intended as a starter kit you can adapt to your team's workflow (bots, webhooks, or serverless functions).

## Features
- Forward important Jira updates to Slack channels.
- Create and update Jira issues from Slack messages using natural language.
- Use AI (optional) to classify messages and suggest issue fields (priority, labels, assignee).
- Configurable mapping between Jira projects and Slack channels.

## Installation
1. Clone the repo:
   git clone https://github.com/chilly23/Jira-slack-AI-automation.git
2. Create a virtual environment and install requirements:
   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
   pip install -r requirements.txt

## Configuration
Create a `.env` file at the repo root with the following variables:

- JIRA_BASE_URL=https://your-domain.atlassian.net
- JIRA_EMAIL=your-jira-email@example.com
- JIRA_API_TOKEN=your-jira-api-token
- SLACK_BOT_TOKEN=xoxb-...
- SLACK_SIGNING_SECRET=...
- AI_PROVIDER_API_KEY=optional-api-key-for-llm

Adjust any project/channel mappings in `config.yaml` (example included in repo).

## Usage
- Run the integration:
  python app.py

- Use the provided Slack slash commands or message shortcuts (see docs in `docs/`) to create or summarize issues.

## Examples
- `/create-issue <summary> — <description>`: Create a Jira issue from Slack.
- `@bot summarize <issue-key>`: Post a short summary to the channel.

## Development
- Tests: pytest
- Lint: flake8 or pylint

## Security
- Never commit secrets. Store tokens in environment variables or a secrets manager.
- Restrict bot permissions to the minimum required scopes.

## Contributing
Contributions welcome. Open an issue or PR describing your change.

## License
Specify a license (e.g., MIT). If you don't have one yet, create a LICENSE file.
