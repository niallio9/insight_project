# SafeRoute

SafeRoute is a tool that enables drivers to make proactive decisions to lower their risk of being in a collision while on the roads in Toronto. A live web application for the city of Toronto can be found at http://nialler.pythonanywhere.com/.

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

