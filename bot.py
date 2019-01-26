# Works with Python 3.6
#3.7 does not play well with async/await

##V1.0.5
##-Storing data taken from sheets into memory
##  -To reduce GET requests but increases mem usage
##  -Should help response time of bot to user requests
##-Force update command added to force refresh data in case of any updates
##-Added images to data
##
##V1.0.4
##-Broadcast command added, @everyone included for channels with permission
##-OAuth2 has been deprecated, google.auth to replace
##-Timestamp dictionary changes
##  -on_ready only stores list of servers now
##  -Members list changed to only add timestamp when a user leaves a msg for the 1st time
##  -This should reduce the mem usage
##  -Command to print timestamps added
##-To be added:
##  -DM bot for feedback
##  -A way to reboot bot instead of killing
##-Consideration to rewrite to discord.py-rewrite branch
##
##-Added mention for embed responses to user commands
##V1.0.3
##-Broadcast message command for all servesr to be added
##-Force refresh of loading tokens and sensitive information to be added
##-Force remove bot from certain servers to be looked into
##
##V1.0.2
##-Added Jan Update commands
##
##V1.0.1
##-Initial upload to git
##-Moved discord/external tokens and configurations to local file

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import discord
import logging
import random
import asyncio
import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
d=datetime.datetime.now()
handler = logging.FileHandler(filename='{0:%Y-%m-%d %H-%M-%S}.log'.format(d), encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Load configuration
with open('config.json') as data_file:
    config = json.load(data_file)

#Google APIs
#-----------------------------------------
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# The ID and range of spreadsheet.
SPREADSHEET_ID = config['main_spreadsheet']
EXPLORER_SHEETS_ID = config['xplorer_spreadsheet']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
            
service = build('sheets', 'v4', credentials=creds)
#----------------------------------------
def royalstyle(fupd):
    global royalstylevalues,royalstyleperiod,fupdate

    if not fupd:
        msg = royalstylevalues
        msgTitle = royalstyleperiod
        em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
        if not royalstyleperiod=='No data available':
            em.set_image(url=config['rs'])
        em.set_author(name='Royal Style', icon_url=discClient.user.default_avatar_url)
        return em
        
    sheet = service.spreadsheets()
    availableRoyal1 = 'RoyalStyle!B2:E2'
    listRoyal1 = 'RoyalStyle!I3:J36'
    availableRoyal2 = 'RoyalStyle!B37:E37'
    listRoyal2 = 'RoyalStyle!I38:J71'
    msg = ''
    #Check if royals available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=availableRoyal1).execute()
    values = result.get('values', [])

    if not values[0][0]:
        royalstyleperiod='No data available'
        royalstylevalues=''
        return ''
    else:        
        msgTitle = '%s'%values[0][3]+'\n%s'%values[0][0]+' to '+'%s'%values[0][1]
        royalstyleperiod = msgTitle
            
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=listRoyal1).execute()
    values = result.get('values', [])

    if not values:
        msg = 'List not updated'
    else:
        
        for row in values:
            # Print columns I and I, which correspond to indices 0 and 0.
            #print('%s, %s' % (row[0], row[0]))
            msg = msg + '\n' + ('%s'%row[0])

    em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
    em.set_image(url=config['rs'])
    em.set_author(name='Royal Style', icon_url=discClient.user.default_avatar_url)
    royalstylevalues = msg
    return em

def goldenapple(fupd):
    global gapplevalues,gappleperiod,fupdate

    if not fupd:
        msg = gapplevalues
        msgTitle = gappleperiod
        em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
        if not gappleperiod=='No data available':
            em.set_image(url=config['ga1'])
        em.set_author(name='Golden Apple', icon_url=discClient.user.default_avatar_url)
        return em
    
    sheet = service.spreadsheets()
    availableGapple1 = 'GoldApple!B2:E2'
    listGapple1 = 'GoldApple!I3:28'
    availableGapple2 = 'GoldApple!B37:E37'
    listGapple2 = 'GoldApple!I30:I'
    msg = ''
    #Check if gapples available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=availableGapple1).execute()
    values = result.get('values', [])

    if not values[0][0]:
        gappleperiod='No data available'
        gapplevalues=''
        return ''
    else:        
        msgTitle = '%s'%values[0][3]+'\n%s'%values[0][0]+' to '+'%s'%values[0][1]
    gappleperiod=msgTitle        
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=listGapple1).execute()
    values = result.get('values', [])
    
    if not values:
        msg = 'List not updated'
    else:
        
        for row in values:
            # Print columns I and I, which correspond to indices 0 and 0.
            #print('%s, %s' % (row[0], row[0]))
            msg = msg + '\n' + ('%s'%row[0])

    em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
    em.set_image(url=config['ga1'])
    em.set_author(name='Golden Apple', icon_url=discClient.user.default_avatar_url)
    gapplevalues=msg
    return em

