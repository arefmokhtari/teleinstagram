#::::::::::::::::::::::::::::::::::::::::::::::::[ Sobhan & Aref ]
import pkg_resources
prerequisites = ['pyrogram','pyromod','redis','python-dotenv','instaloader']
def checklib_Main():
    packages = pkg_resources.working_set; pack_list, s = sorted([i.key for i in packages]), []
    for q in prerequisites:
        if q not in pack_list: print(f'$ pip install {q}'); s.append(q); continue
        if len(s) != 0: print('Install All of these Libraries :',s); sys.exit(0)
    print('Libraries were surveyed')
checklib_Main()
#::::::::::::::::::::::::::::::::::::::::::::::::( Import Libraries )
import os, sys, redis, json, random as rand
import asyncio, requests as req, instaloader
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, errors, enums
from pyrogram.types import *
from pyrogram import filters
from datetime import datetime as dt
from dotenv import load_dotenv
timstart = dt.now()
load_dotenv()
#::::::::::::::::::::::::::::::::::::::::::::::::( Instagram )
def change_file_names(files: os.listdir, path: os.getcwd):
    for file in files:
        if not file.endswith('mp4') or not file.endswith('jpg'):
            if file.endswith('gif'): os.rename(path+'/'+file, path+'/'+file[:file.rfind('.'):]+'.mp4')   
            elif file.endswith('webp'):os.rename(path+'/'+file, path+'/'+file[:file.rfind('.'):]+'.jpg')
async def checkfile(pattern: str) -> bool:
    if pattern.endswith('xz') or pattern.endswith('txt') or pattern.endswith('json'): return False
    return True
async def check_member(uid) -> bool:
    for i in channels:
        try: await gnu.get_chat_member(i, uid)
        except errors.exceptions.bad_request_400.UserNotParticipant: return False
    return True
async def setfilelist(files: list):
    for file in files.copy():
        if file.endswith('.mp4'):
            try:files.remove(file[:file.find('.mp4')]+'.jpg')
            except:pass
async def checklist4insta(pattern: str) -> str:
    if 'https' in pattern and 'instagram.com' in pattern:
        if '/stories/' in pattern: return 'story'
        elif '/p/' in pattern or '/reel/' in pattern or '/tv/' in pattern: return 'post'
        elif '/s/' in pattern: return 'hlight'
        else: return 'profile'
async def removedir(target, cwd):
    for file in os.listdir(cwd+'/'+target): 
        os.remove(cwd+'/'+target+'/'+file)
    os.rmdir(target)
def login_insta(insta, session, username, passwd):
    try: insta.load_session_from_file(username, session)
    except: insta.login(username, passwd); insta.save_session_to_file(session)
async def user_data(user: str):
    if user not in gnudata.lrange('TeleInstaGraMBOT', 0, -1) and int(user) not in sudo: gnudata.lpush('TeleInstaGraMBOT', user)
