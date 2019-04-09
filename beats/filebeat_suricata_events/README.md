This example is built off of fake suricata events using ECS 7.0

#### Mock Data
Add the [index template](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates.html) found in `mappings_filebeat.json` in this directory

Load up the python script `filebeat-ecs.py` to with `python filebeat-ecs.py` to start ingesting fake and randomized suricata logs

#### Workpad

Drag & drop `Security Operations Team.json` into Canvas

![screenshot](https://github.com/alexfrancoeur/kibana_canvas_examples/blob/master/images/filbeat_suricata_events.png)
![screenshot](https://github.com/alexfrancoeur/kibana_canvas_examples/blob/master/images/filbeat_suricata_events_fullscreen.png)
