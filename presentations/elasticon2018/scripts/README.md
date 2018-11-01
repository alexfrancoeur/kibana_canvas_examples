# scripts

### canvas_intro_stats.py

Indexes fake stats data to `canvas_stats`. Requires python3 and the `elasticsearch` and `pytz` modules.

You can use the included Dockerfile to make this easier:

- Edit the `canvas_intro_stats.py` to point at your local cluster
- Build the docker image: `docker build -t elasticon2018-stats-index .`
- Run the docker image: `docker run elasticon2018-stats-index`
