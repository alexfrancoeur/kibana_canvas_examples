FROM python:3-alpine

WORKDIR /app
ADD canvas_intro_stats.py ./

RUN pip install elasticsearch pytz

CMD [ "python", "./canvas_intro_stats.py" ]