def royalhair(fupd):
    global rhairvalues,rhairperiod,fupdate

    if not fupd:
        msg = rhairvalues
        msgTitle = rhairperiod        
        em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
        if not rhairperiod == 'No data available':
            em.set_image(url=config['rh'])
        em.set_author(name='Royal Hair+Face', icon_url=discClient.user.default_avatar_url)
        return em
    
    sheet = service.spreadsheets()
    availableRoyal1 = 'RoyalHairFace!B2:C2'
    listRoyal1 = 'RoyalHairFace!F2:I8'
    msg = ''
    #Check if hair available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=availableRoyal1).execute()
    values = result.get('values', [])

    if not values[0][0]:
        rhairperiod='No data available'
        rhairvalues=''
        return ''
    else:        
        msgTitle = '%s'%values[0][0]+' to '+'%s'%values[0][1]
    rhairperiod=msgTitle        
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=listRoyal1,majorDimension='COLUMNS').execute()
    values = result.get('values',[])
    
    for col in values:
        if len(col)<2:
            msg='List not updated'
            continue

        msg=msg+'%s'%col[0]+':\n'

        for i in range(len(col)-1):
            msg = msg+'%s'%col[i+1]+','
            i+=1
        msg+='\n'

    em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
    em.set_image(url=config['rh'])
    em.set_author(name='Royal Hair+Face', icon_url=discClient.user.default_avatar_url)
    rhairvalues=msg
    return em

def eventspackages(fupd):
    global eventvalues,eventperiod,fupdate

    if not fupd:
        msg = eventvalues
        msgTitle = eventperiod
        em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
        if not (eventperiod=='No data available'or eventvalues=='There does not seem to be any future content'):
            em.set_image(url=config['ep'])
        em.set_author(name='Events & Packages', icon_url=discClient.user.default_avatar_url)    
        return em
    
    sheet = service.spreadsheets()
    availableEvents1 = 'Events&Packages!A:E'
    msg = ''
    #Check if events available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=availableEvents1).execute()
    values = result.get('values', [])

    if not values[0][0]:
        eventperiod='No data available'
        eventvalues=''
        return ''
    else:
        msgTitle = 'List of Events/Packages'
    eventperiod=msgTitle
    for row in values:                
        
        if not row:
            continue
        elif row[0]!='Period':
            continue
        else:
            if len(row)<5:
                continue
            else:
                msg = msg+'Name: %s\n'%row[4]+'Period: %s'%row[1]+' to %s\n\n'%row[2]
               
    if msg == '':
        msg='There does not seem to be any future content'
    em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
    em.set_image(url=config['ep'])
    em.set_author(name='Events & Packages', icon_url=discClient.user.default_avatar_url)
    eventvalues=msg
    return em

def infocheck(fupd):
    global infovalues,infoperiod,fupdate

    if not fupd:
        msg = infovalues
        msgTitle = infoperiod
        em = discord.Embed(title=msgTitle, description=msg)
        em.set_author(name='Leeks', icon_url=discClient.user.default_avatar_url)
        em.set_image(url='https://cdn.discordapp.com/attachments/488019800136876035/533583572297187348/leek.jpg')

        return em
    
    sheet = service.spreadsheets()
    lastUpdated = 'Landing!A2:3'
    msg = ''
    #Check update available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=lastUpdated).execute()
    values = result.get('values', [])

    msgTitle='Info'
    infoperiod=msgTitle

    msg='%s'%values[0][0]+'\n%s\n'%values[1][0]
    em = discord.Embed(title=msgTitle, description=msg)
    em.set_author(name='Leeks', icon_url=discClient.user.default_avatar_url)
    em.set_image(url=config['in'])
    infovalues=msg
    return em

