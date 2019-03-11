import pandas as pd 

 
from bokeh.layouts import row, column
#from bokeh.themes import built_in_themes
from bokeh.models import Select, ColumnDataSource, HoverTool 
from bokeh.palettes import Spectral5 
from bokeh.plotting import curdoc, figure, show, output_file
from bokeh.models.widgets import Div


#output_notebook()

data = pd.read_csv('C:/Users/super/GitHub/project-wt-18-06-immoblienratgeber/Data/cleaned/apartments.csv', sep=",", decimal=",", encoding='iso-8859-1')



# df = df.copy() 
df = data.copy()
source = ColumnDataSource(df)

#df.set_index('SubClass_ID')

SIZES = list(range(6, 22, 3)) 
COLORS = Spectral5 
N_SIZES = len(SIZES) 
N_COLORS = len(COLORS) 



 
columns = sorted(df.columns) 
discrete = [x for x in columns if df[x].dtype == object]  
continuous = [x for x in columns if x not in discrete] 
 

def create_figure(): 
     xs = df[x.value].values 
     ys = df[y.value].values 
     x_title = x.value.title() 
     y_title = y.value.title()
     sc = df['obj_livingSpace'].values
     scid = df['obj_purchasePrice'].values
 
 
     kw = dict() 
     if x.value in discrete: 
         kw['x_range'] = sorted(set(xs)) 
     if y.value in discrete: 
         kw['y_range'] = sorted(set(ys)) 
     kw['title'] = "Blue Yonder: %s vs %s" % (x_title, y_title) 
 
  #    source = ColumnDataSource(ColumnDataSource.from_df(df))
#      df = df.reset_index()
    
    

# #         df = yearly_DF.reset_index() # move index to column.
# # source = ColumnDataSource(ColumnDataSource.from_df(df)

# # hover.tooltips = OrderedDict([('x', '@x'),('y', '@y'), ('year', '$index'), ('weight','$weight'), ('muscle_weight','$muscle_weight'), ('body_fat','$bodyfat_p')])

 
     p = figure(plot_height=900, plot_width=1300, tools='pan,box_zoom,tap,lasso_select,wheel_zoom,reset,hover,save', **kw) 
     p.xaxis.axis_label = x_title 
     p.yaxis.axis_label = y_title
        
     
     p.hover.tooltips = [
         #("SubClass_ID", "@scid"),
         #("Subclass", "@{'sc'}"),
         (x_title, "@{x}"),
         (y_title, "@{y}")]
     
 
         
        
 
     if x.value in discrete: 
         p.xaxis.major_label_orientation = pd.np.pi / 4 
 
 
     sz = 9 
     if size.value != 'None': 
         if len(set(df[size.value])) > N_SIZES: 
             groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop') 
         else: 
             groups = pd.Categorical(df[size.value]) 
         sz = [SIZES[xx] for xx in groups.codes] 
 
 
     c = "#31AADE" 
     if color.value != 'None': 
         if len(set(df[color.value])) > N_SIZES: 
             groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop') 
         else: 
             groups = pd.Categorical(df[color.value]) 
         c = [COLORS[xx] for xx in groups.codes] 
 
 
     p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5) 
 
 
     return p 
 
 
 
 
def update(attr, old, new):
    layout.children[-1] = create_figure()
 


x = Select(title='X-Axis', value="obj_livingSpace", options=columns) 
x.on_change('value', update) 


y = Select(title='Y-Axis', value='obj_purchasePrice', options=columns) 
y.on_change('value', update) 


size = Select(title='Size', value='None', options=['None'] + continuous) 
size.on_change('value', update) 


color = Select(title='Color', value='None', options=['None'] + continuous) 
color.on_change('value', update) 


# controls = column([x, y, color, size], width=200)

# for control in controls:
#     control.on_change('value', lambda attr, old, new: update())

# layout = row(controls, create_figure(), sizing_mode='stretch_both')

#header = Div(text="<link rel='stylesheet' type='text/yaml' href='mycss.yaml'>")


controls = column([x, y, color, size], width=400) 
layout = row(controls, create_figure() ,sizing_mode="fixed") 

 
curdoc().add_root(layout) 
curdoc().title = "Crossfilter"
#curdoc().theme = 'dark_minimal'

output_file("layout.html")

show(layout)
