##Discord MsM LeeksBot
##
##V2.0.0
##-Rewrite completed. async script is now legacy/backup
##
##V1.0.5
##-Changed most of command prefix from ! to ? so as to not clash with most public bots
##  -To do: Change all to ?
##-Storing data taken from sheets into memory
##  -To reduce GET requests but increases mem usage
##  -Should help response time of bot to user requests
##-Force update command added to force refresh data in case of any updates
##-DM bot for feedback added
##-Added images to data
##-Force refresh of loading tokens and sensitive information added to fupdate
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
##  -DM bot for feedback (v1.0.5)
##  -A way to reboot bot instead of killing
##-Consideration to rewrite to discord.py-rewrite branch
##-Added mention for embed responses to user commands
##
##V1.0.3
##-Broadcast message command for all servers to be added
##-Force refresh of loading tokens and sensitive information to be added (v1.0.5)
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
from discord.ext import commands
import logging
import random
import asyncio
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
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
def rs(fupd):
    global royalstylevalues,royalstyleperiod,fupdate

    if not fupd:
        msg = royalstylevalues
        msgTitle = royalstyleperiod
        em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
        if not royalstyleperiod=='No data available':
            em.set_image(url=config['rs'])
        em.set_author(name='Royal Style', icon_url=bot.user.default_avatar_url)
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
    em.set_author(name='Royal Style', icon_url=bot.user.default_avatar_url)
    royalstylevalues = msg
    return em

def ga(fupd):
    global gapplevalues,gappleperiod,fupdate

    if not fupd:
        msg = gapplevalues
        msgTitle = gappleperiod
        em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
        if not gappleperiod=='No data available':
            em.set_image(url=config['ga'])
        em.set_author(name='Golden Apple', icon_url=bot.user.default_avatar_url)
        return em
    
    sheet = service.spreadsheets()
    availableGapple1 = 'GoldApple!B2:E2'
    listGapple1 = 'GoldApple!I3:30'
    availableGapple2 = 'GoldApple!B31:E31'
    listGapple2 = 'GoldApple!I32:I'
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
    em.set_image(url=config['ga'])
    em.set_author(name='Golden Apple', icon_url=bot.user.default_avatar_url)
    gapplevalues=msg
    return em

def rh(fupd):
    global rhairvalues,rhairperiod,fupdate

    if not fupd:
        msg = rhairvalues
        msgTitle = rhairperiod        
        em = discord.Embed(title=msgTitle, description=msg, colour=0x32FF32)
        if not rhairperiod == 'No data available':
            em.set_image(url=config['rh'])
        em.set_author(name='Royal Hair+Face', icon_url=bot.user.default_avatar_url)
        return em
    
    sheet = service.spreadsheets()
    availableRoyal1 = 'RoyalHairFace!B2:C2'
    listRoyal1 = 'RoyalHairFace!F2:I8'
    msg = ''
    #Check if hair available
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=availableRoyal1).execute()
    values = result.get('values', [])
    
    if not (values[0][0]):
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
    em.set_author(name='Royal Hair+Face', icon_url=bot.user.default_avatar_url)
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
        em.set_author(name='Events & Packages', icon_url=bot.user.default_avatar_url)    
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
    em.set_author(name='Events & Packages', icon_url=bot.user.default_avatar_url)
    eventvalues=msg
    return em

def infocheck(fupd):
    global infovalues,infoperiod,fupdate

    if not fupd:
        msg = infovalues
        msgTitle = infoperiod
        em = discord.Embed(title=msgTitle, description=msg)
        em.set_author(name='Leeks', icon_url=bot.user.default_avatar_url)
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
    em.set_author(name='Leeks', icon_url=bot.user.default_avatar_url)
    em.set_image(url=config['in'])
    infovalues=msg
    return em

#3Xplorer update functions changed to general time limited function

