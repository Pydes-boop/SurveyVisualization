# Useful Reference i used for learning this: https://towardsdatascience.com/cleaning-analyzing-and-visualizing-survey-data-in-python-42747a13c713
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl
import seaborn as sns
import numpy as np

# Dont ignore Warings like this, but sometimes they bug me at debugging ;)
import warnings
warnings.filterwarnings('ignore')

from random import gammavariate
from numpy import median, mean
from textwrap import wrap

# MatplotLib Legend Shit you dont necessarily need
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.legend_handler import HandlerBase

# This Class is from this https://stackoverflow.com/questions/55501860/how-to-put-multiple-colormap-patches-in-a-matplotlib-legend answer that i found about creating colormap legends
class HandlerColormap(HandlerBase):
    def __init__(self, cmap, num_stripes=8, **kw):
        HandlerBase.__init__(self, **kw)
        self.cmap = cmap
        self.num_stripes = num_stripes
    def create_artists(self, legend, orig_handle, 
                       xdescent, ydescent, width, height, fontsize, trans):
        stripes = []
        for i in range(self.num_stripes):
            s = Rectangle([xdescent + i * width / self.num_stripes, ydescent], 
                          width / self.num_stripes, 
                          height, 
                          fc=self.cmap((2 * i + 1) / (2 * self.num_stripes)), 
                          transform=trans)
            stripes.append(s)
        return stripes

# Legend shit over


df = pd.read_csv('data.csv')
drop = df.drop(columns=['Timestamp', 'Willst du uns noch irgendetwas sagen?'])

mapping = drop

# How to Filter Columns by Regex and rename them, we dont use this though because we want to see our questions
#mapping.columns = ['game-visual', 'game-fun', 'game-goal', 'sus-playagain', 'sus-toocomplicated', 'sus-interacteasyunderstand', 'sus-needexplanation', 'sus-gameeasyundestand', 'sus-consistentinteraction', 'sus-otherseasyunderstand', 'sys-gameconnectedsys', 'sys-natureconnectedsys', 'sys-interactionnatur', 'ui-interactioneasy', 'ui-notenoughinteraction', 'ui-pretty', 'ui-gamepretty']
#game = mapping.filter(regex='^game')
#sus = mapping.filter(regex='^sus')
#sys = mapping.filter(regex='^sys')
#ui = mapping.filter(regex='^ui')

# Filter by Questions Category
game = mapping.filter(regex='^1.')
sus = mapping.filter(regex='^2.')
sys = mapping.filter(regex='^3.')
ui = mapping.filter(regex='^4.')

# Coloring Schemes we will use for the respective first, second, third, fourth dataframe and their graphs, so we can differentiate categories by color

# color maps from here https://matplotlib.org/stable/tutorials/colors/colormaps.html

c_map = ['OrRd', 'BuPu', 'YlGn', 'YlOrBr']

# Creating a List of our seperate dataframes
TempLists = [game, sus, sys, ui]
Lists = []
# Filtering and Counting the Values Here
for df in TempLists:
    df = df.apply(pd.value_counts).fillna(0).astype(int)
    # Need to append to new List because TempList doesnt save the changes within it and i cant be bothered to do proper referencing in python
    Lists.append(df)

# BUGFIX SPECIFIC TO DATASET manually adding a 0 Count Row for a sub dataset that didnt have any responses with value '1'
Lists[2].loc[1] = [0, 0, 0]

TempLists = Lists
Lists = []
for df in TempLists:
    # Again having weird referencing issues, maybe im stupid but for smaller usecase it doesnt hurt to bad to copy for cleanup
    Lists.append(df.sort_index(ascending=True))

# X Labels we want to use on our Graphs
x = ['Stimme überhaupt nicht zu', 'Stimme nicht zu', 'Stimme weder zu noch lehne ab', 'Stimme zu', 'Stimme voll und ganz zu']

# Setting your sns style to darkgrid, cause it looks cool (use whitegrid, if darkgrid doesnt fit with your colours)
sns.set_style("darkgrid")

