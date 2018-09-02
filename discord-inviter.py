import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import base64
import json
import _thread

start_server()

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        start_server()

    @commands.command()
    async def mycom(self):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff!")

def setup(bot):
    bot.add_cog(Mycog(bot))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)
            if "eid" in query:
                eid = query["eid"][0]

                auth = 'Basic ' + base64.b64encode(bytes('anystring:xxxxxx', 'utf-8')).decode('ascii')
                listId = 'xxxxx'
                
                # 1) Get Member
                url = 'https://us16.api.mailchimp.com/3.0/lists/{0}/members/{1}'.format(listId , eid)
                r = requests.get(url, headers = {'Authorization': auth}, params={'fields': 'merge_fields'}, timeout=1)
                print(r)
                jsonData = json.loads(r.text)
                print(json.dumps(jsonData, indent=4, sort_keys=True))

                inviteCode = jsonData['merge_fields']['INVCODE']
                referrer = jsonData['merge_fields']['REF']
                
                # 2) Update Member with invite code if doesnt exist
                # if inviteCode == '':
                    #generate code
                #use code

                # 3) Get Refferer Member
                if referrer != 'false' and inviteCode == '':
                    url = 'https://us16.api.mailchimp.com/3.0/lists/{0}/members/{1}'.format(listId , referrer)
                    r = requests.get(url, headers = {'Authorization': auth}, params={'fields': 'merge_fields'}, timeout=1)
                    print(r)
                    jsonData = json.loads(r.text)
                    print(json.dumps(jsonData, indent=4, sort_keys=True))

                    refCount = 0
                    if jsonData['merge_fields']['REFERRALS'] != '' :
                        refCount = jsonData['merge_fields']['REFERRALS']
                    refCount += 1
                    print('refcount:' + str(refCount))

                    # 4)Update Refferer Member referral count
                    url = 'https://us16.api.mailchimp.com/3.0/lists/{0}/members/{1}'.format(listId , referrer)
                    r = requests.patch(url, headers = {'Authorization': auth}, data = json.dumps({'merge_fields': {'REFERRALS': refCount}}), timeout=1)
                    print(r.request.body)
                    print(r)
                    jsonData = json.loads(r.text)
                    print(json.dumps(jsonData, indent=4, sort_keys=True))


                redirect = 'https://www.iloveonlinegaming.com/discord'
                html = '<head><meta http-equiv="Refresh" content="0; url=' + redirect + '"></head>'

                self.send_response(200)
                self.end_headers()
                self.wfile.write(html.encode())

        except Exception as e: 
            print(e)

def start_server():
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    try:
        _thread.start_new_thread( httpd.serve_forever() )
    except:
        print ("Error: unable to start server thread")
