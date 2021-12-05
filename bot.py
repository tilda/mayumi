from twitchio.ext import commands
import utils.config
from logbook.compat import redirect_logging
from logbook import StreamHandler
from sys import stdout, exit
from logging import getLogger
from re import compile as compile_regex

config = utils.config.load_config()
bm_regex = "https:\/\/osu\.ppy\.sh\/(?P<endpoint>beatmapsets|beatmaps|b|s)\/\d*"

class Mayumi(commands.Bot):
    def __init__(self):
        # logging stuff
        StreamHandler(stdout).push_application()
        redirect_logging()
        self.log = getLogger('mayumi')
        for logger in ['twitchio.websocket', 'twitchio.client', 'asyncio']:
            logger.setLevel(20) # get rid of unnecessary debug logging

        # startup banner
        if config['misc']['startup_banner']:
            print(open('utils/banner.txt').read())

        # init bot
        self.log.info('starting mayumi...')
        self.regex = compile_regex(bm_regex)
        super().__init__(
            token=config['twitch']['access_token'],
            prefix=config['twitch']['prefix'],
            initial_channels=config['twitch']['channels'] # TBD: load this from DB
        )

    async def event_message(self, message):
        if message.echo:
            return # don't respond to messages sent by bot itself
        
        if self.regex.search(message.content):
            self.log.info(f'Got one! {message.content}')

        await self.handle_commands(message)

    async def event_ready(self):
        self.log.info(f'okay, so... now what?')

bot = Mayumi()
bot.run()