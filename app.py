import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as do
from plotly.subplots import make_subplots
import pandas as pd
from yt_playlist import playlist_serv


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
		html.Div([
			html.Div(
			['Youtube Playlist DataView'],
			style={'color':'#FFFFFF','fontSize':40,'marginLeft':40}
			),
			html.Div(
			['An interactive exploratory data visualization of Youtube playlists'],
			style={'color':'#FFFFFF','fontSize':16,'marginLeft':40}
			),
			html.Br(),
			html.Div(
			[
			dcc.Input(
                		id='link-id',
                		type='text',
                		placeholder='Paste Youtube playlist link here then hit Enter!',
                		debounce=True,
                		value='https://www.youtube.com/playlist?list=OLAK5uy_mL7Do-3QvF2ONCF_iZj2xcc9JBU-Rb0g8',
                		style={'width':600})
			],
			style={'marginLeft':30}
			)
		
		],style={'backgroundColor':'#FF0000'}),
		
		html.Div([
			dcc.Graph(
            		id='view-chart'
        		)
		]),
		
		html.Div([
			dcc.Graph(
            		id='like-chart'
        		)
		]),
		
		html.Div([
			dcc.Graph(
            		id='dislike-chart'
        		)
		]),
		
		html.Div([
			dcc.Graph(
            		id='react-chart'
        		)
		]),
		
		html.Div([
			dcc.Graph(
            		id='rratio-chart'
        		)
		]),
		
		html.Div([
			dcc.Graph(
            		id='lratio-chart'
        		)
		]),
		
		html.Div(
		['This dashboard is in no way connected to Youtube as an organization. (https://github.com/neil-vqa)'],
		style={'fontSize':15, 'textAlign':'center', 'fontStyle':'italic', 'verticalAlign':'middle'}
		)
		
],id='grid',style={'backgroundColor':'#EFEFEF'})

    
@app.callback(
    [Output('view-chart','figure'),
     Output('like-chart','figure'),
     Output('dislike-chart','figure'),
     Output('react-chart','figure'),
     Output('rratio-chart','figure'),
     Output('lratio-chart','figure')],
    [Input('link-id','value')]
)
def youtube(yt_link):
    show = playlist_serv(yt_link, 15)

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
    
    bubbles = (rt_vid['ratio'] / rt_vid['ratio'].max())*150
    shape_line = [do.layout.Shape(
    				type='line',
    				x0= l_vid['title'][i],
    				y0= 0,
    				x1= l_vid['title'][i],
    				y1= l_vid['likes'][i]) for i in range(len(l_vid))]
    
    margins= do.layout.Margin(l=50,r=50,b=70,t=60)
    

    view = do.Figure(data = [do.Bar(
        x= v_vid['title'],
        y= v_vid['views'],
        hoverinfo='y',
        marker={'color':'#05719D'}
    )],
    layout=do.Layout(title=do.layout.Title(text='Video Views', x=0.5), margin=margins))

    like = do.Figure(data = [do.Scatter(
        x= l_vid['title'],
        y= l_vid['likes'],
        hoverinfo='y',
        mode='markers',
        marker={'color':'#3484F0', 'size':15}
    )],
    layout=do.Layout(title=do.layout.Title(text='Likes', x=0.5), shapes=shape_line,
    			xaxis={'showgrid':False}, margin=margins))

    dislike = do.Figure(data = [do.Bar(
        x= d_vid['title'],
        y= d_vid['dislikes'],
        hoverinfo='y',
        marker={'color':'#757575'}
    )],
    layout=do.Layout(title=do.layout.Title(text='Dislikes', x=0.5), margin=margins))
    
    react = do.Figure(data = [do.Bar(
        x= r_vid['title'],
        y= r_vid['dislikes'],
        hoverinfo='y',
        marker={'color':'#757575'}
    	), do.Bar(
    	x= r_vid['title'],
    	y= r_vid['likes'],
    	hoverinfo='y',
        marker={'color':'#3484F0'}
    	)
    	],
    layout=do.Layout(title=do.layout.Title(text='Reaction Count (Likes + Dislikes)', x=0.5),
    			barmode='stack', showlegend=False, margin=margins))
    
    react_ratio = do.Figure(data = [do.Scatter(
        x= rt_vid['likes'],
        y= rt_vid['dislikes'],
        text= rt_vid['title'],
        mode='markers',
        marker={'color':'#D291BC','size':[i for i in bubbles],'opacity':0.4}
    )],
    layout=do.Layout(title=do.layout.Title(text='Reaction Ratio (Likes / Dislikes)', x=0.5),
    		     xaxis={'showgrid':False}, yaxis={'showgrid':False}, margin=margins))
    
    like_ratio = do.Figure(data = [do.Bar(
        x= lr_vid['title'],
        y= lr_vid['like_ratio'],
        hoverinfo='y',
        marker={'color':'#FFDFD3'}
    )],
    layout=do.Layout(title=do.layout.Title(text='Like Ratio (Likes / Reaction Count)', x=0.5), margin=margins))
    
   
    return view, like, dislike, react, react_ratio, like_ratio



if __name__=='__main__':
    app.run_server(debug=True)
