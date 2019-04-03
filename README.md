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

## Programs

There are two programs that I uploaed into this file. The Polar_Plot.py will be animated and run the sql query or what every way you collect data every 5 seconds. The HaysDiffPressSet.py will create a static graph.

You can download this code and change the way that data is read into the program to create one for your self. The rmax can be changed to whatever wind speed that you deem appropriate since 140 mph is not common in most locations outside of the Mount Washington observatory.

## Issues

There are several issues that I have run into that I have not had time to really work on yet:
 - In the most recent matplotlib update there is a runtime error that I have not been able to fix. My current work around was to just keep matplotlib library at its original version that I started with which is 2.2.2. I also had to keep the MKL library at a previous verstion as well. MKL version is 2018.0.0.
 - The text in the file is difficult to work with and change around. I also have not figured out a good way to ajust the text as you ajust the window size.
