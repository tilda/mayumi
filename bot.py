from twitchio.ext import commands
import utils.config
from logbook.compat import redirect_logging
from logbook import StreamHandler
from sys import stdout, exit
from logging import getLogger
from re import compile as compile_regex
from api.server import app as api
from hypercorn.config import Config as hypercorn_config
from hypercorn.asyncio.run import Server
from asyncio import get_event_loop

config = utils.config.load_config()
bm_regex = "https:\/\/osu\.ppy\.sh\/(?P<endpoint>beatmapsets|beatmaps|b|s)\/\d*"

# Thanks: https://github.com/slice/dogbot/blob/master/dog/bot.py#L19
async def _boot_hypercorn(app, config, loop):
    server = await loop.create_server(
        lambda: Server(app, loop, config), host="127.0.0.1", port=app.bot.config["api"]["port"] 
    )
    return server
class Mayumi(commands.Bot):
    def __init__(self):
        # logging stuff
        StreamHandler(stdout).push_application()
        redirect_logging()
        self.log = getLogger('mayumi')
        self.config = config
        for logger in ['twitchio.websocket', 'twitchio.client', 'asyncio']:
            yeah = getLogger(logger)
            yeah.setLevel(20) # get rid of unnecessary debug logging

        # startup banner
        if config['misc']['startup_banner']:
            print(open('utils/banner.txt').read())

        # init bot
        self.log.info('starting mayumi...')
        self.regex = compile_regex(bm_regex)

        api.bot = self
        self.api = api
        self.api_server = None
        self.http_loop = get_event_loop()
        self.http_loop.create_task(self.boot_api_server())
        
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



    async def boot_api_server(self):
        try:
            self.api_server = await _boot_hypercorn(
                self.api, hypercorn_config.from_mapping(config['api']), self.http_loop
            )
        except:
            self.log.exception('failed to start API server')

bot = Mayumi()
bot.run()