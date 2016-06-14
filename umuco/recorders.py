from django.conf import settings
import re
from umuco.models import *
import requests
import json
from umuco.utils import get_or_none
from bdiadmin.models import *


days = {1:'Lundi',2:'Mardi', 3:'Mercredi', 4:'Jeudi', 5:'Vendredi', 6:'Samedi', 7:'Dimanche'}

def check_number_of_values(args):
    #This function checks if the message sent is composed by an expected number of values
    print("==len(args['text'].split('#'))==")
    print(len(args['text'].split('#')))
    print(args['text'].split('#'))
    if(args['message_type']=='PHONE_REGISTRATION'):
        if len(args['text'].split('#')) < 6:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
        if len(args['text'].split('#'))  == 7:
            args['number_of_values'] = 7
            args['valide'] = True
            args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
        if len(args['text'].split('#')) == 6:
            args['valide'] = True
            args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
        if len(args['text'].split('#')) > 7:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."

def check_password(args):
    ''' This function checks if the person who sent this message sent a valid password.
    The password to use is saved in localsettings'''
    the_expected_password = getattr(settings,'PASSWORD','')
    the_sent_password = args['text'].split('#')[1]

    #Let'check if the sent password equals to the expected one
    if the_sent_password == the_expected_password:
        args['valide'] = True
        args['info_to_contact'] = "Le mot de passe envoye est correct."
    else:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Le mot de passe envoye n est pas correct."

def check_commune(args):
    ''' This function checks if the commune is well written
    Names of communes can not made by any caracter not a letter and _ or -'''

    expression = r'[.~!@#$%^&*()=\|]'

    the_sent_commune_name = args['text'].split('#')[2]
    if re.search(expression, the_sent_commune_name):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Le nom de la commune ne peut etre compose que par de lettres, '_' et '-' ."
    elif Commune.objects.filter(name__iexact=the_sent_commune_name).exists():
        args['valide'] = True
        args['info_to_contact'] = "Le nom de la commune est bien ecrit."
    else:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Le nom de la commune n existe pas."

    return args



def check_colline(args):
    ''' This function checks if the colline is well written
    Names of colline can not made by any caracter not a letter and _ or -'''

    expression = r'[.~!@#$%^&*()=\|]'

    the_sent_colline_name = args['text'].split('#')[3]

    if re.search(expression, the_sent_colline_name):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Le nom de la colline ne peut etre compose que par de lettres, '_' et '-' ."
    elif Colline.objects.filter(name__iexact=the_sent_colline_name).exists():
        args['valide'] = True
        args['info_to_contact'] = "Le nom de la colline est bien ecrit."
    else:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Le nom de la colline n existe pas."


def check_phone(args):
    ''' This function cheks if the phone number is well written and the register is not registering himself'''

    if args['phone'].replace("+257", "") in args['text'] :
        args['valide'] = (args['valide'] and False)
        args['info_to_contact'] = "Erreur. Vous ne pouvez pas vous enregistrer vous meme"
        return args

    contact_phone_numbers = args['text'].split('#')[4:-1]
    for contact_phone_number in contact_phone_numbers:
        contact_phone_number_no_space = contact_phone_number.replace(" ", "")
        expression = r'^(\+?(257)?)((62)|(79)|(71)|(76)|(75)|(72)|(61)|(69)|(68))([0-9]{6})$'
        print(contact_phone_number_no_space)
        if re.search(expression, contact_phone_number_no_space) is None:
            #The phone number is not well written
            args['valide'] = (args['valide'] and False)
            args['info_to_contact'] = "Erreur. Le numero de telephone envoye n est pas bien ecrit."
        elif PhoneModel.objects.filter(number='+257'+contact_phone_number_no_space).count() > 0:
            args['valide'] = (args['valide'] and False)
            args['info_to_contact'] = "Erreur. Le numero de telephone existe deja pour un autre groupe."
        else:
            args['valide'] = (args['valide'] and True)
            args['info_to_contact'] = "Le numero de telephone du superviseur est bien ecrit."

def check_report_day(args):
    ''' This function checks if the day on wich this new group will report is valid '''
    expression = r'^[1-7]{1}$'

    #Reporting_day is the day on which the group whose contact is in process of being registered reports
    reporting_day =	args['text'].split('#')[-1]

    if re.search(expression, reporting_day) is None:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Le jour de rapportage indique n est pas correct."
    else:
        args['valide'] = True
        args['info_to_contact'] = "Le jour de rapportage indique est correct."

