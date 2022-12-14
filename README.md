# Google Survey Visualization

This is a simple Python Script to create combined subplots of user surveys which used the standard *Likert-Scale* from 1...5 (Strongly  Disagree...Strongly Agree)

Additionally it uses Color Maps to color code the different parts of our survey

Examples of our generated Graph-Image look like this:

<p align=center>
    <a href="./README.md">
        <img src="./images/Plot1_tight.png" alt="Image showing several survey charts, some colored green and some colored orange"/>
    </a>
    <a href="./README.md">
        <img src="./images/Plot2_tight.png" alt="Image showing several survey charts, some colored green and some colored orange"/>
    </a>
    <br>

</p>

This Code should be easily transferable for other survey results if theyre also using the *Likert-Scale*

## Usage

This is our main method to generate our plot-images
```python
   def plot_subplot(column_count, row_count, df_columns, colorlist, name, deleteLastPlot=False, XLabel=''):
```

**column_count:** amount of columns for image generation<br>
**row_count:** amount of rows for image generation<br>
**df_columns:** Dataframe that includes all the columns we want to plot<br>
**colorlist:** List of ColorMaps or Colors *(needs to be specified for every plot)*<br>
**name:**, filename we use to save in image folder<br>
**deleteLastPlot:** Default: False, If True: removes bottom right (last) plot if we have an odd amount of plots<br>
**XLabel:** Bottom label for all the plots, used to specify what Sub-Survey the questions belong to<br><br>
You can easily generate a **list of colormaps** with the right amount (for every column)
```python
    c_map = ['OrRd', 'BuPu', 'YlGn', 'YlOrBr']
    col_list = [c_map[0] for i in range(len(Lists[0].columns))] + [c_map[1] for i in range(len(Lists[1].columns))]
```
Here we generate 2 lists of repeating [colormaps](https://matplotlib.org/stable/tutorials/colors/colormaps.html) from the amount of columns in our seperated datasets (seperated by Sub-Survey)

## Acknowledgements

This [Article](https://towardsdatascience.com/cleaning-analyzing-and-visualizing-survey-data-in-python-42747a13c713) by [Charlene Chambliss](https://medium.com/@blissfulchar) was very helpful in learning my way around this sort of visualization using seaborn

## Different Approach
If you are considering to visualize your data in a similar fashion to mine, you should really consider this [blogpost](https://medium.com/orikami-blog/behind-the-screens-likert-scale-visualization-368557ad72d1) as a potential alternative for your visualization.

## Further Reading
This project uses both [MatplotLib](https://matplotlib.org/stable/gallery/index.html) and [Seaborn](https://seaborn.pydata.org/examples/index.html). If you want to get into this further or have some weirder data you want to represent (ie.: like 3d Data) you should read more about matplotlib, like in this [article](https://towardsdatascience.com/seaborn-can-do-the-job-then-why-matplotlib-dac8d2d24a5f)
