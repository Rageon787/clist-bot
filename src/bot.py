import discord  
import os 
from dotenv import load_dotenv
import requests
import json 
import re 

load_dotenv() 
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN') 
CLIST_TOKEN = os.getenv('CLIST_TOKEN') 
CLIST_AUTHORIZATION = os.getenv('AUTHORIZATION') 
URL = "https://clist.by:443/api/v4/contest/" + CLIST_AUTHORIZATION

class MyClient(discord.Client): 
    def input_cleaner(self, query_str) -> list[str]:
        pass 
    async def on_ready(self):
        print('bot is running') 
    async def on_message(self, message):
        if message.author == self.user:
            return
        user_query = message.content 
        user_query = user_query.split() 
        if user_query[0].startswith("$contests"):
            """
            max number contests shown -> 100 
            Note: only returns upcoming contests, for past contests use $past_contests 
            $contests (default) -> returns all upcoming contests 
            $contests +timeframe -> returns all upcoming contests in the specified time frame 
            $contests -platform -> returns all upcoming contests in the specified platform 
            """
            response = requests.get(URL + "&limit=5&upcoming=true") 
            if response.status_code == 200:
                data = response.json() 
                result_message = "" 
                for contest in data['objects']:
                    result_message += f"{contest['event']} {contest['host']} \n" 
                await message.channel.send(result_message)       
            else:
                print(f"failure: {response.status_code}")
            
        elif user_query[0].startswith("$past_contests"):
            """
            max number of contests shown -> 100 
            $past_contests (default) -> returns all past contests before 
            $past_contests -> return all past contests in the specified time frame 
            $past_contests +timeframe -> returns all past contests in the specified time frame 
            $past_contests -platform -> returns all past contests in the specified platform  
            """
        return 
    
def main() -> None: 
    intents = discord.Intents.default() 
    intents.message_content = True 
    client = MyClient(intents = intents) 
    client.run(token=DISCORD_TOKEN)  
    
    

if __name__ == "__main__":
    main()  
