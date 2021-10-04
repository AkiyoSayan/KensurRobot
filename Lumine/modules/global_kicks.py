import html
from typing import List, Optional

from telegram import Message, Update, Bot, User, Chat, ParseMode
from telegram.error import BadRequest, TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html

from Lumine import dispatcher, CallbackContext, OWNER_ID, SUDO_USERS, SUPPORT_USERS
from Lumine.modules.helper_funcs.chat_status import user_admin, is_user_admin
from Lumine.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from Lumine.modules.helper_funcs.filters import CustomFilters
from Lumine.modules.helper_funcs.misc import send_to_list
from Lumine.modules.sql.users_sql import get_all_chats

GKICK_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Peer_id_invalid",
    "Group chat was deactivated",
    "Need to be inviter of a user to kick it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can kick group administrators",
    "Channel_private",
    "Not in the chat",
    "Method is available for supergroup and channel chats only",
    "Reply message not found"
}


def gkick(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in GKICK_ERRORS:
            pass
        else:
            message.reply_text("User cannot be Globally kicked because: {}".format(excp.message))
            return
    except TelegramError:
            pass

    if not user_id or int(user_id) == 777000 or int(user_id) == 1087968824:
        message.reply_text("You do not seems to be referring to a user")
        return

    if int(user_id) in SUDO_USERS or int(user_id) in SUPPORT_USERS:
        message.reply_text("OHHH! Someone's trying to gkick a sudo/support user! *Grabs popcorn*")
        return

    if int(user_id) == OWNER_ID:
        message.reply_text("Wow! Someone's so noob that he want to gkick my owner! *Grabs Potato Chips*")
        return

    if user_id == bot.id:
        message.reply_text("-_- So funny, lets gkick myself why don't I? Nice try.")
        return

    message.reply_text("On it!")

    chats = get_all_chats()
    kicker = update.effective_user  # type: Optional[User]
    send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                 "<b>Global Kick</b>" \
                 "\n#GKICK" \
                 "\n<b>Status:</b> <code>Enforcing</code>" \
                 "\n<b>Sudo Admin:</b> {}" \
                 "\n<b>User:</b> {}" \
                 "\n<b>ID:</b> <code>{}</code>".format(mention_html(kicker.id, kicker.first_name),
                                                       mention_html(user_chat.id, user_chat.first_name),
                                                                    user_chat.id),
                html=True)

    message.reply_text("Done! Gkicked.")
    for chat in chats:
        try:
             bot.unban_chat_member(chat.chat_id, user_id)
        except BadRequest as excp:
            if excp.message in GKICK_ERRORS:
                pass
            else:
                message.reply_text("User cannot be Globally kicked because: {}".format(excp.message))
                return
        except TelegramError:
            pass

GKICK_HANDLER = CommandHandler("gkick", gkick, run_async=True,
                              filters=CustomFilters.sudo_filter | CustomFilters.support_filter)

dispatcher.add_handler(GKICK_HANDLER)