# Work with Python 3.6
#3.7 does not support async/await

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
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

store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))
#----------------------------------------
def royalstyle():
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
        return ''
    else:        
        msgTitle = '%s'%values[0][3]+'\n%s'%values[0][0]+' to '+'%s'%values[0][1]
            
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
        em.set_author(name='Royal Style', icon_url=discClient.user.default_avatar_url)
        
        return em

def goldenapple():
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
        return ''
    else:        
        msgTitle = '%s'%values[0][3]+'\n%s'%values[0][0]+' to '+'%s'%values[0][1]
            
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
        em.set_author(name='Golden Apple', icon_url=discClient.user.default_avatar_url)
        
        return em

def royalhair():
    sheet = service.spreadsheets()
    availableRoyal1 = 'RoyalHairFace!B2:C2'
    listRoyal1 = 'RoyalHairFace!F2:I8'
    msg = ''
    #Check if hair available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=availableRoyal1).execute()
    values = result.get('values', [])

    if not values[0][0]:                
        return ''
    else:        
        msgTitle = '%s'%values[0][0]+' to '+'%s'%values[0][1]
            
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
    em.set_author(name='Royal Hair+Face', icon_url=discClient.user.default_avatar_url)
    #em.set_image(url='https://cdn.discordapp.com/attachments/488019800136876035/533583572297187348/leek.jpg')
    
    return em

def eventspackages():
    sheet = service.spreadsheets()
    availableEvents1 = 'Events&Packages!A:E'
    msg = ''
    #Check if events available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=availableEvents1).execute()
    values = result.get('values', [])

    if not values[0][0]:                
        return ''
    else:
        msgTitle = 'List of Events/Packages'

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
        msg='There does not seem to be any future content :('
    em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
    em.set_author(name='Events & Packages', icon_url=discClient.user.default_avatar_url)
    
    
    return em

def infocheck():
    sheet = service.spreadsheets()
    lastUpdated = 'Landing!A2:3'
    msg = ''
    #Check update available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=lastUpdated).execute()
    values = result.get('values', [])

    msgTitle='Info'

    msg='%s'%values[0][0]+'\n%s\n'%values[1][0]
    em = discord.Embed(title=msgTitle, description=msg)
    em.set_author(name='Leeks', icon_url=discClient.user.default_avatar_url)
    em.set_image(url='https://cdn.discordapp.com/attachments/488019800136876035/533583572297187348/leek.jpg')

    return em

#3Xplorer update functions

def xplorer(command):
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

#Used for iterations
i=1
it=1
interval=0

#Used to store author and timestamps
membersDict = {}
serversDict = {}

#check if server exist in dictionary, else prompt owner to initialize
#mostly to deal with newly added servers
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
        for mems in servers.members:
            membersDict[mems.id] = datetime.datetime.utcnow()
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
        for mems in message.server.members:
            membersDict[mems.id] = datetime.datetime.utcnow()
        serversDict[message.server.id]=membersDict
        #clear members dictionary
        membersDict={}
        msg = 'Leeks Seller can now do business :grin:'
        await discClient.send_message(message.channel, msg)
    if not (serverexist(message)):
        return
    #limit user commands to 1 every 2 sec
    if '!' in message.content and not (message.timestamp - serversDict[message.server.id][message.author.id])>datetime.timedelta(seconds=2):
        msg = 'You have already sent a command recently!'
        await discClient.send_message(message.channel, msg)
        #serversDict[message.server.id][message.author.id]=message.timestamp
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
        if not (message.timestamp - serversDict[message.server.id][message.author.id])>datetime.timedelta(seconds=5):
            msg = greetings(message,True)
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
        em = royalstyle()
        if not em:
            msg = 'No Update on Royal Styles found :cry:'
            await discClient.send_message(message.channel, msg)
        else:
            await discClient.send_message(message.channel, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!goldenapple'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = goldenapple()
        if not em:
            msg = 'No Update on Golden Apples found :cry:'
            await discClient.send_message(message.channel, msg)
        else:
            await discClient.send_message(message.channel, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!royalhair'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = royalhair()
        if not em:
            msg = 'No Update on Royal Hair+Face found :cry:'
            await discClient.send_message(message.channel, msg)
        else:
            await discClient.send_message(message.channel, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!events'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = eventspackages()
        if not em:
            msg = 'No Update on Events found :cry:'
            await discClient.send_message(message.channel, msg)
        else:
            await discClient.send_message(message.channel, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp
        
    if message.content.startswith('!info'):
        if not (serverexist):            
            return
        await discClient.send_typing(message.channel)
        em = infocheck()
        await discClient.send_message(message.channel, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp

    if message.content.startswith('!deletebotmsg'):
        if not (serverexist):            
            return
        if message.author == message.server.owner:
            perms = message.channel.permissions_for(message.server.me)
            if (perms.manage_messages):
                deleted = await discClient.purge_from(message.channel, limit=50, check=is_bot)
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
        await discClient.send_message(message.channel, '{} message(s) have been purged'.format(len(deleted)))

    #Jan update commands--------------------------
    if message.content.startswith('!jan'):
        if not message.author.id == BOT_OWNER_ID:
            return
        if 'emblem' in message.content:
            em = xplorer('emblem')
        elif 'exalt' in message.content:
            em = xplorer('exalt')
        else:
            await discClient.send_message(message.channel, 'Argument missing')
            return
        if not em:
            msg = 'No data exist!'
            await discClient.send_message(message.channel, msg)
        else:
            await discClient.send_message(message.channel, embed=em)
        serversDict[message.server.id][message.author.id]=message.timestamp
    
##    if message.content.startswith('!random'):
##        if not (serverexist):            
##            return
##        global i
##        i=1
##        looping=True
##        await discClient.send_typing(message.channel)
##        msg = 'This is message number %d'%i+' for {0.author.mention}'.format(message)
##        await discClient.send_message(message.channel, msg)
##        i+=1
##
##        def iteration(msg):
##            if msg.content.startswith('!next'):
##                return msg.content.startswith('!next')
##            elif msg.content.startswith('!random'):
##                return msg.content.startswith('!random')
##            else:
##                return None
##        
##        while (looping):
##            message.content=''
##            message = await discClient.wait_for_message(author=message.author,check=iteration,timeout=15)
##
##            if message==None:
##                looping=False
##            elif message.content.startswith('!next'):
##                if i>5:
##                    msg = nestedconvo(message,i)
##                    await discClient.send_message(message.channel, msg)
##                    i+=1
##                else:
##                    print (message.content)
##                    msg = 'This is message number %d'%i+' for {0.author.mention}'.format(message)
##                    await discClient.send_message(message.channel, msg)
##                    i+=1
##            else:
##                looping=False
##            print (looping)
##        print ('Out of loop')

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
        'Embed Links\nRead Message History\nMention Everyone (may be required in the future)\n'+\
        '\nIf a special role has not been assigned to the bot, do ensure to do it with the listed'+\
        ' permissions in order to ensure the bot fully works. It is recommended'+\
        ' to limit the bot to a particular channel(s) by banning it from reading messages in the unwanted channels '+\
        '(so as to not populate general channels with spam)\n'+\
        '\nOnce permissions are set, use the command !start in any of the allowed channel(s) to initialize.'
    
    print ('Bot added into: %s'%server,' %s'%server.id)
    try:
        await discClient.send_message(server.owner,msg)
    except discord.Forbidden:
        print ('There is permissions error')

discClient.run(TOKEN)