def record_reporter(args):
    #Let's check if the message sent is composed by an expected number of values
    check_number_of_values(args)
    if not args['valide']:
        return args

    #Let's check if this person sent a valid password
    check_password(args)
    if not args['valide']:
        return args

    #Let's check if this person sent a valid commune name
    check_commune(args)
    if not args['valide']:
        return args
    #Let's check if this person sent a valid colline name
    check_colline(args)
    if not args['valide']:
        return args
    #Let's check if this person sent a valid phone number
    check_phone(args)
    if not args['valide']:
        return args

    #Let's check if this person sent a valid reporting day
    check_report_day(args)
    if not args['valide']:
        return args
    the_commune = args['text'].split('#')[2].title()
    the_colline = args['text'].split('#')[3].title()
    the_meetting_day = args['text'].split('#')[-1]
    colline = get_or_none(Colline, name=the_colline, commune__name=the_commune)
    if colline :
        the_concerned_group, created = Temporaly.objects.get_or_create(colline=colline)
        the_concerned_group = the_concerned_group
        the_concerned_group.day_of_meeting = the_meetting_day
        the_concerned_group.text = args['text']
        the_concerned_group.save()
        args['info_to_contact'] = 'Confirmer le(s) numero de telephone'
        return args


    else:
        args['Ok'] = False
        args['valide'] = False
        args['info_to_contact'] = "La colline {0} de la commune {1} n exite pas.".format(the_colline, the_commune)


def group_confirm(args):
    contact_phone_numbers = args['text'].split('#')
    for contact_phone_number in contact_phone_numbers:
        contact_phone_number_no_space = contact_phone_number.replace(" ", "")
        expression = r'^(\+?(257)?)((62)|(79)|(71)|(76)|(75)|(72)|(61)|(69))([0-9]{6})$'
        print(contact_phone_number_no_space)
        if re.search(expression, contact_phone_number_no_space) is None:
            #The phone number is not well written
            args['valide'] = (args['valide'] and False)
            args['info_to_contact'] = "Erreur. Le numero de telephone envoye n est pas bien ecrit. Recommencez."
            return args

    temp = get_or_none(Temporaly, text__icontains=args['text'])
    #Let's check if this person sent a valid phone number
    if not temp:
        return {'Ok': False, 'info_to_contact': 'Vous avez envoye un different numero. Recommencez.', 'valide': False}
    else:
        the_colline = temp.colline
        the_commune = temp.colline.commune
        the_meetting_day = temp.day_of_meeting
        the_concerned_group , created= NawenuzeGroup.objects.get_or_create(colline=temp.colline, day_of_meeting=temp.day_of_meeting, lamps_in_stock=temp.lamps_in_stock, cost_lamp=temp.cost_lamp, cost_recharge=temp.cost_recharge)
        the_concerned_group.save()
        temp.delete()
        args['valide'] = True
        args['info_to_contact'] = "Tu as enregistres le groupe {0} dans la commune {1} pour donner les rapports tous les {2}.".format(the_colline, the_commune, days[int(the_meetting_day)])
        numbers = []
        for the_phone_number in args['text'].split('#'):
            the_phone_number = the_phone_number.replace(" ", "")
            if len(the_phone_number) == 8:
                the_phone_number = "+257"+the_phone_number
            if len(the_phone_number) == 11:
                the_phone_number = "+"+the_phone_number

            the_phone_object, created = PhoneModel.objects.get_or_create(number = the_phone_number, group = the_concerned_group)
            numbers.append(the_phone_number)

        url = "https://app.rapidpro.io/api/v1/broadcasts.json"
        for i in numbers:
            print 'envoi a %s' % (i)
            the_message_to_send = "Tu as ete enregistres comme rapporteur du groupe {0} dans la commune {1}. Nous attendons les rapports tous les {2}".format(the_colline, the_commune, days[int(the_meetting_day)])
            data = {"urns": ['tel:' + i],"text": the_message_to_send}
            requests.post(url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % settings.TOKEN}, data = json.dumps(data))
        args['envoye'] = the_message_to_send
        return args