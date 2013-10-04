import pickle, logging
from google.appengine.ext import db

class PickledProperty(db.Property):
    data_type = db.Blob

    def get_value_for_datastore(self, model_instance):
        value = self.__get__(model_instance, model_instance.__class__)
        if value is not None:
            return db.Blob(pickle.dumps(value))

    def make_value_from_datastore(self, value):
        logging.info(value)
        #if value is not None:
        #    return pickle.loads(str(value))
        return pickle.loads(str(value))
