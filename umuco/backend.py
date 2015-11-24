from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt
import re
from django.conf import settings
from recorders import *
import urllib

def identify_message(args):
    ''' This function identifies which kind of message this message is. '''
    incoming_prefix = args['text'].split('#')[0].upper()
    if args['text'].split('#')[0].upper() in getattr(settings,'KNOWN_PREFIXES',''):
    	#Prefixes and related meanings are stored in the dictionary "KNOWN_PREFIXES"
        args['message_type'] = getattr(settings,'KNOWN_PREFIXES','')[incoming_prefix]
    else:
        args['message_type'] = "UNKNOWN_MESSAGE"

def eliminate_unnecessary_spaces(args):
    '''This function eliminate unnecessary spaces in an incoming message'''
    the_incoming_message = args['text']
    print("The text before sub             "+the_incoming_message)
    #Messages from RapidPro comes with spaces replaced by '+'
    #Let's replace those '+' (one or more) by one space
    # import ipdb; ipdb.set_trace()
    the_new_message = re.sub('[\#]+',' ',the_incoming_message)
    # Find any comma
    the_new_message = urllib.unquote_plus(the_new_message)
    #Let's eliminate spaces at the begining and the end of the message
    print("The text after sub              "+the_new_message)
    args['text'] = the_new_message
    print("The text after sub args['text'] "+args['text'])

@csrf_exempt
@json_view
def handel_rapidpro_request(request):
    '''This function receives requests sent by RapidPro.
    This function send json data to RapidPro as a response.'''
    #We will put all data sent by RapidPro in this variable
    incoming_data = {}

    #Two couples of variable/value are separated by &
    #Let's put couples of variable/value in a list called 'list_of_data'
    list_of_data = request.body.split("&")

    #Let's put all the incoming data in the dictionary 'incoming_data'
    for couple in list_of_data:
        incoming_data[couple.split("=")[0]] = couple.split("=")[1]

    #Let's assume that the incoming data is valide
    incoming_data['valide'] = True
    incoming_data['info'] = "The default information."

    #Because RapidPro sends the contact phone number by replacing "+" by "%2B"
    #let's rewrite the phone number in a right way.
    incoming_data['phone'] = incoming_data['phone'].replace("%2B","+")

    #Let's instantiate the variable this function will return
    response = {}

    #Let's eliminate unnecessary spaces in the incoming message
    eliminate_unnecessary_spaces(incoming_data)

    #Let's check which kind of message this message is.
    identify_message(incoming_data)
    print("0000000000000000000000000000000000000000000000")
    print("incoming_data['message_type']")
    print(incoming_data['message_type'])
    if(incoming_data['message_type']=='PHONE_REGISTRATION'):
        print("1111111111111111111111111111111111111111111111111")
        #This message is sent to register a reporter
        record_reporter(incoming_data)
        print("2222222222222222222222222222222222222222222222222")

    if incoming_data['valide'] :
        #The message have been recorded
        response['ok'] = True
    else:
    	#The message haven't been recorded
        response['ok'] = False

    response['info_to_contact'] = incoming_data['info_to_contact']

    return response
