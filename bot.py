import requests
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7814501361:AAFzLWQ8Dg7GF_2TWs52Fu_TBtXuQJC85D0"
TMDB_API_KEY = "05bc9865c7fc036f226159010cd7c6a2"

def get_movie_details(movie_name):
    """Fetch movie details from TMDb API."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(url).json()

    if response["results"]:
        movie = response["results"][0]
        title = movie["title"]
        overview = movie["overview"]
        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        rating = movie["vote_average"]
        release_date = movie["release_date"]

        # Fake streaming link (replace with actual)
        streaming_link = f"https://example.com/watch/{movie['id']}"

        return title, overview, poster_url, rating, release_date, streaming_link
    return None

async def start(update: Update, context: CallbackContext) -> None:
    """Handles /start command."""
    await update.message.reply_text("🎬 Welcome to Movie Bot!\nSend me a movie name to get details.")

async def handle_movie_request(update: Update, context: CallbackContext) -> None:
    """Handles movie name search."""
    movie_name = update.message.text
    movie_details = get_movie_details(movie_name)

    if movie_details:
        title, overview, poster_url, rating, release_date, streaming_link = movie_details
        caption = f"🎬 *{title}*\n📅 Release: {release_date}\n⭐ Rating: {rating}/10\n📝 {overview}\n\n🔗 [Watch Here]({streaming_link})"

        await update.message.reply_photo(photo=poster_url, caption=caption, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Movie not found. Try another name.")

def main():
    """Start the bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_request))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