#3Xplorer update functions

def xplorer(command,fupd):
    sheet = service.spreadsheets()
    if command == 'emblem':
        r = 'Emblem!A2:H12'
        msgTitle='Emblem'
    elif command == 'exalt':
        r = 'Exalt!A2:C45'
        msgTitle='Exalt'
    elif command == 'all':
        msgTitle='All updates'
        return #to be updated
    msg =''
    #Check xplorer update available
    result = sheet.values().get(spreadsheetId=EXPLORER_SHEETS_ID,
                                range=r).execute()
    values = result.get('values', [])

    for row in values:
        i=0
        for i in range(len(row)):
            msg += '{},'.format(row[i])
            i+=1
        msg+='\n'

    em = discord.Embed(title=msgTitle, description=msg, colour=0x0000FF)
    em.set_author(name='3xplorer Update', icon_url=discClient.user.default_avatar_url)

    return em


#--------------------------------------------
def greetings(message,check):
    
    listofstrings={1:'Hello {0.author.mention}'.format(message),
                   2:'Greetings {0.author.mention}'.format(message),
                   3:'Howdy {0.author.mention}'.format(message),
                   4:'Sup {0.author.mention}'.format(message),
                   5:'Hey {0.author.mention}'.format(message)
                   }
    if not check:
        r = random.randint(1,len(listofstrings))
    else:
        return nestedconvo(message,6)
    return listofstrings[r]


def nestedconvo(message,iterations):
    
    listofstrings={1:'Aren\'t you tired {0.author.mention} :open_mouth: '.format(message),
                   2:'Getting real tired of you {0.author.mention} :angry: '.format(message),
                   3:'Don\'t you have better things to do {0.author.mention} :unamused: '.format(message),
                   4:'Stop bothering me already {0.author.mention} :expressionless: '.format(message),
                   5:'WATER U WAN {0.author.mention} :rage: '.format(message),
                   6:'I can do this all day {0.author.mention}'.format(message)                  
                   }
    r = random.randint(1,len(listofstrings))
    return listofstrings[r]

def is_bot(m):
    asyncio.sleep(0.5)
    return m.author == discClient.user

def checkperms(mem,c):
    print ('Checking permissions for : %s'%mem.name+' in %s'%c.name)
    permissions = c.permissions_for(mem)
    if not (permissions.send_messages):
        return False
    if not (permissions.read_messages):
        return False
    if not (permissions.manage_messages):
        return False
    if not (permissions.read_message_history):
        return False
    if not (permissions.embed_links):
        return False
    return True

#----------------------------------------------
#Discord Py
            
TOKEN = config['bot_token']
BOT_OWNER_ID = config['bot_owner_id']

discClient = discord.Client()

#Global variables
fupdate = True
royalstylevalues=''
royalstyleperiod=''
gapplevalues=''
gappleperiod=''
eventvalues=''
eventperiod=''
infovalues=''
infoperiod=''


#Used to store author and timestamps
membersDict = {}
serversDict = {}

#check if server exist in dictionary, so as to not trigger yet until owner initiates
def serverexist(m):
        if (m.server.id in serversDict):
            return True
        else:
            return False

def servererror(check):
    if (check):
        return 'Please use \!start in a channel in {0} to initialize bot'
    else:
        return
    

@discClient.event
async def on_ready():
    global membersDict,serversDict
    print('Logged in as')
    print(discClient.user.name)
    print(discClient.user.id)
    print('------')

    for servers in discClient.servers:       
        #Store only bot timestamp, other members to be stored dynamically
        membersDict[servers.me.id]=datetime.datetime.utcnow()
        serversDict[servers.id]=membersDict
        #clear members dictionary
        membersDict={}
    print ('Bot ready as of '+str(datetime.datetime.utcnow()))
    
