from urllib.parse import quote, urlencode
import requests

# Client ID and secret from Azure AD
client_id = '1e06f32d-531a-42ae-917e-40b9904bb5a3'
client_secret = 'YcvFcqm0knHADJboSLxT3Ampq+Em9M6xgkgf0KFgy3A='

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/token')

def get_signin_url(redirect_uri):
  # Build the query parameters for the signin url
  params = { 'client_id': client_id,
             'redirect_uri': redirect_uri,
             'response_type': 'code',
             'prompt': 'login',
           }
      
  # Format the sign-in url for redirection     
  signin_url = authorize_url.format(urlencode(params))
  
  return signin_url
  
def get_token_from_code(auth_code, redirect_uri, resource):
  # Build the post form for the token request
  post_data = { 'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': redirect_uri,
                'resource': resource,
                'client_id': client_id,
                'client_secret': client_secret
              }
     
  # Perform the post to get access token         
  response = requests.post(token_url, data = post_data)
  
  try:
    # try to parse the returned JSON for an access token
    access_token = response.json()['access_token']
    return access_token
  except:
    return 'Error retrieving token: {0} - {1}'.format(response.status_code, response.text)