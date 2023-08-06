# Jira data

![Python package](https://github.com/KhalidCK/jiradata/workflows/Python%20package/badge.svg)

> Cause sometimes you need to sort out your issues

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

They are issues in json format retrieved using the JIRA REST API.

What I found convenient is to use the [search API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/#api-rest-api-2-search-post) with JQL.

For example, using [httpie](https://httpie.org/) :

`config.json`

```json
{
  "jql": "project = QA",
  "startAt": 0,
  "maxResults": 2,
  "fields": ["id", "key"]
}
```

Command line

```sh
cat config.json|http -a myusername post 'https://<site-url>/rest/api/2/search'
```

## Related

- [Export results to microsoft Excel](https://confluence.atlassian.com/jira061/jira-user-s-guide/searching-for-issues/working-with-search-result-data/exporting-search-results-to-microsoft-excel)
- [Jira python](https://github.com/pycontribs/jira)