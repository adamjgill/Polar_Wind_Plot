# Polar Wind Plots
Plotting wind 24 hour wind on Polar Plots

This was created to replicate our analog instrumentation for digitization in the event that it eventually breaks.
The program will link to a sql database and plot the winds. It can easily be converted to plot a CSV file as well.
One of the programs will plot the data in real time, doing a new query every 5 seconds or so and the other is a static
page that will just plot the data within the timestamps that are given.

The peak wind will also be plotted as well with an arrow pointing to the peak gust. Text is written within the center of the page
to indicate the speed and the time that it occured.

Below is a sample of the output:
![alt text](https://github.com/adamjgill/Polar_Wind_Plot/blob/master/Setra_Hays.png)