#::::::::::::::::::::::::::::::::::::::::::::::::( Clients )
insta = instaloader.Instaloader()
gnu = Client("Gnubot", api_id=os.getenv('api_id'), api_hash=os.getenv('api_hash'), bot_token= os.getenv('token'))
login_insta(insta, session = 'gnu_instagram', username = os.getenv('insta_username'), passwd = os.getenv('insta_password'))
#::::::::::::::::::::::::::::::::::::::::::::::::( DataBase )
gnudata = redis.StrictRedis(host = str(os.getenv('host', '127.0.0.1')), port = os.getenv('port', 6379), db= os.getenv('db', 1), decode_responses = True) 
gnudata.set('Aref&Sobhan', 'gun')
#::::::::::::::::::::::::::::::::::::::::::::::::( Random )
TS1, TS2 = ["➲ ","》 ","❈ ","⇝ ","⊶ ","⟝ ","⊱ ","⭑ ","⭒ ","- "], [" ⊷"," ⊰"," ⭑"," ⭒"," !"]
PL0, SLPP, SLP = [" • "," ⭑ "," ❈ "," ✯ "," ✮ "," ◈ "," ⌬ "," ⎆ "], [10, 11, 12, 13, 14, 15, 16], [3, 4, 5, 6]
HP1, HP2 = ["✩","❖","✯","⎆","✺","❖","♤","◗","♧","▣","♢","▸"], ["○","✞","◈","⋆","◖","☻","❅","❃","✪","✵","❅","✾","≛"]
ACS = ["typing","choose_sticker","import_history","upload_photo","record_video","upload_video","record_audio","upload_audio","upload_document","find_location","record_video_note","upload_video_note","playing","choose_contact","speaking"]
#::::::::::::::::::::::::::::::::::::::::::::::::( Variable )
sudo, channels = [int(i) for i in os.getenv('sudo').split()], [int(i) for i in os.getenv('ch_join', None).split()]
channels_username, bot_username = [i for i in os.getenv('channels_username', None).split()], os.getenv('bot_username', None)
#::::::::::::::::::::::::::::::::::::::::::::::::( Class Main ) 
class Main:
    async def Post(_, msg: Message, uid):
        tmsg, chat_id = msg.text, msg.chat.id
        ST1, ST2, ST3, ST4 = rand.choice(TS1), rand.choice(TS2), rand.choice(ACS), rand.choice(HP1)
        if not await check_member(uid):
            mark_channels = [[InlineKeyboardButton(f'[{ST4} {channel} {ST4}]' ,url=f"https://t.me/{channel}")] for channel in channels_username]
            mark_channels.append([InlineKeyboardButton(f"[{ST4} Start {ST4}]" ,url=f"https://t.me/{bot_username}?start=start",)])
            mark = InlineKeyboardMarkup(mark_channels)  
            await msg.reply(f'{ST1}شما عضو چنل نیستی{ST2}', reply_markup= mark)
        else:
            tp = tmsg.replace('?', '/').split('/'); linkpost = tp [4]; xt = ''.join(chr(rand.randint(97, 122)) for _ in range(4)); target =  xt+linkpost
            try : post = instaloader.Post.from_shortcode(insta.context, linkpost)
            except instaloader.exceptions.BadResponseException: await msg.reply(f'{ST1}پست مورد نظر یافت نشد{ST2}')
            else:
                if (post.video_duration or 0) <= 300:
                    wait_msg = await msg.reply(f'{ST1}لطفا صبر کنید{ST2}')
                    await msg.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
                    insta.download_post(post, target) 
                    change_file_names(os.listdir(os.getcwd()+'/'+target), os.getcwd()+'/'+target)
                    filelist = os.listdir(os.getcwd()+'/'+target)
                    file_jpg_mp4 = [file for file in filelist if await checkfile(file)]
                    await setfilelist(file_jpg_mp4)
                    send_file = [os.getcwd()+'/'+target+'/'+file for file in file_jpg_mp4]
                    caption = f'{ST1} username = {post.owner_username}\n{ST1} like = {post.likes}\n{ST1} comments = {post.comments}\n{ST1} caption = {post.caption}\n__________________ \n{ST1} @{bot_username}'
                    caption = caption[: 1024 if len(caption)>1024 else len(caption)]
                    tfile, end_file = [InputMediaVideo(file) if file.endswith('.mp4') else InputMediaPhoto(file) for file in  send_file], send_file[len(send_file)-1]
                    tfile[len(tfile)-1] = InputMediaVideo(end_file,caption= caption) if end_file.endswith('.mp4') else InputMediaPhoto(end_file,caption= caption)
                    await gnu.send_media_group(chat_id, tfile)
                    await wait_msg.delete()
                    await removedir(target, os.getcwd())
                else: await msg.reply(f'{ST1}ویدیوی پست بیشتر از 5 دیقس{ST2}')
    async def PorFile(_, msg: Message, uid):
        tmsg, chat_id = msg.text, msg.chat.id
        ST1, ST2, ST3, ST4 = rand.choice(TS1), rand.choice(TS2), rand.choice(ACS), rand.choice(HP1)
        if not await check_member(uid):
            mark_channels = [[InlineKeyboardButton(f'[{ST4} {channel} {ST4}]' ,url=f"https://t.me/{channel}")] for channel in channels_username]
            mark_channels.append([InlineKeyboardButton(f"[{ST4} Start {ST4}]" ,url=f"https://t.me/{bot_username}?start=start",)])
            mark = InlineKeyboardMarkup(mark_channels)  
            await msg.reply(f'{ST1}شما عضو چنل نیستی{ST2}', reply_markup= mark)
        else:
            tp = tmsg.replace('?', '/').split('/'); username = tp[3]
            profile = instaloader.Profile.from_username(insta.context, username)
            wait_msg = await msg.reply(f'{ST1}لطفا صبر کنید{ST2}')
            await msg.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
            insta.download_profile(profile, profile_pic_only=True)
            caption = f'{ST1}name = {profile.full_name}\n{ST1}bio = {profile.biography}\n{ST1}followers = {profile.followers:,}\n__________________ \n{ST1} @{bot_username}'
            caption = caption[: 1024 if len(caption)>1024 else len(caption)]
            profile_photo = [photo for photo in os.listdir(os.getcwd()+'/'+username) if photo.endswith('.jpg')][0]
            await gnu.send_photo(chat_id, os.getcwd()+'/'+username+'/'+profile_photo, caption=caption)
            await wait_msg.delete()
            await removedir(username, os.getcwd())
    async def Story(_, msg: Message, uid):
        tmsg, chat_id = msg.text, msg.chat.id
        ST1, ST2, ST3, ST4 = rand.choice(TS1), rand.choice(TS2), rand.choice(ACS), rand.choice(HP1)
        if not await check_member(uid):
            mark_channels = [[InlineKeyboardButton(f'[{ST4} {channel} {ST4}]' ,url=f"https://t.me/{channel}")] for channel in channels_username]
            mark_channels.append([InlineKeyboardButton(f"[{ST4} Start {ST4}]" ,url=f"https://t.me/{bot_username}?start=start",)])
            mark = InlineKeyboardMarkup(mark_channels)  
            await msg.reply(f'{ST1}شما عضو چنل نیستی{ST2}', reply_markup= mark)
        else:
            wait_msg = await msg.reply(f'{ST1}لطفا صبر کنید{ST2}')
            await msg.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
            try:
                tp = tmsg.replace('?', '/').split('/') ; username, story_id = [tp[4], int(tp[5])]
                target = username+str(story_id)
                profile = instaloader.Profile.from_username(insta.context,username)#insta.check_profile_id(username)
            except (instaloader.exceptions.ProfileNotExistsException, ValueError) as e: 
                await wait_msg.edit(f'{ST1} یافت نشد {ST2}')
                print('-',e)
            else:
                for story in insta.get_stories(userids=[profile.userid]):
                    for item in story.get_items():
                        if story_id == item.mediaid:
                            insta.download_storyitem(item, target=target)
                            change_file_names(os.listdir(os.getcwd()+'/'+target), os.getcwd()+'/'+target)
                            filelist = os.listdir(os.getcwd()+'/'+target)
                            file_jpg_mp4 = [file for file in filelist if await checkfile(file)]
                            await setfilelist(file_jpg_mp4)
                            caption = f'{ST1}username : {username}\n{ST1}name : {profile.full_name}\n__________________ \n{ST1} @{bot_username}'
                            send_file = [os.getcwd()+'/'+target+'/'+file for file in file_jpg_mp4][0]
                            await gnu.send_video(chat_id, send_file, caption=caption) if send_file.endswith('.mp4') else await gnu.send_photo(chat_id, send_file, caption=caption)
                            await removedir(target, os.getcwd())
                            await wait_msg.delete()
                            return
                await removedir(username, os.getcwd())
                print('--')
                await wait_msg.edit(f'{ST1} یافت نشد {ST2}')
    async def Light(_, msg: Message, uid):
        tmsg, chat_id = msg.text, msg.chat.id
        ST1, ST2, ST3, ST4 = rand.choice(TS1), rand.choice(TS2), rand.choice(ACS), rand.choice(HP1)
        if not await check_member(uid):
            mark_channels = [[InlineKeyboardButton(f'[{ST4} {channel} {ST4}]' ,url=f"https://t.me/{channel}")] for channel in channels_username]
            mark_channels.append([InlineKeyboardButton(f"[{ST4} Start {ST4}]" ,url=f"https://t.me/{bot_username}?start=start",)])
            mark = InlineKeyboardMarkup(mark_channels)  
            await msg.reply(f'{ST1}شما عضو چنل نیستی{ST2}', reply_markup= mark)
        else:
            wait_msg = await msg.reply(f'{ST1}لطفا صبر کنید{ST2}')
            await msg.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
            try:
                media_id, username = map(int,tmsg[tmsg.find('story_media_id')+15:tmsg.rfind('&igshid')].split('_'))
                target = str(username)+str(media_id)
                profile = instaloader.Profile.from_id(insta.context, username)
                
            except (instaloader.exceptions.ProfileNotExistsException, ValueError): await wait_msg.edit(f'{ST1} یافت نشد {ST2}')
            else:
                for highlight in insta.get_highlights(profile):
                    for item in highlight.get_items():
                        if media_id == item.mediaid:
                            insta.download_storyitem(item, target=target)
                            change_file_names(os.listdir(os.getcwd()+'/'+target), os.getcwd()+'/'+target)
                            filelist = os.listdir(os.getcwd()+'/'+target)
                            file_jpg_mp4 = [file for file in filelist if await checkfile(file)]
                            await setfilelist(file_jpg_mp4)
                            caption = f'{ST1}username : {profile.username}\n{ST1}name : {profile.full_name}\n__________________ \n{ST1} @{bot_username}'
                            send_file = [os.getcwd()+'/'+target+'/'+file for file in file_jpg_mp4][0]
                            await gnu.send_video(chat_id, send_file, caption=caption) if send_file.endswith('.mp4') else await gnu.send_photo(chat_id, send_file, caption=caption)
                            await removedir(target, os.getcwd())
                            await wait_msg.delete()
                            return
                await removedir(username, os.getcwd())
                await wait_msg.edit(f'{ST1} یافت نشد {ST2}')
    async def Tiktok(_, msg: Message, uid):
        pass
    async def Antiflood(_, msg:Message)->int:
        uid, cid, msgj = msg.from_user.id, str(msg.chat.id), json.loads(str(msg))
        ST1 = rand.choice(TS1)
        if msgj['chat']['type'] == 'ChatType.SUPERGROUP' and filters.group:
            if gnudata.get(cid): 
                await msg.reply(f"{ST1}Erorr Flood : s{gnudata.ttl(cid)}")
            else:
                gnudata.setex(cid, 10, 'Group')
                return 1
        elif msgj['chat']['type'] == 'ChatType.PRIVATE' and filters.private:
            if 'Private' == gnudata.get(uid): 
                await msg.reply(f'{ST1}Erorr Flood : s{gnudata.ttl(uid)}')
            else:
                gnudata.setex(uid, 5, 'Private')
                return 1
