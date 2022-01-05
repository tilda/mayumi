# OAuth and how to trick it into working
I fucking hate OAuth oh god I had to wrestle with it for like 6 hours oh my god fuck.

Anyways, yeah.

# For Twitch!
The chatbot portion of the application.

# Creating a OAuth application
This is the easiest part, so I will [leave it to Twitch to explain, from their documentation](https://dev.twitch.tv/docs/authentication#registration). You will want to add `http://localhost` as a redirect URL because it will come in handy later. Also, create a client secret and save it for later, as well as the client ID. Both are very important for the next step!

# Authenticating our application
You will want to take this following URL:
```
https://id.twitch.tv/oauth2/authorize?client_id=<your client ID>&redirect_uri=http://localhost&response_type=code&scope=chat:read%20chat:edit
```

Don't enter it into the address bar yet. Replace the `<your client ID>` with the client ID from earlier, and *then* you can press Enter. You can then press that little purple Authorize button.

Assuming you don't actually have anything running under localhost on port 80, it will return a "refused to connect". This is fine, and works for our next step.

# Finally getting a refresh token
You will need a HTTP client for this one. It doesn't matter what you use as long as it can send POST requests. If you don't have one lying around, you can use [reqbin](https://reqbin.com/).

Remember that previous step? You will want to take the `code` part of that URL, we need it to generate a refresh token for the bot.
```md
http://localhost/?code=**0123456789abcdefghijABCDEFGHIJ**&scope=chat%3Aread+chat%3Aedit
```

Now that you have the code from the authorization process, take this following URL:
```
https://id.twitch.tv/oauth2/token?client_id=<your client ID>&client_secret=<your client secret>&code=<your code>&grant_type=authorization_code&redirect_uri=http://localhost
```

Replace the placeholders with the needed information, i.e. `<your client ID>` with your client ID and etc. You will want to send a POST request to this URL. In reqbin this is done with the selection dropdown next to the "URL" input.

Once you've sent the request, you should receive a response fairly quickly. An average response looks like this:
```json
{"access_token":"0123456789abcdefghijABCDEFGHIJ","expires_in":14275,"refresh_token":"0123456789abcdefghijABCDEFGHIJ","scope":["chat:edit","chat:read"],"token_type":"bearer"}
```

What's important here is the value under `refresh_token`. Create a new file under the bot folder named `oauth_cache.json` and input the following (replacing the value of `refresh_token` with your result):
```json
{"refresh_token":"0123456789abcdefghijABCDEFGHIJ"}
```
# Congratulations!
You have successfully finished setting up Twitch authentication for the bot. You shouldn't have to touch it from now on unless something goes wrong. Have fun!