import twitter

twitter_consumer_key = 'pRFp145vTu8Gvq1O5VhsdCx1B'
twitter_consumer_secret = '0Gg4511PEeNuAQNS8uENGkCXSBsUz4RhOITQT6YjE6e2m6wKNY'

twitter_access_token = '133239839-8rlvnxA91qYSroNv8KzyPFoulxiitWpqyoJhFNmx'
twitter_token_secret = 'qTjFuYubwxyCBohHqBJMUAo48PF0lfIisTyXmN6BQnrk2'

api = twitter.Api(
    consumer_key=twitter_consumer_key,
    consumer_secret=twitter_consumer_secret,
    access_token_key=twitter_access_token,
    access_token_secret=twitter_token_secret)

# Gets the trends from the api based on their Woeid [Yahoo Where on earth identifiers]
trends = api.GetTrendsWoeid('23424833')

# for trend in trends:
#     # print('*' * 30)
#     print(trend.name)
#     # print(trend.query)
#     print(trend.timestamp)
#     # print(trend.url)
#     # print('*' * 30)
#     print("\n")

# print('{} trending tweets'.format(len(trends)))

tweets = api.GetSearch(trends[0].query, count=100, lang='el')

print(tweets[0].text)

print(len(tweets))
