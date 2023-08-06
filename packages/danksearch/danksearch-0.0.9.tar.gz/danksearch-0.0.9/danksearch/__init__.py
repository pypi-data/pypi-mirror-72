#! /usr/bin/python3
from aiohttp import TCPConnector, ClientSession
import aiohttp, asyncio
from lxml import etree
from io import BytesIO, StringIO
import os, pkgutil
import atexit, re
sfilter=pkgutil.get_data(__package__, 'safesearchfilter.txt').decode('utf-8').replace("\r","").split("\n")
#print(sfilter)
SAFESEARCH=False
class CS:

    _cs: ClientSession

    def __init__(self):
        self._cs = ClientSession(connector=TCPConnector(verify_ssl=False))

    async def get(self, url):
        async with self._cs.get(url) as resp:
            return await resp.text()

    async def close(self):
        await self._cs.close()
adapter=CS()
class VideoList:
    '''Gives a list of video urls, 
    100x more performant than manually 
    querying results using Video Object
    
    returns: list of video urls'''

    def __init__(self):
        self.videos=[]
    async def search(self, query, retries=5):
                    html=await adapter.get(f"http://www.youtube.com/search?q={query}")
                    data=etree.HTML(html)
                    self.videos=["https://youtube.com"+url for url in data.xpath("//div[contains(@class,'yt-lockup-thumbnail')]/a/@href")] # Parses data to extracts urls of all videos
                    if len(self.videos)==0:
                        print(f"Couldn't fetch video list, retrying...")
                        return await self.search(query, retries=retries-1)
class Video:
    ''' Search for a youtube video'''
    def __init__(self,advanced=False):
        if SAFESEARCH:
            self.__censoredcontent=sfilter
        self.url=None
        self.advanced=advanced
        self.title=None
        self.thumbnail=None
        if self.advanced:
            self.views=None
            self.published_on=None
            self.channel=None
            self.creator=None
            self.likes=None
            self.dislikes=None
            self.description=None
    async def search(self, name, index=0, retries=5):
        if SAFESEARCH:
            for word in self.__censoredcontent:
                name=name.lower().replace(word,"")
        if retries==0:
            print("Exceeded max retry limit")
            return
        if name=="":
            name="never gonna give you up"
        # Create a url and send a request to youtube about it
        queryurl = ('http://www.youtube.com/results?search_query=' + name)
        text=await adapter.get(queryurl)
        data=etree.HTML(text)
        try:
            self.url="https://youtube.com"+data.xpath("//div[contains(@class,'yt-lockup-thumbnail')]/a/@href")[index]
            self.thumbnail=data.xpath("//div[contains(@class,'yt-lockup-thumbnail')]/a//img/@src")[index] # May not work after the 5th result because of how youtube loads it client sided
            self.title=data.xpath("//h3[contains(@class,'yt-lockup-title')]/a")[index].text
        except IndexError:
            print(f"Couldn't fetch video, retrying...")
            await self.search(name,index,retries=retries-1)
        if self.advanced:
            adv=adapter.get(self.url)    
            advdata=etree.HTML(adv)
            try:
                self.views=advdata.xpath("//div[contains(@class,'watch-view-count')]")[0].text
                self.published_on=advdata.xpath("//strong[contains(@class,'watch-time-text')]")[0].text 
                self.channel="https://youtube.com"+advdata.xpath("//div[contains(@class,'yt-user-info')]/a/@href")[0]
                self.creator=advdata.xpath("//div[contains(@class,'yt-user-info')]/a")[0].text
                self.likes=advdata.xpath("//button[contains(@class,'like-button-renderer-like-button')]/span")[0].text#like-button-renderer-like-button
                self.dislikes=advdata.xpath("//button[contains(@class,'like-button-renderer-dislike-button')]/span")[0].text#like-button-renderer-dislike-button
                self.description=advdata.xpath("//p[contains(@id,'eow-description')]")[0].text#eow-description
            except IndexError:
                print(f"Couldn't fetch advanced data, retrying...")
                await self.search(name,index,retries=retries-1)
class BetterVideo:
    ''' An attempt to decrease request
    time using regex search and aiohttp
    sessions '''
    def __init__(self):
        self.url=None
        self.links=[]
    async def search(self, query, index=0):
        code= await adapter.get(f"https://youtube.com/results?search_query={query}")
        data = [i.start() for i in re.finditer(r"watch\?v", code)] 
        self.links=["https://youtube.com/"+code[index:index+19] for index in data]
        self.url=self.links[index]
atexit.register(lambda: asyncio.get_event_loop().run_until_complete(adapter.close()))
