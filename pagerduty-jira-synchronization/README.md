# Project installation and configuration

Clone the project:

```
git clone git@github.com:filetrust/gw-proxy-serverless.git
```

and cd to the project directory:

```
cd pagerduty-jira-synchronization
```

Make and activate a virtual environment:

```
python -m env env
source env/bin/activate
```

Install `serverless`:

```
npm install -g serverless
```

and other dependencies:

```
npm install
```

# Configure Jira

Sign up and create a project.

Go to [API tokens](https://id.atlassian.com/manage/api-tokens) and
create API token.

Copy `.env.example` to `.env` and edit it. Put your email to
`JIRA_USER_EMAIL`, put the API token to `JIRA_API_TOKEN`, put your
atlassian root URL (e.g. https://username.atlassian.net) to
`JIRA_SERVER_URL`. Put the key of your project to `JIRA_PROJECT_KEY`
(you can find the key in the list of the existing projects).

# Deploy serverless application

In order to deploy the application execute the following command:

```
sls deploy
```

The command should output an endpoint URL, for instance:

```
[...]
endpoints:
  POST - https://oqzgxd0euf.execute-api.us-east-1.amazonaws.com/dev/pagerduty-webhook
[...]

```

This is an endpoint for a PagerDuty webhook.

# Configure PagerDuty webhook

Go to [Extensions](https://atykhonov.pagerduty.com/extensions) page,
click on `New Extension`, select `Generic V2 Webhook`, put into `Name`
some name (e.g. `pjsync`), select an existing PagerDuty service
(create it if it doesn't exist) and input the PagerDuty webhook URL
into `URL` field. Click `Save`.

After this the serverless application should be executed each time
when a new incident is created.