def timelimited(c,fupd):
    sheet = service.spreadsheets()
    xtramsg=''
    try:
        command = str.lower(c)
    except:
        return None
    if command == 'mf':
        r = 'Moonlight!F:F'
        msgTitle='Moonlight Fragments'
        xtramsg = '\n\nAppend \'shop\' to the command to view shop list'   
    elif command == 'mfshop':
        r = 'Moonlight!B:E'
        msgTitle='MF Shop'
    elif command == 'smr' or command == 'sr':
        r = 'SoulRing!A:H'
        msgTitle='Soul Made Ring'
    elif command == 'ss':
        r = 'SurpriseStore!A:H'
        msgTitle='Surprise Store'
    elif command == 'emrb':
        em = discord.Embed(title='Extra Mysterious Random Box',\
                           description='Use this Extra Mysterious Random Box to acquire 1 of the following: 4 2,000,000 Red Meso Exchange Ticket, 10,000,000 Enhanced Meso Discount, Innocence Scroll, Advanced Innocence Scroll, Red Cube, Black Cube, Choice Cube, Unique/Legendary Weapon/Armor Whetstones, Unique Weapon/Armor Rank Up Stones, Shield Scroll, Shielding Ward, Lucky Day Scroll (5%, 7%, or 10%).\nProducts can be purchased 10 times per account.')
        em.set_image(url='https://i.imgur.com/Q8ipCZa.png')
        em.set_author(name='Carnival Update', icon_url=bot.user.default_avatar_url)
        return em
    elif command == 'twp':
        em = discord.Embed(title='Toy World Pet')
        em.set_image(url='https://i.imgur.com/MGmJ8GX.png')
        em.set_author(name='Carnival Update', icon_url=bot.user.default_avatar_url)
        return em
    elif command == 'wpc':
        em = discord.Embed(title='White Proposal Costume')
        em.set_image(url='https://i.imgur.com/IhP326g.png')
        em.set_author(name='Carnival Update', icon_url=bot.user.default_avatar_url)
        return em
    elif command == 'adrc':
        em = discord.Embed(title='Antique Dylan & Rosalia Costume')
        em.set_image(url='https://i.imgur.com/7E9QUdB.png')
        em.set_author(name='Carnival Update', icon_url=bot.user.default_avatar_url)
        return em
    elif command == 'gbm':
        em = discord.Embed(title='Glowy Butterfly Masterlabel')
        em.set_image(url='https://i.imgur.com/IQj37Od.png')
        em.set_author(name='Carnival Update', icon_url=bot.user.default_avatar_url)
        return em
    elif command == 'cbbe':
        em = discord.Embed(title='Cherry Blossom Box Event')
        em.add_field(name='Condition',value='Open 30 Cherry Blossom Boxes\nOpen 70 Cherry Blossom Boxes\nOpen 100 Cherry Blossom Boxes',inline=True)
        em.add_field(name='Reward',value='Lucky Day Scroll 7%\nArmor Legendary Rank Up Stone\nNormal Transcendence Stone',inline=True)
        em.set_author(name='Carnival Update', icon_url=bot.user.default_avatar_url)
        return em

    else:
        return None
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

    msg+=xtramsg
    em = discord.Embed(title=msgTitle, description=msg, colour=0x0000FF)
    if (command == 'mf'):
        em.set_image(url=config['mfpony'])

    em.set_author(name='Carnival Update', icon_url=bot.user.default_avatar_url)

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
        return listofstrings[random.randint(1,len(listofstrings))]
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
    return listofstrings[random.randint(1,len(listofstrings))]

def is_bot(m):
    return m.author == bot.user

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

bot = commands.Bot(command_prefix='?')

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
        if (m.guild.id in serversDict):
            return True
        else:
            return False

def servererror(check):
    if (check):
        return 'Please use \?start in a channel in {0} to initialize bot'
    else:
        return

@bot.event
async def on_ready():
    global membersDict,serversDict,fupdate
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    for guilds in bot.guilds:       
        #Store only bot timestamp, other members to be stored dynamically
        membersDict[guilds.me.id]=datetime.datetime.utcnow()
        serversDict[guilds.id]=membersDict
        #clear members dictionary
        membersDict={}
    try:
        rs(True)
        ga(True)
        rh(True)
        eventspackages(True)
        infocheck(True)
        fupdate=False
        print('Sheet data valid')
    except:
        print ('Error in retrieving sheet data. Try to manually force update')
    print ('Bot ready as of '+str(datetime.datetime.utcnow()))
    
#Start of commands----------------------------------------------
#check if initialized in server
@bot.command(name='start',hidden=True,help='To initialize bot in server',brief='Owner')
async def initialstart(ctx):
    global membersDict,serversDict
    if (serverexist(ctx.message)):
        print ('Already initialized')
        return
    if not (ctx.author==ctx.guild.owner):
        await ctx.send('You do not have permissions to do that!')
        return
    await ctx.send('Initializing...')
    if not (checkperms(ctx.guild.me,ctx.message.channel)):
        await ctx.send('Error in permissions. Make sure to assign a special role and required permissions to the bot.')
        return
    #Store only bot timestamp, other members to be stored dynamically
    membersDict[ctx.message.guild.me.id]=datetime.datetime.utcnow()
    serversDict[ctx.message.guild.id]=membersDict
    #clear members dictionary
    membersDict={}
    msg = 'Leeks Seller can now do business :grin:'
    await ctx.send(msg)    

