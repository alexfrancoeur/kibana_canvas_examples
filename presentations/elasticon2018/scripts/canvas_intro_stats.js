const elasticsearch = require('elasticsearch');
const runInterval = require('interval-promise');

const doctype = 'canvas_stats';
const statusList = ['good', 'warning', 'severe'];
const urlList = [
  'http://canvas.elastic.co/',
  'http://canvas.elastic.co/stories/installing.html',
  'http://canvas.elastic.co/videos/index.html',
  'http://canvas.elastic.co/index.html/stories/index.html',
  'http://canvas.elastic.co/blog/00029-more-example-workpads.html',
  'http://canvas.elastic.cox/reference/index.html',
  'http://canvas.elastic.co/reference/functions.html',
  'http://canvas.elastic.co/videos/101-welcome1.html',
  'http://canvas.elastic.co/blog/00028-canvas-and-coffee.html',
];
const osList = ['ios', 'osx', 'win xp', 'win 8', 'win 7'];
const countryList = ['US', 'CN', 'CA', 'FR', 'BR', 'DE', 'JP', 'AU'];

// pull values from ENV
const {
  ELASTICSEARCH_HOST = 'localhost',
  ELASTICSEARCH_PORT = 9200,
  ELASTICSEARCH_USERNAME,
  ELASTICSEARCH_PASSWORD,
  ELASTICSEARCH_LOG = 'error',
  ELASTICSEARCH_INDEX = 'canvas_stats',
  INDEX_INTERVAL = 3,
} = process.env;

const indexMapping = {
  timestamp: { type: 'date' },
  total_downloads: { type: 'long' },
  unique_users: { type: 'long' },
  reports_generated: { type: 'long' },
  office_displays: { type: 'long' },
  custom_plugins: { type: 'long' },
  mini_apps: { type: 'long' },
  status: { type: 'keyword' },
  url: { type: 'keyword' },
  os: { type: 'keyword' },
  country: { type: 'keyword' },
};

function getRandomInt(min = 1, max = 100) {
  //The maximum is exclusive and the minimum is inclusive
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

function pickRandom(list) {
  const idx = getRandomInt(0, list.length);
  return list[idx];
}

async function createConnection() {
  const host = `${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}`;
  console.log(`Connecting to elasticsearch at: ${host}`);
  const config = {
    host,
    log: ELASTICSEARCH_LOG,
  };

  if (ELASTICSEARCH_USERNAME) {
    console.log('Authentication enabled');
    config.httpAuth = `${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD}`;
  } else {
    console.log('Authentication skipped');
  }

  // make sure we can connect to the node
  const client = new elasticsearch.Client(config);
  await client.ping();
  return client;
}

async function createIndex(client) {
  return client.indices
    .create({
      index: ELASTICSEARCH_INDEX,
      body: {
        settings: {},
        mappings: {
          [doctype]: {
            properties: indexMapping,
          },
        },
      },
    })
    .catch(err => {
      if (err instanceof elasticsearch.errors.BadRequest) {
        return client.indices.get({ index: ELASTICSEARCH_INDEX });
      }

      throw err;
    });
}

function getDoc() {
  return {
    timestamp: new Date(new Date().getTime() + getRandomInt(-45000, 45000)),
    total_downloads: getRandomInt(1000, 10000000),
    unique_users: getRandomInt(1000, 5000000),
    reports_generated: getRandomInt(1000, 10000000),
    office_displays: getRandomInt(1000, 1000000),
    custom_plugins: getRandomInt(1000, 500000),
    mini_apps: getRandomInt(1000, 50000),
    status: pickRandom(statusList),
    url: pickRandom(urlList),
    os: pickRandom(osList),
    country: pickRandom(countryList),
  };
}

async function indexDocs(client, count = 1) {
  const body = [];
  for (let i = 0; i < count; i++) {
    body.push({ index: { _index: ELASTICSEARCH_INDEX, _type: doctype } });
    body.push(getDoc());
  }

  console.log(`Indexing ${body.length / 2} documents`);

  const res = await client.bulk({
    body,
  });

  if (res.errors) throw new Error(res.items[0].index.error.reason);
  return res;
}

(async function() {
  try {
    const client = await createConnection();
    await createIndex(client);
    await indexDocs(client, getRandomInt(3, 10));
    if (INDEX_INTERVAL != null)
      runInterval(
        () => indexDocs(client, getRandomInt(3, 10)),
        INDEX_INTERVAL * 1000
      );
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
})();
