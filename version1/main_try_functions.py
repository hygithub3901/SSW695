from functions import *
from flask import json
from datetime import datetime
from api import  app


response = app.test_client().post(
'/serach_food_result/hy@zhang.com', 
data=json.dumps({
     
        "keywords":"b"
    
}),
content_type='application/json',
)
data = response.get_data(as_text=True)
print(json.loads(data))