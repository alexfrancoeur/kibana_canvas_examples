[Boston Data set - 2017 Reported Energy and Water Metrics](https://data.boston.gov/dataset/building-energy-reporting-and-disclosure-ordinance/resource/5b027436-5213-4be6-ab5f-485a03f74500?inner_span=True)

[Boston.gov Branding](https://www.boston.gov/news/colors-typefaces-and-look-bostongov)

Use this [demo script](https://docs.google.com/document/d/1k3kjuscjdLkW_ECTMT9qE9Ck8Rdcl6IELiZO78aboWs/edit#bookmark=id.g37wsibtoia2) to build as part of a demo.

### Ingest data
Add the csv, template and configuration to your logstash directory and run the following command
```
cat boston_energy_water_metrics_2017.csv | bin/logstash -f boston_energy_water_metrics_2017.conf
```

Drag and drop the Canvas workpad in the Canvas app

Dashboard
![screenshot](https://github.com/alexfrancoeur/kibana_canvas_examples/blob/master/images/boston_dashboard.png)

Canvas Workpad
![screenshot](https://github.com/alexfrancoeur/kibana_canvas_examples/blob/master/images/boston_workpad.png)
