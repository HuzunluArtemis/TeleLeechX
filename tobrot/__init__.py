#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
# Copyright 2022 - TeamTele-LeechX
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# https://huzunluartemis.github.io/TeleLeechX 


import asyncio
import logging
import os
import subprocess
import time
from collections import defaultdict
from logging.handlers import RotatingFileHandler
import urllib.request
import dotenv
import requests
import telegram.ext as tg
from pyrogram.types import User
from pyrogram import Client

if os.path.exists("log.txt"):
    with open("log.txt", "r+") as f_d:
        f_d.truncate(0)

# the logging things >>>>>>>>>>>
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "log.txt", maxBytes=50000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

user_specific_config=dict()

def getConfig(name: str):
    return os.environ[name]
CONFIG_FILE_URL = os.environ.get('CONFIG_FILE_URL')
try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = requests.get(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            LOGGER.error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        LOGGER.error(f"CONFIG_FILE_URL: {e}")
except:
    pass

try:
    HEROKU_API_KEY = getConfig('HEROKU_API_KEY')
    HEROKU_APP_NAME = getConfig('HEROKU_APP_NAME')
    if len(HEROKU_API_KEY) == 0 or len(HEROKU_APP_NAME) == 0:
        raise KeyError
except:
    HEROKU_APP_NAME = None
    HEROKU_API_KEY = None

dotenv.load_dotenv("config.env", override=True)

alive = subprocess.Popen(["python3", "alive.py"])
time.sleep(0.5)

# checking compulsory variable NOT NEEDED FOR OKTETO!! Just Use Your Brain
'''
for imp in ["TG_BOT_TOKEN", "APP_ID", "API_HASH", "OWNER_ID", "AUTH_CHANNEL"]:
    try:
        value = os.environ[imp]
        if not value:
            raise KeyError
    except KeyError:
        LOGGER.critical(f"Oh...{imp} is missing from config.env ... fill that")
        exit()
'''

# The Telegram API things >>>>>>>>>>>
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "232452345:23453245")
APP_ID = os.environ.get("APP_ID", "23452345")
API_HASH = os.environ.get("API_HASH", "234523452345")
OWNER_ID = int(os.environ.get("OWNER_ID", "2345234532"))

# Authorised Chat Functions >>>>>>>>>>>
AUTH_CHANNEL = [int(x) for x in os.environ.get("AUTH_CHANNEL", "-1001270496331 -1001508663868").split()]
SUDO_USERS = [int(sudos) if (' ' not in os.environ.get('SUDO_USERS', '')) else int(sudos) for sudos in os.environ.get('SUDO_USERS', '').split()]
AUTH_CHANNEL.append(OWNER_ID)
AUTH_CHANNEL += SUDO_USERS
# Download Directory >>>>>>>>>>>
DOWNLOAD_LOCATION = "./DOWNLOADS"

# chunk size that should be used with requests
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "128"))
# default thumbnail to be used in the videos
DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://telegra.ph/file/9763f9dabbc0a51f2b800.jpg")
# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096
# set timeout for subprocess
PROCESS_MAX_TIMEOUT = 3600
# Internal Requirements >>>>>>>>>>>
SP_LIT_ALGO_RITH_M = os.environ.get("SP_LIT_ALGO_RITH_M", "hjs")
ARIA_TWO_STARTED_PORT = int(os.environ.get("ARIA_TWO_STARTED_PORT", "6800"))
EDIT_SLEEP_TIME_OUT = int(os.environ.get("EDIT_SLEEP_TIME_OUT", "10"))
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(os.environ.get("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 600))

# add config vars for the display progress
FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "■")
UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "□")

# add offensive API
TG_OFFENSIVE_API = os.environ.get("TG_OFFENSIVE_API", None)
CUSTOM_FILE_NAME = os.environ.get("CUSTOM_FILE_NAME", "")

