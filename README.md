### Twitter collector — mentions of cryptocurrencies in tweets<br><sup>Results are available at https://storage.zahrevsky.com/twitter-collector/tweets-dumped.json<br/></sup>

Using Twitter API, Twitter collector monitors 142 crypto influencers, that were manually selected. In tweets of those influencers, mentions of currencies are counted per given time period. Result looks like this:
![Statistic screenshot](https://storage.zahrevsky.com/twitter-collector/stats-example.png)

**Note** Dumped results are in JSON format and should be post-processed to obtain an image as above.

<br/>

**Under the hood**<br/>Using Twitter API, tweets are stored in Redis DB. This helps to count even mentions in deleted tweets, as it is a common practice for an influencer to delete it's tweets.

Instead of access via an API, data from database is simply dumped into JSON file, which is publically available at https://storage.zahrevsky.com/twitter-collector/tweets-dumped.json. This approach saves a lot of time in development, and is OK, as this tool is not commonly used and doesn't need to be fast or work in real-time.
