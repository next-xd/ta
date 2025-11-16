import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import json
import os
import re

# تهيئة الثوابت (المعرفات والتفاصيل الخاصة بالبوت)
TOKEN = "8519443259:AAGfeeVA-E9g0omKqiD_XPTxxzjoOo9xGsc"    # توكنك 
DEV_IDS = ["5895430724",]    # iD مطورين 
USERNAME_BOT = "@nexxxxxxtbot"    # يوزر بوتك
CHANNEL_SUPPORT = "u_99s"    # يوزر قناتك 
DEV_USERNAME = "@u_nJl"    # يوزرك 
ADMIN_ID = "5895430724"    # iD ادمن 
CHANNEL_CODE = ""    # اتركها فارغة عادي 

# تعريف الأزرار الثابتة المطلوبة
FIXED_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("𓄼𝗗𝗲𝘃𓄹", url="https://t.me/u_99s")],
        [InlineKeyboardButton("𓄼𝗦𝗼𝗼𝘂𝗿𝗰𝗲𓄹", url="")],
    ]
)

# مسارات حفظ بيانات JSON
DATA_DIR = "data"
USER_FILE = os.path.join(DATA_DIR, "user.json")

# وظيفة قراءة وكتابة ملفات JSON
def load_data(file_path, default_data={}):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default_data
    return default_data

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_user_data(user_id):
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    user_id_str = str(user_id)
    
    default_user_data = {
        "invite": "0", "coin": "0", "setchannel": "لا يوجد !", 
        "setmember": "لا يوجد !", "inviter": "none", "file": "none",
        "acceptrules": False, "canceljoin": False, "channeljoin": [], "listorder": []
    }
    
    default_data_structure = {"userfild": {user_id_str: default_user_data}}
    
    data = load_data(file_path, default_data_structure)
    
    if "userfild" not in data or not isinstance(data["userfild"], dict):
        data["userfild"] = {}

    if user_id_str not in data["userfild"]:
        data["userfild"][user_id_str] = default_user_data
    
    return data

def save_user_data(user_id, data):
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    save_data(file_path, data)

# وظيفة لإرسال الرسائل مع الأزرار الثابتة
async def send_message_with_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id, text, reply_markup=None, parse_mode='Markdown', disable_web_page_preview=True):
    if reply_markup is None:
        final_keyboard = FIXED_KEYBOARD
    else:
        if isinstance(reply_markup, InlineKeyboardMarkup):
            # تحويل الأزرار المخصصة إلى قائمة قابلة للتعديل
            custom_buttons = list(reply_markup.inline_keyboard)
            
            fixed_buttons_list = FIXED_KEYBOARD.inline_keyboard
            
            if not any(row == fixed_buttons_list[0] for row in custom_buttons):
                custom_buttons.extend(fixed_buttons_list)

            final_keyboard = InlineKeyboardMarkup(custom_buttons)
        else:
            final_keyboard = FIXED_KEYBOARD
            
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=final_keyboard
        )
    except Exception:
        pass

async def edit_message_text_with_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id, message_id, text, reply_markup=None, parse_mode='Markdown', disable_web_page_preview=True):
    if reply_markup is None:
        final_keyboard = FIXED_KEYBOARD
    else:
        if isinstance(reply_markup, InlineKeyboardMarkup):
            # تحويل الأزرار المخصصة إلى قائمة قابلة للتعديل
            custom_buttons = list(reply_markup.inline_keyboard)
            
            fixed_buttons_list = FIXED_KEYBOARD.inline_keyboard
            
            if not any(row == fixed_buttons_list[0] for row in custom_buttons):
                custom_buttons.extend(fixed_buttons_list)

            final_keyboard = InlineKeyboardMarkup(custom_buttons)
        else:
            final_keyboard = FIXED_KEYBOARD

    try:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=final_keyboard
        )
    except Exception:
        pass


# الدوال المساعدة (تحويل دوال PHP)
async def get_chat_member_status(context: ContextTypes.DEFAULT_TYPE, chat_id, user_id):
    try:
        member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status
    except telegram.error.BadRequest:
        return None
    except Exception:
        return None

async def get_chat_members_count(context: ContextTypes.DEFAULT_TYPE, chat_id_username):
    try:
        count = await context.bot.get_chat_members_count(chat_id=chat_id_username)
        return count
    except telegram.error.BadRequest:
        return 0
    except Exception:
        return 0

async def get_chat_admins_status(context: ContextTypes.DEFAULT_TYPE, chat_id_username):
    try:
        admins = await context.bot.get_chat_administrators(chat_id=chat_id_username)
        bot_user = await context.bot.get_me()
        for admin in admins:
            if admin.user.id == bot_user.id:
                return True
        return False
    except telegram.error.BadRequest:
        return False
    except Exception:
        return False

async def get_chat_info(context: ContextTypes.DEFAULT_TYPE, chat_id_username):
    try:
        chat = await context.bot.get_chat(chat_id=chat_id_username)
        return chat
    except telegram.error.BadRequest:
        return None
    except Exception:
        return None

# وظيفة التحقق من حالة العضو في القناة الرئيسية
async def is_subscribed(context: ContextTypes.DEFAULT_TYPE, chat_id, user_id):
    status = await get_chat_member_status(context, f"@{CHANNEL_SUPPORT}", user_id)
    return status in ['member', 'administrator', 'creator']

# الدوال المساعدة التي كانت داخل handle_callback_query (تم نقلها لتصحيح SyntaxError)
async def handle_next_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, start_index, cuser, user_data, chatid, messageid, fromid, firstname):
    all_channels_list = user_data.get("channellist", [])
    next_channel_index = -1
    next_channel_id = None
    
    for idx in range(start_index, len(all_channels_list)):
        ch_id = all_channels_list[idx]
        status = await get_chat_member_status(context, ch_id, fromid)
        if status not in ['member', 'creator', 'administrator']:
            next_channel_index = idx
            next_channel_id = ch_id
            break
    
    if next_channel_id:
        chat_info = await get_chat_info(context, next_channel_id)
        
        if chat_info and chat_info.username:
            name = chat_info.title
            username = chat_info.username
            channel_id = chat_info.id
            description = chat_info.description or "لا يوجد وصف"
            
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                f"- اسم القناة ؛ {name}\n- معرف القناة ؛ @{username} ،\n- ايدي القناة ؛ {channel_id}\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n- وصف القناة ؛ {description}",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("- اشتراك ، 📢 '", url=f"https://t.me/{username}"),
                        InlineKeyboardButton("- التالي ، 📻 '", callback_data='truechannel')
                    ],
                    [
                        InlineKeyboardButton("• تخطي ، 📌 '", callback_data='nextchannel'),
                        InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')
                    ],
                    [InlineKeyboardButton("- الابلاغ عن هذه القناة ، 📕'", callback_data='badchannel')],
                ])
            )
            
            cuser["userfild"][fromid]["getjoin"] = username
            cuser["userfild"][fromid]["arraychannel"] = str(next_channel_index)
            save_user_data(fromid, cuser)
            
            await send_message_with_keyboard(
                update, context, ADMIN_ID,
                f"- هذا ديجمع (نقل/تخطي) ،\n\t- [{firstname}](tg://user?id={fromid})",
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=None
            )
        else:
            if next_channel_index != -1:
                del user_data["channellist"][next_channel_index]
                del user_data["setmemberlist"][next_channel_index]
                user_data["channellist"] = list(user_data["channellist"])
                user_data["setmemberlist"] = list(user_data["setmemberlist"])
                save_data(USER_FILE, user_data)
                await handle_next_channel(update, context, next_channel_index, cuser, user_data, chatid, messageid, fromid, firstname) 
            else:
                await show_no_channels_message(update, context, chatid, messageid, fromid, firstname)
    else:
        await show_no_channels_message(update, context, chatid, messageid, fromid, firstname)