@discClient.event
async def on_message(message):
    global serversDict,membersDict    
    # we do not want the bot to reply to itself
    if message.author == discClient.user:
        return
    # ignore other bots as well
    if message.author.bot:
        return    
    #initialize bot to start only if command given (only needs to be done once per server)
    if (message.content == '!start'):
        if (serverexist(message)):            
            return
        if not (message.author==message.server.owner):
            await discClient.send_message(message.channel, 'You do not have permissions to do that!')
            return
        await discClient.send_message(message.channel, 'Initializing...')
        if not (checkperms(message.server.me,message.channel)):
            await discClient.send_message(message.channel, 'Error in permissions. Make sure to assign a special role and required permissions to the bot.')
            return
        #Store only bot timestamp, other members to be stored dynamically
        membersDict[message.server.me.id]=datetime.datetime.utcnow()
        serversDict[message.server.id]=membersDict
        #clear members dictionary
        membersDict={}
        msg = 'Leeks Seller can now do business :grin:'
        await discClient.send_message(message.channel, msg)    
    
    #Check if DM
    if (message.channel.type==discord.ChannelType.private):
        msg = '\n'+message.content
        try:
            feedback=open('feedback.txt','a')
            feedback.write(str(msg))
            feedback.close()
        except:
            await discClient.send_message(message.channel,'There was an error recording your request. Please try again later.')
            return
        await discClient.send_message(message.channel,'Response recorded.')
        return
    
    if not (serverexist(message)):
        return

    #Check if sheets data needs to forced update
    if (message.content.startswith('!fupdate')):
        global fupdate,config
        if not message.author.id == BOT_OWNER_ID:
            await discClient.delete_message(message)
            return
        try:
            royalstyle(True)
            print('rs')
            goldenapple(True)
            print('ga')
            royalhair(True)
            print('rh')
            eventspackages(True)
            print('ep')
            infocheck(True)
            print('in')
            fupdate=False
            with open('config.json') as data_file:
                config=json.load(data_file)
        except:
            await discClient.send_message(message.channel,'There was an error refreshing data')
            await discClient.delete_message(message)
            fupdate=True
        
        await discClient.send_message(message.channel,'Force update successful')
        await discClient.delete_message(message)
        return
    
    #Check if user timestamp exist then limit user commands to 1 every 2 sec
    if message.author.id in serversDict[message.server.id]:
        if '!' in message.content and not (message.timestamp - serversDict[message.server.id][message.author.id])>datetime.timedelta(seconds=2):
            msg = '{0.author.mention} You have already sent a command recently!'.format(message)
            await discClient.send_message(message.channel, msg)            
            return
    
    if message.content.startswith('!help'):
        msg = 'Available commands:\n!help\n!hello\n!test\n!royalstyle\n!goldenapple\n!royalhair\n!events\n!info'
        #msg = 'Available commands:\n!help\n!hello\n!test'
        await discClient.send_message(message.channel, msg)

    if message.content.startswith('!end'):
        if message.author == message.server.owner:
            print ('closing')
            await discClient.close()
        else:
            print ('failed')
            await discClient.send_message(message.channel, '{0.author.mention}, looks like you don\'t have permission to do that'.format(message))
            
    if 'leeks' in message.content and message.content.startswith('!give'):
        msg = 'I haz leeks... if you have shinies...'
        await discClient.send_message(message.channel,msg)
        serversDict[message.server.id][message.author.id]=message.timestamp

    if message.content.startswith('!hello'):
        await discClient.send_typing(message.channel)
        if message.author.id in serversDict[message.server.id]:
            if not (message.timestamp - serversDict[message.server.id][message.author.id])>datetime.timedelta(seconds=5):
                msg = greetings(message,True)
            else:        
                msg = greetings(message,False)
        else:
            msg = greetings(message,False)
        await discClient.send_message(message.channel, msg)
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!test'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        msg = 'This is a test message for {0.author.mention}'.format(message)        
        await discClient.send_message(message.channel, msg)
        serversDict[message.server.id][message.author.id]=message.timestamp
            
    if message.content.startswith('!royalstyle'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = royalstyle(fupdate)
        if not em:
            msg = 'No Update on Royal Styles found :cry:'
            await discClient.send_message(message.channel, msg)
        else:
            msg = '{0.author.mention}'.format(message)
            await discClient.send_message(message.channel, content = msg, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!goldenapple'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = goldenapple(fupdate)
        if not em:
            msg = 'No Update on Golden Apples found :cry:'
            await discClient.send_message(message.channel, msg)
        else:
            msg = '{0.author.mention}'.format(message)           
            await discClient.send_message(message.channel, content=msg, embed=em)            
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!royalhair'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = royalhair(fupdate)
        if not em:
            msg = 'No Update on Royal Hair+Face found :cry:'
            await discClient.send_message(message.channel, msg)
        else:
            msg = '{0.author.mention}'.format(message)
            
            await discClient.send_message(message.channel, content=msg, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!events'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = eventspackages(fupdate)
        if not em:
            msg = 'No Update on Events found :cry:'
            await discClient.send_message(message.channel, msg)
        else:
            msg = '{0.author.mention}'.format(message)
            
            await discClient.send_message(message.channel, content=msg, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!info'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = infocheck(fupdate)
        msg = '{0.author.mention}'.format(message)
        await discClient.send_message(message.channel, content=msg, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp

    if message.content.startswith('!feedback'):
        await discClient.send_message(message.channel,'Leaving a feedback? Just slide into my DMs :kissing_heart:')

    if message.content.startswith('!deletebotmsg'):
        if not (serverexist):            
            return
        if message.author == message.server.owner:
            perms = message.channel.permissions_for(message.server.me)
            if (perms.manage_messages):
                deleted = await discClient.purge_from(message.channel, limit=100, check=is_bot)
            else:
                msg = 'Bot does not have the required permission(s)'
                await discClient.send_message(message.channel, msg)
                return
        await discClient.send_message(message.channel, '{} message(s) have been purged'.format(len(deleted)))
        
    if message.content.startswith('!deleteall'):
        if not (serverexist):            
            return
        if message.author==message.server.owner:
            perms = message.channel.permissions_for(message.server.me)
            if (perms.manage_messages):
                await discClient.send_message(message.channel,'Do you really want to purge messages? Enter \'Yes\' to confirm\nCommand expires in 10 seconds' )
                confirm = await discClient.wait_for_message(author=message.author, content='Yes',timeout=10)
                if confirm==None:
                    await discClient.send_message(message.channel,'Cancelled')
                    return
                deleted = await discClient.purge_from(message.channel)
            else:
                msg = 'Bot does not have the required permission(s)'
                await discClient.send_message(message.channel, msg)
                return
        else:
            msg = 'It doesn\'t seem like you have the permissions to do that {0.author.mention}'.format(message)
            await discClient.send_message(message.channel,msg)
            return
        await discClient.send_message(message.channel, '{} message(s) have been purged'.format(len(deleted)))

    #To be used by owner of bot. Broadcasts message across all servers
    #Main intention is to inform users of any downtime/maintenance/status of bot
        
    if message.content.startswith('!broadcast'):
        if not message.author.id == BOT_OWNER_ID:
            return
                
        await discClient.send_message(message.channel,'Type your message now.\nUse !cancel to cancel broadcast.')
        msgtobroadcast = await discClient.wait_for_message(author=message.author)

        #check if cancelled by owner
        if msgtobroadcast.content.startswith('!cancel'):
            await discClient.send_message(message.channel,'Broadcast cancelled')
            return

        tempmsg = 'Please check if message is correct.\n'+\
                  msgtobroadcast.content+'\nType \'Yes\' to confirm. Confirmation expires in 10 seconds'

        print (tempmsg)
        print (msgtobroadcast.role_mentions)

        await discClient.send_message(message.channel,tempmsg)
        tempmsg = await discClient.wait_for_message(author=message.author,content='Yes',timeout=10)
        if tempmsg == None:
            await discClient.send_message(message.channel,'Broadcast cancelled due to timeout')
            return

        #Start broadcast
        #Get list of servers
        for server in discClient.servers:
            #flag to see if at least one message posted in a server, temp string
            posted=False
            tempstring=''
            #Get list of channels
            for channel in server.channels:
                #Check if voice or text
                print (channel.type)
                if (channel.type == discord.ChannelType.text):
                    print ('in')
                    #Check for permissions
                    if checkperms(server.me,channel):
                        if (channel.permissions_for(server.me).mention_everyone):
                            tempstring = '@everyone\n'+msgtobroadcast.content
                        else:
                            tempstring = msgtobroadcast.content
                        await discClient.send_message(channel,tempstring)
                        await asyncio.sleep(0.3)
                        posted=True
            #If no message posted in server, send message to owner instead
            if not posted:
                try:
                    await discClient.send_message(server.owner,msgtobroadcast.content)
                except discord.Forbidden:
                    print ('Forbidden to message user')
                await asyncio.sleep(0.3)

    if message.content.startswith('!ctime'):
        if not message.author.id == BOT_OWNER_ID:
            return
        for servers in serversDict:
            print (serversDict[servers])
            for mems in serversDict[servers]:
                print (str(serversDict[servers][mems]))
                        
    
    #Jan update commands--------------------------
    if message.content.startswith('!3xp'):
        if not message.author.id == BOT_OWNER_ID:
            return
        if 'emblem' in message.content:
            em = xplorer('emblem',fupdate)
        elif 'exalt' in message.content:
            em = xplorer('exalt',fupdate)
        else:
            await discClient.send_message(message.channel, 'Argument missing')
            await discClient.delete_message(message)
            return
        if not em:
            msg = 'No data exist!'
            await discClient.send_message(message.channel, msg)
            await discClient.delete_message(message)
        else:
            msg='{0.author.mention}'.format(message)
            await discClient.send_message(message.channel, content=msg, embed=em)
            await discClient.delete_message(message)
        serversDict[message.server.id][message.author.id]=message.timestamp
    
@discClient.event
async def on_member_join(member):
    global serversDict,membersDict
    membersDict = serversDict[member.server.id]
    if not (member.id in membersDict):        
        membersDict[member.id]=datetime.datetime.utcnow()
        serversDict[member.server.id]=membersDict
        membersDict={}
        print ('Added %s'%member.id+' to %s'%member.server.id)

@discClient.event
async def on_member_remove(member):
    global serversDict,membersDict
    membersDict = serversDict[member.server.id]
    if (member.id in membersDict):
        del membersDict[member.id]
        serversDict[member.server.id]=membersDict
        membersDict={}
        print ('Removed %s'%member.id+' from %s'%member.server.id)
        
@discClient.event
async def on_channel_update(before,after):
    #Check for permission changes
    print (before.permissions_for(before.server.me).value)
    print (after.permissions_for(after.server.me).value)
    if not (before.permissions_for(before.server.me).value == after.permissions_for(after.server.me).value):
        if not (checkperms(after.server.me,after)):
            msg = 'Permissions have been changed for me which may affect my functionality :eyes:'        
        else:
            msg = 'My permissions seem to have changed...:thinking: I should be working properly now :grin:'
        try:
            await discClient.send_message(after,msg)
            return
        except discord.Forbidden:
            print ('There is permissions error')
        try:
            msg = 'Permission changes have made me unable to work in %s'%after.name+', %s'%after.server.name
            await discClient.send_message(after.server.owner,msg)
        except discord.Forbidden:
            print ('Forbidden to contact owner of server')
            
    
@discClient.event
async def on_server_remove(server):
    global serversDict
    msg = 'You have removed %s'%discClient.user.name+' from %s server'%server
    try:
        await discClient.send_message(server.owner,msg)
    except discord.Forbidden:
        print ('There is permissions error')
        
    #remove server dictionary if exist
    if server.id in serversDict:
        del serversDict[server.id]
    print ('Bot removed from: %s'%server,' %s'%server.id)
    
@discClient.event
async def on_server_join(server):
    msg = 'You have added %s'%discClient.user.name+' to %s server\n\n'%server
    msg+='Permissions required are listed below: \n'+\
        'Read Messages\nSend Messages\nManage Messages\n'+\
        'Embed Links\nRead Message History\nMention Everyone (Optional)\n'+\
        '\nIf a special role has not been assigned to the bot, do ensure to do it with the listed'+\
        ' permissions in order to ensure the bot fully works. It is recommended'+\
        ' to limit the bot to a particular channel(s) by banning it from reading messages in the unwanted channels '+\
        '(so as to not populate general channels with spam)\n'+\
        '\nOnce permissions are set, use the command !start in any of the allowed channel(s) to initialize.'
    msg2='Special commands for server owners:\n!deletebotmsg - Checks the most recent 100 messages and deletes ONLY the bot messages.'+\
          '\n!deleteall - Purges the most recent 100 messages (regardless of user) in the current channel. Confirmation is required to purge.'
    print ('Bot added into: %s'%server,' %s'%server.id)
    try:
        await discClient.send_message(server.owner,msg)
        await discClient.send_message(server.owner,msg2)
    except discord.Forbidden:
        print ('There is permissions error')

discClient.run(TOKEN)