#::::::::::::::::::::::::::::::::::::::::::::::::( Class GData )
class GData:
    async def Dbase()->json:
        datab = gnudata.hget('gnu', 'data'); basej = None if datab is None else json.loads(datab)
        database ={'uptime': 0, 'total_usage': 0, 'last_changer': None,
                    'service': {
                        'insta':{'dpost': {'_': 1, 'used': 0},
                                'dprof': {'_': 1, 'used': 0},
                                'dstoy': {'_': 1, 'used': 0},
                                'dlight': {'_': 1, 'used': 0}},
                        'tiktok':{'_': 1, 'used': 0}},
                    'advertising': {'_': 1, 'posted': 0, 'information': {}}, 'boycott': []}
        if basej == None : 
            gnudata.hset('gnu', 'data', json.dumps(database))
            return await GData.Dbase()
        else : return basej
    async def Duser(uid)->json:
        datau = gnudata.hget('gnu', uid); userj = None if datau is None else json.loads(datau)
        datauser ={'amsg': 0, 'ilink': 0, 'tlink': 0}
        if userj == None: 
            gnudata.hset('gnu', uid, json.dumps(datauser))
            return await GData.Duser(uid)
        else : return userj
    async def Cinsta(_t, uid):
        db, du = await GData.Dbase(),await GData.Duser(uid)
        if _t =='post':
            db['service']['insta']['dpost']['used'] += 1
        elif _t == 'profile':
            db['service']['insta']['dprof']['used'] += 1
        elif _t == 'story':
            db['service']['insta']['dstoy']['used'] += 1
        elif _t == 'hlight':
            db['service']['insta']['dlight']['used'] += 1
        db['total_usage'] += 1
        du['amsg']  += 1
        du['ilink'] += 1
        gnudata.hset('gnu', 'data', json.dumps(db)); gnudata.hset('gnu', uid, json.dumps(du))
    async def Ctiktok(_t, uid):
        db, du = await GData.Dbase(),await GData.Duser(uid)
        db['service']['tiktok']['used'] += 1
        db['total_usage'] += 1
        du['amsg'] += 1
        du['tlink'] += 1
        gnudata.hset('gnu', 'data', json.dumps(db)); gnudata.hset('gnu', uid, json.dumps(du))
    async def GetMember()->list:
        db = gnudata.hgetall('gnu')
        return List(db.keys())
    async def __dir__(uid):
        db, du = await GData.Dbase(),await GData.Duser(uid)
        print(db, "\n====================\n", du)