async def show_no_channels_message(update: Update, context: ContextTypes.DEFAULT_TYPE, chatid, messageid, fromid, firstname):
    await edit_message_text_with_keyboard(
        update, context, chatid, messageid,
        "- انتهت القنوات المضافةه ؛ يرجى المحاولة مرة اخرى في تجميع النقاط ، او قم بمشاركة الرابط بدل عن الاشتراك في القنوات ، 📻 ' !",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("- تحديث ، 📑 '", callback_data='takecoin'),
                InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')
            ],
        ])
    )
    await send_message_with_keyboard(
        update, context, ADMIN_ID,
        f"- هذا خلص لقنوات ،\n\t- [{firstname}](tg://user?id={fromid})",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=None
    )

# معالج أمر /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    from_id = update.message.from_user.id
    name = update.message.from_user.first_name
    tc = update.message.chat.type
    textmassage = update.message.text
    
    user_data = load_data(USER_FILE, {"userlist": [], "blocklist": [], "channellist": [], "setmemberlist": []})
    juser = load_user_data(from_id)
    
    user_info = juser["userfild"].get(str(from_id))
    
    is_new_user = str(from_id) not in user_data.get("userlist", [])

    if is_new_user:
        user_data["userlist"].append(str(from_id))
        save_data(USER_FILE, user_data)
        
    if str(from_id) in user_data.get("blocklist", []):
        await send_message_with_keyboard(
            update, context, chat_id,
            "- انت محظور من البوت ياعزيزي ، ⚖ !\n- بسبب عدم اتباعك قوانين البوت ؛ لا تقم بارسال الرسائل مرة اخرى ، 🔱\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
            reply_markup=telegram.ReplyKeyboardRemove()
        )
        await send_message_with_keyboard(
            update, context, ADMIN_ID,
            f"- محظور دز رسالة للبوت ،\n\t- [{name}](tg://user?id={from_id})",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=None
        )
        return

    main_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("- تجمبع النقاط ، 📻 '", callback_data='takecoin')],
        [
            InlineKeyboardButton("- شراء الاعضاء ، 💸 '", callback_data='takemember'),
            InlineKeyboardButton("- احصائيات نقاطك ، 📊 '", callback_data='accont')
        ],
        [
            InlineKeyboardButton("- مشاركةه الرابط ، 📧 '", callback_data='member'),
            InlineKeyboardButton("- تحويل نقاط ، ♻️ '", callback_data='sendcoin')
        ],
        [InlineKeyboardButton("- ارسال اقتراح ، 🇮🇶 '", callback_data='sup')],
    ])

    if tc == "private":
        
        if not user_info:
            juser = load_user_data(from_id)
            user_info = juser["userfild"].get(str(from_id))
            save_user_data(from_id, juser)

        if textmassage.startswith("/start ") and len(textmassage.split()) > 1:
            inviter_id = textmassage.split()[1]
            
            if not is_new_user:
                await send_message_with_keyboard(
                    update, context, chat_id,
                    "• انت مشترك بالفعل في البوت ، 📌 !\n• لا يمكنك الاشتراك او الدخول الى الرابط مرة اخرى ، ⚜ '\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                    reply_markup=main_keyboard
                )
                await send_message_with_keyboard(
                    update, context, ADMIN_ID,
                    f"- دخل للرابط مرا لاخ ،\n\t- [{name}](tg://user?id={from_id})",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=None
                )
                return

            inuser = load_user_data(inviter_id)
            
            current_member = int(inuser["userfild"].get(inviter_id, {}).get("invite", "0"))
            current_coin = int(inuser["userfild"].get(inviter_id, {}).get("coin", "0"))
            
            member_plus = current_member + 1
            coin_plus = current_coin + 1
            
            await send_message_with_keyboard(
                update, context, inviter_id,
                f"- تم دخول عضو جديد من الرابط الخاص بك ، 🇮🇶 '\n- عدد الاعضاء الذين قامو بالدخول الى الرابط الخاص بك ؛ {member_plus} ،\n- عدد النقاط الخاصة بك ؛ {coin_plus} ،",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                ])
            )
            
            if inviter_id in inuser["userfild"]:
                inuser["userfild"][inviter_id]["invite"] = str(member_plus)
                inuser["userfild"][inviter_id]["coin"] = str(coin_plus)
                save_user_data(inviter_id, inuser)

            juser["userfild"][str(from_id)]["inviter"] = inviter_id
            save_user_data(from_id, juser)
            
            welcome_text = (
                f"• اهلا بك يا ؛ [{name}](tg://user?id={chat_id})\n\n"
                "- في بوت زيادة الاعضاء ، 📻 '\n"
                "- قم بتجميع النقاط وشراء الاعضاء لقناتك ، ⚖ '\n"
                "- التجميع عن طريق مشاركه الرابط او الاشتراك بالقنوات ، 💸 '\n"
                "- قم باختيار ما تريد من هذه الازرار ، 🔰 ؛\n"
                "﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n"
                f"[اضغط هنا وتابع جديدنا ، 📢](https://t.me/{CHANNEL_SUPPORT})"
            )
            await send_message_with_keyboard(
                update, context, chat_id, welcome_text,
                reply_markup=main_keyboard
            )
            
            await send_message_with_keyboard(
                update, context, ADMIN_ID,
                f"- دز ستارت للبوت ،\n\t- [{name}](tg://user?id={from_id})",
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=None
            )
        
        elif textmassage == "/start":
            
            welcome_text = (
                f"• اهلا بك يا ؛ [{name}](tg://user?id={chat_id})\n\n"
                "- في بوت زيادة الاعضاء ، 📻 '\n"
                "- قم بتجميع النقاط وشراء الاعضاء لقناتك ، ⚖ '\n"
                "- التجميع عن طريق مشاركه الرابط او الاشتراك بالقنوات ، 💸 '\n"
                "- قم باختيار ما تريد من هذه الازرار ، 🔰 ؛\n"
                "﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n"
                f"[اضغط هنا وتابع جديدنا ، 📢](https://t.me/{CHANNEL_SUPPORT})"
            )
            
            await send_message_with_keyboard(
                update, context, chat_id, welcome_text,
                reply_markup=main_keyboard
            )
            
            await send_message_with_keyboard(
                update, context, ADMIN_ID,
                f"- دز ستارت ،\n\t- [{name}](tg://user?id={from_id})",
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=None
            )

            juser["userfild"][str(from_id)]["file"] = "none"
            save_user_data(from_id, juser)


