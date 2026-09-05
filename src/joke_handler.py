import aiohttp
import asyncio

class JokeHandler:
    def __init__(self):
        self.apis = {
            'JokeAPI': 'https://v2.jokeapi.dev/joke/{category}',
            'Official Joke API': 'https://official-joke-api.appspot.com/jokes/{category}/random',
            'Ninja Jokes': 'https://api.api-ninjas.com/v1/jokes'
        }
    
    async def fetch_joke(self, api_source, category=None):
        try:
            if api_source == 'JokeAPI':
                return await self._fetch_jokeapi(category)
            elif api_source == 'Official Joke API':
                return await self._fetch_official_joke_api(category)
            elif api_source == 'Ninja Jokes':
                return await self._fetch_ninja_jokes()
        except Exception as e:
            raise Exception(f'Error fetching joke: {str(e)}')
    
    async def _fetch_jokeapi(self, category=None):
        url = 'https://v2.jokeapi.dev/joke/'
        if category and category.lower() == 'programming':
            url += 'Programming'
        elif category and category.lower() == 'knock-knock':
            url += 'Knock-Knock'
        else:
            url += 'Any'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['type'] == 'twopart':
                        return f"{data['setup']}\n\n{data['delivery']}"
                    else:
                        return data['joke']
                else:
                    raise Exception(f'API returned status {response.status}')
    
    async def _fetch_official_joke_api(self, category=None):
        url = 'https://official-joke-api.appspot.com/jokes/'
        if category and category.lower() == 'knock-knock':
            url += 'knock-knock/random'
        else:
            url += 'general/random'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list):
                        data = data[0]
                    return f"{data['setup']}\n\n{data['punchline']}"
                else:
                    raise Exception(f'API returned status {response.status}')
    
    async def _fetch_ninja_jokes(self):
        url = 'https://api.api-ninjas.com/v1/jokes'
        headers = {'X-Api-Key': 'demo'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list) and len(data) > 0:
                        return data[0]['joke']
                    elif 'joke' in data:
                        return data['joke']
                    else:
                        raise Exception('Invalid response format')
                else:
                    raise Exception(f'API returned status {response.status}')