#::::::::::::::::::::::::::::::::::::::::::::::::( Start )
@gnu.on_message(filters.private & filters.command(["start", " Back 《"], ["/","》"]))
async def Start(_, msg: Message):
    ST1, ST2, uid = rand.choice(TS1), rand.choice(TS2), msg.from_user.id
    await user_data(str(uid))
    mark = ReplyKeyboardMarkup(keyboard=[[KeyboardButton("》 مدیریت 《")]], resize_keyboard= True)
    pm = f'{ST1} سلام مدیر {msg.from_user.mention} , به ربات خودتون خوشامدید {ST2}\n\n{ST1}از دکمه های زیر برای مدیریت ربات استفاده کنید{ST2}\n{ST1}برای دانلود از اینستاگرام لینک را ارسال کنید {ST2}\n\n{ST1} @{bot_username}'
    pm1 = f'{ST1} سلام کاربر عزیز {msg.from_user.mention} , برای دانلود از اینستاگرام لینک را ارسال کنید {ST2}\n\n{ST1} @{bot_username}'
    await msg.reply(pm, reply_markup= mark) if uid in sudo else await msg.reply(pm1)
#::::::::::::::::::::::::::::::::::::::::::::::::( Manage )
@gnu.on_message(filters.private & filters.command(" مدیریت 《", "》") & filters.user(sudo))
async def Manage(_, msg: Message):
    ST1, ST2, dj, ul = rand.choice(TS1), rand.choice(TS2), await GData.Dbase(), await GData.GetMember()
    mark = ReplyKeyboardMarkup(keyboard=[[KeyboardButton("• پشتیبانگیری •")], [KeyboardButton("》 Back 《")]], resize_keyboard= True)
    await msg.reply(f'{ST1}به بخش مدیریت ربات خوش امدید {ST2}\n{ST1}با استفاده از دکمه ها به بخش های که مد نظرتان است بروید .{ST2}\n\n{ST1}کل دانلود ها : {dj["total_usage"]}\n{ST1}پست ها : {dj["service"]["insta"]["dpost"]["used"]}\n{ST1}پروفایل ها : {dj["service"]["insta"]["dprof"]["used"]}\n{ST1}ستوری ها : {dj["service"]["insta"]["dstoy"]["used"]}\n{ST1}ممبر ها :{(len(ul)-1)}\n\n{ST1} @{bot_username}', reply_markup= mark)
