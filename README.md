# personal-monitor-api
Project for developing a REST API using Django for storing, retrieving, and analysing personal information like finances, time tracking, etc. This API is intended to be *local-only* i.e. no cloud involved.

## Accessing the repository
On my work machine, accessing the repository can be tricky as this repository is created using my personal Github 
account (`tejas-kale`) whereas all my work-related repositories use my work-specific GitHub account
(`tejas-kale-relayr`). In order to perform most GitHub-related operations on this repository, I will need to 
specify my GitHub ID (`tejas-kale`) and a personal access token. This can be found in the GitHub section of my 
password manager. Examples include:

```shell
# Clone repository
git clone https://tejas-kale@github.com/tejas-kale/cricket-analysis-api.git
```

## `docker-compose` commands
- To execute `flake8` on our source code, execute the command: `docker-compose run --rm app sh -c "flake8"`
- To create a new Django project in the container, execute the command:
`docker-compose run --rm app sh -c "django-admin startproject app ."`. The `.` at the end ensures that the
project is created in our root directory. If not specified, an `app` sub-directory will be created by Django
inside the `app` directory leading to a confusing directory structure.
