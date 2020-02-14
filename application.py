#Importing necessary libraries
import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_auth
import dash_table
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime 

dash_app = dash.Dash(__name__)  #creating a dash object

app = dash_app.server  


dash_app.config.suppress_callback_exceptions = True  #For not triggering the exceptions

dash_app.layout = html.Div(children = [
    html.Div(" "),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#Main Page / Home page of the websote
index_page =   html.Div(children = [
                  html.Div(className="header", children = [
    	    	html.Div(className="logo", children = [
		   html.Img(src= '/assets/ERM_Logo.png')
		]),
		html.Div(className="banner",children = [
		   html.H1("Dynamic Crash Prevention Solution")
		]),
 		html.Div(className="header-images",children = [
		   html.Div(className="header-image1",children = [
 			html.Img(src= '/assets/DCP_Img_1.jpg',width=250,height=75)
		   ]),
		   html.Div(className="header-image2",children = [
 			html.Img(src= '/assets/DCP_Img_2.jpg',width=250,height=75)
		   ]),
		   html.Div(className="header-image3",children = [
 			html.Img(src= '/assets/DCP_Img_3.jpg',width=250,height=75)
		   ])
		])
           
             
]),
html.Div(className = "bg",children = [
 html.Div(className = "mp-route-option", children = [
                html.Div(className="mp-upper-part",children = [
                     html.Div(className="mp-route1-img",children = [
			  html.Div("Jamnagar to Rajkot",style={'background-color':'Dark Green','color':'White'}),
                          dcc.Link(html.Img(src = "/assets/Jam_Rajkot.png",width=800,height=300),href = "/JRK")
                     ]),
                     html.Div(className="mp-route2-img",children = [
       	    		  html.Div("Jamnagar to Naghedi",style={'background-color':'Dark Green','color':'White'}),
                          html.A(html.Img(src = "/assets/Jamnagar_Naghedi.png",width=800,height=300),href = "/JNG")
                     ]),
                     html.Div(className="mp-route3-img",children = [
			  html.Div("Vadodra IOCL to Vemali Vadodra",style={'background-color':'Dark Green','color':'White'}),
                          dcc.Link(html.Img(src = "/assets/Vadodra_Internal.png",width=800,height=300),href = "/Sample")
                     ]),
                     html.Div(className="mp-route4-img",children = [
			  html.Div("Vadodra to Rajkot",style={'background-color':'Dark Green','color':'White'}),
                          dcc.Link(html.Img(src = "/assets/Vadodra_Rajkot.png",width=800,height=300),href = "/")
                     ])
                ])
          ])
])
])


@dash_app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/JNG':  #if url is observations then render the layout of Safety Observations
        return real_time_layout
    else:
        return index_page 

real_time_layout =  html.Div(children = [ 
					  
                      #html.Button("Show Graph",id = "Show Graph"),
					  
					  html.Div(id = "Page_Load",children = [html.Img(src = "/assets/page-loading-gif-14.gif", style = {'margin-left': 'auto', 'margin-right': 'auto','display':'block','width':'40%' })] ),
                      html.Div(className="row",children = [
					  html.Div(className = "column", children = [
					  dcc.Interval(
						id='interval-component',
						interval=2*1000, # in milliseconds
						n_intervals=0
						),
					  html.Div(className = "column middle",children = [dcc.Graph(id="Scatterplotmap",figure={'layout': { 'clickmode': 'event+select'}})]),
					  html.Div(className = "column side",children = [
							html.Div(className="table_space",id="show_message"),
							html.Div(className="driver_info", children = [
							html.Div(id="Driver_UI"),
							html.Div(id = "Alert Message",style={'color':'white'}),
							html.Div(id = "Alarm Message",style={'color':'white'}),
							])
						])
					])
					]),
					
					dcc.Graph(id="Route_Map",figure={'layout': { 'clickmode': 'event+select'}},style = {'display':'none'}),
					
					dcc.Graph(id="Telemetry_Alerts_Track",figure={'layout': { 'clickmode': 'event+select'}}, style = {'display':'none'}),
					dcc.Graph(id="OBC_Alerts_Track",figure={'layout': { 'clickmode': 'event+select'}},style = {'display':'none'}),
					html.Div("Video Track",id = "OBC_Video")
					

])


@dash_app.callback(
    dash.dependencies.Output('Page_Load', 'style'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])

def real_time_map(n):
    if n>2: 
        return {'display':'none'}
					

@dash_app.callback(
    dash.dependencies.Output('Scatterplotmap', 'style'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])

def real_time_map(n):
    if n>2: 
        return {'display':'block','height':'900px'}
    else: 
        return {'display':'none'}
					
#Reading csv file
route_data= pd.read_csv("Trip_Data_v1.csv")
alerts_data= pd.read_csv("Alerts_Data.csv")

@dash_app.callback(
  	dash.dependencies.Output('Scatterplotmap', 'figure'),
    	[dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(n):
	if n>-1:
		key_api = "pk.eyJ1IjoiYWRpdHlhdGFvcmkiLCJhIjoiY2s1NTMzM205MGJyNjNla2JxZDRxdHBvdiJ9.OmOHzC_AyvWfjv9Sulz3tw"
		mapbox_access_token = key_api
		#For moving the vehicle
		current_pos = route_data[route_data["Time Interval"]==n+1]
		
		#to find unique number of drivers
		unique_drivers = current_pos["Driver ID"].unique()
		num_drivers = len(unique_drivers)
		mutiple_markers = ["bus"]*num_drivers
		text_str = []
		text_mar = []
		driver_custom_data = []
		for dc in range(0,num_drivers):
			ind_driver_id= unique_drivers[dc]
			ind_customer_data = str(n) +"_"+ str(ind_driver_id)
			driver_custom_data.append(ind_customer_data)
		for nd in range(0,num_drivers):
			ind_driver = current_pos["Driver Name"].iloc[nd]
			ind_vehicle = current_pos["Vehicle Number"].iloc[nd]
			ind_risk_rating = current_pos["Risk Rating"].iloc[nd]
			ind_driving_hrs = current_pos["Duty Hours Completed"].iloc[nd]
			ind_overspeed = current_pos["Overspeeding"].iloc[nd]
			ind_lane_violations = current_pos["Lane Violations"].iloc[nd]
			ind_ha = current_pos["Harsh Accelaration"].iloc[nd]
			ind_hb = current_pos["Harsh Braking"].iloc[nd]
			ind_hc = current_pos["Harsh Cornering"].iloc[nd]
			ind_distr = current_pos["Distractions "].iloc[nd]
			ind_yawn = current_pos["Yawning"].iloc[nd]
			
			ind_str_text = "Driver Name: "+ind_driver+"<br>Vehicle Number:"+ind_vehicle+"<br>Risk Rating: "+str(ind_risk_rating)+"<br> Continuous Driving Hours"+str(ind_driving_hrs)+"<br>Overspeeding: "+str(ind_overspeed)+"<br>Lane Violations: "+str(ind_lane_violations)+"<br>Harsh Accelaration: "+str(ind_ha)+"<br>Harsh Braking: "+str(ind_hb)+"<br>Harsh Cornering: "+str(ind_hc)+"<br>Distractions: "+str(ind_distr)+"<br>Yawning: "+str(ind_yawn)
			
			text_str.append(ind_str_text)
			text_mar.append(ind_vehicle)	
		
		#print(current_pos)
		weight = current_pos["RI_Driver"]
		#For plotting a route the vehicle follows 
		line_route = route_data[route_data["Time Interval"].isin(range(1,n))]
		#print(line_route)
		line_route_lat = line_route.Latitude#Latitudes of route followed till now 
		line_route_lon = line_route.Longitude #Longitudes of route followed till now
		line_route_wt = line_route["RI_Driver"]  
		#Changing the colour on the basis of the risk index
		green_code = 'rgb(0,255,0)'  #For safe
		amber_code = 'rgb(255,191,0)'  #For monitor
		red_code = 'rgb(255,0,0)'  #For take action
		fig = go.Figure()  
		#desired_color = green_code if weight==1 else (amber_code if weight==2 else red_code)
		#print(desired_color)
		overspeeding = current_pos["Overspeeding"].iloc[0]
		driver_name = current_pos["Driver Name"].iloc[0]
		time_int = n
		#cust_list = []
        #cust_list.append(
        #Layer for moving the vehicle in the real time
		fig.add_trace(go.Scattermapbox(
				lat=current_pos.Latitude,
				lon=current_pos.Longitude,
				mode='markers',
				marker=go.scattermapbox.Marker(
					size=18,
					color= weight,
					opacity=0.7,
					cmin = 1,
					cmax = 3,
					cmid = 2,
					colorscale = [[0, 'rgb(0,255,0)'],[0.5,'rgb(255,165,0)'], [1, 'rgb(255,0,0)']]
				),
				text="",
				hoverinfo='text',
				
			))
		
		
		#Layer for showing the color of the icon
		fig.add_trace(go.Scattermapbox(
				lat=current_pos.Latitude,
				lon=current_pos.Longitude,
				mode='markers+text',
				marker = {'size': 14, 'symbol': mutiple_markers,'color':'black'},
				text= text_mar,
				customdata=driver_custom_data,
				hovertext = text_str,
				textposition = "top left",
				textfont = {'color':'#fff'}
				)
			)
		
		 
		
		#Layer for showing the route the vehicle followed till now
		if False: 
			fig.add_trace(go.Scattermapbox(
				lat=line_route_lat,
				lon=line_route_lon,
				mode='lines',
				line = {'width':4,'color':'rgb(255,192,0)'}
				)
				)        
	
		
		

		
		fig.update_layout(
			title={'text':'Jamnagar Route','font':{'color':'white'}},
			autosize=True,
			hovermode='closest',
			showlegend=False,
			mapbox=go.layout.Mapbox(
				accesstoken=mapbox_access_token,
				bearing=0,
				center=go.layout.mapbox.Center(
					lat=current_pos.Latitude.iloc[2],
					lon=current_pos.Longitude.iloc[2]
				),
				pitch=0,
				zoom=11,
				style='dark'
			),
			paper_bgcolor = 'black',
			legend = {'font':{'color':'#fff'}}
		)
		#print(fig)
		return fig

@dash_app.callback(
    dash.dependencies.Output('show_message', 'children'),
    [dash.dependencies.Input('Scatterplotmap', 'clickData')])

def click_processing(clickData):
	if clickData!=None:
		#print("Click Processing")
		#print(clickData)
		X = clickData
		Y = X["points"][0]
		ind_driver_meta = Y['customdata']
		split_op = ind_driver_meta.split("_")
		ind_interval = split_op[0]
		ind_driver_id = split_op[1]
		#print("Interval ID: "+str(ind_interval))
		#print("Driver ID: "+str(ind_driver_id))
		r_int_data = route_data[route_data["Time Interval"]==int(ind_interval)]
		r_index = list(r_int_data.index)
		driver_record =  r_int_data[r_int_data["Driver ID"]==int(ind_driver_id)].index 
		driver_index = r_index.index(driver_record)
		print("driver_index = "+str(driver_index))
		r_int_data["Longitude"] = round(r_int_data["Longitude"],5)
		r_int_data["Latitude"] = round(r_int_data["Latitude"],5)
		
		subset_data = r_int_data[['Driver ID','Driver Name','Vehicle Number','RI_Driver','Duty Hours Completed','Events','Distractions ','Yawning']]
		#print(isinstance(subset_data,pd.DataFrame))
		#print("Subset Data")
		#print(subset_data)
		print("r_int_data")
		print(r_int_data)
		
		#print("r_int = "+str(driver_index))
		return html.Div([ html.Div([html.H1("Real Time Driver Risk Scorecard")],style = {'color':'white','text-align':'center'}),
					dash_table.DataTable(
					id='Driver Details',
					data=subset_data.to_dict('records'),
					columns=[
						{"name": i, "id": i,"selectable":True} for i in subset_data.columns
						],
					row_selectable="single",
					selected_rows = [],
					style_data_conditional=[{
						"if": {"row_index":driver_index},
						"backgroundColor": "rgb(0,255,0)",
						'color': 'white'
		},
		{
			"if": {'column_id':'Yawning',
				   'filter_query':'{Yawning} > 3'},
			'color':'red'
		},
		{
			"if": {'column_id':'Events',
				   'filter_query':'{Events} > 5'},
			'color':'red'
		},
		{
			"if": {'column_id':'RI_Driver',
				   'filter_query':'{RI_Driver}>1'},
			'color':'rgb(255,192,0)'
		},
		{
			"if": {'column_id':'Distractions',
				   'filter_query':'{Distractions} > 4'},
			'color':'red'
		},
		
		],
		style_table={'fontFamily': 'Times New Roman',
					
                    }, 
		style_header = {'backgroundColor':'rgb(30,30,30)','color':'white'},
		style_cell = {'textAlign':'left', 'fontFamily': 'Times New Roman','backgroundColor':'rgb(50,50,50)','color':'white'},
		style_cell_conditional = [
					{'if': {'column_id':'Driver Name'}, 'width':'15%'},
					
		])
		])

@dash_app.callback(
    Output('Driver Details', 'style_data_conditional'),
    [Input('Driver Details', 'selected_rows'),
	Input('Scatterplotmap', 'clickData')]
)
def update_styles(selected_rows,clickData):
	print("Selected Rows")
	print(selected_rows)
	print("sample")
	X = clickData
	Y = X["points"][0]
	ind_driver_meta = Y['customdata']
	split_op = ind_driver_meta.split("_")
	ind_interval = split_op[0]
	ind_driver_id = split_op[1]
	#print("Interval ID: "+str(ind_interval))
	#print("Driver ID: "+str(ind_driver_id))
	r_int_data = route_data[route_data["Time Interval"]==int(ind_interval)]
	r_index = list(r_int_data.index)
	driver_record =  r_int_data[r_int_data["Driver ID"]==int(ind_driver_id)].index 
	driver_index = r_index.index(driver_record)
		
	if len(selected_rows)>0:
		return [{
							"if": {"row_index":selected_rows[0]},
							"backgroundColor": "rgb(0,255,0)",
							'color': 'white'
			},
			{
				"if": {'column_id':'Yawning',
					   'filter_query':'{Yawning} > 3'},
				'color':'red'
			},
			{
				"if": {'column_id':'Events',
					   'filter_query':'{Events} > 5'},
				'color':'red'
			},
			{
				"if": {'column_id':'RI_Driver',
					   'filter_query':'{RI_Driver}>1'},
				'color':'rgb(255,192,0)'
			},
			{
				"if": {'column_id':'Distractions',
					   'filter_query':'{Distractions} > 4'},
				'color':'red'
			} ]
	else:
		return [{
							"if": {"row_index":driver_index},
							"backgroundColor": "rgb(0,255,0)",
							'color': 'white'
			},
			{
				"if": {'column_id':'Yawning',
					   'filter_query':'{Yawning} > 3'},
				'color':'red'
			},
			{
				"if": {'column_id':'Events',
					   'filter_query':'{Events} > 5'},
				'color':'red'
			},
			{
				"if": {'column_id':'RI_Driver',
					   'filter_query':'{RI_Driver}>1'},
				'color':'rgb(255,192,0)'
			},
			{
				"if": {'column_id':'Distractions',
					   'filter_query':'{Distractions} > 4'},
				'color':'red'
			} ]
		
@dash_app.callback( 
	dash.dependencies.Output('Driver_UI','children'),
	[dash.dependencies.Input('Driver Details','derived_virtual_data')
	,dash.dependencies.Input('Driver Details','derived_virtual_selected_rows')])
	
def show_driver_ui(row_data,derived_virtual_selected_rows):
	if derived_virtual_selected_rows ==[]:
		print("Empty")
	else: 
		print("Virtual Data")
		print(row_data)
		print("Selected rows")
		print(derived_virtual_selected_rows)
		selected_driver_row = row_data[derived_virtual_selected_rows[0]]
		print(selected_driver_row)
		d_name = selected_driver_row["Driver Name"]
		veh_num = selected_driver_row["Vehicle Number"]
		d_id = selected_driver_row["Driver ID"]
		
		
		return html.Div([
			html.Br(),
			html.Img(src = dash_app.get_asset_url("Driver_"+str(d_id)+".jpg"), width=256,height = 256),
			html.Br(),
			html.B("Driver Name: "+d_name),
			html.Br(),
			html.B("Vehicle Number:" +veh_num),
			html.Br(),
			html.B("Time:"+str(datetime.now())),
			html.Br(),
			html.B("Temperature: 26 C"),
			html.Br(),
			html.Br(),
			html.Button("Send an ALERT",id="Send Alert",style={'font-size': '20px'}),
			html.Button("Raise an ALARM",id="ALARM",style={'font-size': '20px','float':'right'})
		])

@dash_app.callback(
    dash.dependencies.Output('Telemetry_Alerts_Track', 'style'),
    [dash.dependencies.Input('Driver Details', 'derived_virtual_selected_rows')])

def show_alerts_map(derived_virtual_selected_rows):
    
    if derived_virtual_selected_rows!=[]:
        print("show graph3")
        return {'width':'1900px','height':'500px','display':'block'}
    else:
        return {'display':'none'}


		
@dash_app.callback( 
	dash.dependencies.Output('Telemetry_Alerts_Track','figure'),
	[dash.dependencies.Input('Driver Details','derived_virtual_data'),
	dash.dependencies.Input('Driver Details','derived_virtual_selected_rows')])
	
def alerts_tracking(row_data,derived_virtual_selected_rows):
	
	#print(derived_virtual_selected_rows)
	selected_driver_row = row_data[derived_virtual_selected_rows[0]]
	driver_id = selected_driver_row["Driver ID"]
	print("Driver ID: "+str(driver_id))
	print(alerts_data)
	driver_alerts_data = alerts_data[alerts_data["Driver Id"]==driver_id]
	os_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "AOS"]
	lv_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "ALV"]
	ha_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "AHA"]
	hb_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "AHB"]
	hc_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "AHC"]
	dis_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "AD"]
	yawn_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "AY"]
	print(driver_alerts_data)
	print("OS Alerts Data")
	print(os_alerts_data)
	fig = go.Figure()  
	
	fig.add_trace(go.Scatter(x = driver_alerts_data["Time of Incident"], y = driver_alerts_data["Dummy Axis"],mode='lines',name = "Time of Incident"))
	fig.add_trace(go.Scatter(x = os_alerts_data["Time of Incident"], y = os_alerts_data["Dummy Axis"],mode='markers', name = "Over Speeding", marker= {'size':20}))
	fig.add_trace(go.Scatter(x = lv_alerts_data["Time of Incident"], y = lv_alerts_data["Dummy Axis"],mode='markers', name = "Lane Violations", marker = {'symbol': 'diamond', 'size':20}))
	fig.add_trace(go.Scatter(x = ha_alerts_data["Time of Incident"], y = ha_alerts_data["Dummy Axis"],mode='markers', name = "Harsh Accelaration", marker = {'symbol': 'x','size':20}))	
	fig.add_trace(go.Scatter(x = hb_alerts_data["Time of Incident"], y = hb_alerts_data["Dummy Axis"],mode='markers', name = "Harsh Braking", marker = {'symbol': 'pentagon','size':20}))
	fig.add_trace(go.Scatter(x = hc_alerts_data["Time of Incident"], y = hc_alerts_data["Dummy Axis"],mode='markers', name = "Harsh Cornering", marker = {'symbol': 'star-diamond','size':20}))
	fig.update_layout(
		title = {'text':'Telemetry Alerts','font':{'color':'white'}},
		yaxis ={'visible':False},
		showlegend = True, 
		plot_bgcolor = "black",
		paper_bgcolor = "black",
		xaxis = {'color':"#fff", 'title' : {'text':'Time of Incident'},'showgrid':False},
		legend = {'font':{'color':'#fff'}})
	
	
	return fig

