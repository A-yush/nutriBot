from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from pprint import pprint
import requests,urllib3,json,re
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

PAGE_ACCESS_TOKEN="YOUR_PAGE_TOKEN"
VERIFY_TOKEN="654321"
list_data=[]

class nutriView(generic.View):
	def get(self,request,*args,**kwargs):
		if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error,Invalid Token')

	@method_decorator(csrf_exempt)
	def dispatch(self,request,*args,**kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)


	def post(self,request,*args,**kwargs):
		# Converts the text payload into a python dictionary
		incoming_mssgs=json.loads(self.request.body.decode('utf-8'))
		# Facebook recommends going through every entry since they might send
        	# multiple messages in a single call during high load
		for entry in incoming_mssgs['entry']:
			for message in entry['messaging']:
			# Check to make sure the received call is a message call
                	# This might be delivery, optin, postback for other events
				if 'message' in message:
					pprint(message)
					post_facebook_msg(message['sender']['id'],message['message']['text'])
			return HttpResponse()

def post_facebook_msg(fbid,received_message):
	tokens=re.sub(r"[^a-zA-Z0-9\s]",' ',received_message).lower().split()
	count=0
	for token in tokens:
		list1=['hy','hello','sup','hola','hey','heya']
		if token in list1:
			nutri_text="hi I am nutri bot. Type the name of the product you want to see."
			post_response_message(fbid,nutri_text)
			break
		else:
			received_message=received_message.replace(" ","%20")
			nutriData(received_message)
			for i in range(0,len(list_data)):
				count+=1
				if count >4:
					break
				nutri_text=list_data[i]
				print(nutri_text)
				post_response_message(fbid,nutri_text)
			del list_data[:]

def post_response_message(fbid,nutri_text):
		post_msg_url='https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
		response_msg=json.dumps({"recipient":{"id":fbid},"message":{"text":nutri_text}})
		status=requests.post(post_msg_url,headers={"content-Type":"application/json"},data=response_msg)

#function to handle nutrition api
def nutriData(name):
	front_main_api='https://api.nutritionix.com/v1_1/search/'
	back_main_api='?results=0%3A7&cal_min=0&cal_max=50000&fields=*&appId=APP_IDd&appKey=APP_KEY'
	URL=front_main_api+name+back_main_api
	#print(URL)

	JSON_OBJ=requests.get(URL).json()
	for each in JSON_OBJ['hits']:
		brand_name=each['fields']['brand_name']
		item_name=each['fields']['item_name']
		calories=each['fields']['nf_calories']
		fat=each['fields']['nf_total_fat']
		cholestrol=each['fields']['nf_cholesterol']
		itemData="Brand Name: "+brand_name+"\n Item Name: "+item_name+"\n Calories: "+str(calories)+"\n fat: "+str(fat)+"\n Cholestrol: "+str(cholestrol)
		list_data.append(itemData)







		
	 