#::::::::::::::::::::::::::::::::::::::::::::::::( Ping )
@gnu.on_message(filters.command("ing", ['p', 'P']) & filters.user(sudo))
async def Ping(_, msg: Message):
    ST1, ST2, dj = rand.choice(TS1), rand.choice(TS2), await GData.Dbase()
    tStart = dt.now();pm = f'{ST1} Bot is Alive {ST2}\n\n{ST1} UpTime  : {dj["uptime"]}\n{ST1} Pong  : {(dt.now()-tStart).microseconds/100} s\n\n{ST1} @{bot_username}'
    await msg.reply(pm)
#::::::::::::::::::::::::::::::::::::::::::::::::( Backup )
@gnu.on_message(filters.private & filters.command(" پشتیبانگیری •", '•') & filters.user(sudo))
async def Backup(_, msg: Message):
    ST1, ST2 = rand.choice(TS1), rand.choice(TS2)
    gpj = gnudata.hgetall('gnu')
    filename = "Gnu"+'.json'
    with open(filename, 'w') as f:
        json.dump(gpj, f) 
    await msg.reply_document(filename, caption=f'{ST1}فایل ارسال شد{ST2}\n\n{ST1} @{bot_username}')
#::::::::::::::::::::::::::::::::::::::::::::::::( Rload )
@gnu.on_message(filters.command("eload", ['r', 'R']) & filters.user(sudo))
async def RloadBot(_, msg: Message):
    ST1, ST2, db = rand.choice(TS1), rand.choice(PL0), await GData.Dbase()
    db["uptime"] = 0
    await msg.reply (f'{ST1} Bot Reloaded {ST2}')
    gnudata.hset('gnu', 'data', json.dumps(db))
    os.execl(sys.executable, sys.executable, *sys.argv)
