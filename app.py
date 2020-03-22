import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as do
import pandas as pd
from yt_playlist import playlist_serv

app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server
app.title= 'View Playlist Data!'

input_link = dbc.InputGroup([
	dbc.Input(id="input-field", placeholder="Paste Youtube playlist link here",
			value='https://www.youtube.com/playlist?list=OLAK5uy_mL7Do-3QvF2ONCF_iZj2xcc9JBU-Rb0g8'),
	dbc.InputGroupAddon([
		dbc.Button("Get stats!", id="input-link-button")
	],addon_type="append")
	
])

header = dbc.Container([
	dbc.Row([
		dbc.Col(html.H1("Youtube Playlist DataView", style={'color':'#FFFFFF'}, className='mt-3 ml-3'))
	]),
	dbc.Row([
		dbc.Col(html.H6("Learn which video in your favorite playlist has the most views, likes, and dislikes!", style={'color':'#FFFFFF'}, className='ml-3'))
	]),
	dbc.Row([
		dbc.Col(input_link, className='mb-3 ml-3 mt-2', md=6)
	])
	
], fluid=True, style={'backgroundColor':'#FF0000'}, className='shadow')

body = dbc.Container([
	dbc.Row([
		dbc.Col(html.Div(dcc.Graph(id='view-chart')), className='shadow mr-3 ml-3 mt-3 rounded-lg'),
		dbc.Col(html.Div(dcc.Graph(id='like-chart')), className='shadow mr-3 ml-3 mt-3 rounded-lg')
	]),
	dbc.Row([
		dbc.Col(html.Div(dcc.Graph(id='dislike-chart')), className='shadow mr-3 ml-3 mt-3 rounded-lg'),
		dbc.Col(html.Div(dcc.Graph(id='react-chart')), className='shadow mr-3 ml-3 mt-3 rounded-lg')
	], className='mt-4'),
	dbc.Row([
		dbc.Col(html.Div(dcc.Graph(id='rratio-chart')), className='shadow mr-3 ml-3 mt-3 rounded-lg'),
		dbc.Col(html.Div(dcc.Graph(id='lratio-chart')), className='shadow mr-3 ml-3 mt-3 rounded-lg')
	], className='mt-4')
], className='mt-3 mb-3')

footer = dbc.Container([
	dbc.Row([
		dbc.Col(html.Div("Developer: nvqa.business@gmail.com | This dashboard is in no way connected to Youtube as an organization.", style={'color':'#FFFFFF','fontSize':12}, className='mt-3 mb-3 ml-3'))
	])
], fluid=True, style={'backgroundColor':'#FF0000'}, className='shadow mt-5')

def serve_layout():
	return html.Div([header, body, footer])

app.layout = serve_layout

@app.callback(
    [Output('view-chart','figure'),
     Output('like-chart','figure'),
     Output('dislike-chart','figure'),
     Output('react-chart','figure'),
     Output('rratio-chart','figure'),
     Output('lratio-chart','figure')],
    [Input('input-link-button','n_clicks')],
    [State('input-field','value')]
)
def youtube(n_clicks, value):
	show = playlist_serv(str(value), 30)

	df = pd.DataFrame(show)
	df1 = df[['title','views','likes','dislikes']]
	df1['views'] = df1.views.astype(int)
	df1['likes'] = df1.likes.astype(int)
	df1['dislikes'] = df1.dislikes.astype(int)
	df1['react'] = df1['likes'] + df1['dislikes']
	df1['ratio'] = df1['likes'] / df1['dislikes']
	df1['like_ratio'] = df1['likes'] / df1['react']

	vid = df1
	v_vid = vid.sort_values(['views'],ascending=False)
	l_vid = vid.sort_values(['likes'],ascending=False)
	d_vid = vid.sort_values(['dislikes'],ascending=False)
	r_vid = vid.sort_values(['react'],ascending=False)
	rt_vid = vid.sort_values(['ratio'],ascending=False)
	lr_vid = vid.sort_values(['like_ratio'],ascending=False)
    	
	bubbles = (rt_vid['ratio'] / rt_vid['ratio'].max())*90
	shape_line = [do.layout.Shape(
    				type='line',
    				x0= l_vid['title'][i],
    				y0= 0,
    				x1= l_vid['title'][i],
    				y1= l_vid['likes'][i],
    				line_color='#3484F0') for i in range(len(l_vid))]
	margins= do.layout.Margin(l=50,r=50,b=70,t=60)
    	
	view = do.Figure(data = [do.Bar(
        x= v_vid['title'],
        y= v_vid['views'],
        hoverinfo='y',
        marker={'color':'#05719D'},
        width=.4
	)],
	layout=do.Layout(title=do.layout.Title(text='Video Views', x=0.5), margin=margins, plot_bgcolor='#ffffff'))
    
	like = do.Figure(data = [do.Scatter(
        x= l_vid['title'],
        y= l_vid['likes'],
        hoverinfo='y',
        mode='markers',
        marker={'color':'#3484F0', 'size':15}
	)],
	layout=do.Layout(title=do.layout.Title(text='Likes', x=0.5), shapes=shape_line,
    			xaxis={'showgrid':False}, margin=margins, plot_bgcolor='#ffffff'))
    			
	dislike = do.Figure(data = [do.Bar(
        x= d_vid['title'],
        y= d_vid['dislikes'],
        hoverinfo='y',
        marker={'color':'#757575'},
        width=.4
	)],
	layout=do.Layout(title=do.layout.Title(text='Dislikes', x=0.5), margin=margins, plot_bgcolor='#ffffff'))
    
	react = do.Figure(data = [do.Bar(
        x= r_vid['title'],
        y= r_vid['dislikes'],
        hoverinfo='y+name',
        marker={'color':'#757575'},
        width=.4,
        name='Dislikes'
	), do.Bar(
	x= r_vid['title'],
	y= r_vid['likes'],
	hoverinfo='y+name',
        marker={'color':'#3484F0'},
        width=.4,
        name='Likes'
	)
	],
	layout=do.Layout(title=do.layout.Title(text='Reaction Count (Likes + Dislikes)', x=0.5),
    			barmode='stack', showlegend=False, margin=margins, plot_bgcolor='#ffffff'))
    			
	react_ratio = do.Figure(data = [do.Scatter(
        x= rt_vid['likes'],
        y= rt_vid['dislikes'],
        text= rt_vid['title'],
        mode='markers',
        marker={'color':'#D291BC','size':[i for i in bubbles],'opacity':0.4}
	)],
	layout=do.Layout(title=do.layout.Title(text='Reaction Ratio (Likes / Dislikes)', x=0.5),
    		     xaxis={'showgrid':False}, yaxis={'showgrid':False}, margin=margins, plot_bgcolor='#ffffff'))
    		     
	like_ratio = do.Figure(data = [do.Barpolar(
        r= lr_vid['like_ratio'],
        theta=list(range(0,360,360//len(lr_vid['like_ratio']))),
        width=[360/len(lr_vid['like_ratio'])]*len(lr_vid['like_ratio']),
        hoverinfo='r+text',
        text= lr_vid['title'],
        marker={'color':lr_vid['like_ratio'],'colorscale': 'Viridis'}
	)],
	layout=do.Layout(title=do.layout.Title(text='Like Ratio (Likes / Reaction Count)', x=0.5), margin=margins,
    			polar={'radialaxis':{'showticklabels':False}, 'angularaxis':{'showticklabels':False}}, plot_bgcolor='#ffffff'))
    			
	return view, like, dislike, react, react_ratio, like_ratio
	
if __name__=='__main__':
    app.run_server(debug=True)

