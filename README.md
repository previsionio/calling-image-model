# Image model Calling

## SETUP

``` 
git clone git@github.com:previsionio/calling-image-model.git
python -m venv env
source env/bin/activate
pip install -r requirements.txt 
```

In order to call the model you need your model url, secret ID and access Key. They all can be found on the [deployment page of the model](https://doc.prevision.io/en/latest/studio/deployments/index.html#inspect-and-monitor-a-deployed-experiment).

Fill a .env file with your credentials ( used the provided .env.example) or put them in env var.

```
client_id=<YOUR_ID>
client_secret=<YOUR_SECRET>
model_url=<YOUR_URL>
```  


## Using the service


```python
import model
testimg=open('banana_for_test.jpeg', 'rb')
pred = model.send(testimg)
print(pred)
``` 

## Authorization flow

We use the OAuth2 Authorization flow which means :

- you must first get an acess token from the Auth Server `https://accounts.prevision.io/auth/realms/prevision.io/protocol/openid-connect/token` 
- then put it in your API call header `Authorization`field  with a `Bearer`  :

```
Authorization: Bearer <ACCESS_TOKEN>
``` 

See [this explanation](https://stackoverflow.com/questions/11068892/oauth-2-0-authorization-header)

## Exposte a flask API to your service

A WSGI server is provided that you can launch with gunicorn :


```
gunicorn --bind 0.0.0.0:8080  --timeout 120  --limit-request-line 0   --access-logfile - run:app
```

The service exposes two API you can test with whatever client you want :


```sh
curl --location --request GET 'http://localhost:8080/api/mymodel/health'

> {"msg":"I'm OK"}

curl --location --request POST 'http://localhost:8080/api/mymodel/prediction' --form 'img=@"./banana_for_test.jpeg"'

> {"infos":26497,"predictions":[{"detection_box":[0.07150368033648791,0.25276153346328784,0.8937960042060988,0.4093567251461988],"label":"pots",
> "probability":0.0021450864151120186},{"detection_box":[0.3280757097791798,0.7875243664717348,0.9400630914826499,0.9928525016244314],
> "label":"cartons","probability":0.002546289237216115}],"source":"banana_for_test.jpeg"}
```