
last.fm-twitter


Posts your top 3 artsists from last.fm to twitter. 

Providing the -y or --yearly options will post your top 3 artists for the past twelve months.

Currently you need to use the -j or --json option to link to a secrets file with your API secrets for last.fm and twitter.

Format should be:

.. code-block:: JSON

    {"lastfm":
                {"key": "alphanumeric",
                "secret": "alphanumeric"},
    "twitter":
            {"consumer_key": "alphanumeric",
            "consumer_secret": "alphanumeric",
            "token_key": "alphanumeric-alphanumeric",
            "token_secret": "alphanumeric"}


After installing via pip, you can run python -m lastfmtwitter.lastfm_twitter -h to learn usage

official documentation at: http://server.ericsbinaryworld.com/gpl_code/lastfmtwitter/index.html
