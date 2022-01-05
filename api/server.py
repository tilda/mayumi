from quart import Quart, g

import api.bp as bp

app = Quart(__name__)
app.bot = None

@app.before_request
def assign_globals():
    g.bot = app.bot
    g.config = app.bot.config

@app.route('/')
async def root():
    return 'hello there'

app.register_blueprint(bp.auth.api, url_prefix='/api/auth')
app.register_blueprint(bp.dashboard.api, url_prefix='/api/dashboard')
app.register_blueprint(bp.settings.api, url_prefix='/api/settings')