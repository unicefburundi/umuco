from django.conf import settings
import re
from models import *

def check_number_of_values(args):
	#This function checks if the message sent is composed by an expected number of values
	print("==len(args['text'].split(' '))==")
	print(len(args['text'].split(' ')))
	print(args['text'].split(' '))
	if(args['message_type']=='PHONE_REGISTRATION'):
		if len(args['text'].split('#')) < 6:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split('#')) > 6:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
		if len(args['text'].split('#')) == 6:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."

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

	expression = r'[.~!@#$%^&*()=\|/0-9]'

	the_sent_commune_name = args['text'].split('#')[2]
	
	if re.search(expression, the_sent_commune_name):
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le nom de la commune ne peut etre compose que par de lettres, '_' et '-' ."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le nom de la commune est bien ecrit."


def check_colline(args):
	''' This function checks if the colline is well written 
	Names of colline can not made by any caracter not a letter and _ or -'''

	expression = r'[.~!@#$%^&*()=\|/0-9]'

	the_sent_colline_name = args['text'].split('#')[3]
	
	if re.search(expression, the_sent_colline_name):
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le nom de la colline ne peut etre compose que par de lettres, '_' et '-' ."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le nom de la colline est bien ecrit."


def check_phone(args):
	''' This function cheks if the phone number is well written '''
	contact_phone_number = args['text'].split('#')[4]
	contact_phone_number_no_space = contact_phone_number.replace(" ", "")
	expression = r'^(\+?(257)?)((62)|(79)|(71)|(76)|(75)|(72))([0-9]{6})$'
	print(contact_phone_number_no_space)
	if re.search(expression, contact_phone_number_no_space) is None:
		#The phone number is not well written
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le numero de telephone envoye n est pas bien ecrit."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien ecrit."

def check_report_day(args):
	''' This function checks if the day on wich this new group will report is valid '''
	expression = r'^[1-7]{1}$'

	#Reporting_day is the day on which the group whose contact is in process of being registered reports
	reporting_day =	args['text'].split('#')[5]

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
		return

	#Let's check if this person sent a valid password
	check_password(args)
	if not args['valide']:
		return

	#Let's check if this person sent a valid commune name
	check_commune(args)
	if not args['valide']:
		return

	#Let's check if this person sent a valid colline name
	check_colline(args)
	if not args['valide']:
		return

	#Let's check if this person sent a valid phone number
	check_phone(args)
	if not args['valide']:
		return

	#Let's check if this person sent a valid reporting day
	check_report_day(args)
	if not args['valide']:
		return

	the_commune = args['text'].split('#')[2].upper()
	the_colline = args['text'].split('#')[3].upper()
	the_phone_number = args['text'].split('#')[4]
	the_meetting_day = args['text'].split('#')[5]

	the_phone_number = the_phone_number.replace(" ", "")
	if len(the_phone_number) == 8:
		the_phone_number = "+257"+the_phone_number
	if len(the_phone_number) == 11:
		the_phone_number = "+"+the_phone_number

	the_concerned_group = NawenuzeGroup.objects.get_or_create(commune = the_commune, colline = the_colline)
	the_concerned_group = the_concerned_group[0]
	the_concerned_group.day_of_meeting = the_meetting_day
	the_concerned_group.save()

	the_phone_object = PhoneModel.objects.get_or_create(number = the_phone_number, group = the_concerned_group)

	args['valide'] = True
	args['info_to_contact'] = "Bien fait."
	