@bot.command(name='give',hidden=True,help='Vegetable',brief='')
async def leeks(ctx,*arg):
    msg = 'I haz leeks... if you have shinies...'
    await ctx.send(msg)

@bot.command(help='Hola! Bonjour! Konnichiwa! Please use English!',brief='')
async def hello(ctx):
    await ctx.channel.trigger_typing()
    if ctx.author.id in serversDict[ctx.guild.id]:
        if not (ctx.message.created_at - serversDict[ctx.guild.id][ctx.author.id])>datetime.timedelta(seconds=5):
            msg = greetings(ctx.message,True)
        else:        
            msg = greetings(ctx.message,False)
    else:
        msg = greetings(ctx.message,False)
    await ctx.send(msg)
    serversDict[ctx.guild.id][ctx.author.id]=ctx.message.created_at

@bot.command(aliases=['royal','royals'],help='Upcoming Overpriced Clothing',brief='')
async def royalstyle(ctx):
    if not (serverexist(ctx.message)):            
        return
    await ctx.channel.trigger_typing()
    em = rs(fupdate)
    if not em:
        msg = 'No Update on Royal Styles found :cry:'
        await ctx.send(msg)
    else:
        msg = '{0.author.mention}'.format(ctx.message)
        await ctx.send(content = msg, embed=em)
    #serversDict[ctx.guild.id][ctx.author.id]=ctx.message.created_at


@bot.command(aliases=['apple','gapple','goldapple'],help='Upcoming Poison Apple',brief='')
async def goldenapple(ctx):
    if not (serverexist(ctx.message)):            
        return
    await ctx.channel.trigger_typing()
    em = ga(fupdate)
    if not em:
        msg = 'No Update on Golden Apples found :cry:'
        await ctx.send(msg)
    else:
        msg = '{0.author.mention}'.format(ctx.message)           
        await ctx.send(content=msg, embed=em)            
    #serversDict[ctx.guild.id][ctx.author.id]=ctx.message.created_at

@bot.command(aliases=['hair','face'],help='Upcoming Expensive Hair and Plastic Surgery',brief='')
async def royalhair(ctx):
    if not (serverexist(ctx.message)):            
        return
    await ctx.channel.trigger_typing()
    em = rh(fupdate)
    if not em:
        msg = 'No Update on Royal Hair+Face found :cry:'
        await ctx.send(msg)
    else:
        msg = '{0.author.mention}'.format(ctx.message)
        
        await ctx.send(content=msg, embed=em)
    #serversDict[ctx.guild.id][ctx.author.id]=ctx.message.created_at

@bot.command(aliases=['event','package','packages'],help='Upcoming Events that have miserable rewards and Cash grabs to fund dev parties',brief='')
async def events(ctx):
    if not (serverexist(ctx.message)):            
        return
    await ctx.channel.trigger_typing()
    em = eventspackages(fupdate)
    if not em:
        msg = 'No Update on Events found :cry:'
        await ctx.send(msg)
    else:
        msg = '{0.author.mention}'.format(ctx.message)
        
        await ctx.send(content=msg, embed=em)
    #serversDict[ctx.guild.id][ctx.author.id]=ctx.message.created_at

@bot.command(aliases=['information','lastupdate'],help='Data last updated and other general information',brief='')
async def info(ctx):
    if not (serverexist(ctx.message)):            
        return
    await ctx.channel.trigger_typing()
    em = infocheck(fupdate)
    msg = '{0.author.mention}'.format(ctx.message)
    await ctx.send(content=msg, embed=em)
    #serversDict[ctx.guild.id][ctx.author.id]=ctx.message.created_at

@bot.command(aliases=['badbot','complain'],help='Not happy with me?',brief='')
async def feedback(ctx):
    await ctx.send('Spot a bug? Leaving feedback? Drop a DM to the bot or submit them here\: discord.gg\/HYWn5bT')

@bot.command(aliases=['extra'],help='Additional Temporary command for time-limited data',brief='')
async def xtra(ctx,*arg):
    if len(arg)==1:
        em=timelimited(arg[0],fupdate)
    elif len(arg)==2:
        em=timelimited(arg[0]+arg[1],fupdate)
    elif arg==None:
        await ctx.send('')
    else:
        await ctx.send('Arguments invalid')
        return
    
    if em is None:
        await ctx.send('Command or arguments not available')        
    else:
        msg='{0.author.mention}'.format(ctx.message)
        await ctx.send(content=msg,embed=em)

