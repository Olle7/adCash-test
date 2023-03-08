import requests

# The API endpoint
url="http://127.0.0.1:5000/response_to_application"

# POST
#print(requests.post(url,{"amount":"100","currency":"100","term":"100","name":"100","personal_ID":"100","contact":"100","type_of_contact":"100","comment":"100"}))

#GET
#print(requests.get(url+"?amount=&contact=GETT&currency=CUR&comment=YYY&term=ttt&name=olger&personal_ID=123&type_of_contact=gsm"))

#GET+POST overlapping params
#print(requests.post(url+"?amount=111&contact=Gmail&currency=GCUR&comment=YYY&term=ttt&name=olger&personal_ID=123&type_of_contact=gsm",{"amount":"982","currency":"100","term":"100","name":"100","personal_ID":"100","contact":"100","type_of_contact":"100","comment":"100"}))

#GET+POST not overlapping params
print(requests.post(url+"?amount=111&contact=Gmail&currency=GCUR",{"term":"100","name":"100","personal_ID":"100","type_of_contact":"100","comment":"100"}))