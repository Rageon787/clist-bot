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
CONTEST_URL = "https://clist.by:443/api/v4/contest/" + CLIST_AUTHORIZATION
RESOURCE_URL = "https://clist.by:443/api/v4/resource/" + CLIST_AUTHORIZATION


platform_shorthand = {} 

class MyClient(discord.Client): 
    
    def get_platforms(self): 
        response = requests.get(RESOURCE_URL) 
        data = response.json() 
        for platform in data['objects']: 
            platform_shorthand[platform['name']] = platform['short'] 
    
    async def on_ready(self):
        print('bot is running') 
        self.get_platforms() 
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        user_query_author = message.author 
        user_query = message.content 
        user_query = user_query.split() 
        if user_query[0].startswith("$contests"):
            """
            max number contests shown -> 100 
            Note: only returns upcoming contests, for past contests use $past_contests 
            $contests (default) -> returns all upcoming contests 
            $contests -platform -> returns all upcoming contests in the specified platform 
            """
            if user_query[0].startswith("$contests +cf") or user_query[0].startswith("$contests +codeforces"):
                response = requests.get(CONTEST_URL + "&limit=100&upcoming=true&host=codeforces.com") 
            elif user_query[0].startswith("$contests +cc") or user_query[0].startswith("$contests +codechef"):
                response = requests.get(CONTEST_URL + "&limit=100&upcoming=true&host=codechef.com")
            elif user_query[0].startswith("$contests +lc") or user_query[0].startswith("$contests + leetcode"):
                response = requests.get(CONTEST_URL + "&limit=100&upcoming=true&host=leetcode.com") 
            else: 
                response = requests.get(CONTEST_URL + "&limit=100&upcoming=true") 
            if response.status_code == 200:
                pages = [] 
                data = response.json() 
                cnt = 0 
                embedVar = discord.Embed(title="Future Contests | Page 1", color=0x00ff00) 
                for contest in data['objects']: 
                    field_name = f"{contest['event']}" 
                    field_value = "[" + contest['host'] + "]" + "(" + contest['href'] + ")" 
                    embedVar.add_field(name=field_name, value=field_value, inline=False) 
                    cnt += 1 
                    if cnt == 10:
                        pages.append(embedVar) 
                        cnt = 0 
                        new_embedVar = discord.Embed(title=f"Future contests | Page {len(pages) + 1}", color=0x00ff00) 
                        embedVar = new_embedVar 
                if cnt > 0:
                    pages.append(embedVar) 
                current_page = 0 
                message = await message.channel.send(embed=pages[current_page])  
                
                reactions = ['⬅️', '➡️']
                for reaction in reactions:
                    await message.add_reaction(reaction)
                
                def check(reaction, user):
                    return user == user_query_author and str(reaction.emoji) in reactions 

                while True:
                    try:
                        reaction, user = await self.wait_for('reaction_add', timeout=60.0, check=check)  
                        if str(reaction.emoji) == '➡️':
                            print("right") 
                            current_page = (current_page + 1) % len(pages)
                        elif str(reaction.emoji) == '⬅️':
                            print("left") 
                            current_page = (current_page - 1) % len(pages)

                        await message.edit(embed=pages[current_page])
                        await message.remove_reaction(reaction, user)

                    except TimeoutError:
                        break

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
            response = requests.get(CONTEST_URL + "&limit=100&upcoming=false") 
            if response.status_code == 200:
                pages = [] 
                data = response.json() 
                cnt = 0 
                embedVar = discord.Embed(title="Past Contests | Page 1", color=0x00ff00) 
                for contest in data['objects']: 
                    field_name = f"{contest['event']}" 
                    field_value = "[" + contest['host'] + "]" + "(" + contest['href'] + ")" 
                    embedVar.add_field(name=field_name, value=field_value, inline=False) 
                    cnt += 1 
                    if cnt == 10:
                        pages.append(embedVar) 
                        cnt = 0 
                        new_embedVar = discord.Embed(title=f"Past contests | Page {len(pages) + 1}", color=0x00ff00) 
                        embedVar = new_embedVar 
                if cnt > 0:
                    pages.append(embedVar) 
                current_page = 0 
                message = await message.channel.send(embed=pages[current_page])  
                
                reactions = ['⬅️', '➡️']
                for reaction in reactions:
                    await message.add_reaction(reaction)
                
                def check(reaction, user):
                    return user == user_query_author and str(reaction.emoji) in reactions 

                while True:
                    try:
                        reaction, user = await self.wait_for('reaction_add', timeout=60.0, check=check)  
                        if str(reaction.emoji) == '➡️':
                            print("right") 
                            current_page = (current_page + 1) % len(pages)
                        elif str(reaction.emoji) == '⬅️':
                            print("left") 
                            current_page = (current_page - 1) % len(pages)

                        await message.edit(embed=pages[current_page])
                        await message.remove_reaction(reaction, user)

                    except TimeoutError:
                        break

            else:
                print(f"failure: {response.status_code}")
        
          
    
def main() -> None: 
    intents = discord.Intents.default() 
    intents.message_content = True 
    client = MyClient(intents = intents) 
    client.run(token=DISCORD_TOKEN)  
    
    

if __name__ == "__main__":
    main()  
