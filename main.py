#!/usr/bin/python
from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
import urllib
import sqlite3

#Brendan M. Lowe
### Functions for Usage

## Apply current settings to table then apply to hardware
def apply_settings(new_settings):
	#Obtain the old settings so that hardware can be manipulated following the save.	
   old_settings = current_settings()   
   conn = sqlite3.connect("inc/ampdb.sql")

   # This enables column access by name: row['column_name']
   conn.row_factory = sqlite3.Row

   c = conn.cursor()	

   # Save the Amp Setting
   statement = "UPDATE current SET preset_name = '%s', volume = %s, tone = %s WHERE id = 1" % (new_settings['new_preset'],new_settings["volume"],new_settings["tone"])
   c.execute(statement) 

    #Close the SQL Connection
   conn.commit()
   conn.close()		
	
   return statement



## Obtain Current Settings From the SQLite Database
def current_settings():
   conn = sqlite3.connect("inc/ampdb.sql")

   # This enables column access by name: row['column_name']
   conn.row_factory = sqlite3.Row

   c = conn.cursor()
   # Obtain Current Amp Settings
   c.execute("SELECT * FROM current")
   info = c.fetchone()
   setting = dict(info)

   if setting["preset_name"] is None:
      setting["preset_name"] = "none"

    #Close the SQL Connection
   conn.commit()
   conn.close()

   return setting

def amp_info():
   conn = sqlite3.connect("inc/ampdb.sql")

   # This enables column access by name: row['column_name']
   conn.row_factory = sqlite3.Row

   c = conn.cursor()
   # Obtain Amp Name
   c.execute("SELECT * FROM info")

   pi_info = c.fetchone()
   pi_info = dict(pi_info)

   #Close the SQL Connection
   conn.commit()
   conn.close()

   return pi_info
   
def preset_info():   
	conn = sqlite3.connect("inc/ampdb.sql")
	
	# This enables column access by name: row['column_name']
	conn.row_factory = sqlite3.Row
   
	c = conn.cursor()
	# Obtain All the Presets in the database.
	c.execute("SELECT * FROM preset")
   
	settings_info = c.fetchall()
	settings = [ dict(preset) for preset in settings_info ]

	#Close the SQL Connection
	conn.commit()
	conn.close()

	return settings

## Save Settings in the SQLite Database
def save_settings(save):	
	
   conn = sqlite3.connect("inc/ampdb.sql")

   if save["new_preset"] is None:
      save["new_preset"] = "none"

   # This enables column access by name: row['column_name']
   conn.row_factory = sqlite3.Row

   c = conn.cursor()
   # Save the Amp Setting
   statement = "INSERT INTO preset (preset_name, volume, tone ) VALUES ('%s',%s,%s)" % (save['new_preset'],save["volume"],save["tone"])
   c.execute(statement)   
   

   #Close the SQL Connection
   conn.commit()
   conn.close()

   return statement   
   
# Deletes single preset data from the SQL database	
def preset_delete(id):
   conn = sqlite3.connect("inc/ampdb.sql")

   # This enables column access by name: row['column_name']
   conn.row_factory = sqlite3.Row

   c = conn.cursor()
   # Obtain Preset Amp Settings
   statement = "DELETE FROM preset WHERE preset_id = %s" % (id)
   c.execute(statement)
   #info = c.fetchone()
   #setting = dict(info)

   #Close the SQL Connection
   conn.commit()
   conn.close()

   return statement	
   
   
# Gets single preset data from the SQL database	
def preset_id(id):
   conn = sqlite3.connect("inc/ampdb.sql")

   # This enables column access by name: row['column_name']
   conn.row_factory = sqlite3.Row

   c = conn.cursor()
   # Obtain Preset Amp Settings
   statement = "SELECT * FROM preset WHERE preset_id = %s" % (id)
   c.execute(statement)
   info = c.fetchone()
   setting = dict(info)

   if setting["preset_name"] is None:
      setting["preset_name"] = "none"

    #Close the SQL Connection
   conn.commit()
   conn.close()

   return setting	

#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################

#Provide Main Web Interface for Digital Amp.
app = Flask(__name__)

@app.route("/")
def main_page():

   # Obtain Amp Information
   information = amp_info()
   information["name"]=information["name"]+' '

   #Obtain Current Settings Information
   setting = current_settings()

   return render_template('index.html', ampname=information["name"], **setting)


@app.route("/preset")

@app.route("/settings")
def hello():
    return "Hello World!"

@app.route("/api", methods=['GET', 'POST'])
def api():

	information = dict()
	information["info"] = None
	information["error"] = None
	
	
	if request.method == 'POST':
		if 'apply_settings' in request.form:		
			information["info"] = apply_settings(request.form)
		elif 'save' in request.form:
			information["info"] = save_settings(request.form)
		elif 'delete_preset' in request.form:
			information["info"] = preset_delete(request.form["id"])
		else:
			information["info"] = "Error"
			information["error"] = "Something has gone terribly wrong"

	elif request.method == 'GET':		
		if 'presets' in request.args:
			information["info"] = preset_info()
		elif 'preset' in request.args:
			information["info"] = preset_id(request.args.get('id'))
		elif 'settings' in request.args:
			information["info"] = current_settings()
		elif 'info' in request.args:
			information["info"] = amp_info()
	else:
		information["info"] = "Error"
		information["error"] = "Something has gone terribly wrong"

	information = 	json.dumps(information)
	return information

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80, threaded=True, debug=True)

class MyFlask(Flask):
    
    def handle_exception(self, e):
        # add all necessary log info here
        log.info("dumping session: %s", session)
        log.info("dumping request: %s", request)
        log.info("dumping request args: %s", request.args)
        return super(MyFlask, self).handle_exception(e)