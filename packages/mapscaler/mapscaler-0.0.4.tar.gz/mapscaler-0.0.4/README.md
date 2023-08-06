# MapScaler
![Example visualization](https://raw.githubusercontent.com/conditg/mapscaler/master/images/header.png)

Scale areas of a geopandas map by any property (such as population) - without the shapes overlapping - to create more intuitive and beautiful choropleth visualizations.

[Official Documentation](https://mapscaler.readthedocs.io/en/latest/shapescaler.html)


## Quick Start:
Suppose you have a GeoPandas Dataframe `df`, including a column `scaleby` that is a float column indicating how much each sample should grow or shrink to reflect each location's respective population. The goal is for the area of each location to visually portray it's contribution to the entire map for your chosen variable (population, in this example).     
```python
import mapscaler as ms

ss = ms.ShapeScaler()
scaled_df = ss.scale_map(df, 'scaleby')
```
The above code returns a new GeoPandas dataframe with an updated geometry column, with each shape's area having been scaled (up or down) to reflect its respective scalar.  
Similarly, all shapes can be converted to circles before scaling by using the BubbleScaler:

```python
import mapscaler as ms

bs = ms.BubbleScaler()
scaled_df = bs.scale_map(df, 'scaleby')
```
More realistically, you may need to tweak a few arguments to get an ideal map, depending on the distribution of your initial areas and the distribution of your scalars. See [the documentation](https://mapscaler.readthedocs.io/en/latest/shapescaler.html) for full examples. 

