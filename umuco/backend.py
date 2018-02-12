from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt
import re
from django.conf import settings
from recorders import *
import urllib
import json


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def identify_message(args):
    ''' This function identifies which kind of message this message is. '''
    incoming_prefix = args['text'].split('# ')[0].upper()
    if args['text'].split('# ')[0].upper() in getattr(settings,'KNOWN_PREFIXES',''):
        # Prefixes and related meanings are stored in the dictionary "KNOWN_PREFIXES"
        args['message_type'] = getattr(settings,'KNOWN_PREFIXES','')[incoming_prefix]
    else:
        args['message_type'] = "UNKNOWN_MESSAGE"


def eliminate_unnecessary_spaces(args):
    '''This function eliminate unnecessary spaces in an incoming message'''
    the_incoming_message = args['text']
    # Messages from RapidPro comes with spaces replaced by '+'
    # Let's replace those '+' (one or more) by one space
    the_new_message = urllib.unquote_plus(the_incoming_message)
    the_new_message = re.sub('[\# ]+','# ',the_new_message)
    #  Find any comma
    # Let's eliminate spaces at the begining and the end of the message
    args['text'] = the_new_message


@csrf_exempt
@json_view
def handel_rapidpro_request(request):
    '''This function receives requests sent by RapidPro.
    This function send json data to RapidPro as a response.'''
    # We will put all data sent by RapidPro in this variable
    incoming_data = {}

    # Let's put all the incoming data in the dictionary 'incoming_data'
    incoming_data = byteify(json.loads(request.body))

    # Let's assume that the incoming data is valid
    incoming_data['valide'] = True
    incoming_data['info'] = "The default information."

    # Because RapidPro sends the contact phone number in the format "tel:+12345678925"
    # let's get it from incomming_data
    incoming_data['phone'] = incoming_data['contact']['urn'].replace("tel:", "")
    incoming_data['text'] = incoming_data['results']['rapport1']['input']

    # Let's instantiate the variable this function will return
    response = {}

    # Let's eliminate unnecessary spaces in the incoming message
    eliminate_unnecessary_spaces(incoming_data)

    # Let's check which kind of message this message is.
    identify_message(incoming_data)
    if(incoming_data['message_type'] == 'PHONE_REGISTRATION'):
        # This message is sent to register a reporter
        response = record_reporter(incoming_data)

    if response['valide']:
        # The message have been recorded
        response['Ok'] = True
    else:
        # The message haven't been recorded
        response['Ok'] = False

    #  response['info_to_contact'] = incoming_data['info_to_contact']
    #  response['envoye'] = incoming_data['envoye']

    return response


@csrf_exempt
@json_view
def group_confirmation(request):
    '''This function receives requests sent by RapidPro.
    This function send json data to RapidPro as a response.'''
    # We will put all data sent by RapidPro in this variable
    incoming_data = {}

    # Let's put all the incoming data in the dictionary 'incoming_data'
    incoming_data = byteify(json.loads(request.body))

    # Let's assume that the incoming data is valid
    incoming_data['valide'] = True
    incoming_data['info'] = "The default information."

    # Because RapidPro sends the contact phone number in the format "tel:+12345678925"
    # let's get it from incomming_data
    incoming_data['phone'] = incoming_data['contact']['urn'].replace("tel:", "")
    incoming_data['text'] = incoming_data['results']['rapport1']['input']

    # Let's eliminate unnecessary spaces in the incoming message
    eliminate_unnecessary_spaces(incoming_data)

    # Let's instantiate the variable this function will return
    response = group_confirm(incoming_data)

    return response