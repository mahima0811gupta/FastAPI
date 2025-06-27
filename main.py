from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal

import json

app=FastAPI()    

class Patient(BaseModel):
     id:Annotated[str,Field(...,description='ID of the patient')]
     name:Annotated[str,Field(...,description='Name of the patient')]
     city:Annotated[str,Field(...,description='City where the patient is living')]
     age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the Patient')]
     gender:Annotated[Literal['male','female','others'],Field(...,description='Gender of the patient')]
     height:Annotated[float,Field(...,gt=0,description='Height of the Patient in mt')]
     weight:Annotated[float,Field(...,gt=0,description='Weight of the Patient in kg')]

     @computed_field
     @property
     def bmi(self)->float:
           return round(self.weight / (self.height ** 2), 2)
           return bmi
          

     @computed_field
     @property
     def verdict(self)->str:
          
          if self.bmi<18.5:
               return 'Underweight'
          elif self.bmi<25:
               return 'Normal'
          elif self.bmi<30:
               return 'Normal'
          else:
               return 'Obese'
               


        

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data   


def sava_data(data):
         with open('patients.json','w') as f:
              json.dump(data,f)

@app.get("/")
def hello():
    return{'message':'Patient Management System API'}


@app.get('/about')
def about():
    return {'message':'A fully functional API to manage your patient records'}


@app.get('/view')
def view():
    data=load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='Id of the patient in DB')):
#load all the patients
    data=load_data()

    if patient_id in data:
     return data[patient_id]

    raise HTTPException(status_code=404,detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by:str= Query(...,description='Sort on the basis of height,weight or bmi'),order:str=Query('asc',description='sort in asc or desc order')):

    valid_field=['height','weight','bmi']

    if sort_by not in valid_field:
        return HTTPException(status_code=404,detail='invalid_field select from {valid_field}')
    
    if order not in ['asc','desc']:
                      return HTTPException(status_code=404,detail='invalid order select between asc and desc')
    
    data=load_data()

    sort_order=True if order=='desc' else False

    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data


@app.post('/create')

def create_patient(patient:Patient):
     #load exiting data
    data=load_data()

     #check if already exist
    if patient.id in data:
         raise HTTPException(status_code=400,detail='patient already exists')
    
    #new patient add to the dataBASE
    #for this fisrt convert the pydantic data into dictionary
    data[patient.id]=patient.model_dump(exclude=['id'])
  

    #save into json file
    sava_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})



    

    



