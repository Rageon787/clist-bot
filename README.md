# clist-bot
Discord bot to fetch contests from the contest aggregator clist.by with personalized pings 

# Basic commands 
``$contests`` -> fetches the next 100 upcoming contests with 10 per page (Done) \
``$past-contests`` -> fetches the last 100 contests with 10 per page (Done) 

# Optional parameters 
``+[platform_name]`` -> fetches upcoming contests in that platform (e.g +cf/codeforces, +lc/leetcode, +cc/codechef)  

# Set your pings 
The most important and distinct of this specific is the ability to set your own pings. 

To set your pings, you must first invoke the ``$contests [optional parameters]`` to fetch the list of upcoming contests. Then pick the id of the contest your interested and set the ping using the following command: 

``$ping [contest_id]`` 

To set pings for multiple contests:
``ping [contest_id1] [contest_id2] .... [contest_idN]``

If you've set your pings correctly, you will be pinged around 24 hours before the contest

Everyone who set a ping for a particular contest, will be pinged simultaneously 

# Remove your pings 
To remove your pings: \ 
1) invoke ``$mypings`` which gives you a list of all your contest pings with the contest id 
2) You can remove your pings in a similar way to setting your pings: ``$removeping [contest_id1] [contest_id2] .... [contest_idN]``
