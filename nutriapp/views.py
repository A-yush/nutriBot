from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from pprint import pprint
import requests,urllib3,json,re
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

PAGE_ACCESS_TOKEN="EAAEnu2J7KlQBAB23Lgz3VNZCUVPCt3DfRcbreTuIwZARNgwq38ZAejRjIc28ZAZAFe4fUTuogSNBX1tHujCcFLpAqWFoHtgVQJ8kzH2kYTA2pORx4nGZBAMyhPIU6DLGZCfAOkQBPrnan6nl5apsMh0Q9I0a7iq06ADJQkmYMKlvgZDZD"
VERIFY_TOKEN="654321"

class nutriView(generic.View):
	name="taco"

	def get(self,request,*args,**kwargs):
		if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error,Invalid Token')

	@method_decorator(csrf_exempt)
	def dispatch(self,request,*args,**kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)


	def post(self,request,*args,**kwargs):
		incoming_mssgs=json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_mssgs['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					pprint(message)
					post_facebook_msg(message['sender']['id'],message['message']['text'])
			return HttpResponse()

def post_facebook_msg(fbid,received_message):
	tokens=re.sub(r"[^a-zA-Z0-9\s]",' ',received_message).lower().split()
	for token in tokens:
		list1=['hy','hello','sup','hola']
		if token in list1:
			nutri_text="hi I am nutri bot. Type the name of the product you want to see."
			break
		else:
			nutri_text=nutriData(token)
			print(nutri_text)
	post_response_message(fbid,nutri_text)

def post_response_message(fbid,nutri_text):
		post_msg_url='https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
		response_msg=json.dumps({"recipient":{"id":fbid},"message":{"text":nutri_text}})
		status=requests.post(post_msg_url,headers={"content-Type":"application/json"},data=response_msg)

#function to handle nutrition api
def nutriData(name):
	front_main_api='https://api.nutritionix.com/v1_1/search/'
	back_main_api='?results=0%3A20&cal_min=0&cal_max=50000&fields=item_name%2Cbrand_name%2Citem_id%2Cbrand_id&appId=71e7277d&appKey=b9c6e8d9b38f67926271245d3b352c38'
	URL=front_main_api+name+back_main_api
	#print(URL)

	JSON_OBJ=requests.get(URL).json()
	for each in JSON_OBJ['hits']:
		brand_name=each['fields']['brand_name']
		item_name=each['fields']['item_name']
		itemData=brand_name+"\n"+item_name
		return itemdata






#view=nutriView()
#print(view.nutriData("butter"))





		
	 
