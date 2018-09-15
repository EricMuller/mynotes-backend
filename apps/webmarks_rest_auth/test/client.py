import urllib2
import json



def get_auth_token():
    
    req = urllib2.Request(
        "https://xforce-api.mybluemix.net/auth/anonymousToken")
    response = urllib2.urlopen(req)
    html = response.read()
    json_obj = json.loads(html)
    token_string = json_obj["token"].encode("ascii", "ignore")
    return token_string


def get_response_json_object(url, auth_token):
    '''
      returns json object with info
    '''
    auth_token = get_auth_token()
    req = urllib2.Request(
        url, None, {"Authorization": "Bearer %s" % auth_token})
    response = urllib2.urlopen(req)
    html = response.read()
    json_obj = json.loads(html)
    return json_obj
