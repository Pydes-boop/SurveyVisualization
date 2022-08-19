# Useful Reference i used for learning this: https://towardsdatascience.com/cleaning-analyzing-and-visualizing-survey-data-in-python-42747a13c713

from random import gammavariate
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from textwrap import wrap

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

# X Labels we want to use on our Graphs
x = ['Stimme nicht zu', 'Stimme leicht dagegen', 'Neutral', 'Stimme leicht zu', 'Stimme voll und ganz zu']

def plot_subplot(column_count, row_count, df_columns, colorlist, name, deleteLastPlot=False, XLabel=''):
    fig, ax = plt.subplots(nrows=row_count, ncols=column_count, figsize=(5*column_count,3*row_count), sharey=True, sharex=True)

    for a, column_name, col in zip(ax.flatten(), df_columns, colorlist):
        # Here we wrap our column names so they linebreak after a certain char count to make our questions properly readable
        wrapped_column_name = ("\n".join(wrap(column_name, 40)))

        print(wrapped_column_name)

        # Plotting our Graph
        sns.barplot(df_columns[column_name], x, palette = col, edgecolor = 'black', ax=a).set_title('{}'.format(wrapped_column_name))

        # Keeps x-axis tick labels for each group of plots
        a.xaxis.set_tick_params(which='both', labelbottom=True)
        
        
        # Suppresses displaying the question along the y-axis and remove title from x-axis
        a.yaxis.label.set_visible(False)
        a.xaxis.label.set_visible(False)

    # If we have an uneven amount dataframes to plot we want to delete the last one
    if(deleteLastPlot):
         fig.delaxes(ax[row_count-1, column_count-1])
    
    fig.supxlabel(XLabel)
    plt.tight_layout()
    plt.savefig('images/{}.png'.format(name))

plot1_name = 'Plot1_tight'
plot2_name = 'Plot2_tight'

# Creating a color list that repeats the color values x - column amount of times so our function has same length lists for the loop
col_list = [c_map[0] for i in range(len(Lists[0].columns))] + [c_map[1] for i in range(len(Lists[1].columns))]

# Plotting our first subplot
plot_subplot(5, 2, Lists[0].join(Lists[1]), col_list, plot1_name, XLabel='1. General Game Questions in Red\n2. Adjusted System Usability Scale in Purple')

# Same as before, creating list of colors for specific plots with same amounts as columns
col_list = [c_map[2] for i in range(len(Lists[2].columns))] + [c_map[3] for i in range(len(Lists[3].columns))]

# Plotting our second subplot
plot_subplot(4, 2, Lists[2].join(Lists[3]), col_list, plot2_name, deleteLastPlot=True, XLabel='3. Interconnected Nature in Green\n4. UI and Interaction in Orange')