@dash_app.callback(
    dash.dependencies.Output('OBC_Alerts_Track', 'style'),
    [dash.dependencies.Input('Driver Details', 'derived_virtual_selected_rows')])

def show_alerts_map(derived_virtual_selected_rows):
    
    if derived_virtual_selected_rows!=[]:
        print("show graph3")
        return {'width':'1900px','height':'500px','display':'block'}
    else:
        return {'display':'none'}


		
@dash_app.callback( 
	dash.dependencies.Output('OBC_Alerts_Track','figure'),
	[dash.dependencies.Input('Driver Details','derived_virtual_data'),
	dash.dependencies.Input('Driver Details','derived_virtual_selected_rows')])
	
def alerts_tracking(row_data,derived_virtual_selected_rows):
	
	#print(derived_virtual_selected_rows)
	selected_driver_row = row_data[derived_virtual_selected_rows[0]]
	driver_id = selected_driver_row["Driver ID"]
	print("Driver ID: "+str(driver_id))
	print(alerts_data)
	driver_alerts_data = alerts_data[alerts_data["Driver Id"]==driver_id]
	dis_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "AD"]
	yawn_alerts_data = driver_alerts_data[driver_alerts_data["Alert Id"] == "AY"]
	print(driver_alerts_data)
	print("OS Alerts Data")
	#print(os_alerts_data)
	fig = go.Figure()  
	
	fig.add_trace(go.Scatter(x = driver_alerts_data["Time of Incident"], y = driver_alerts_data["Dummy Axis"],mode='lines',name = "Time of Incident"))
	fig.add_trace(go.Scatter(x = dis_alerts_data["Time of Incident"], y = dis_alerts_data["Dummy Axis"],mode='markers', name = "Distractions", marker = {'symbol': 'hexagram','size':20}))
	fig.add_trace(go.Scatter(x = yawn_alerts_data["Time of Incident"], y = yawn_alerts_data["Dummy Axis"],mode='markers',name = "Yawning", marker = {'symbol': 'hourglass','size':20}))
	fig.update_layout(
		title = {'text':'On Board Camera Alerts','font':{'color':'white'}},
		yaxis ={'visible':False},
		showlegend = True, 
		plot_bgcolor = "black",
		paper_bgcolor="black",
		xaxis = {'color':"#fff", 'title' : {'text':'Time of Incident'},'showgrid':False},
		legend = {'font':{'color':'#fff'}})
	
	
	return fig	