@bot.command(hidden=True,name='emrb',aliases=['ss','smr','sr','mf','cbbe','wpc','twp','adrc','gbm'],help='Redirector',brief='')
async def temp(ctx):
    await ctx.send('You are trying to use a temporary command. Please use them as arguments in ?extra <arg>')
    
#Server owner/bot owner commands----------------------------------------------
    
@bot.command(name='fupdate',hidden=True,help='Force update only for bot owner',brief='')
async def forceupdate(ctx):
    global fupdate,config
    try:
        with open('config.json') as data_file:
            config=json.load(data_file)
            TOKEN = config['bot_token']
            BOT_OWNER_ID = config['bot_owner_id']
    except:
        await ctx.message.delete()
        await ctx.send('Error in config')
        return
    if not ctx.author.id == BOT_OWNER_ID:
        await ctx.message.delete()
        return
    try:
        rs(True)
        print('rs')
        ga(True)
        print('ga')
        rh(True)
        print('rh')
        eventspackages(True)
        print('ep')
        infocheck(True)
        print('in')
        fupdate=False
        
    except:
        await ctx.send('There was an error refreshing data')
        await ctx.message.delete()
        fupdate=True
    
    await ctx.send('Force update successful')
    await ctx.message.delete()
    return

@bot.command(hidden=True,help='Megaphone that is not for you',brief='Not for you')
async def broadcast(ctx):
    if not ctx.author.id == BOT_OWNER_ID:
        return

    def check(m):
        return (m.channel==ctx.channel and m.author==ctx.author)
    
    await ctx.send('Type your message now.\nUse !cancel to cancel broadcast.')
    msgtobroadcast = await bot.wait_for('message', check=check)

    #check if cancelled by owner
    if msgtobroadcast.content.startswith('!cancel'):
        await ctx.send('Broadcast cancelled')
        return

    tempmsg = 'Please check if message is correct.\n'+\
              msgtobroadcast.content+'\nType \'Yes\' to confirm. Confirmation expires in 10 seconds'

    await ctx.send(tempmsg)

    def confirm(m):
        return (m.content=='Yes' and m.author==ctx.author)
    tempmsg2=None
    try:
        tempmsg2 = await bot.wait_for('message', check=confirm, timeout=10)
    except asyncio.TimeoutError:
        print('Timeout')
    if tempmsg2 == None:
        await ctx.send('Broadcast cancelled due to timeout')
        return

    #Start broadcast
    #Get list of servers
    for guild in bot.guilds:
        #flag to see if at least one message posted in a server, temp string
        posted=False
        tempstring=''
        #Get list of channels
        for channel in guild.text_channels:
            print ('in')
            #Check for permissions
            if checkperms(guild.me,channel):
                tempstring = msgtobroadcast.content
                await channel.send(tempstring)
                await asyncio.sleep(0.3)
                posted=True
        #If no message posted in server, send message to owner instead
        if not posted:
            try:
                await guild.owner.send(content=msgtobroadcast.content)
            except discord.Forbidden:
                print ('Forbidden to message user')
            await asyncio.sleep(0.3)
            
@bot.command(hidden=True,help='It is the end of the world',brief='Not for you')
async def end(ctx):
    if ctx.author.id==BOT_OWNER_ID:
        await bot.close()
    else:
        await ctx.send('{0.author.mention}, looks like you don\'t have permission to do that'.format(ctx.message))

@bot.command(help='No arg = Delete all\n\'bot\' arg = Delete only messages from this bot',brief='Server owner')
async def deletemsg(ctx,*arg):
    if not (serverexist(ctx.message)):            
        return
    if ctx.message.author == ctx.message.guild.owner:
        perms = ctx.message.channel.permissions_for(ctx.message.guild.me)
        if (perms.manage_messages):
            if len(arg)<1:
                deleted = await ctx.channel.purge(limit=100)
            elif (len(arg)==1 and 'bot' in arg):                
                deleted = await ctx.channel.purge(limit=100, check=is_bot)
            else:
                return
            await ctx.send('{} message(s) have been purged'.format(len(deleted)))
        else:
            msg = 'Bot does not have the required permission(s)'
            await ctx.send(msg)
            return
#Error handling----------------------------------------------

@bot.event
async def on_command_error(ctx,error):

    if isinstance(error,discord.ext.commands.errors.CommandNotFound):
        print ('Command Not Found')
        return
    else:
        print (error)
        
bot.run(TOKEN)
