
import json
from pickle import FALSE
from pydoc import pathdirs
import requests
import webbrowser
import os
import random
import getpass
import urllib
from os import listdir
from os.path import isfile, join


def read_config():
  #
  # read_config reads the 3rd party API configuration. 
  # The configuration contains the API URL and the data for authorization.
  #
  # :return: the 3rd party API configuration
  #
  path = os.path.join('Config', 'config.json')
  datei = open(path,'r')
  data = datei.read()
  return json.loads(data)
  
 
def read_webhook():
  #
  # read_webhook reads a preconfigured function webhook as JSON for creation or update porpose
  #
  # :return: the function webhook to be created or updated
  #
  onlyfiles = [f for f in listdir('SampleWebHooks') if isfile(join('SampleWebHooks', f))]
  i = 1
  for file in onlyfiles:
    print('Enter ' + str(i) + " for webhook config >" + file + "<")
    i+=1

  choice = input('Enter your choice: ')  
  index = int(choice)

  path = os.path.join('SampleWebHooks', onlyfiles[index - 1])
  datei = open(path,'r')
  data = datei.read()
  return json.loads(data) 


def enter_webhook_names():
  #
  # read_webhook_names reads the names of a function webhook as JSON from the command line
  #
  # :return: webhook names as json
  #
  locationName = input('Enter function webhook location name: ')
  functionName = input('Enter function webhook function name: ')

  jsonstr =  '{"locationName": "' + locationName + '", "functionName":"' + functionName + '"}'
  return jsonstr


def enter_access_token():
  #
  # enter_access_token request a token from command line input
  #
  # :return: The entered OAuth2 access token 
  #
  token = input('Paste your access token here and press enter: ')
  return token



def request_authorization(config):
  #
  # requests the authorization to the 3rd party API 
  #
  # :param config: The configuration contains the API URL and the data for authorization
  # :return: The OAuth2 authorization code needed for requesting the OAuth2 access token
  #
  print ("\n##### requesting authorization code #####\n")

  state = random.randint(10000, 99999)
  scope = urllib.parse.quote_plus(config['scope'])
  redirect_uri = urllib.parse.quote_plus(config['redirect_url'])
  request_url = config['authorize_url'] + '?response_type=code&client_id=' + config['client_id'] + '&redirect_uri=' + redirect_uri + '&scope=' + scope + '&response_mode=query&state=' + str(state)

  webbrowser.open(request_url)
  print("Enter your credentials at the browser and copy the returned URL: ")
  raw_code = input('Paste URL or authorization code here and press enter: ')
  posCode = raw_code.find("code=")

  authorization_code = raw_code
  if posCode > 0:
    authorization_code = raw_code[posCode+5:]

  return authorization_code  


def request_access_token(config, authorization_code):
  #
  # request_access_token gets the bearer token for accessing 
  #
  # :param config: The configuration contains the API URL and the data for authorization
  # :param authorization_code: The OAuth2 authorization code
  # :return: The OAuth2 access token
  #
  print ("\n##### requesting access token #####\n")

  params = {
      'grant_type': 'authorization_code',
      'code': authorization_code,
      'redirect_uri': config['redirect_url'],
      'client_id': config['client_id']
  }
  
  if 'client_secret' in config and len(config['client_secret']) > 0:
    params['client_secret'] = config['client_secret']

  access_token_response = requests.post(config['token_url'], params=params, headers = {"Accept": "application/json"})
  if access_token_response.status_code >= 400:
    print("Error: " + str(access_token_response.status_code) + " : " + access_token_response.text)
    return None
  else:
    print ("The access token for later use:\n")

    tokens = json.loads(access_token_response.text)
    access_token = tokens['access_token']

    print(access_token)
    return access_token


