# Jira data

> Cause sometimes you need to sort out your issues

Programmatic way to pull out your issues.

## Install

`pip install jiradata`

## How to use ?

Write a csv report

```shell
cat response.json | jiradata myreport.csv
```

With some 'Epic' and issue related to it :

```shell
cat response.json |jiradata --epic-field customfield_10000 report.csv
```

## Hold up what is this `reponse.json` ?

Issues in json format from the JIRA REST API.

What I found convenient is to use the [search API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/#api-rest-api-2-search-post)) with JQL.

You can chain unix style arguments using [httpie](https://httpie.org/)

config.json

```json
{
  "jql": "project = QA",
  "startAt": 0,
  "maxResults": 2,
  "fields": ["id", "key"]
}
```

Command line (redirect stdout to the right location)

```sh
cat config.json|http -a myusername post 'https://<site-url>/rest/api/2/search'
```

## Related

- Built in jira : [Export results to microsoft Excel](https://confluence.atlassian.com/jira061/jira-user-s-guide/searching-for-issues/working-with-search-result-data/exporting-search-results-to-microsoft-excel)
- https://github.com/pycontribs/jira