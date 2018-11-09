# scripts

### canvas_intro_stats

Indexes fake stats data to `canvas_stats`. Requires NodeJS 8+ and the `elasticsearch` and `interval-promise` modules.

You can use the included Dockerfile to make this easier:

- Build the docker image: `docker build -t elasticon2018-stats-index .`
- Run the docker image: `docker run --rm elasticon2018-stats-index`

### Environment variables

By default, the script will connect to localhost:9200, without auth, and write documents every 3 seconds. The docker container will connect to your host machine by default.

You can modify the following with environment variables.

var | default | description
--- | ------- | -----------
ELASTICSEARCH_HOST | 'localhost' (or 'host.docker.internal' in Docker) | Hostname to connect to
ELASTICSEARCH_PORT | 9200 | Port to connect to
ELASTICSEARCH_USERNAME | | Username to use (optional)
ELASTICSEARCH_PASSWORD | | Password to use (optional)
ELASTICSEARCH_LOG | 'error' | Log setting for the elasticsearchjs client
ELASTICSEARCH_INDEX | 'canvas_stats' | Index to write to
INDEX_INTERVAL | 3 | Index writing interval, in seconds

If you are using security, for example, you can use the following with the Docker container:

```
docker run --rm -e ELASTICSEARCH_USERNAME=elastic -e ELASTICSEARCH_PASSWORD=changeme elasticon2018-stats-index
```
