import asyncio
import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import tasks
from flask import Flask
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("main")

# Load environment variables
load_dotenv()

# Web Server (Flask) to keep the bot alive on free hosting platforms
app = Flask('')

@app.route('/')
def home():
    return "Discord Voice Idle Bots are running! 🚀", 200

def run_web_server():
    port = int(os.environ.get('PORT', 8080))
    # host '0.0.0.0' is required for external hosting services to ping it
    logger.info(f"Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port)

# Define a custom client class to handle voice connection and auto-reconnection
class IdleVoiceBot(discord.Client):
    def __init__(self, bot_name, voice_channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_name = bot_name
        self.voice_channel_id = voice_channel_id

    async def on_ready(self):
        logger.info(f"[{self.bot_name}] Logged in as {self.user} (ID: {self.user.id})")
        # Start the background loop to maintain voice connection
        if not self.maintain_voice_connection.is_running():
            self.maintain_voice_connection.start()

    @tasks.loop(seconds=30)
    async def maintain_voice_connection(self):
        if not self.voice_channel_id:
            logger.warning(f"[{self.bot_name}] No voice channel ID configured in .env.")
            return

        try:
            channel_id = int(self.voice_channel_id)
        except ValueError:
            logger.error(f"[{self.bot_name}] Invalid voice channel ID: '{self.voice_channel_id}' (Must be digits)")
            return

        # Check if we are connected to the voice client in any guild
        voice_client = None
        for vc in self.voice_clients:
            # Find voice client associated with this bot's target guild
            channel = self.get_channel(channel_id)
            if channel and vc.guild.id == channel.guild.id:
                voice_client = vc
                break

        # If already connected, verify if it is in the target channel
        if voice_client:
            if voice_client.channel.id == channel_id:
                if voice_client.is_connected():
                    # We are in the correct channel and connected, everything is fine
                    return
                else:
                    logger.info(f"[{self.bot_name}] Voice client disconnected state detected, cleaning up...")
                    try:
                        await voice_client.disconnect(force=True)
                    except Exception:
                        pass
            else:
                # Connected to a different channel, disconnect first
                logger.info(f"[{self.bot_name}] Connected to channel ID {voice_client.channel.id}, but target is {channel_id}. Reconnecting...")
                try:
                    await voice_client.disconnect(force=True)
                except Exception:
                    pass

        # Connect to the target voice channel
        channel = self.get_channel(channel_id)
        if not channel:
            try:
                channel = await self.fetch_channel(channel_id)
            except discord.NotFound:
                logger.error(f"[{self.bot_name}] Voice channel with ID {channel_id} not found.")
                return
            except discord.Forbidden:
                logger.error(f"[{self.bot_name}] Bot lacks permission to access channel ID {channel_id}.")
                return
            except Exception as e:
                logger.error(f"[{self.bot_name}] Error fetching channel {channel_id}: {e}")
                return

        if not isinstance(channel, discord.VoiceChannel):
            logger.error(f"[{self.bot_name}] Channel ID {channel_id} is not a Voice Channel (Type: {type(channel)})")
            return

        logger.info(f"[{self.bot_name}] Attempting to connect to voice channel '{channel.name}' (Guild: '{channel.guild.name}')...")
        try:
            await channel.connect(reconnect=True, timeout=20.0)
            logger.info(f"[{self.bot_name}] Successfully connected to voice channel '{channel.name}'!")
        except Exception as e:
            logger.error(f"[{self.bot_name}] Error connecting to voice channel: {e}")

    @maintain_voice_connection.before_loop
    async def before_maintain_voice(self):
        await self.wait_until_ready()

async def main():
    # Retrieve configuration
    token1 = os.getenv("BOT_TOKEN_1")
    channel1 = os.getenv("VOICE_CHANNEL_ID_1")
    token2 = os.getenv("BOT_TOKEN_2")
    channel2 = os.getenv("VOICE_CHANNEL_ID_2")

    # Configure intents
    intents = discord.Intents.default()
    intents.guilds = True
    intents.voice_states = True

    bots = []

    # Configure Bot 1
    if token1 and token1.strip() and token1 != "YOUR_BOT_TOKEN_1_HERE":
        bot1 = IdleVoiceBot(bot_name="Bot_1", voice_channel_id=channel1, intents=intents)
        bots.append((bot1, token1))
    else:
        logger.warning("Bot 1 token is missing or contains placeholder. Skipping Bot 1.")

    # Configure Bot 2
    if token2 and token2.strip() and token2 != "YOUR_BOT_TOKEN_2_HERE":
        bot2 = IdleVoiceBot(bot_name="Bot_2", voice_channel_id=channel2, intents=intents)
        bots.append((bot2, token2))
    else:
        logger.warning("Bot 2 token is missing or contains placeholder. Skipping Bot 2.")

    if not bots:
        logger.error("No valid bot tokens configured. Please update your .env file with your Discord bot tokens.")
        # We start the web server anyway so the deployment doesn't crash immediately due to no port binding
        web_thread = threading.Thread(target=run_web_server, daemon=True)
        web_thread.start()
        logger.info("Keep-alive Web Server started in placeholder mode. Keeping process alive...")
        # Keep process alive
        while True:
            await asyncio.sleep(3600)

    # Start Flask Web Server in a background daemon thread
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info("Keep-alive Web Server started.")

    # Run bots concurrently
    tasks = [bot.start(token) for bot, token in bots]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bots shutting down...")