#Bot Command [Leech]  >>>>>>>>>>>
LEECH_COMMAND = os.environ.get("LEECH_COMMAND", "leech")
LEECH_UNZIP_COMMAND = os.environ.get("LEECH_UNZIP_COMMAND", "extract")
LEECH_ZIP_COMMAND = os.environ.get("LEECH_ZIP_COMMAND", "archive")
GLEECH_COMMAND = os.environ.get("GLEECH_COMMAND", "gleech")
GLEECH_UNZIP_COMMAND = os.environ.get("GLEECH_UNZIP_COMMAND", "gleechunzip")
GLEECH_ZIP_COMMAND = os.environ.get("GLEECH_ZIP_COMMAND", "gleechzip")

#Bot Command [ytdl] >>>>>>>>>>>
YTDL_COMMAND = os.environ.get("YTDL_COMMAND", "ytdl")
GYTDL_COMMAND = os.environ.get("GYTDL_COMMAND", "gytdl")

#Bot Command [RClone]  >>>>>>>>>>>
RCLONE_CONFIG = os.environ.get("RCLONE_CONFIG", "")
DESTINATION_FOLDER = os.environ.get("DESTINATION_FOLDER", "TeleLeechX")
INDEX_LINK = os.environ.get("INDEX_LINK", "https://infyplexultra.mysterydemon.workers.dev/0:/TeleLeechX")
TELEGRAM_LEECH_COMMAND = os.environ.get("TELEGRAM_LEECH_COMMAND", "tleech")
TELEGRAM_LEECH_UNZIP_COMMAND = os.environ.get("TELEGRAM_LEECH_UNZIP_COMMAND", "tleechunzip")
CANCEL_COMMAND_G = os.environ.get("CANCEL_COMMAND_G", "cancel")
GET_SIZE_G = os.environ.get("GET_SIZE_G", "getsize")
STATUS_COMMAND = os.environ.get("STATUS_COMMAND", "status")
SAVE_THUMBNAIL = os.environ.get("SAVE_THUMBNAIL", "savethumb")
CLEAR_THUMBNAIL = os.environ.get("CLEAR_THUMBNAIL", "clearthumb")
UPLOAD_AS_DOC = os.environ.get("UPLOAD_AS_DOC", "False")
PYTDL_COMMAND = os.environ.get("PYTDL_COMMAND", "pytdl")
GPYTDL_COMMAND = os.environ.get("GPYTDL_COMMAND", "gpytdl")
LOG_COMMAND = os.environ.get("LOG_COMMAND", "log")
CLONE_COMMAND_G = os.environ.get("CLONE_COMMAND_G", "gclone")
UPLOAD_COMMAND = os.environ.get("UPLOAD_COMMAND", "upload")
RENEWME_COMMAND = os.environ.get("RENEWME_COMMAND", "renewme")
RENAME_COMMAND = os.environ.get("RENAME_COMMAND", "rename")
TOGGLE_VID = os.environ.get("TOGGLE_VID", "togglevid")
TOGGLE_DOC = os.environ.get("TOGGLE_DOC", "toggledoc")
RCLONE_COMMAND = os.environ.get("RCLONE_COMMAND", "rclone")

#Bot Command [Utils]  >>>>>>>>>>>
HELP_COMMAND = os.environ.get("HELP_COMMAND", "help")
SPEEDTEST = os.environ.get("SPEEDTEST", "speedtest")
TSEARCH_COMMAND = os.environ.get("TSEARCH_COMMAND", "tshelp")
MEDIAINFO_CMD = os.environ.get("MEDIAINFO_CMD", "mediainfo")
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "Anonymous")
CAP_STYLE = os.environ.get("CAP_STYLE", "code")
BOT_NO = os.environ.get("BOT_NO", "")

