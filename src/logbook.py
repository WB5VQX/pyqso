#!/usr/bin/env python 
# File: logbook.py

#    Copyright (C) 2012 Christian Jacobs.

#    This file is part of PyQSO.

#    PyQSO is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyQSO is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyQSO.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GObject
import logging

from record import *
from adif import *

class Logbook(Gtk.ListStore):
   
   def __init__(self):
            
      self.SELECTED_FIELD_NAMES_TYPES = AVAILABLE_FIELD_NAMES_TYPES # FIXME: Allow the user to select the field names. By default, let's select them all.
      
      # The ListStore constructor needs to know the data types of the
      # columns, so let's make a list containing these now.
      data_types = [int]
      for key in self.SELECTED_FIELD_NAMES_TYPES.keys():
         # NOTE: we store all boolean field values as strings
         # and use the combo boxes rather than the toggle buttons.
         # The latter are are easier to modify accidentally.
         data_types.append(str)
      
      # Call the constructor of the super class (Gtk.ListStore)
      Gtk.ListStore.__init__(self, *data_types)
      
      # Begin with no records.
      self.records = []
      
      logging.debug("New Logbook instance created!")
      
   def add_record(self):
      # Adds a blank record to the end of the logbook,
      # to be completed by the user.
      
      fields_and_data_dictionary = {}
      
      logbook_entry = [len(self.records)] # Add the next available record index
      field_names = self.SELECTED_FIELD_NAMES_TYPES.keys()
      for i in range(0, len(field_names)):
         # Initialise all field data to None.
         fields_and_data_dictionary[field_names[i]] = None
         logbook_entry.append(None)
         
      record = Record(fields_and_data_dictionary)
      self.records.append(record)
      self.append(logbook_entry)
      # Hopefully this won't change anything as check_consistency
      # is also called in delete_record, but let's keep it
      # here as a sanity check.
      self.check_consistency() 
      
      return
      
   def delete_record(self, iter, index):
      # Deletes the record with index 'index' from self.records.
      # 'iter' is needed to remove the record from the ListStore itself.
      self.records.pop(index)
      self.remove(iter)
      self.check_consistency()
      return
      
   def check_consistency(self):
      # Make sure all the record indices are consecutive and 
      # correctly ordered.
      for i in range(0, len(self.records)):
         if(self[i][0] != i):
            self[i][0] = i
      return
         
   def populate(self):
      # Remove everything that is rendered already and start afresh
      self.clear()
      
      for i in range(0, len(self.records)):
         logbook_entry = [] # Create a new logbook entry
         # First append the unique index given to the record.
         logbook_entry.append(i)
         for field in self.SELECTED_FIELD_NAMES_TYPES.keys():
            logbook_entry.append(self.records[i].get_field_data(field))
         self.append(logbook_entry)
      
      return
      
      