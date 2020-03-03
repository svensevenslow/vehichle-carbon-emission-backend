This project is a flask backened that aims to predict the carbon emissions by your vehicle during a trip  

To set it up on your local (Windows):  
  1.Install python 3.7.5  
  2.mkdir major_project_backend  
  3.cd major_project_backend  
  4.py -3 -m venv venv  
  5.venv\Scripts\activate  
  6.pip install -r requirements.txt  
  7.set FLASK_APP=flaskApp  
  8.set FLASK_ENV=development  
  9.flask run  
  
If any dependencies are required to be installed, after doing a pip install, run: pip freeze > requirements.txt

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/svensevenslow/vehichle-carbon-emission-backend/tree/testButton/flaskApp)
