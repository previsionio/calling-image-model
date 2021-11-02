import logging
logger = logging.getLogger('Prevision Model')
logging.basicConfig(format='[ %(name)s API ] %(asctime)s %(message)s', level=logging.INFO)


from requests.exceptions import ConnectionError
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

import os
from dotenv import load_dotenv

load_dotenv()

# Fill up a .env file or set you var in env
#  Go to your model deploy page to get this information

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
# Your model url
predict_url = os.getenv('model_url')

client = BackendApplicationClient(client_id=client_id)

def send(img):
    try :
        # First Get a token from Prevision Token server
        oauth = OAuth2Session(client=client)
        oauth.fetch_token(token_url='https://accounts.prevision.io/auth/realms/prevision.io/protocol/openid-connect/token', client_id=client_id,  client_secret=client_secret)                  
        files = {'image': img}       
        # Model predicti API 
        prediction = oauth.post("{}/model/predict".format(predict_url), files=files)
        return prediction.json()
    except ConnectionError:
        logger.error("Cannot call model")
        return {}




def predict_file(img):
    """Do something with your file a prediction or whatever

    Args:
        img (Bytes): A file in RAM

    Returns:
        dict : Some json about the file
    """
    logging.info("Prediction over a file")
    p = send(img)
    predictions =  p["predictions"]
    infos = len(img.getvalue())
    logging.debug(infos)
    return {"infos":infos, "predictions":predictions}

