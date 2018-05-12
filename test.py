#!/usr/bin/python
import sqlite3
import json

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
   
print preset_id('1')
