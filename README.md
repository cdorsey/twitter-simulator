# Twitter Simulator
Uses Markov chains to simulate a user on Twitter. Invoked via user mention and keyword sent to a "bot" account. 

## Usage
Requires an account to send users back their formed tweets. Bot is activated when a user mentions them (bot's screen name should be defined in a file called name.txt) with a set keyword (defined at the top of main.py). A full set of Twitter API keys is also required. See https://dev.twitter.com/oauth/overview/application-owner-access-tokens for info

## Authorization
In order to authenticate with Twitter's API, create a file called keys.json in the following format:

    {
       "consumer":{
          "key":"ConsumerKey",
          "secret":"ConsumerSecret"
       },
       "access_token":{
          "key":"Access Key",
          "secret":"Access Secret"
       }
    }