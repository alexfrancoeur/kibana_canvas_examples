# Canvas Deep Dive Demo

#### Title

##### Markdown
```javascript
| markdown "Elastic Tweets Sentiment Analysis - " {date | formatDate "MMMM D, YYYY"}
```
---
#### Total Tweets Metric
##### SQL
```sql
SELECT COUNT(*) tweets
FROM
"twitter-sentiment"
```
---
#### Total Tweets Over Time
##### SQL
```sql
SELECT HISTOGRAM("@timestamp", INTERVAL 1 DAY) day, COUNT (*) tweets
FROM
"twitter-sentiment"
GROUP BY day
```
---
#### Pie Chart
##### SQL
```sql
SELECT "sentiment.language.keyword" as language, COUNT(*) as count
FROM "twitter-sentiment"
WHERE language IS NOT NULL
GROUP BY language
ORDER BY count DESC
```
---
#### Image Reveal
##### SQL
```sql
SELECT PERCENTILE(sentiment.documentSentiment.score,95) AS sentiment
FROM "twitter-sentiment*"
```
---
#### Dynamic Markdown
##### SQL
```sql
SELECT COUNT(*) tweets, PERCENTILE(sentiment.documentSentiment.score,95) "95_perc_sent", PERCENTILE(sentiment.documentSentiment.score,50) "50_perc_sent", PERCENTILE(sentiment.documentSentiment.magnitude,95) "95_perc_mag", PERCENTILE(sentiment.documentSentiment.magnitude,50) "50_perc_mag"
FROM "twitter-sentiment"
```
##### Markdown
```javascript
| markdown "Out of the **" {getCell "tweets" | formatNumber "0.00a"} "** tweets, the 95th percentile sentiment score was **"
  {getCell "95_perc_sent" | formatNumber "0.00a"} "** with a magnitude of **" {getCell "95_perc_mag" | formatNumber "0.00a"}
  "** and the 50th percentile had a sentiment score of **" {getCell "50_perc_sent" | formatNumber "0.00a"} "** and with a magnitude of **"
  {getCell "50_perc_mag" | formatNumber "0.00a"} "**"
```
---
#### Score vs. Magnitude
##### SQL
```sql
SELECT TRUNCATE("sentiment.documentSentiment.magnitude",3) AS magnitude, TRUNCATE("sentiment.documentSentiment.score",3) AS sentiment, COUNT(*) AS count
FROM "twitter-sentiment"
GROUP BY magnitude, sentiment
```
---
#### Twitter Feed
##### SQL
```sql
SELECT text
FROM "twitter-sentiment*"
WHERE "sentiment.documentSentiment.score" IS NOT NULL
ORDER BY "@timestamp" DESC
LIMIT 40
```
##### CSS
```css
.canvasDataTable__tr {
  display: inline-block;
  background: white;
  font-family: "Helvetica Neue", Roboto, "Segoe UI", Calibri, sans-serif;
  font-size: 14px;
  line-height: 16px;
  border-color: #eee #ddd #bbb;
  border-radius: 5px;
  border-style: solid;
  border-width: 1px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
  margin: 10px 5px;
  padding: 0 16px 16px 16px;
  max-width: 468px;
}

.canvasDataTable__tr p {
  font-size: 16px;
  font-weight: normal;
  line-height: 20px;
}

.canvasDataTable__tr a {
  color: inherit;
  font-weight: normal;
  text-decoration: none;
  outline: 0 none;
}

.canvasDataTable__tr:hover,
.canvasDataTable__tr a:focus {
  text-decoration: underline;
}
```
---
#### Dropdown menu
#### SQL
```sql
SELECT "sentiment.language.keyword"
FROM "twitter-sentiment"
```
#### SQL
```sql
SELECT "sentiment.language.keyword"
FROM "twitter-sentiment"
```
#### Values
`sentiment.language.keyword`