# معالج الأوامر الإدارية (مثل /panel, /admin)
async def admin_panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat_id = update.message.chat_id
    from_id = str(update.message.from_user.id)
    textmassage = update.message.text
    
    if from_id in DEV_IDS and update.message.chat.type == "private":
        juser = load_user_data(from_id)
        
        if textmassage in ["/panel", "/admin", "ادمن"]:
            admin_keyboard = telegram.ReplyKeyboardMarkup([
                ["- عدد الاعضاء ، 👤 '"],
                ["- رسالة للكل ، 🎒 '", "- توجيه للكل ، 🧜‍♂ '"],
                ["- عرض القنوات ، 🔱 '", "- حذف قناة ، 📛 '"],
                ["📍 نقاط للكل", "- ارسال نقاط ، 🕊 '"],
            ], resize_keyboard=True)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text="- اهلا بك عزيزي المطور ، 🧜‍♂ '\n- قم باختيار ماتريد من القائمةه التي في الاسفل ، 👅 '\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                reply_to_message_id=update.message.message_id,
                reply_markup=admin_keyboard
            )
            
            juser["userfild"][from_id]["file"] = "none"
            save_user_data(from_id, juser)
            return

        user_data = load_data(USER_FILE, {"userlist": [], "blocklist": [], "channellist": [], "setmemberlist": []})
        
        if textmassage == "- عدد الاعضاء ، 👤 '":
            all_users = len(user_data["userlist"])
            order_count = len(user_data["channellist"])
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"• اهلا بك يا عزيزي المطور ؛ @{DEV_USERNAME} !\n\n◾️ عدد الاعضاء ؛ {all_users} ،\n▫️ عدد القنوات بقائمةه التمويل ؛ {order_count} .\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
            )
            return
        
        elif textmassage == "- رسالة للكل ، 🎒 '":
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"- اهلا بك يا ؛ @{DEV_USERNAME} !\n- الان قم بارسال الرسالة ليتم ارسالها للكل ، 🇮🇶 '",
                reply_to_message_id=update.message.message_id,
                reply_markup=telegram.ReplyKeyboardMarkup([["• العودة ، 🔙 '"]], resize_keyboard=True)
            )
            juser["userfild"][from_id]["file"] = "sendtoall"
            save_user_data(from_id, juser)
            return
            
        elif textmassage == "- توجيه للكل ، 🧜‍♂ '":
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"- اهلا بك يا ؛ @{DEV_USERNAME} !\n- الان قم بارسال التوجيه ليتم ارسالة للكل ، 🇮🇶 '",
                reply_to_message_id=update.message.message_id,
                reply_markup=telegram.ReplyKeyboardMarkup([["• العودة ، 🔙 '"]], resize_keyboard=True)
            )
            juser["userfild"][from_id]["file"] = "fortoall"
            save_user_data(from_id, juser)
            return
            
        elif textmassage == "- عرض القنوات ، 🔱 '":
            order_list = user_data["channellist"]
            order_count = len(order_list)
            result = ""
            for channel in order_list:
                result += f"{channel}\n"
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"- اهلا بك ؛ @{DEV_USERNAME} !! \n\n◾️ عدد القنوات التي تحت التمويل ؛ {order_count}\n\t▫️ لستةه معرفات القنوات التي تحت التمويل ؛ 📌\n{result}",
                reply_markup=telegram.ReplyKeyboardRemove()
            )
            return
        
        elif textmassage == "- حذف قناة ، 📛 '":
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"- حسنا ياعزيزي ؛ @{DEV_USERNAME} !\n- الان قم بارسال معرف القناة التي تود حذفها ، 🔘\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                reply_markup=telegram.ReplyKeyboardMarkup([["• العودة ، 🔙 '"]], resize_keyboard=True)
            )
            juser["userfild"][from_id]["file"] = "remorder"
            save_user_data(from_id, juser)
            return
            
        elif textmassage == "- ارسال نقاط ، 🕊 '":
            await context.bot.send_message(
                chat_id=chat_id,
                text="ارسل ايدي العضو الذي تريد الاىسال اليه او ارسل توجيه من العضو",
                reply_markup=telegram.ReplyKeyboardMarkup([["• العودة ، 🔙 '"]], resize_keyboard=True)
            )
            juser["userfild"][from_id]["file"] = "adminsendcoin"
            save_user_data(from_id, juser)
            return
            
        elif textmassage == '📍 نقاط للكل':
            await context.bot.send_message(
                chat_id=chat_id,
                text="ادخل العدد الذي تريده للنقود",
                reply_to_message_id=update.message.message_id,
                reply_markup=telegram.ReplyKeyboardMarkup([["• العودة ، 🔙 '"]], resize_keyboard=True)
            )
            juser["userfild"][from_id]["file"] = "sendcointoall"
            save_user_data(from_id, juser)
            return