def get_all_systems(config, access_token):
  #
  # get_all_systems get all systems of the current authenticated user
  # 
  # :param config:  The configuration contains the API URL and the data for authorization
  # :param access_token:  The OAuth2 access token for accessing the 3rd party API
  # :return: A list of ekey bionyx systems where the user can create function webhooks
  #
  print ("\n##### get all systems #####\n")

  api_call_headers = {'Authorization': 'Bearer ' + access_token}
  url = config['api_url'] + 'api/systems/'

  api_call_response = requests.get(url, headers=api_call_headers)
  if api_call_response.status_code >= 400:
    print("Error: " + str(api_call_response.status_code) + " : " + api_call_response.text)
    return None
  else:
    systems = json.loads(api_call_response.text)
    print("\nYou are able to add 3rd party web hooks to following systems:")
    for system in systems:
      print("Name: " + system['systemName'] + ' ID: ' + system['systemId'] )
    return systems


def create_webhook(config, access_token, system):
  #
  # create_webhook creates a new function webhook for the specified ekey bionyx system.
  # 
  # :param config: The configuration contains the API url and the data for authorization
  # :param access_token:  The OAuth2 access token for accessing  the 3rd party API
  # :param system: the ekey bionyx system
  #
  print ("\n##### create webhook #####\n")

  api_call_headers = {'Authorization': 'Bearer ' + access_token}
  create_url = config['api_url'] + 'api/systems/' + system['systemId'] + '/function-webhooks'
  webhook = read_webhook()

  api_call_response = requests.post(create_url, json=webhook, headers=api_call_headers)
  if api_call_response.status_code >= 400:
    print("Error: " + str(api_call_response.status_code) + " : " + api_call_response.text)
  else:
    print("Success. Webhook created")


def enumerate_webhooks(config, access_token, system):
  # enumerate_webhooks gets all function webhooks available for the specified ekey bionyx system..
  # 
  # :param config: The configuration contains the API URL and the data for authorization
  # :param access_token:  The OAuth2 access token for accessing the 3rd party API
  # :param system: the ekey bionyx system
  #
  print ("\n##### enumerate webhooks #####\n")

  api_call_headers = {'Authorization': 'Bearer ' + access_token}
  enum_url = config['api_url'] + 'api/systems/' + system['systemId'] + '/function-webhooks'

  api_call_response = requests.get(enum_url, headers=api_call_headers)
  if api_call_response.status_code >= 400:
    print("Error: " + str(api_call_response.status_code) + " : " + api_call_response.text)
  else:
    webhooks = json.loads(api_call_response.text)
    print("\nThe following function webhooks are in the system:")
    for webhook in webhooks:
      print("Name: " + webhook['integrationName'] + ' ID: ' + webhook['functionWebhookId'] )


def get_webhook(config, access_token, system):
  # enumerate_webhooks gets all function webhooks available for the specified ekey bionyx system..
  # 
  # :param config: The configuration contains the API url and the data for authorization
  # :param access_token:  The OAuth2 access token for accessing  the 3rd party API
  # :param system:  the ekey bionyx system
  #
  print ("\n##### get webhook #####\n")

  webhook_id = input('Enter function webhook ID: ')
  api_call_headers = {'Authorization': 'Bearer ' + access_token}
  get_url = config['api_url'] + 'api/systems/' + system['systemId'] + '/function-webhooks/' + webhook_id

  api_call_response = requests.get(get_url, headers=api_call_headers)
  if api_call_response.status_code >= 400:
    print("Error: " + -str(api_call_response.status_code) + " : " + api_call_response.text)
  else:
    webhook = json.loads(api_call_response.text)
    print("\nFunction webhook data:")
    print(webhook)



def delete_webhook(config, access_token, system):
  # delete_webhook Requests deletion of an existing function webhook for the specified ekey bionyx system. 
  # The ekey bionyx system administrator is informed about the deletion request and must confirm it in order to execute the deletion. 
  # 
  # :param config: The configuration contains the API URL and the data for authorization
  # :param access_token:  The OAuth2 access token for accessing the 3rd party API
  # :param system: the ekey bionyx system
  #
  print ("\n##### delete webhook #####\n")

  webhook_id = input('Enter function webhook ID which should be deleted: ')
  api_call_headers = {'Authorization': 'Bearer ' + access_token}
  get_url = config['api_url'] + 'api/systems/' + system['systemId'] + '/function-webhooks/' + webhook_id

  api_call_response = requests.delete(get_url, headers=api_call_headers)
  if api_call_response.status_code >= 400:
    print("Error: " + str(api_call_response.status_code) + " : " + api_call_response.text)
  else:
    print("\nFunction webhook" +  webhook_id + "successfully deleted - users will be notified!")



