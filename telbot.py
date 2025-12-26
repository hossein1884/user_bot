import logging
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json ,sqlite3
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
cn=sqlite3.connect("data.db")
cur=cn.cursor()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger=logging.getLogger(__name__)
# f=open("users.txt","w",encoding="utf-8")
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /start is issued."""
#     global users
#     user=update.effective_user
#     users+=user.username+","
#     f.write(users)
    

#     await update.message.reply_html(rf"Hi {user.mention_html()}!",reply_markup=ForceReply(selective=True),)
print(dir(Update.effective_user))
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if 1 not in cn.execute("select 1 from users where id=?",(str(user.id,))).fetchone():
        cur.execute(f"INSERT INTO users VALUES ('{user.id}','{user.full_name}','{user.username}')")
        cn.commit()
   
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user=update.effective_user
    print(user)
    await update.message.reply_html(rf"Goodbye {user.username}!",reply_markup=ForceReply(selective=True),)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if update.message.text == "hi" : 
        await update.message.reply_text( "Hello Buddy")    
    else: 
        await update.message.reply_text( "wrong question")

async def price_btc(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    
    headers = {
    'Accepts': 'application/json',
    'Accept-Encoding': 'deflate, gzip',
    'X-CMC_PRO_API_KEY': 'put your coinmarketcap api in here',
    }

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        with open("price.json","wb") as f:
            f.write(response._content)
        f=open("price.json","rb")
        f1=json.loads(f.read())
        for i in f1["data"]:
            if i["symbol"]=="BTC":
                await update.message.reply_text( "the Bitcoin dollar price is {}$".format(i["quote"]["USD"]["price"]))
        
            
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    

def main()->None:
    """Start the bot."""
    application=Application.builder().token("your token").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("end", end))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()