#::::::::::::::::::::::::::::::::::::::::::::::::( GetLink )
@gnu.on_message(filters.private and filters.chat(chats=[-1001517322540, -1001553910373, -1001555983672, -1001658873133, -1001623086386]) and filters.text)
async def GetLink(_, msg: Message):
    tmsg, uid = msg.text, msg.from_user.id
    await user_data(str(uid))
    gettmsg = await checklist4insta(tmsg)
    if gettmsg == 'post':
        if await Main.Antiflood(_, msg): await Main.Post(_, msg, uid)
        await GData.Cinsta(gettmsg, uid)
    elif gettmsg == 'profile':
        if await Main.Antiflood(_, msg): await Main.PorFile(_, msg, uid)
        await GData.Cinsta(gettmsg, uid)
    elif gettmsg == 'story':
        if await Main.Antiflood(_, msg): await Main.Story(_, msg, uid)
        await GData.Cinsta(gettmsg, uid)
    elif gettmsg == 'hlight':
        if await Main.Antiflood(_, msg): await Main.Light(_, msg, uid)
        await GData.Cinsta(gettmsg, uid)
#::::::::::::::::::::::::::::::::::::::::::::::::( Main Inline )
@gnu.on_inline_query()
async def MaiNInliNe(_, callq: InlineQuery):
    typemsg = await checklist4insta(callq.query)
    if typemsg == 'post' :
        await callq.answer(results=[InlineQueryResultPhoto(title="Photo",
            input_message_content=InputTextMessageContent("**Photo**"), description="How ",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ Start ]" ,url=f"https://t.me/{bot_username}?start=start")]])),
        InlineQueryResultVideo(title="Video",
            input_message_content=InputTextMessageContent("**Video**"), description="How ",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ Start ]" ,url=f"https://t.me/{bot_username}?start=start")]]))], cache_time=1)
    elif typemsg == 'profile' :
        await callq.answer(results=[InlineQueryResultPhoto(title="Photo",
            input_message_content=InputTextMessageContent("**Photo**"), description="How ",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ Start ]" ,url=f"https://t.me/{bot_username}?start=start")]]))], cache_time=1)
    elif typemsg == 'story' : await InlineStory(_, callq)
#::::::::::::::::::::::::::::::::::::::::::::::::( Inline Story )
async def InlineStory(_, callq: InlineQuery):
        tmsg = callq.query
        ST1, ST2, ST3 = rand.choice(TS1), rand.choice(TS2), rand.choice(ACS)     
        try:
            tp = tmsg.replace('?', '/').split('/') ; username, story_id = [tp[4], int(tp[5])]
            target = username+str(story_id)
            profile = insta.check_profile_id(username)
        except (instaloader.exceptions.ProfileNotExistsException, ValueError): pass
        else:
            for story in insta.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    if story_id == item.mediaid:
                        insta.download_storyitem(item, target=target)
                        filelist = os.listdir(os.getcwd()+'/'+target)
                        file_jpg_mp4 = [file for file in filelist if await checkfile(file)]
                        profile_photo = [photo for photo in filelist if photo.endswith('.jpg')][0]
                        await setfilelist(file_jpg_mp4)
                        send_file = [os.getcwd()+'/'+target+'/'+file for file in profile_photo][0]
                        if send_file.endswith('.mp4'):
                            await callq.answer(results=[InlineQueryResultVideo(video_url= send_file, thumb_url=send_file, title="Video",
                                input_message_content=InputTextMessageContent(f"**{username}**"), description="How ", 
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ Start ]" ,url=f"https://t.me/{bot_username}?start=start")]]))], cache_time=1)
                        else :
                            await callq.answer(results=[InlineQueryResultPhoto(photo_url= send_file, thumb_url=send_file, title="Photo",
                            input_message_content=InputTextMessageContent(f"**{username}**"),  description="How ",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("[ Start ]" ,url=f"https://t.me/{bot_username}?start=start")]]))], cache_time=1)
                        await removedir(target, os.getcwd()); return
#::::::::::::::::::::::::::::::::::::::::::::::::( In_Time )
async def in_time():
    databj = await GData.Dbase()
    databj['uptime'] += 1
    gnudata.hset('gnu', 'data', json.dumps(databj))
scheduler = AsyncIOScheduler(timezone="Asia/Tehran")
scheduler.add_job(in_time, "interval", minutes = 60, next_run_time=f'{dt.today().year}-{dt.today().month}-{dt.today().day} {dt.today().hour}:00:00') 
scheduler.start()
#::::::::::::::::::::::::::::::::::::::::::::::::( Run )
if __name__ == "__main__":
    print('_______________________________[ Gnu 0.4 ]_______________________________')
    print(f'______________________[ Bot Lunched in : {(dt.now()-timstart).microseconds/1000} ms ]______________________')
    gnu.run()