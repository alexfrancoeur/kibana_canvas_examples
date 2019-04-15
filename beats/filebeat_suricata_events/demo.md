# ElasticGov Demo

### Security Operations Team Report
---
#### Add SEV1 Metric

##### SQL
```sql
SELECT COUNT(*) total
FROM "filebeat-*"
WHERE event.severity=1
AND "@timestamp" > NOW() - INTERVAL 7 DAYS
```
---
#### Event Duration Percentile Metric

##### SQL
```sql
SELECT PERCENTILE(event.duration, 95)*0.000011574 AS "perc_95",PERCENTILE(event.duration, 50)*0.000011574 AS "perc_50"
FROM "filebeat-*"
WHERE "@timestamp" > NOW() - INTERVAL 7 DAYS
```
---
#### Event Duration Percentile Time Series

##### SQL
```sql
SELECT HISTOGRAM("@timestamp", INTERVAL 1 HOURS) AS x, PERCENTILE(event.duration, 95) AS "perc_95",PERCENTILE(event.duration, 50) AS "perc_50"
FROM "filebeat-*"
WHERE "@timestamp" > NOW() - INTERVAL 7 DAYS
GROUP BY x
```
----

#### SEV1 Context Markdown

##### SQL
```sql
SELECT host.hostname host, COUNT(*) total
FROM "filebeat-*"
WHERE event.severity=1
AND "@timestamp" > NOW() - INTERVAL 7 DAYS
GROUP BY host
ORDER BY total DESC
```

##### Markdown
```javascript
| markdown "Out of the **" {math "sum(total)" | formatNumber "0.[00a]"}
"** SEV1's that occurred this past week, the top three hosts were **"
{getCell "host" row=0} "** with **" {getCell "total" row=0 | formatNumber "0.[0a]"} "**, **"
{getCell "host" row=1} "** with **" {getCell "total" row=1 | formatNumber "0.[0a]"} "**, **"
{getCell "host" row=2} "** with **" {getCell "total" row=2 | formatNumber "0.[0a]"} "**"
```

##### CSS
```css
.canvasRenderEl {
    background: #e6ebf2;
    border: 1px solid #ddd;
    border-left: 3px solid #00bfb3;
    color: #666;
    page-break-inside: avoid;
    font-family: monospace;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 0.5em;
    max-width: 100%;
    overflow: auto;
    padding: 0.5em 0.5em;
    display: block;
    word-wrap: break-word;
}
```
---
#### Alerts Context Markdown

##### SQL
```sql
SELECT suricata.eve.alert.category alert, count(*) total
FROM "filebeat-*"
WHERE "@timestamp" > NOW() - INTERVAL 7 DAYS
GROUP BY alert
ORDER BY total desc
```

##### Markdown
```javascript
| markdown "Out of the **" {math "sum(total)" | formatNumber "0.[00a]"}
"** alerts that occurred this past week, **" {getCell "alert"}
"** was the most frequent with **" {getCell "total" | formatNumber "0.[0a]"} "** total alerts"
```

##### CSS
```css
.canvasRenderEl {
    background: #e6ebf2;
    border: 1px solid #ddd;
    border-left: 3px solid #00bfb3;
    color: #666;
    page-break-inside: avoid;
    font-family: monospace;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 0.5em;
    max-width: 100%;
    overflow: auto;
    padding: 0.5em 0.5em;
    display: block;
    word-wrap: break-word;
}
```
---
#### Add Date to Title

##### Markdown
```javascript
| markdown "Security Operations Team - " {date | formatDate "MMMM D, YYYY"}
```
### Pew Pew Map

Customer dark TMS layer from Carto: `http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png`
