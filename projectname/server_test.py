from flask import Flask, render_template, request
import sys
sys.path.insert(0, '/Users/niall/insight_project/projectname/projectname')
import custom_funcs as CF
import os
from datetime import datetime as dt
import glob



# Create the application object
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
def home_page():
    return render_template('index.html')  # render a template

@app.route('/output')
def recommendation_output():
       [os.remove(file) for file in glob.glob('/Users/niall/insight_project/projectname/static/map_out_*.png')]
       rightnow = dt.now()
       picname = "map_out_%i%i%i%i%i" % (rightnow.month, rightnow.day, rightnow.hour, rightnow.minute, rightnow.second)
       filename_out = '/Users/niall/insight_project/projectname/static/%s' % (picname)
       # Pull input
       input1 =request.args.get('user_input1')            
       input2 =request.args.get('user_input2')            
       print(input1)
       
       # Case if empty
       if input1 =="" or input2 =="":
           return render_template("index.html",
                                  my_input = input1,
                                  my_form_result="Empty")
       else:
           input1= input1.split(',')
           input2= input2.split(',')
           origin = [float(input1[0]), float(input1[1])]
           destination = [float(input2[0]), float(input2[1])]
           # get the weather data
           current_weather = CF.get_current_weather_toronto()
           # add the weather data to the unique roads
           roads_with_weather = CF.add_current_weather_to_unique_roads(current_weather)
           # run the unique roads through the classifier and save locally
           roads_with_weather = CF.get_collision_probs(roads_with_weather)
           # save the graph as the name used by the return statement below
           CF.plot_map_with_probs_routes(roads_with_weather, origin, destination, filename=filename_out)
#           CF.plot_map_with_probs_routes(roads_with_weather)
           
           some_output = "yeay!"
           some_number = 0
           some_image = '%s%s' % (picname, '.png')
           return render_template("index.html",
                              my_input=input1,
                              my_output=some_output,
                              my_number=some_number,
                              my_img_name=some_image,
                              my_form_result="NotEmpty")
           
# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True) #will run locally http://127.0.0.1:5000/

