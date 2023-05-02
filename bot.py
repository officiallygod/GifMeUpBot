import re
from typing import Final

# pip install Google-Images-Search
from google_images_search import GoogleImagesSearch

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')
        
TOKEN: Final = 'YOUR_TELEGRAM_BOT_TOKEN'
BOT_USERNAME: Final = '@gifmeupbot' 
GOOGLE_API_KEY: Final = 'YOUR_GOOGLE_API_KEY'
gis = GoogleImagesSearch('CUSTOM_IMAGE_KEY', 'CUSTOM_IMAGE_PROJECT')

# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Heyo Bruhhh! I\'m a Gif bot.\n\nLemme Gif you up! Start by entering a Search Text.')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')
    

def handle_response(text: str) -> list:
    # Create your own response logic
    processed: str = text.lower()

    links = []
    x = re.search("allen*", processed)
    y = re.search("gif*", processed)

    if x == None:
        return links
    else:
        processed.replace("allen", "")
    
    if y == None:
        processed += ' gifs'
        
    # define search params
    _search_params = {
        'q': processed,
        'num': 20,
        'fileType': 'gif',
    }

    gis.search(search_params=_search_params)
    for image in gis.results():
        links.append(image.url)
        
    return links


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            responses: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        responses: str = handle_response(text)

    # Reply normal if the message is in private
    if len(responses) > 0:
        for response in responses:
            await update.message.reply_video(response)
    else:
        await update.message.reply_text("You are not authorised to use the bot!!! :(")
        
# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
    
# https://customsearch.googleapis.com/customsearch/v1?cx=716ebf52eec9843a9&q=test+gifs&searchType=image&
# num=10&start=201&fileType=gif&safe=off&key=AIzaSyCwO04Ut_SGVbOrDXJRiSxlf7XStvDJn5E&alt=json