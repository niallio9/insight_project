# SafeRoute

SafeRoute is a tool that enables drivers to make proactive decisions to lower their risk of being in a collision while on the roads in Toronto. A live web application for the city of Toronto can be found at http://nialler.pythonanywhere.com/.


SafeRoute combines vehicle collsion data from the Toronto Police Department, with map information from OpenStreetMap, and weather inforamtion from Dark Sky API.

Map data is converted to a graph network format, where intersections are represented by nodes, and street segments are represented by edges. Each collsion data point is linked to a street segment using a k-nearest neighbour algorithm, which also provides a collision history for each street segment. Weather data for each collision point is taken from the high-resolution (hourly) historical Dark Sky API.

The combined information is used to train a random forest classifier, which estimates whether a collision is likely to occur on a given street segment under given conditions.

The web application (link above) uses this trained model in a navigation application in the following way:

1. Get the origin and destination addresses from the user.
2. Get the current weather information from Dark Sky API.
3. Classify each street segment using the street network and weather information as input to the model.
4. Calculate routes along the road (graph) network according to "shortest route" and "safest route".
5. Plot these routes on a map for the user.

The html templates and server file are included in this repository for reference to help anyone to implement a similar web application.

### Prerequisites

osmnx: https://github.com/gboeing/osmnx

scikit-learn

flask (to implement a web application)

Dark Sky API: get a free API key at https://darksky.net/dev

### Running the tests

The main functions for running the app are located in 'custom_funcs.py'.

To test that these functions run correctly with the neccesary packages, use a testing function in '/saferoute/saferoute/'.
Make sure to change the path to your local directory in 'custom_funcs.py'

From a terminal in the above directory run:

```
python test_custom_funcs.py
```

This should produce a .png file with the shortest and safest routes plotted on a road map of Toronto.
The origin and destination are defaults.

The output file is called 'custom_functions_test_output.png', and is saved to a folder named 'images'.

## Acknowledgments

* All my friends and the cool people at Insight Data Science who gave great feedback on the project. And Jag and Cado :)