# معالج رسائل المستخدمين العاديين والإداريين
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.message.chat_id
    from_id = str(update.message.from_user.id)
    textmassage = update.message.text
    
    juser = load_user_data(from_id)
    user_info = juser["userfild"].get(from_id, {})
    user_state = user_info.get("file", "none")
    user_data = load_data(USER_FILE, {"userlist": [], "blocklist": [], "channellist": [], "setmemberlist": []})
    
    is_dev = from_id in DEV_IDS
    
    if from_id in user_data.get("blocklist", []):
        return 

    # معالجة الردود من المطور (Reply)
    if update.message.reply_to_message and is_dev and update.message.chat.type == "private":
        reply_to_message = update.message.reply_to_message
        forward_from = reply_to_message.forward_from
        
        if forward_from:
            reply_user_id = str(forward_from.id)
            
            await send_message_with_keyboard(
                update, context, chat_id,
                f"- تم ارسال رسالتك الى العضو بنجاح ، 🎌 !\n- بواسطه ؛ @{update.message.from_user.username}!",
                reply_markup=None
            )
            
            await context.bot.send_message(
                chat_id=reply_user_id,
                text=textmassage,
                parse_mode='Markdown'
            )
            return

    # معالجة حالات المطور (Admin States)
    if is_dev:
        if textmassage == "• العودة ، 🔙 '":
            await admin_panel_command(update, context)
            juser["userfild"][from_id]["file"] = "none"
            save_user_data(from_id, juser)
            return

        elif user_state == 'sendtoall':
            juser["userfild"][from_id]["file"] = "none"
            save_user_data(from_id, juser)
            numbers = user_data["userlist"]
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"- تم ارسال الرسالة الى جميع مشتركين البوت بنجاح بواسطة ؛ @{DEV_USERNAME} ، 📢 !",
                reply_to_message_id=update.message.message_id,
                reply_markup=telegram.ReplyKeyboardRemove()
            )
            
            for target_id in numbers:
                await send_message_with_keyboard(
                    update, context, target_id,
                    f"{textmassage}\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                    reply_markup=None 
                )
            return

        elif user_state == 'fortoall':
            juser["userfild"][from_id]["file"] = "none"
            save_user_data(from_id, juser)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"- تم ارسال التوجيه الى جميع مشتركين البوت بنجاح بواسطة ؛ @{DEV_USERNAME} ، 📢 !",
                reply_to_message_id=update.message.message_id,
                reply_markup=telegram.ReplyKeyboardRemove()
            )
            
            numbers = user_data["userlist"]
            for target_id in numbers:
                try:
                    await context.bot.forward_message(
                        chat_id=target_id,
                        from_chat_id=chat_id,
                        message_id=update.message.message_id
                    )
                except Exception:
                    pass
            return

        elif user_state == 'remorder':
            if textmassage != "• العودة ، 🔙 '":
                target_channel = textmassage
                
                if target_channel in user_data["channellist"]:
                    try:
                        how = user_data["channellist"].index(target_channel)
                        
                        del user_data["setmemberlist"][how]
                        del user_data["channellist"][how]
                        
                        user_data["channellist"] = list(user_data["channellist"])
                        user_data["setmemberlist"] = list(user_data["setmemberlist"])
                        
                        save_data(USER_FILE, user_data)
                        
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=f"- تم حذف القناة من البوت بنجاح ، ⚠️\n- بواسطة ؛ @{DEV_USERNAME} ، !",
                            reply_to_message_id=update.message.message_id,
                        )
                    except ValueError:
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text="- خطأ داخلي في تحديد موقع القناة للحذف.",
                            reply_to_message_id=update.message.message_id,
                        )
                else:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="- القناة غير موجودة في قائمة التمويل.",
                        reply_to_message_id=update.message.message_id,
                    )

                juser["userfild"][from_id]["file"] = "none"
                save_user_data(from_id, juser)
            return

        elif user_state == 'adminsendcoin':
            if textmassage != "• العودة ، 🔙 '":
                forward_from = update.message.forward_from
                
                target_id = None
                target_username = None
                
                if forward_from:
                    target_id = str(forward_from.id)
                    target_username = forward_from.username
                elif textmassage.isdigit():
                    target_id = textmassage
                
                if target_id:
                    target_juser = load_user_data(target_id)
                    if not target_juser["userfild"].get(target_id):
                         await context.bot.send_message(
                            chat_id=chat_id,
                            text="هذا المستخدم غير مشترك في البوت.",
                            reply_to_message_id=update.message.message_id,
                        )
                         juser["userfild"][from_id]["file"] = "none"
                         save_user_data(from_id, juser)
                         return

                    juser["idforsend"] = target_id
                    juser["userfild"][from_id]["file"] = "sethowsendcoin"
                    save_user_data(from_id, juser)
                    
                    if not target_username:
                        try:
                            chat_info = await context.bot.get_chat(chat_id=target_id)
                            target_username = chat_info.username
                        except telegram.error.BadRequest:
                            pass
                            
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"حسنا عزيزي المطور\n\nالايدي : {target_id}\nالمعرف : @{target_username or 'لا يوجد'}\n\nدز عدد النقاط الان",
                        reply_to_message_id=update.message.message_id,
                        reply_markup=telegram.ReplyKeyboardMarkup([["• العودة ، 🔙 '"]], resize_keyboard=True)
                    )
                else:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="يرجى إرسال إيدي صحيح أو توجيه.",
                        reply_to_message_id=update.message.message_id,
                    )
            return

        elif user_state == 'sethowsendcoin':
            if textmassage != "• العودة ، 🔙 '" and textmassage.isdigit():
                send_amount = int(textmassage)
                target_id = juser.get("idforsend")
                
                if target_id:
                    juser["userfild"][from_id]["file"] = "none"
                    del juser["idforsend"]
                    save_user_data(from_id, juser)

                    inuser = load_user_data(target_id)
                    current_coin = int(inuser["userfild"].get(target_id, {}).get("coin", "0"))
                    coin_plus = current_coin + send_amount
                    inuser["userfild"][target_id]["coin"] = str(coin_plus)
                    save_user_data(target_id, inuser)
                    
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"📍 العدد {send_amount} تم الارسال الى : {target_id} بنجاح ^_^",
                        reply_to_message_id=update.message.message_id,
                        reply_markup=telegram.ReplyKeyboardRemove()
                    )

                    await send_message_with_keyboard(
                        update, context, target_id,
                        f"- تم ارسال واضافة ؛ {send_amount} الى نقاطك من قبل مبرمج البوت ، 💚🐬 !",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                        ])
                    )
                else:
                    await context.bot.send_message(chat_id, "خطأ في تحديد المستخدم الهدف.")
            return
            
        elif user_state == 'sendcointoall':
            if textmassage != "• العودة ، 🔙 '" and textmassage.isdigit():
                send_amount = int(textmassage)
                numbers = user_data["userlist"]
                
                juser["userfild"][from_id]["file"] = "none"
                save_user_data(from_id, juser)
                
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="نم ارسال النقاط للجميع ✔️",
                    reply_to_message_id=update.message.message_id,
                    reply_markup=telegram.ReplyKeyboardRemove()
                )
                
                for target_id in numbers:
                    target_juser = load_user_data(target_id)
                    current_coin = int(target_juser["userfild"].get(target_id, {}).get("coin", "0"))
                    coin_plus = current_coin + send_amount
                    target_juser["userfild"][target_id]["coin"] = str(coin_plus)
                    save_user_data(target_id, target_juser)
                    
                    await send_message_with_keyboard(
                        update, context, target_id,
                        f"- هدية من قبل الادارة ؛ عدد النقاط التي حصلت عليها {send_amount} . 🇮🇶 '\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                        ])
                    )
            return

    # معالجة حالات المستخدم (User States)
    
    elif user_state == 'sendsup':
        await send_message_with_keyboard(
            update, context, chat_id,
            "• تم ارسال رسالتك الى مبرمج البوت ، \n• انتظر الاجابة من فضلك ، ",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
            ])
        )
        await context.bot.forward_message(
            chat_id=DEV_IDS[0],
            from_chat_id=chat_id,
            message_id=update.message.message_id
        )
        juser["userfild"][from_id]["file"] = "none"
        save_user_data(from_id, juser)
        return
    
    elif user_state == 'sendcoin':
        coin = int(user_info.get("coin", "0"))
        forward_from = update.message.forward_from
        
        target_id = None
        target_name = None
        target_username = None
        
        if forward_from:
            target_id = str(forward_from.id)
            target_name = forward_from.first_name
            target_username = forward_from.username
        
        elif textmassage and textmassage.isdigit():
            target_id = textmassage
        
        if target_id == from_id:
            await send_message_with_keyboard(
                update, context, chat_id,
                "- لا يمكن الارسال لنفسك ؛ ⚠️\n- قم بالارسال لصديق او لحسابك الثاني ، ☑️\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                ])
            )
            return

        if target_id:
            target_juser = load_user_data(target_id)
            
            if target_juser["userfild"].get(target_id):
                
                if not forward_from and not target_name:
                    try:
                        chat_info = await context.bot.get_chat(chat_id=target_id)
                        target_name = chat_info.first_name
                        target_username = chat_info.username
                    except telegram.error.BadRequest:
                        target_name = "غير معروف"

                await send_message_with_keyboard(
                    update, context, chat_id,
                    f"• تم العثور على المستخدم معلومات المستخدم ، 💚👇🏿؛\n\n▫️ الاسم ؛ {target_name or 'لا يوجد'}\n◾️ المعرف ؛ @{target_username or 'لا يوجد'}\n▫️ الايدي ؛  {target_id}\n\n- الان قم بارسال العدد الذي تريد تحويله الى المستخدم ،\n- عدد النقاط الخاصةه بك ؛ {coin} ",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                    ])
                )
                juser["userfild"][from_id]["file"] = "setsendcoin"
                juser["userfild"][from_id]["sendcoinid"] = target_id
                save_user_data(from_id, juser)
            else:
                await send_message_with_keyboard(
                    update, context, chat_id,
                    "• ايدي العضو غير صحيح او المستخدم غير مشترك في البوت يرجى التاكد من الايدي او قم بالاشتراك في البوت ، 🔰؛\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                    ])
                )
        else:
            await send_message_with_keyboard(
                update, context, chat_id,
                "- الايدي الخاص بالمستخدم غير صحيح ، 🔱\n- قم بالتاكد من الايدي وارسالة مرة اخرى الى البوت ، 🕊 !",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                ])
            )
        return
    
    elif user_state == "setsendcoin":
        if textmassage and textmassage.isdigit():
            send_amount = int(textmassage)
            coin = int(user_info.get("coin", "0"))
            userid = juser["userfild"][from_id].get("sendcoinid")
            
            if not userid:
                juser["userfild"][from_id]["file"] = "none"
                save_user_data(from_id, juser)
                return 

            if send_amount > 0 and send_amount <= coin:
                coin_minus = coin - send_amount
                
                inuser = load_user_data(userid)
                coinuser = int(inuser["userfild"].get(userid, {}).get("coin", "0"))
                sendcoinplus = coinuser + send_amount
                
                await send_message_with_keyboard(
                    update, context, chat_id,
                    f"- تم ارسال النقاط الى المستخدم بنجاح ، ⚖ !\n- المعلومات العامةه للعضو والنقاط ، 📌 ؛\n\n▫️ ايدي العضو ؛ {userid}\n◾️ عدد النقاط التي تم ارسالها ؛ {send_amount}\n▫️ عدد نقاطك الآن ؛ {coin_minus}",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                    ])
                )
                
                sender_username = update.message.from_user.username or "لا يوجد"
                await send_message_with_keyboard(
                    update, context, userid,
                    f"- تم ارسال {send_amount} من النقاط اليك ، 🌟 !\n- معلومات العضو الذي قام بأرسال النقاط اليك ، 🔱 ؛\n\n◾️ ايدي العضو ؛ {from_id}\n▫️ المعرف ؛ @{sender_username}",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                    ])
                )
                
                juser["userfild"][from_id]["file"] = "none"
                juser["userfild"][from_id]["coin"] = str(coin_minus)
                del juser["userfild"][from_id]["sendcoinid"]
                save_user_data(from_id, juser)
                
                if userid in inuser["userfild"]:
                    inuser["userfild"][userid]["coin"] = str(sendcoinplus)
                    save_user_data(userid, inuser)
                
                await send_message_with_keyboard(
                    update, context, ADMIN_ID,
                    f"- هذا دز نقاط ،\n\t- [{update.message.from_user.first_name}](tg://user?id={from_id})",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=None
                )
            else:
                await send_message_with_keyboard(
                    update, context, chat_id,
                    f"- عدد النقاط الذي تود ارسالة اقل من عدد نقاطك ، 🐬 !\n- اقصى عدد يمكنك ارساله ؛ {coin}",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                    ])
                )
        else:
            await send_message_with_keyboard(
                update, context, chat_id,
                "- يرجى إرسال رقم صحيح لعدد النقاط.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                ])
            )
        return

    elif user_state == 'setchannel':
        if re.match(r'^(@)(.*)', textmassage):
            channel_username_or_id = textmassage
            coin = int(user_info.get("coin", "0"))
            max_member = coin // 2
            
            await send_message_with_keyboard(
                update, context, chat_id,
                f"• تم حفظ القناة الخاصةه بك ، ☑️ '\n- القناة الخاصة بك ؛ {channel_username_or_id}\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n\n- عدد الاعضاء الذي يمكنك طلبهم للقاة ؛ {max_member} .\n\n• الان قم بأرسال العدد المطلوب من الاعضاء لقناتك مثل 50 ؛ علماً ان العضو الواحد ب2 من العملات ، 🏹 '",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                ])
            )
            
            juser["userfild"][from_id]["file"] = "setmember"
            juser["userfild"][from_id]["setchannel"] = channel_username_or_id
            save_user_data(from_id, juser)
        else:
            await send_message_with_keyboard(
                update, context, chat_id,
                f"• معرف القناة غير صحيح ، 🏉 '\n• ارسل المعرف الصحيح مثل ؛ @{CHANNEL_SUPPORT} .",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                ])
            )
        return

    elif user_state == 'setmember':
        if textmassage and textmassage.isdigit():
            requested_members = int(textmassage)
            coin = int(user_info.get("coin", "0"))
            setchannel = user_info.get("setchannel")
            max_member = coin // 2
            
            if requested_members > 0 and requested_members <= max_member:
                
                chat_info = await get_chat_info(context, setchannel)
                if not chat_info:
                    await send_message_with_keyboard(
                        update, context, chat_id,
                        f"- القناة التي ادخلتها غير موجودة او غير عامة ، 💔'\n- يرجى التأكد من المعرف وإعادة المحاولة.",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                        ])
                    )
                    juser["userfild"][from_id]["file"] = "none"
                    juser["userfild"][from_id]["setchannel"] = "لا يوجد !"
                    save_user_data(from_id, juser)
                    return


                how_member = await get_chat_members_count(context, setchannel)
                end_member = how_member + requested_members
                
                await send_message_with_keyboard(
                    update, context, chat_id,
                    f"• معلومات النقاط والتمويل وعدد الاعضاء ، ⚖ ؛\n\n- معرف القناة ؛ *{setchannel}* ،\n - العدد المطلوب ؛ *{requested_members}* ،\n- عدد اعضاء القناة ؛ *{how_member}* ،\n- عدد الاعضاء بعد التمويل ؛ *{end_member}* ،\n\n• الان عليك رفع البوت مشرف في القناة ليتم العمل بصورة صحيحة ؛ قم برفع البوت ثم اضغط على زر تأكيد الذي يوجد تحت ، 💌 '",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("- تأكيد ، 🇮🇶 '", callback_data='trueorder')],
                        [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
                    ])
                )
                
                juser["userfild"][from_id]["file"] = "none"
                juser["userfild"][from_id]["setmember"] = str(requested_members)
                save_user_data(from_id, juser)
            else:
                await send_message_with_keyboard(
                    update, context, chat_id,
                    f"• العدد الذي قمت بطلبه اكثر من نقاطك ، ⚜ '\n• لذلك لم يتم استجابة طلبكك ، 🔘 '\n\n- الحد الاقصى للعدد الذي يمكنك طلبه هوة ؛ {max_member} !\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                    ])
                )
        else:
            await send_message_with_keyboard(
                update, context, chat_id,
                "- يرجى إرسال عدد صحيح للأعضاء المطلوبين.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')]
                ])
            )
        return

    if textmassage and not is_dev:
        await send_message_with_keyboard(
            update, context, chat_id,
            f"• يرجى استخدام ازرار البوت فقط ارسل /start لرؤيةه الازرار ، للاستفسار او لشراء النقاط عليك مراسلة المبرمج ؛ @{DEV_USERNAME} ، 💌 !",
            reply_markup=None 
        )

