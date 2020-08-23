import streamlit as st
import pandas as pd
from pandas.io.json import json_normalize
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import json
import math


st.title('Skill analyzer')

dashboard = st.sidebar.selectbox(
    "Select dashboard:",
    ("Inprogress vs open", "Gantt", "Advanced Gantt")
)

filterType = st.sidebar.multiselect(
     'Add Filter on',
     ['order', 'mainProcess', 'machineGroup', 'projectName', 'item'],
     ['order'])

with open('./doneByUserJuly.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df['createdAt'] = json_normalize(df['meta']) 

df = df.sort_values(by=['createdAt'])

if dashboard == 'Gantt':
    typeOfTime = st.radio(
         "Inprogress or Open Time",
         ('open', 'inprogress'))

if dashboard == 'Inprogress vs open':
   colorOnType = st.radio(
         "Color of bubble on:",
         ('machineGroup', 'projectName', 'mainProcess', 'item', 'order'))


range = st.slider(
     "Only show shift with value higher than [m]:", 0, 50, 5)


dataOrderTasks = df.groupby(['order']).size()
dataOrderTasks = json.loads(dataOrderTasks.sort_values().to_json(orient='table'))
dataOrderTasks = [order['order'] for order in dataOrderTasks['data']]
dataOrderTasks.reverse()

dataMainProcessFilter = df['mainProcess'].unique()
datamachineGroupFilter = df['machineGroup'].unique()
dataProjectNameFilter = df['projectName'].unique()
dataItemFilter = df['item'].unique()

aph150 = df

if 'order' in filterType:
  orderFilter = st.selectbox('Select an order:', dataOrderTasks)
  aph150 =  aph150[aph150.order.isin([orderFilter])]

if 'mainProcess' in filterType:
  mainProcessFilter = st.selectbox('Select a mainProcess: ', dataMainProcessFilter)
  aph150 =  aph150[aph150.mainProcess.isin([mainProcessFilter])]

if 'machineGroup' in filterType:
  machineGroupFilter = st.selectbox('Select a machineGroup: ', datamachineGroupFilter)
  aph150 =  aph150[aph150.machineGroup.isin([machineGroupFilter])]

if 'projectName' in filterType:
  projectNameFilter = st.selectbox('Select a projectName: ', dataProjectNameFilter)
  aph150 =  aph150[aph150.projectName.isin([projectNameFilter])]

if 'item' in filterType:
  itemFilter = st.selectbox('Select an item: ', dataItemFilter)
  aph150 =  aph150[aph150.item.isin([itemFilter])]


###########
## LOGIC ##
###########

if dashboard == 'Gantt':
  split_by_open_inprogress = []
  color_scale = ["#1a9850", "#66bd63", "#a6d96a", "#d9ef8b", "#ffffbf", "#fee08b", "#fdae61", "#f46d43", "#d73027"]


  res = aph150.groupby(['key', 'roleName', 'shiftDay', 'shiftNumber'])['inprogress'].agg(['sum', 'count'])
  resOpen = aph150.groupby(['key', 'roleName', 'shiftDay', 'shiftNumber'])[typeOfTime].agg(['mean'])

  highestVal = resOpen['mean'].max() / 60


  resOpen = json.loads(resOpen.to_json(orient='table'))
  res = json.loads(res.to_json(orient='table'))



  res = res['data']
  resOpen = resOpen['data']


  resOpenMap = dict([(f"{resOpenShift['key']}_{resOpenShift['roleName']}", resOpenShift) for resOpenShift in resOpen])
  percentUsed = []

  for i, shift in enumerate(res):
      percentUsed.append(((shift['sum'] / 60) / (8 * 60)) + 4)
      shiftStart = "06:00" if shift['shiftNumber'] == 1 else "14:00" if shift['shiftNumber'] == 2 else "22:00"
    
                    
      #shiftEnd = datetime.strptime(shiftStart, '%H:%M') + timedelta(hours=int((shift['sum'] / 3600)), minutes=shift['sum'] % 60)
      shiftEnd = datetime.strptime(shiftStart, '%H:%M') + timedelta(hours=int(8), minutes=0)
    
      shiftStart = datetime.strptime(shiftStart, '%H:%M')
      res[i]['isInNewDay'] = shiftStart.date() == shiftEnd.date()
      res[i]['shiftEndDate'] = shiftEnd
      res[i]['shiftStartDate'] = shiftStart

      shiftDay = datetime.strptime(shift['shiftDay'], '%Y-%m-%d') + timedelta(days=1) if shiftStart.date() != shiftEnd.date() else datetime.strptime(shift['shiftDay'], '%Y-%m-%d')
      shiftDay = datetime.strftime(shiftDay, '%Y-%m-%d')    

      shiftEnd = datetime.strftime(shiftEnd, '%H:%M')
      shiftStart = datetime.strftime(shiftStart, '%H:%M')

      res[i]['startDate'] = f"{shift['shiftDay']}T{shiftStart}"
      res[i]['endDate'] = f"{shiftDay}T{shiftEnd}"
      res[i]['endProgressTime'] = f"{int(shift['sum'] / 3600):02d}:{shift['sum'] % 60}"
      res[i][typeOfTime] = (resOpenMap[f"{shift['key']}_{shift['roleName']}"]['mean']) / 60
      res[i]['roleName'] = ''.join(res[i]['roleName'].split('BRU - ')[1:])

  valGreen = 3 / highestVal
  valOrange = 5 / highestVal
  valRed = 8 / highestVal
  
  res = [shift for shift in res if shift[typeOfTime] > range]

  fig = px.timeline(res, x_start="startDate",  x_end="endDate", y="roleName", color=typeOfTime, color_continuous_scale=[(0, "green"), (valOrange, "orange"), (valRed, "red"), (1, 'red')])
  fig.update_yaxes(autorange="reversed")
elif dashboard == 'Advanced Gantt':
  aph150Open = aph150.groupby(['key', 'roleName', 'projectName', 'shiftDay'])['open'].agg(['mean'])
  highestVal = aph150Open['mean'].max() / 60
  

  aph150inprogress = aph150.groupby(['key', 'roleName', 'projectName', 'shiftDay'])['inprogress'].agg(['mean'])

  aph150Open = json.loads(aph150Open.to_json(orient='table'))
  aph150inprogress = json.loads(aph150inprogress.to_json(orient='table'))
   
  aph150Open = aph150Open['data']
  aph150inprogress = aph150inprogress['data']


  valGreen = 3 / highestVal
  valOrange = 5 / highestVal
  valRed = 8 / highestVal


  aph150inprogressMap = dict([(f"{aph150inprogressShift['key']}_{aph150inprogressShift['roleName']}", aph150inprogressShift) for aph150inprogressShift in aph150inprogress])

  for i, shift in enumerate(aph150Open):
      aph150Open[i]['meanInProgressMin'] = (aph150inprogressMap[f"{shift['key']}_{shift['roleName']}"]['mean']) / 60
      aph150Open[i]['meanOpenMin'] = shift['mean'] / 60

  aph150Open = [shift for shift in aph150Open if shift['meanInProgressMin'] > range and shift['meanOpenMin'] > range]
                                                              
  fig = px.scatter(aph150Open, x="shiftDay", y="roleName", color="meanOpenMin", size='meanInProgressMin', color_continuous_scale=[(0, "green"), (valOrange, "orange"), (valRed, "red"), (1, 'red')]#, hover_data=['petal_width']
                )
  fig.update_yaxes(autorange="reversed")
elif dashboard == 'Inprogress vs open':
  aph150Open = aph150.groupby(['key', 'roleName', colorOnType])['open'].agg(['mean'])
  amountTasks = aph150.groupby(['key', 'roleName', colorOnType]).size()
  aph150inprogress = aph150.groupby(['key', 'roleName', colorOnType])['inprogress'].agg(['mean'])

  aph150Open = json.loads(aph150Open.to_json(orient='table'))
  amountTasks = json.loads(amountTasks.to_json(orient='table'))
  aph150inprogress = json.loads(aph150inprogress.to_json(orient='table'))

  aph150Open = aph150Open['data']
  amountTasks = amountTasks['data']
  aph150inprogress = aph150inprogress['data']


  aph150inprogressMap = dict([(f"{aph150inprogressShift['key']}_{aph150inprogressShift['roleName']}", aph150inprogressShift) for aph150inprogressShift in aph150inprogress])
  amountTasksMap = dict([(f"{amountTasksShift['key']}_{amountTasksShift['roleName']}", amountTasksShift) for amountTasksShift in amountTasks])

  for i, shift in enumerate(aph150Open):
      aph150Open[i]['meanInProgressMin'] = (aph150inprogressMap[f"{shift['key']}_{shift['roleName']}"]['mean']) / 60
      aph150Open[i]['meanOpenMin'] = shift['mean'] / 60
      aph150Open[i]['amountTasks'] = (amountTasksMap[f"{shift['key']}_{shift['roleName']}"]['values'])

  aph150Open = [shift for shift in aph150Open if shift['meanInProgressMin'] > range and shift['meanOpenMin'] > range]

  fig = px.scatter(aph150Open, x="meanOpenMin", y="meanInProgressMin", color=colorOnType, size='amountTasks'
                   , hover_data=['roleName', 'key']
  )

  fig.update_xaxes(rangemode="tozero")
  fig.update_yaxes(rangemode="tozero")


st.plotly_chart(fig)


#st.write(df[['machineGroup', 'machineId', 'doneAt', 'createdAt', 'acceptedAt', 'open']])

