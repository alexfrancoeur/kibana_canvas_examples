**Please note that there are image assets in this workpad that are not cannot be used for redistribution. This Canvas workpad is solely meant to be an example to learn from**

### Data set and branding

[Boston Data set - 2017 Reported Energy and Water Metrics](https://data.boston.gov/dataset/building-energy-reporting-and-disclosure-ordinance/resource/5b027436-5213-4be6-ab5f-485a03f74500?inner_span=True)

[Boston.gov Branding](https://www.boston.gov/news/colors-typefaces-and-look-bostongov)

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
