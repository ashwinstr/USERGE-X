# created for USERGE-X by @Kakashi_HTK/@ashwinstr

import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait

from userge import Config, Message, get_collection, userge

SAVED_SETTINGS = get_collection("CONFIGS")


async def _init() -> None:
    data = await SAVED_SETTINGS.find_one({"_id": "TAG_LOGGING"})
    if data:
        Config.TAG_LOGGING = bool(data["is_active"])


tagLoggingFilter = filters.create(lambda _, __, ___: Config.TAG_LOGGING)


@userge.on_cmd(
    "tag_log",
    about={
        "header": "Toggle logging of PM and groups[all]",
        "description": "Logs all PMs and group mentions",
        "flag": {
            "-c": "Check tag_log status",
        },
        "usage": "{tr}tag_log",
    },
    allow_channels=False,
)
async def all_log(message: Message):
    """ enable / disable [all Logger] """
    flag = message.flags
    if "-c" in flag:
        if Config.TAG_LOGGING:
            switch = "enabled"
        else:
            switch = "disabled"
        await message.edit(f"Tag logger is {switch}.", del_in=3)
        return
    if Config.TAG_LOGGING:
        Config.TAG_LOGGING = False
        await message.edit("`Tag logger disabled !`", del_in=3)
    else:
        Config.TAG_LOGGING = True
        await message.edit("`Tag logger enabled !`", del_in=3)
    await SAVED_SETTINGS.update_one(
        {"_id": "TAG_LOGGING"}, {"$set": {"is_active": Config.TAG_LOGGING}}, upsert=True
    )


@userge.on_message(
    filters.group & ~filters.bot & ~filters.me & tagLoggingFilter,
)
async def grp_log(_, message: Message):
    me = await userge.get_me()
    id = message.message_id
    reply = message.reply_to_message
    log = f"""
#TAGS
<b>Sent by :</b> {message.from_user.mention}
<b>Group :</b> <code>{message.chat.title}</code>
<b>Message link :</b> <a href={message.link}>link</a>
<b>Message :</b> ⬇
"""
    if reply:
        replied = reply.from_user.id
        if replied == me.id:
            try:
                await asyncio.sleep(0.5)
                await userge.send_message(
                    Config.LOG_CHANNEL_ID,
                    log,
                    parse_mode="html",
                    disable_web_page_preview=True,
                )
            except FloodWait as e:
                await asyncio.sleep(e.x + 3)
    mention = f"@{me.username}"
    if mention in message.text:
        try:
            await asyncio.sleep(0.5)
            await userge.send_message(
                Config.LOG_CHANNEL_ID,
                log,
                parse_mode="html",
                disable_web_page_preview=True,) 
        except FloodWait as e:
            await asyncio.sleep(e.x + 3)
