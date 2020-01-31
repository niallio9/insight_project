from flask import Flask, render_template, request

# Create the application object
app = Flask(__name__)

@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
def home_page():
    return render_template('index.html')  # render a template

@app.route('/output')
def recommendation_output():
#       
       # Pull input
       some_input1 =request.args.get('user_input1')            
       some_input2 =request.args.get('user_input2')            
       print(some_input1)
       
       # Case if empty
       if some_input1 =="" or some_input2 =="":
           return render_template("index.html",
                                  my_input = some_input1,
                                  my_form_result="Empty")
       else:
           some_output="yeay!"
           some_number=0
           some_image="map_10am_jan.png"
           return render_template("index.html",
                              my_input=some_input1,
                              my_output=some_output,
                              my_number=some_number,
                              my_img_name=some_image,
                              my_form_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True) #will run locally http://127.0.0.1:5000/