def plot_subplot(column_count, row_count, df_columns, colorlist, name, deleteLastPlot=False, legend_labels=[], legend_cm=[]):
    fig, ax = plt.subplots(nrows=row_count, ncols=column_count, figsize=(5*column_count,3*row_count), sharey=True, sharex=True)

    for a, column_name, col in zip(ax.flatten(), df_columns, colorlist):
        # Here we wrap our column names so they linebreak after a certain char count to make our questions properly readable
        wrapped_column_name = ("\n".join(wrap(column_name, 40)))

        # Plotting our Graph
        sns.barplot(df_columns[column_name], x, palette = col, edgecolor = 'black', ax=a).set_title('{}'.format(wrapped_column_name))

        # Keeps x-axis tick labels for each group of plots
        a.xaxis.set_tick_params(which='both', labelbottom=True)

        # Add Mean / Median Values
        # First we reverse our previous pandas value counts operation because otherwise np doesnt calculate mean/median correctly
        reverseValueCounts = pd.Series(np.repeat(df_columns[column_name].index,df_columns[column_name]))
        # We draw a line into our subplots that represents the mean / median values
        # BUGFIX we -1 our median and mean values because otherwise they appear scuffed in our barplot, probably because the x labels might be starting at index 0 and not 1
        mean = reverseValueCounts.mean() - 1
        median = reverseValueCounts.median() - 1
        a.axhline(mean - 1, c='k', ls='-', lw=1.5)
        a.axhline(median - 1, c='dodgerblue', ls='--', lw=1.5)
        
        # Suppresses displaying the question along the y-axis and remove title from x-axis
        a.yaxis.label.set_visible(False)
        a.xaxis.label.set_visible(False)

    # If we have an uneven amount dataframes to plot we want to delete the last one
    if(deleteLastPlot):
         fig.delaxes(ax[row_count-1, column_count-1])
    
    # We create some space below our plot to place our legend elements there, this is so tight layout knows it needs to keep space below the plot
    # Potential BUG This can lead to errors if its not perfect, so you should probably remove this if you just want to generate a few plots to see without legend
    fig.supxlabel(" ")
    
    # Creating a Custom Colormap for Black bar

    blackdict = {'red':     ((0.0,  0.0, 0.0),
                        (1.0,  0.0, 0.0)),
            'green':    ((0.0,  0.0, 0.0),
                        (1.0,  0.0, 0.0)),
            'blue':     ((0.0,  0.0, 0.0),
                        (1.0,  0.0, 0.0))}

    dodgerbluedict = {'red':    ((0.0,  0.11, 0.11),
                                (1.0,  0.11, 0.11)),
                    'green':    ((0.0,  0.56, 0.56),
                                (1.0,  0.56, 0.56)),
                    'blue':     ((0.0,  1, 1),
                                (1.0,  1, 1))}                    
    
    cmaps = [plt.cm.get_cmap(name=legend_cm[0]), plt.cm.get_cmap(name=legend_cm[1])]
    solid_cmaps = [LinearSegmentedColormap('black', blackdict), LinearSegmentedColormap('dodgerblue', dodgerbluedict)] 

    cmap_handles = [Rectangle((0, 0), 1, 1) for _ in cmaps]
    mm_handles = [Rectangle((0, 0), 1, 1) for _ in solid_cmaps]

    handler_map = dict(zip(cmap_handles, [HandlerColormap(cm, num_stripes=5) for cm in cmaps]))
    handler_map.update({mm_handles[0]: HandlerColormap(solid_cmaps[0], num_stripes=1)})
    handler_map.update({mm_handles[1]: HandlerColormap(solid_cmaps[1], num_stripes=2)})

    all_handles = cmap_handles + mm_handles

    labels = legend_labels + ["Mean", "Median"]

    fig.legend(handles=all_handles, labels=labels, handler_map=handler_map ,loc='lower center', fancybox=True, ncol=4, edgecolor='w')
    
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('images/{}.png'.format(name))

plot1_name = 'Plot1_tight'
plot2_name = 'Plot2_tight'

# Creating a color list that repeats the color values x - column amount of times so our function has same length lists for the loop
col_list = [c_map[0] for i in range(len(Lists[0].columns))] + [c_map[1] for i in range(len(Lists[1].columns))]

cm_labels = []
legend_text = []
# Plotting our first subplot
plot_subplot(5, 2, Lists[0].join(Lists[1]), col_list, plot1_name, legend_labels=['1. General Game Questions', '2. Adjusted System Usability Scale'], legend_cm=[c_map[0], c_map[1]])

# Same as before, creating list of colors for specific plots with same amounts as columns
col_list = [c_map[2] for i in range(len(Lists[2].columns))] + [c_map[3] for i in range(len(Lists[3].columns))]

# Plotting our second subplot
plot_subplot(4, 2, Lists[2].join(Lists[3]), col_list, plot2_name, deleteLastPlot=True, legend_labels=['3. Interconnected Nature', '4. UI and Interaction'], legend_cm=[c_map[2], c_map[3]])