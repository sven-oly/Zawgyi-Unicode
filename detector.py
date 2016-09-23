#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import json
import logging
import os
import pickle
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.ext.webapp import template

# Import the model definition.
import ngram
from ngram import ngramModel

# Storage for pickeled objects.
# Use this property to store objects.
class ObjectProperty(db.BlobProperty):
	def validate(self, value):
		try:
			result = pickle.dumps(value)
			return value
		except pickle.PicklingError, e:
			return super(ObjectProperty, self).validate(value)

	def get_value_for_datastore(self, model_instance):
		result = super(ObjectProperty, self).get_value_for_datastore(model_instance)
		result = pickle.dumps(result)
		return db.Blob(result)

	def make_value_from_datastore(self, value):
		try:
			value = pickle.loads(str(value))
		except:
			pass
		return super(ObjectProperty, self).make_value_from_datastore(value)

# Stores models
class MyDetector(db.Model):
  name = db.StringProperty()
  lang = db.StringProperty()
  font = db.StringProperty()
  level = db.IntegerProperty()
  obj = ObjectProperty() # The Detector object itself


# Globals
allModels = None

# Use histogram models to estimate the font encoding and language of text.
class DetectResultHandler(webapp2.RequestHandler):

  def get(self):
    global allModels

    text = unicode(self.request.get('text'))
    logging.info('DetectResultHandler text         = %s' % text)
    filenames = None
    if allModels == None:
      (filenames, models) = loadModels()
      allModels = models
    else:
      models = allModels
  
    # TODO: Call the detectors.
    if not models:
      result = 'NO DETECTION READY YET'
    else:
      result = '%d models detected.' % len(allModels)
    logging.info('FILENAMES: %s' % filenames)
    
    msg = 'MESSAGE'
    obj = { 'input_text': text,
            'msg': msg,
            'detected': result,
            'modelCount': models,
            'filenames': filenames,
    }
    self.response.out.write(json.dumps(obj))

  
# Show detection page.
class DetectHandler(webapp2.RequestHandler):

  def get(self):
    text = unicode(self.request.get('text'))
    logging.info('DetectHandler text         = %s' % text)
    template_values = {
      'input_text': text,
    }
    path = os.path.join(os.path.dirname(__file__), 'detect.html')
    self.response.out.write(template.render(path, template_values))
   
    
def loadModels():
  filenames = glob.glob('models/*2_model*.save')
  logging.info('FILENAMES: %s' % filenames)
  models = None
  try:
    models = ngram.getSavedModels(filenames)
  except:
    logging.info('CANNOT LOAD files: %s' % filenames)
    models = None
    
  return (filenames, models)
  
	
# Generates a model from a given file, language, font, and ngram.
class ComputeModel(webapp2.RequestHandler):

  def get(self):
    trainingFile = self.request.get('filename')
    ngramLength = self.request.get('ngram', 3)
    lang = self.request.get('lang', 'burmese')
    font = self.request.get('font', 'unicode')
    logging.info('filename: %s' % trainingFile)
    
    nModel = ngramModel(lang, font, fileName=trainingFile)
    nModel.setN(int(ngramLength))
    nModel.addFileToModel()
    
    name = '%s_%s_%s_%s' % (trainingFile, ngramLength,
      lang, font)
    entity = MyDetector(name=name, obj=nModel, lang=lang,
      font=font, level=int(ngramLength))
    entity.put() # Saves the entity to the datastore

    logging.info('$$$$$$ entity: %s' % entity)
   
    # data = pickle.dumps(nModel)

    results = nModel.getModelStats()
    results['entity'] = entity.name
    self.response.out.write(json.dumps(results))
    

class ShowAllModels(webapp2.RequestHandler):

  def get(self):
    logging.info('ShowAllModels @#$%^&^*')
    entities = MyDetector.all()
    logging.info('ShowAllModels gets %s' % entities)
    # entities = entities.fetch(10)
    items = []
    for entity in entities:
      model = entity.obj
      items.append([entity.name, entity.lang, entity.font, entity.level])

    results = {
      'numItems': len(items),
      'items': items,
    }

    self.response.out.write(json.dumps(results))
