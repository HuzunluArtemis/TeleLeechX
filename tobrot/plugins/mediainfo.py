#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @MysterySD (https://github.com/code-rgb/USERGE-X/issues/9)
# Copyright (C) 2020 BY - GitHub.com/code-rgb [TG - @deleteduser420]
# Taken From Slam-mirrorbot, I thereby Take No Extra Credit on Code !!
# Copyright 2022 - TeamTele-LeechX
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# https://huzunluartemis.github.io/TeleLeechX

import asyncio
import os
import datetime

from html_telegraph_poster import TelegraphPoster
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tobrot import app, bot, UPDATES_CHANNEL 
from tobrot.plugins import runcmd 
from tobrot.helper_funcs.display_progress import humanbytes
from tobrot.helper_funcs.bot_commands import BotCommands


def post_to_telegraph(a_title: str, content: str) -> str:
    """ Create a Telegram Post using HTML Content """
    post_client = TelegraphPoster(use_api=True)
    auth_name = "TeleLeechX"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=a_title,
        author=auth_name,
        text=content,
    )
    return post_page["url"]

def safe_filename(path_):
    if path_ is None:
        return
    safename = path_.replace("'", "").replace('"', "")
    if safename != path_:
        os.rename(path_, safename)
    return safename


async def mediainfo(client, message):
    reply = message.reply_to_message
    if not reply:
        await message.reply_text("`Reply to Telegram Media to Generate MediaInfo !!`", parse_mode=enums.ParseMode.MARKDOWN)
        return
    process = await message.reply_text("`Gᴇɴᴇʀᴀᴛɪɴɢ ...`")
    x_media = None
    available_media = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
        "new_chat_photo",
    )
    for kind in available_media:
        x_media = getattr(reply, kind, None)
        if x_media is not None:
            break
    if x_media is None:
       await process.edit_text("<b>⚠️Opps⚠️ \n\n<i>⊠ Reply To a Valid Media Format to process.</i></b>")
       return
    media_type = str(type(x_media)).split("'")[1]
    file_path = safe_filename(await reply.download())
    output_ = await runcmd(f'mediainfo "{file_path}"')
    out = None
    if len(output_) != 0:
         out = output_[0]
    body_text = f"""
<h2>DETAILS</h2>
<pre>{out or 'Not Supported'}</pre>
"""
    title = "TeleLeechX MediaInfo"
    text_ = media_type.split(".")[-1]
    link = post_to_telegraph(title, body_text)
    textup = f"""
ℹ️ <code>MEDIA INFO</code> ℹ
┃
┃• <b>File Name :</b> <code>{x_media['file_name']}</code>
┃• <b>Mime Type :</b> <code>{x_media['mime_type']}</code>
┃• <b>File Size :</b> <code>{humanbytes(x_media['file_size'])}</code>
┃• <b>Date :</b> <code>{datetime.datetime.utcfromtimestamp(x_media['date']).strftime('%I:%M:%S %p %d %B, %Y')}</code>
┃• <b>File ID :</b> <code>{x_media['file_id']}</code>
┃• <b>Media Type :</b> <code>{text_}</code>
┃
┗━♦️Powered By {UPDATES_CHANNEL}♦️━╹
"""
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Mᴇᴅɪᴀ Iɴғᴏ", url=link)]])
    await process.edit_text(text=textup, reply_markup=markup)