# معالج الاستدعاءات (Callback Queries)
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chatid = query.message.chat_id
    messageid = query.message.message_id
    fromid = str(query.from_user.id)
    firstname = query.from_user.first_name
    usernames = query.from_user.username
    membercall = query.id
    
    cuser = load_user_data(fromid)
    user_data = load_data(USER_FILE, {"userlist": [], "blocklist": [], "channellist": [], "setmemberlist": []})
    
    user_info = cuser["userfild"].get(fromid, {})

    # 1. التحقق من حالة المغادرة (خصم النقاط)
    if user_info.get("channeljoin"):
        all_channel_joined = user_info["channeljoin"]
        
        channels_to_remove = []
        
        for idx, ch_username in enumerate(all_channel_joined):
            status = await get_chat_member_status(context, f"@{ch_username}", fromid)
            
            if status not in ['member', 'creator', 'administrator']:
                channels_to_remove.append((idx, ch_username))
                break

        if channels_to_remove:
            idx, ch_username = channels_to_remove[0]
            
            current_coin = int(user_info.get("coin", "0"))
            
            plus_coin = current_coin - 2
            
            if len(all_channel_joined) > idx and all_channel_joined[idx] == ch_username:
                del cuser["userfild"][fromid]["channeljoin"][idx]
                cuser["userfild"][fromid]["channeljoin"] = list(cuser["userfild"][fromid]["channeljoin"])
                
                cuser["userfild"][fromid]["coin"] = str(plus_coin)
                save_user_data(fromid, cuser)

                await context.bot.answer_callback_query(
                    membercall,
                    text=f"- بسبب مغادرة القناة ؛ @{ch_username} ، تم خصم 2 من نقاطك ، ⚠️ .",
                    show_alert=False
                )
                
                await send_message_with_keyboard(
                    update, context, chatid,
                    f"• لقد قمت بمغادرة بعض القنوات وقمت باخذ النقاط مقابل الانضمام ؛ وبسبب ذلك تم خصم 2 من النقاط لكل قناة من القنوات التي قمت بالمغادرة منها ، 🇮🇶\n\n• تستطيع اعادة النقاط التي تم خصمها من نقاطك بأعادة الاشتراك في القنوات التي قمت بالمغادرة منها قم بالاشتراك ثم اضغط على تحديث ؛ @{ch_username} ، 🐬 !",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("- تحديث ،  '", callback_data='takecoin')]
                    ])
                )
                
                await send_message_with_keyboard(
                    update, context, ADMIN_ID,
                    f"- هذا غادر ،\n\t- [{firstname}](tg://user?id={fromid})",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=None
                )
                return

    # 2. معالجة الأوامر الرئيسية

    if data == "panel":
        main_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("- تجمبع النقاط ، 📻 '", callback_data='takecoin')],
            [
                InlineKeyboardButton("- شراء الاعضاء ، 💸 '", callback_data='takemember'),
                InlineKeyboardButton("- احصائيات نقاطك ، 📊 '", callback_data='accont')
            ],
            [
                InlineKeyboardButton("- مشاركةه الرابط ، 📧 '", callback_data='member'),
                InlineKeyboardButton("- تحويل نقاط ، ♻️ '", callback_data='sendcoin')
            ],
            [InlineKeyboardButton("- ارسال اقتراح ، 🇮🇶 '", callback_data='sup')],
        ])
        
        await edit_message_text_with_keyboard(
            update, context, chatid, messageid,
            f"• اهلا بك يا ؛ [{firstname}](tg://user?id={chatid})\n\n- في بوت زيادة الاعضاء ، 📻 '\n- قم بتجميع النقاط وشراء الاعضاء لقناتك ، ⚖ '\n- التجميع عن طريق مشاركه الرابط او الاشتراك بالقنوات ، 💸 '\n- قم باختيار ما تريد من هذه الازرار ، 🔰 ؛\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n[اضغط هنا وتابع جديدنا ، 📢](https://t.me/{CHANNEL_SUPPORT})",
            reply_markup=main_keyboard
        )
        
        cuser["userfild"][fromid]["file"] = "none"
        save_user_data(fromid, cuser)
        return

    elif data == "takecoin" or data == "takecoin_accept":
        
        rules_accepted = user_info.get("acceptrules")
        
        if not rules_accepted:
            rules_text = (
                "• انتظر قليلا يجب عليك قراءة ما يلي ؛ 💚👇🏿 '\n"
                "• اكمل قراءة النقاط ثم ابدأ بجمع العملات ، \n\n"
                "١. الحصول على عملة من خلال الاشتراك في كل قناة\n"
                "٢. اذا قمت بالمغادرة من اي قناة بعد العضوية فسوف يتم خصم عملتين من عملاتك ،\n"
                "٣. يمكنك الحصول على عضو واحد مقابل عملتين ،\n"
                "٤. اذا قمت بتسجيل قناة غير اخلاقية سيتم حظرك من البوت ،\n\n"
                "- ملاحظة 🏹 ؛ اذا كانت لديك اي مشاكل في الاشتراك بالقنوات واستلام العملات او رأيت قنوات انحرافية وغير اخلاقية فيرجى الابلاغ عن القناة .\n\n"
                "- اذا قمت بقراءة جميع النقاط اضغط على زر تمت القراءة في الاسفل ؛ 🔰 !"
            )
            
            if data == "takecoin":
                await edit_message_text_with_keyboard(
                    update, context, chatid, messageid,
                    rules_text,
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("- تمت القراءة ، 🎲 '", callback_data="takecoin_accept"),
                            InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')
                        ],
                    ])
                )
            elif data == "takecoin_accept":
                cuser["userfild"][fromid]["acceptrules"] = True
                save_user_data(fromid, cuser)
            
            if data == "takecoin":
                return
        
        is_main_subscribed = await is_subscribed(context, f"@{CHANNEL_SUPPORT}", fromid)
        
        if not is_main_subscribed and not user_info.get("canceljoin"):
            
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                "- القناة الرئيسيةه للبوت اذا كنت غير مشترك عند اشتراكك سوف تحصل على 2 من النقاط ، 💬 '\n\n- واذا كنت مشترك مسبقا سوف تحصل على 2 من النقاط مجانا ، 📬 '\n\n• هذه الفرصة لا تتكرر ، بعد الاشتراك اضغط على التالي ، ♥️👇🏿؛",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("- اشتراك ، 📢 '", url=f"https://t.me/{CHANNEL_SUPPORT}"),
                        InlineKeyboardButton("- التالي ، 📻 '", callback_data='mainchannel')
                    ],
                    [
                        InlineKeyboardButton("• مشترك مسبقا ، 📮 '", callback_data='takecoin'),
                        InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')
                    ],
                ])
            )
            
            cuser["userfild"][fromid]["canceljoin"] = True
            save_user_data(fromid, cuser)
            return
        
        await handle_next_channel(update, context, 0, cuser, user_data, chatid, messageid, fromid, firstname)
        return

    elif data == "mainchannel":
        is_main_subscribed = await get_chat_member_status(context, f"@{CHANNEL_SUPPORT}", fromid)
        
        if is_main_subscribed not in ['member', 'creator', 'administrator']:
            await context.bot.answer_callback_query(
                membercall,
                text="• قم بألاشتراك في القناة اولا ؛ ثم اضغط على التالي ، 🔱 !",
                show_alert=True
            )
        else:
            current_coin = int(user_info.get("coin", "0"))
            plus_coin = current_coin + 2
            
            cuser["userfild"][fromid]["coin"] = str(plus_coin)
            if CHANNEL_SUPPORT not in cuser["userfild"][fromid]["channeljoin"]:
                cuser["userfild"][fromid]["channeljoin"].append(CHANNEL_SUPPORT)
            save_user_data(fromid, cuser)
            
            await context.bot.answer_callback_query(
                membercall,
                text="• تهانينا تم الحصول على 2 من النقاط واضافة النقاط الى رصيدك ، 🔰 !",
                show_alert=False
            )
            
            await handle_next_channel(update, context, 0, cuser, user_data, chatid, messageid, fromid, firstname)
        return

    elif data == "truechannel":
        getjoinchannel_username = user_info.get("getjoin")
        arraychannel_index = user_info.get("arraychannel")
        
        if not getjoinchannel_username or arraychannel_index is None:
            await context.bot.answer_callback_query(membercall, text="حدث خطأ في تحديد القناة.", show_alert=True)
            return

        status = await get_chat_member_status(context, f"@{getjoinchannel_username}", fromid)
        
        if status not in ['member', 'creator', 'administrator']:
            await context.bot.answer_callback_query(
                membercall,
                text="• قم بألاشتراك في القناة اولا ؛ ثم اضغط على التالي ، 🔱 !",
                show_alert=True
            )
        else:
            await context.bot.answer_callback_query(
                membercall,
                text="• تهانينا تم الحصول على نقطة واحدة واضافة العدد الى رصيدك ، 🔰 !",
                show_alert=False
            )
            
            current_coin = int(user_info.get("coin", "0"))
            current_coin += 1
            
            user_data = load_data(USER_FILE, {"userlist": [], "blocklist": [], "channellist": [], "setmemberlist": []})
            
            try:
                arraychannel_index = int(arraychannel_index)
                
                down_channel = int(user_data["setmemberlist"][arraychannel_index]) - 1
            except (ValueError, IndexError):
                down_channel = 0
                arraychannel_index = -1
            
            
            if down_channel > 0 and arraychannel_index != -1:
                user_data["setmemberlist"][arraychannel_index] = str(down_channel)
            elif arraychannel_index != -1:
                try:
                    del user_data["setmemberlist"][arraychannel_index]
                    del user_data["channellist"][arraychannel_index]
                    user_data["channellist"] = list(user_data["channellist"])
                    user_data["setmemberlist"] = list(user_data["setmemberlist"])
                except IndexError:
                    pass

            save_data(USER_FILE, user_data)
            
            if getjoinchannel_username not in cuser["userfild"][fromid]["channeljoin"]:
                cuser["userfild"][fromid]["channeljoin"].append(getjoinchannel_username)
            cuser["userfild"][fromid]["coin"] = str(current_coin)
            save_user_data(fromid, cuser)
            
            await handle_next_channel(update, context, arraychannel_index + 1 if arraychannel_index != -1 else 0, cuser, user_data, chatid, messageid, fromid, firstname)
        return

    elif data == "nextchannel":
        await context.bot.answer_callback_query(membercall, text="- انتظر قليلا ... 📌 !", show_alert=False)
        arraychannel_index = user_info.get("arraychannel", "-1")
        if arraychannel_index.isdigit():
            start_index = int(arraychannel_index) + 1
        else:
            start_index = 0
            
        await handle_next_channel(update, context, start_index, cuser, user_data, chatid, messageid, fromid, firstname)
        return

    elif data == "badchannel":
        getjoinchannel_username = user_info.get("getjoin")
        
        await context.bot.answer_callback_query(
            membercall,
            text="- تم ارسال الابلاغ الى مبرمج البوت ؛ وسوف يقوم بمراجعة القناة وحذفها من البوت نشكرك للتعاون معنا  ، ♥️ !",
            show_alert=True
        )
        
        await send_message_with_keyboard(
            update, context, DEV_IDS[0],
            f"- ابلاغ جديد عن قناة غير ملتزمة او انحرافية في البوت ، معرف القناة ؛ @{getjoinchannel_username} !\n\n\t﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n• معلومات العضو الذي قام بالابلاغ عن القناة ؛ 👇🏿♥️ ؛\n\n▫️ الايدي ؛ {fromid} ،\n◾️ المعرف ؛ @{usernames or 'لا يوجد'} ،",
            reply_markup=None
        )
        return

    elif data == "accont":
        invite = user_info.get("invite")
        coin = user_info.get("coin")
        setchannel = user_info.get("setchannel")
        setmember = user_info.get("setmember")
        
        await edit_message_text_with_keyboard(
            update, context, chatid, messageid,
            f"• جميع احصائيات النقاط الخاصةه بك ؛ 💛👇🏿 '\n\n◾️ عدد النقاط ؛ {coin}\n▫️ اخر قناة قمت بتمويلها ؛ {setchannel}\n◾️ عدد الاعضاء الذي قمت بطلبهم للقناة ؛ {setmember}\n▫️ عدد الذين قامو باستخدام رابطك ؛ {invite}\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n• معلومات حسابك الشخصي ؛ 📌'\n\n◾️ الاسم ؛ {firstname}\n▫️ المعرف ؛ @{usernames or 'لا يوجد'}\n◾️ الايدي ؛ {fromid}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("- القنوات التي تم الاشتراك فيها ، 📭 '", callback_data='mechannel')],
                [InlineKeyboardButton("- القنوات التي تم تمويلها من البوت ، ⚖ '", callback_data='order')],
                [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
            ])
        )
        return

    elif data == "mechannel":
        all_channel_joined = user_info.get("channeljoin", [])
        result = ""
        for ch_username in all_channel_joined:
            result += f"📍 @{ch_username}\n"
        
        if result:
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                f"- لستةه القنوات التي قمت بالاشتراك فيها ، 💛👇🏿؛\n\n{result}\n• ملاحظة : عند مغادرتك قناة واحدة سوف يتم خصم 2 من نقاطك ' بسبب المغادرة ؛ لذلك وجب التنبيه ، 📂 '",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
                ])
            )
        else:
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                "- انت لم تقم بالاشتراك في أي قناة من قنوات البوت ياعزيزي ؛ يرجى الاشتراك وتجميع النقاط ومن بعدها الضغط على زر القنوات التي تم الاشتراك فيها ، 🚸 .\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel'),
                        InlineKeyboardButton("- تجميع ، 📻 '", callback_data='takecoin')
                    ],
                ])
            )
        return

    elif data == "order":
        all_orders = user_info.get("listorder", [])
        result = ""
        for order in all_orders:
            result += f"📍 {order}\n"
            
        if result:
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                f"- لستةه القنوات التي قمت بتمويلها ؛ 🌼👇🏿 '\n\n{result}\n\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
                ])
            )
        else:
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                f"- عذرا ياعزيزي انت لم تقم بتمويل أي قناة من قنواتك ؛ لانك لا تمتلك النقاط او تمتلك ولكنك لم تقم بالتمويل .. اذا كانت لديك نقاط كافية لشراء الاعضاء اضغط على الزر الموجود بالاسفل ، 🇮🇶 '\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel'),
                        InlineKeyboardButton("- شراء الاعضاء ، 💸 '", callback_data='takemember')
                    ],
                ])
            )
        return

    elif data == "member":
        invite = user_info.get("invite")
        coin = user_info.get("coin")
        
        link_message = (
            f"- بوت زيادة الاعضاء للقنوات ، ⚖ !\n\n"
            f"- يمكنك جمع النقاط وزيادة اعضاء قناتك اعضاء حقيقيين من خلال البوت باليوم 500 عضو واكثر وكلشي مضمون ، 📻 !\n\n"
            f"- قم بالدخول الى البوت من خلال الرابط التالي لا تقم بتفويت هذه الفرصةه العظيمةه ، 👇🏿♥️ ؛\n"
            f"https://t.me/{USERNAME_BOT}?start={fromid}"
        )
        
        await send_message_with_keyboard(update, context, chatid, link_message, reply_markup=None)
        
        await send_message_with_keyboard(
            update, context, chatid,
            f"- قم بمشاركةه الرابط الذي في الاعلى واحصل على النقاط بكل سهولة ؛ دون الاشتراك في القنوات قم بارسال رابطك الى جميع المجموعات والقنوات واحصل على النقاط ، 🐬 !\n\n• عدد النقاط الخاصةه بك ؛ {coin}\n• عدد الذين قامو بالدخول الى رابطك ؛ {invite}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
            ])
        )
        return

    elif data == "sendcoin":
        await edit_message_text_with_keyboard(
            update, context, chatid, messageid,
            "- لارسال النقاط الى مستخدم اخر يجب ان يكون المستخدم مشترك في البوت وبعدها قم بارسال ايدي المستخدم لارسال النقاط اليه ، 📌 !\n\n\t- او قم بأرسال توجيه رسالة من رسائل المستخدم الذي تريد ارسال النقاط اليه الى البوت ، 💬 '\n\t﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
            ])
        )
        cuser["userfild"][fromid]["file"] = "sendcoin"
        save_user_data(fromid, cuser)
        return

    elif data == "takemember":
        coin = int(user_info.get("coin", "0"))
        
        if coin >= 10:
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                f"- الان قم بأرسال معرف القناة ؛ 🎲 !\n- مثال ؛ @{CHANNEL_SUPPORT}\n﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
                ])
            )
            cuser["userfild"][fromid]["file"] = "setchannel"
            save_user_data(fromid, cuser)
        else:
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                f"- يجب ان يكون لديك 10 نقاط على الاقل لشراء الاعضاء ،  🇮🇶 '\n\n- عدد النقاط ؛ {coin} !",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel'),
                        InlineKeyboardButton("- تجميع ، 📻 '", callback_data='takecoin')
                    ],
                ])
            )
        return

    elif data == "trueorder":
        setchannel = user_info.get("setchannel")
        setmember = int(user_info.get("setmember", "0"))
        
        is_admin = await get_chat_admins_status(context, setchannel)
        
        if not is_admin:
            await context.bot.answer_callback_query(
                membercall,
                text="- قم برفع البوت ادمن في القناة ليتم التمويل بصورة صحيحة ، 📡 '",
                show_alert=True
            )
        else:
            await edit_message_text_with_keyboard(
                update, context, chatid, messageid,
                "- تم تنفيذ طلبك بنجاح ، ⚠️\n\n- يمكنك طلب الهدايا ايضا ؛ ملاحظة اذا قمت بمخالفة قوانين وقواعد وتعليمات البوت سوف نقوم بحذف قناتك تأكد من الذهاب الى المساعدة والقواعد لتجنب الحظر ، 🐬 !",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
                ])
            )
            
            current_coin = int(user_info.get("coin", "0"))
            cost = setmember * 2
            coin_plus = current_coin - cost
            
            cuser["userfild"][fromid]["coin"] = str(coin_plus)
            cuser["userfild"][fromid]["listorder"].append(f"{setchannel} -> {setmember}")
            save_user_data(fromid, cuser)
            
            user_data = load_data(USER_FILE, {"userlist": [], "blocklist": [], "channellist": [], "setmemberlist": []})
            user_data["channellist"].append(setchannel)
            user_data["setmemberlist"].append(str(setmember))
            save_data(USER_FILE, user_data)
            
            await send_message_with_keyboard(
                update, context, ADMIN_ID,
                f"- هذا ضاف قناتة ،\n\t- [{firstname}](tg://user?id={fromid})",
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=None
            )
        return

    elif data == "sup":
        await edit_message_text_with_keyboard(
            update, context, chatid, messageid,
            "- الدعم وحل المشاكل الموجودة بالبوت ؛\n\n- الرجاء ارسال الشكاوي او المشاكل الموجودة بالبوت ليتم تصحيحها ارسل مشكلتك برسالة واحدة فضلا ؛ 🕊 !\n\n- يمكنك ايضا ارسال الميديا ؛ الصور والملصقات والصوت وغيرها .. ",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• العودة ، 🔙 '", callback_data='panel')],
            ])
        )
        cuser["userfild"][fromid]["file"] = "sendsup"
        save_user_data(fromid, cuser)
        return


# الدالة الرئيسية لتشغيل البوت
def main():
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start_command))
    
    # تصحيح الفلتر النحوي: تم التأكد من استخدام | للفصل داخل regex والهروب من '
    # (؟:...) يضمن عدم أسر المجموعات
    admin_commands_filter = filters.TEXT & filters.Regex(
        r'^(?:/panel|/admin|ادمن|- عدد الاعضاء ، 👤 \'|- رسالة للكل ، 🎒 \'|- توجيه للكل ، 🧜‍♂ \'|- عرض القنوات ، 🔱 \'|- حذف قناة ، 📛 \'|📍 نقاط للكل|- ارسال نقاط ، 🕊 \'|• العودة ، 🔙 \')$'
    )
    application.add_handler(MessageHandler(admin_commands_filter, admin_panel_command))
    
    # معالج الرسائل العادية ورسائل الحالات
    application.add_handler(MessageHandler(filters.TEXT | filters.FORWARDED, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()