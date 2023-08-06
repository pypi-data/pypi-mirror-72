#! /usr/bin/python3
import aiohttp, asyncio, discord
from lxml import etree
from io import BytesIO, StringIO
from PIL import Image
import os, pkgutil
sfilter=pkgutil.get_data(__package__, 'safesearchfilter.txt').decode('utf-8').replace("\r","").split("\n")
#print(sfilter)
SAFESEARCH=False
class ImageDataNotFound(Exception):
    '''No data about the thumbnail could be found because the video wasn't searched yet'''
    pass
class BadRequest(Exception):
    '''Non 200 response code'''
    pass
class VideoList:
    '''Gives a list of video urls, 
    100x more performant than manually 
    querying results using Video Object
    
    returns: list of video urls'''

    def __init__(self):
        self.videos=[]
    async def search(self, query, retries=5):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://youtube.com/search?q={query}") as r:
                if r.status==200:
                    html=await r.text()
                    data=etree.HTML(html)
                    self.videos=["https://youtube.com"+url for url in data.xpath("//div[contains(@class,'yt-lockup-thumbnail')]/a/@href")] # Parses data to extracts urls of all videos
                    if len(self.videos)==0:
                        print(f"Couldn't fetch video list, retrying...")
                        return await self.search(query, retries=retries-1)
                else:      
                    raise BadRequest  
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
        async with aiohttp.ClientSession() as session:
            async with session.get(queryurl) as r:
                if r.status == 200:
                    text=await r.text()
                    
                else:
                    raise BadRequest
        data=etree.HTML(text)
        try:
            self.url="https://youtube.com"+data.xpath("//div[contains(@class,'yt-lockup-thumbnail')]/a/@href")[index]
            self.thumbnail=data.xpath("//div[contains(@class,'yt-lockup-thumbnail')]/a//img/@src")[index] # May not work after the 5th result because of how youtube loads it client sided
            self.title=data.xpath("//h3[contains(@class,'yt-lockup-title')]/a")[index].text
        except IndexError:
            print(f"Couldn't fetch video, retrying...")
            await self.search(name,index,retries=retries-1)
        if self.advanced:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as r:
                    if r.status == 200:
                        adv=await r.text()
                    else:
                        raise BadRequest    
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
    async def image(self):
        if not self.thumbnail:
            raise ImageDataNotFound
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.thumbnail) as r:
                    if r.status == 200:
                        resp=await r.read()
                        thumbnail=Image.open(BytesIO(resp))
                    else:
                        raise BadRequest            
            buffer = BytesIO()  # Create a Byte Buffer
            thumbnail.save(buffer,format="PNG")  # Save image to buffer in order to avoid saving to disk
            buffer.seek(0)
            return discord.File(buffer,'thumbnail.png')  # Instantiate a file object using created buffer