@dash_app.callback(
    dash.dependencies.Output('Route_Map', 'style'),
    [dash.dependencies.Input('Scatterplotmap', 'clickData')])

def show_route_map(clickData):
    
    if clickData is not None:
        print("show graph3")
        return {'width':'1900px','height':'900px','display':'block'}
    else:
        return {'display':'none'}   
	
	
@dash_app.callback(
  	dash.dependencies.Output('Route_Map', 'figure'),
    	[dash.dependencies.Input('Scatterplotmap', 'clickData')])
def update_output_2(clickData):
	
	print("Route Map Activated")
	key_api = "pk.eyJ1IjoiYWRpdHlhdGFvcmkiLCJhIjoiY2s1NTMzM205MGJyNjNla2JxZDRxdHBvdiJ9.OmOHzC_AyvWfjv9Sulz3tw"
	mapbox_access_token = key_api
	#For moving the vehicle
	
	X = clickData
	Y = X["points"][0]
	ind_driver_meta = Y['customdata']
	split_op = ind_driver_meta.split("_")
	click_interval = split_op[0]
	click_driver_id = split_op[1]
	current_pos = route_data[route_data["Time Interval"]==int(click_interval)]
	print("current_pos")
	print(current_pos)
	#to find unique number of drivers
	unique_drivers = current_pos["Driver ID"].unique()
	num_drivers = len(unique_drivers)
	mutiple_markers = ["bus"]*num_drivers
	text_str = []
	driver_custom_data = []
	for dc in range(0,num_drivers):
		ind_driver_id= unique_drivers[dc]
		ind_customer_data = str(click_interval) +"_"+ str(ind_driver_id)
		driver_custom_data.append(ind_customer_data)
	for nd in range(0,num_drivers):
		ind_driver = current_pos["Driver Name"].iloc[nd]
		ind_vehicle = current_pos["Vehicle Number"].iloc[nd]
		ind_risk_rating = current_pos["Risk Rating"].iloc[nd]
		ind_driving_hrs = current_pos["Duty Hours Completed"].iloc[nd]
		ind_overspeed = current_pos["Overspeeding"].iloc[nd]
		ind_lane_violations = current_pos["Lane Violations"].iloc[nd]
		ind_ha = current_pos["Harsh Accelaration"].iloc[nd]
		ind_hb = current_pos["Harsh Braking"].iloc[nd]
		ind_hc = current_pos["Harsh Cornering"].iloc[nd]
		ind_distr = current_pos["Distractions "].iloc[nd]
		ind_yawn = current_pos["Yawning"].iloc[nd]
		
		ind_str_text = "Driver Name: "+ind_driver+"<br>Vehicle Number:"+ind_vehicle+"<br>Risk Rating: "+str(ind_risk_rating)+"<br> Continuous Driving Hours"+str(ind_driving_hrs)+"<br>Overspeeding: "+str(ind_overspeed)+"<br>Lane Violations: "+str(ind_lane_violations)+"<br>Harsh Accelaration: "+str(ind_ha)+"<br>Harsh Braking: "+str(ind_hb)+"<br>Harsh Cornering: "+str(ind_hc)+"<br>Distractions: "+str(ind_distr)+"<br>Yawning: "+str(ind_yawn)
		
		text_str.append(ind_str_text)
	weight = current_pos["RI_Driver"]
	#For plotting a route the vehicle follows 
	click_driver_data = route_data[route_data["Driver ID"]==int(click_driver_id)]
	print(click_driver_data)
	click_driver_route = click_driver_data[click_driver_data["Time Interval"].isin(range(1,int(click_interval)))]
	print("Route Map __ Click Driver Route")
	print(click_driver_route)
	line_route_lat = click_driver_route.Latitude
	line_route_lon = click_driver_route.Longitude #Longitudes of route followed till now
	line_route_wt = click_driver_route["RI_Driver"]  
	print("Route Latitude")
	print(line_route_lat)
	#Changing the colour on the basis of the risk index
	green_code = 'rgb(0,255,0)'  #For safe
	amber_code = 'rgb(255,191,0)'  #For monitor
	red_code = 'rgb(255,0,0)'  #For take action
	fig = go.Figure()  
	#desired_color = green_code if weight==1 else (amber_code if weight==2 else red_code)
	#print(desired_color)
	overspeeding = current_pos["Overspeeding"].iloc[0]
	driver_name = current_pos["Driver Name"].iloc[0]
	#time_int = n
	#cust_list = []
	#cust_list.append(
	#Layer for moving the vehicle in the real time
	fig.add_trace(go.Scattermapbox(
			lat=current_pos.Latitude,
			lon=current_pos.Longitude,
			mode='markers',
			marker=go.scattermapbox.Marker(
				size=12,
				color= weight,
				opacity=0.7,
				cmin = 1,
				cmax = 3,
				cmid = 2,
				colorscale = [[0, 'rgb(0,255,0)'],[0.5,'rgb(255,165,0)'], [1, 'rgb(255,0,0)']]
			),
			text="",
			hoverinfo='text',
			
		))
	
	
	#Layer for showing the color of the icon
	fig.add_trace(go.Scattermapbox(
			lat=current_pos.Latitude,
			lon=current_pos.Longitude,
			mode='markers',
			marker = {'size': 10, 'symbol': mutiple_markers,'color':'black'},
			text= text_str,
			customdata=driver_custom_data
			)
		)
	 
		#Layer for showing the route the vehicle followed till now
	if False:
		fig.add_trace(go.Scattermapbox(
		lat=line_route_lat,
		lon=line_route_lon,
		mode='lines',
		line = {'width':4,'color':'rgb(255,192,0)'}
		)
		) 

	fig.add_trace(go.Scattermapbox(
		lat=line_route_lat,
		lon=line_route_lon,
		mode='lines+markers',
		marker=go.scattermapbox.Marker(
				size=12,
				color= line_route_wt,
				opacity=0.7,
				cmin = 1,
				cmax = 3,
				cmid = 2,
				colorscale = [[0, 'rgb(0,255,0)'],[0.5,'rgb(255,165,0)'], [1, 'rgb(255,0,0)']],
				#line = {'width':14,'color':line_route_wt,'cmin':1,'cmax':3,'cmid':2,'colorscale':[[0, 'rgb(0,255,0)'],[0.5,'rgb(255,165,0)'],[1,'rgb(255,0,0)']]}
			)
		)
	)
		
	fig.update_layout(
		title={'text':'Jamnagar Route','font':{'color':'white'}},
		autosize=True,
		hovermode='closest',
		showlegend=True,
		mapbox=go.layout.Mapbox(
			accesstoken=mapbox_access_token,
			bearing=0,
			center=go.layout.mapbox.Center(
				lat=22.37087,
				lon=69.86777
			),
			pitch=0,
			zoom=12,
			style='dark'
		),
		paper_bgcolor = 'black',
		legend = {'font':{'color':'#fff'}}
		
	)

	return fig
	
		