def update_webhook(config, access_token, system):
  # update_webhook Requests an update of an existing function webhook for the specified ekey bionyx system. 
  # The ekey bionyx system administrator is informed about the update request and must confirm it in order for the update to become effective.
  # 
  # :param config: The configuration contains the API url and the data for authorization
  # :param access_token:  The OAuth2 access token for accessing  the 3rd party API
  # :param system: the ekey bionyx system
  #
  print ("\n##### update webhook #####\n")

  webhook_id = input('Enter function webhook ID which should be updated: ')
  api_call_headers = {'Authorization': 'Bearer ' + access_token}
  update_url = config['api_url'] + 'api/systems/' + system['systemId'] + '/function-webhooks/' + webhook_id

  webhook = read_webhook()

  api_call_response = requests.put(update_url, json=webhook, headers=api_call_headers)
  if api_call_response.status_code >= 400:
    print("Error: " + str(api_call_response.status_code) + " : " + api_call_response.text)
  else:
    print("\nFunction webhook" +  webhook_id + "successfully updated - users will be notified!")



def update_webhook_name(config, access_token, system):
  # update_webhook_name Updates the specified function webhook name. 
  # This change does not require confirmation by the ekey bionyx system administrator.
  # 
  # :param config: The configuration contains the API URL and the data for authorization
  # :param access_token:  The OAuth2 access token for accessing the 3rd party API
  # :param system: the ekey bionyx system
  #
  print ("\n##### update webhook name #####\n")

  webhook_id = input('Enter function webhook ID which should be changed: ')
  api_call_headers = {'Authorization': 'Bearer ' + access_token}
  update_url = config['api_url'] + 'api/systems/' + system['systemId'] + '/function-webhooks/' + webhook_id + '/name'

  webhook_names = enter_webhook_names()

  api_call_response = requests.patch(update_url, json=json.loads(webhook_names), headers=api_call_headers)
  if api_call_response.status_code >= 400:
    print("Error: " + str(api_call_response.status_code) + " : " + api_call_response.text)
  else:
    print("\nFunction webhook" +  webhook_id + "successfully updated names.")



#main  
# read 3rd party API configuration
config = read_config()

# First, we need the OAuth2 access token
print('\n\n######################### ekey 3rd party API sample #############################\n')
print('To access the 3rd party API an access token is needed')
print('Enter 1 if you already have an access token')
print('Enter 2 if you need an access token')
choice = input('Enter your choice: ')

access_token = None
if choice == '2':
  authorization_code = request_authorization(config)
  access_token = request_access_token(config, authorization_code)
else:
  # enter the access token via command line 
  access_token = enter_access_token()

#  Second, we need a system where we can manage the function webhooks
systems = get_all_systems(config, access_token)

if len(systems) > 0:
  while True:
    print('\nWhich action do you want to perform?')
    print('Enter 1 to create a function webhook')
    print('Enter 2 to list all function webhooks')
    print('Enter 3 to get the function webhook information')
    print('Enter 4 to delete a function webhook (user interaction required)')
    print('Enter 5 to update the function webhook name')
    print('Enter 6 to update the function webhook (user interaction required)')
    action = input('Enter 0 for Exit: ')

    if action == '1':
      create_webhook(config, access_token, systems[0])
    elif action == '2':  
      enumerate_webhooks(config, access_token, systems[0])
    elif action == '3':
      get_webhook(config, access_token, systems[0])  
    elif action == '4':
      delete_webhook(config, access_token, systems[0]) 
    elif action == '5':
      update_webhook_name(config, access_token, systems[0]) 
    elif action == '6':
      update_webhook(config, access_token, systems[0]) 
    else:
      break  
else:
  print('\nNo systems with activated Third Party Integration API found. Did you activate it in the App?\n')

