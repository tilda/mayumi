from requests import get, post
from json import load, dumps
from json.decoder import JSONDecodeError
from logging import getLogger
from pathlib import Path

logger = getLogger('mayumi.oauth')

class InvalidOAuthToken(Exception):
    pass

def create_token(id: str, secret: str, token: str):
    access_token = post(
        'https://id.twitch.tv/oauth2/token'
        f'?client_id={id}'
        f'&client_secret={secret}'
        '&grant_type=refresh_token'
        f'&refresh_token={token}'
    )
    if access_token.status_code == 200:
        logger.info('new token generated')
        return access_token.json()
    else:
        logger.exception('something happened while generating the token?!')

def validate_token(token: str):
    validate_req = get('https://id.twitch.tv/oauth2/validate', headers={
        'Authorization': f'Bearer {token}'
    })
    if validate_req.status_code == 200:
        logger.info('token is valid')
        return True
    else:
        raise InvalidOAuthToken(f'validation request returned HTTP {validate_req.status_code}')

def retrieve_token(id: str, secret: str):
    logger.info('attempting to retrieve token from cache')
    try:
        if Path('./oauth_cache.json').exists() == False:
            open('oauth_cache.json', 'x') # create file 
        token_cache_file = open('oauth_cache.json', 'r+')
        token_cache = load(token_cache_file)
        refresh_token = token_cache.get('refresh_token')
    except:
        logger.warning('token not found, requesting fresh one')
        response = create_token(id, secret, refresh_token)
        access_token = response['access_token']
        logger.info('writing new token to cache')
        token_cache_file.write(dumps({
            'access_token': response['access_token']
        }))
    finally:
        try:
            token = create_token(id, secret, refresh_token)
            validate_token(token['access_token'])
            return token['access_token']
        except:
            exit(1)
