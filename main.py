from telegram import Update , InlineKeyboardButton ,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder , CommandHandler , ContextTypes , filters , MessageHandler , CallbackQueryHandler
from dotenv import load_dotenv
import os
import re
import aiohttp
import json

load_dotenv()
TOKEN=os.getenv("token")
BASE_URL=os.getenv("base_url")
url=os.getenv("api_url")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Accept": "application/json, text/plain, */*"}

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    username=update.effective_user.username
    keyboard=[
        [InlineKeyboardButton("قیمت طلا 💰",callback_data="gold")],
        [InlineKeyboardButton("قیمت ارز 💸",callback_data="currency")]
    ]
    menu = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(f"سلام {username} !\nبه ربات قیمت ارز و طلا خوش آمدید\n",reply_markup=menu)
    elif update.callback_query:
        await update.callback_query.edit_message_text(f"سلام {username} !\nبه ربات قیمت ارز و طلا خوش آمدید\n",reply_markup=menu)

def gold_menu():

        keyboard=[
        [InlineKeyboardButton("18 عیار 💰",callback_data="18")],
        [InlineKeyboardButton("24 عیار 💰",callback_data="24")],
        [InlineKeyboardButton("بازگشت 🔙",callback_data="return")]
        ]
        return InlineKeyboardMarkup(keyboard)
def currency_menu():
        keyboard=[
        [InlineKeyboardButton("دلار 💵",callback_data="dollar")],
        [InlineKeyboardButton("یورو 💶",callback_data="euro")],
        [InlineKeyboardButton("بازگشت 🔙",callback_data="return")]
        ]
        return InlineKeyboardMarkup(keyboard)

def back_to_menu():
     keyboard=[
          [InlineKeyboardButton("بازگشت 🔙",callback_data="return")]
     ]
     return InlineKeyboardMarkup(keyboard)

async def handler_button(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    user_id=update.effective_user.id
    first_name=update.effective_user.first_name
    await query.answer()
    
    if query.data=="currency":
        await query.edit_message_text(f"لطفا ارز مورد نظر خود را انتخاب کنید ",reply_markup=currency_menu())
    elif query.data=="gold":
        await query.edit_message_text(f"لطفا عیار مورد نظر خود را انتخاب کنید",reply_markup=gold_menu())
    elif query.data=="dollar":
        async with aiohttp.ClientSession(headers=headers) as session:
             async with session.get(url=url) as response:
                  if response.status !=200:
                       await update.message.reply_text("خطا در ارتباط با سرور ❌")
                       return

                  data= await response.json()
                  currency_list=data.get("currency")  
                  for item in currency_list:
                       name=item["name"] 
                       if name=="دلار":  
                            text=f"دلار آمریکا 💵 : {item["name"]} , قیمت : {item["price"]} تومان"
                            await query.edit_message_text(text=text,reply_markup=back_to_menu())
                            break        
    elif query.data=="18":
        async with aiohttp.ClientSession(headers=headers) as session:
             async with session.get(url=url) as response:
                  if response.status !=200:
                       await update.message.reply_text("خطا در ارتباط با سرور ❌")
                       return

                  data= await response.json()
                  gold_list=data.get("gold")  
                  for item in gold_list:
                       name=item["name"] 
                       if name=="طلای 18 عیار":  
                            text=f"نوع طلا 💰 : {item["name"]} , قیمت : {item["price"]} تومان"
                            await query.edit_message_text(text=text,reply_markup=back_to_menu())
                            break
    elif query.data=="24":
        async with aiohttp.ClientSession(headers=headers) as session:
             async with session.get(url=url) as response:
                  if response.status !=200:
                       await update.message.reply_text("خطا در ارتباط با سرور ❌")
                       return

                  data= await response.json()
                  gold_list=data.get("gold")  
                  for item in gold_list:
                       name=item["name"] 
                       if name=="طلای 24 عیار":  
                            text=f"نوع طلا 💰 : {item["name"]} , قیمت : {item["price"]} تومان"
                            await query.edit_message_text(text=text,reply_markup=back_to_menu())
                            break 
    elif query.data=="euro":
        async with aiohttp.ClientSession(headers=headers) as session:
             async with session.get(url=url) as response:
                  if response.status !=200:
                       await update.message.reply_text("خطا در ارتباط با سرور ❌")
                       return

                  data= await response.json()
                  currency_list=data.get("currency")  
                  for item in currency_list:
                       name=item["name"] 
                       if name=="یورو":  
                            text=f"یورو 💶 : {item["name"]} , قیمت : {item["price"]} تومان"
                            await query.edit_message_text(text=text,reply_markup=back_to_menu())
                            break            
                                                            
    elif query.data=="return":
        await start(update,context)  


async def GetTextFromUser(update:Update,context:ContextTypes.DEFAULT_TYPE):
    text=update.message.text
    if text:
     user=update.effective_user.first_name
     await update.message.reply_text(f"{user} عزیز لطفا از منو جهت استغاده از بات اقدام کنید") 
     await start(update,context)

def main():
    print("bot is running...")
    app=ApplicationBuilder().token(TOKEN).base_url(BASE_URL).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,GetTextFromUser))
    app.add_handler(CallbackQueryHandler(handler_button))
    app.run_polling()

if __name__=="__main__":
    main()   
    