@dash_app.callback( 
	dash.dependencies.Output('Alert Message','children'),
	[dash.dependencies.Input('Send Alert','n_clicks')])

def raise_alert_action(n_clicks):
	if n_clicks>0:
		return html.Div([html.Img(src = "/assets/send alert.gif",width=200, height=200),
						html.Audio(src= "/assets/Alert_beep.mp3",autoPlay=True, controls =False,loop=True)])

@dash_app.callback(
    dash.dependencies.Output('OBC_Video', 'children'),
    [dash.dependencies.Input('OBC_Alerts_Track', 'clickData')])

def show_OBC_Video(clickData):
	if clickData!=None:
		#print("Click Processing")
		print("OBC Video")
		X = clickData
		Y = X["points"][0]
		
		print(Y)
		return html.Div([html.Video(src = "/assets/23012020AK.mp4",controls=True,loop=True,autoPlay=True)])

@dash_app.callback( 
	dash.dependencies.Output('Alarm Message','children'),
	[dash.dependencies.Input('ALARM','n_clicks')])

def raise_alarm_action(n_clicks):
	if n_clicks>0:
		return  html.Div([html.Img(src = "assets/raise_alarm.gif",width=200,height=200),
						html.Audio(src= "/assets/Annoying_Alien_Buzzer-Kevan-1659966176.mp3",autoPlay=True, controls =False,loop=True)])
		
		
if __name__ == '__main__':
    dash_app.run_server()