#Bot Command [Token Utils]  >>>>>>>>>>>
UPTOBOX_TOKEN = os.environ.get("UPTOBOX_TOKEN", "xxx")
EMAIL = os.environ.get("EMAIL", "ajajssjs@akakka.com")
PWSSD = os.environ.get("PWSSD", "277287d7dodkdk")
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "ajajjxnsnxjsnA")
CRYPT = os.environ.get("CRYPT", "sjskkxkekdkd")
#PHPSESSID = os.environ.get("PHPSESSID", "jskwkxkekkdkd")
HUB_CRYPT = os.environ.get("HUB_CRYPT", "dkekdkkskd")
DRIVEFIRE_CRYPT = os.environ.get("DRIVEFIRE_CRYPT", "djkskxksmdmd")
KATDRIVE_CRYPT = os.environ.get("KATDRIVE_CRYPT", "cjdkkxkkd")
KOLOP_CRYPT = os.environ.get("KOLOP_CRYPT", "sjksksk")
DRIVEBUZZ_CRYPT = os.environ.get("DRIVEBUZZ_CRYPT", "sjskkdkdkd")
GADRIVE_CRYPT = os.environ.get("GADRIVE_CRYPT", "skskkskss")
STRING_SESSION = os.environ.get("STRING_SESSION", "")

#Bot Command [IMDB]  >>>>>>>>>>>
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "")
MAX_LIST_ELM = os.environ.get("MAX_LIST_ELM", None)
DEF_IMDB_TEMPLATE = os.environ.get("IMDB_TEMPLATE", """<i><b>⚡Title: </b> {title}
<b>⚡IMDB Rating:</b> <code>{rating} </code>
<b>⚡Quality:  </b>
<b>⚡Release Date: </b> {release_date}
<b>⚡Genre: </b>{genres}
<b>⚡IMDB: </b>{url}
<b>⚡Language:  </b>{languages}
<b>⚡Country: </b> {countries}
<b>⚡Subtitles: </b>
<b>⚡Story Line: </b><code>{plot}</code>
""")

#Bot Command [Bot PM & Log Channel]  >>>>>>>>>>>
LEECH_LOG = os.environ.get("LEECH_LOG", "-1001569981856")
EX_LEECH_LOG = os.environ.get("EX_LEECH_LOG", "")
EXCEP_CHATS = os.environ.get("EXCEP_CHATS", "")
BOT_PM = os.environ.get("BOT_PM", "True")
# 4 GB Upload Utils >>>>>>>>>>>
PRM_LOG = os.environ.get("PRM_LOG", "-1001620169370")

BOT_START_TIME = time.time()
# dict to control uploading and downloading
gDict = defaultdict(lambda: [])
# user settings dict #ToDo
user_settings = defaultdict(lambda: {})
gid_dict = defaultdict(lambda: [])
_lock = asyncio.Lock()

# Rclone Config Via any raw url
###########################################################################
try:                                                                      #
    RCLONE_CONF_URL = os.environ.get('RCLONE_CONF_URL', "")               #
    if len(RCLONE_CONF_URL) == 0:                                         #
        RCLONE_CONF_URL = None                                            #
    else:                                                                 #
        urllib.request.urlretrieve(RCLONE_CONF_URL, '/app/rclone.conf')   #
except KeyError:                                                          #
    RCLONE_CONF_URL = None                                                #
###########################################################################

def multi_rclone_init():
    if RCLONE_CONFIG:
        LOGGER.warning("Don't use this var now, put your rclone.conf in root directory")
    if not os.path.exists("rclone.conf"):
        LOGGER.warning("Sed, No rclone.conf found in root directory")
        return
    if not os.path.exists("rclone_bak.conf"):  # backup rclone.conf file
        with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fole:
            with open("rclone.conf", "r") as f:
                fole.write(f.read())
        LOGGER.info("rclone.conf backuped to rclone_bak.conf!")

multi_rclone_init()

# Pyrogram Client Intialization >>>>>>>>>>>
app = Client("LeechBot", bot_token=TG_BOT_TOKEN, api_id=APP_ID, api_hash=API_HASH, workers=343)

# Telegram maximum file upload size dynamical

def getUserFilesize():
    maxfilesize = 2097152000
    ubot = None
    if len(STRING_SESSION) > 10:
        ubot = Client("TeleLeechXUSER", api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION)
        if ubot:
            ubot.start()
            if (ubot.get_me()).is_premium: maxfilesize = 4194304000
            LOGGER.info("[PRM] Initiated USERBOT") #Logging is Needed Very Much
        else: LOGGER.warning("Userbot cannot started.")
    return maxfilesize, ubot

TG_MAX_FILESIZE, userBot = getUserFilesize()

updater = tg.Updater(token=TG_BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher
