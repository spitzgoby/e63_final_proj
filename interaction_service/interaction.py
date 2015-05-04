import logging

class Coords(object):
  COORDS_LATITUDE = 'latitude'
  COORDS_LONGITUDE = 'longitude'

  def __init__(self, jsonObj):
    self.latitude = jsonObj[Coords.COORDS_LATITUDE] 
    self.longitude = jsonObj[Coords.COORDS_LONGITUDE]

class Interaction(object):

  INTERACTION_USER_ID = 'user_id'
  INTERACTION_TIME_STAMP = 'time_stamp'
  INTERACTION_DURATION = 'duration'
  INTERACTION_COORDS = 'coords'

  @property
  def user_id(self):
      return self._user_id
 
  @property
  def time_stamp(self):
      return self._time_stamp

  @property
  def duration(self):
      return self._duration
  
  @property
  def coords(self):
      return self._coords

  def __init__(self, jsonObj):
    self._user_id = jsonObj[Interaction.INTERACTION_USER_ID]
    self._time_stamp = jsonObj[Interaction.INTERACTION_TIME_STAMP]
    self._duration = jsonObj[Interaction.INTERACTION_DURATION]
    self._coords = Coords(jsonObj[Interaction.INTERACTION_COORDS])

  @staticmethod
  def validate_interaction(jsonObj, logger=None):
    """Return true if the json represents a valid interaction object

    Parameters:
    jsonObj - The json object to be validated
    """
    # Attempt to parse the objects, exceptions represent invalid objects
    logger = logging.getLogger()
    logger.debug("Validating posted json data, %s" % (jsonObj))
    try:
      int(jsonObj[Interaction.INTERACTION_USER_ID])
      logger.debug("User id validated")
      float(jsonObj[Interaction.INTERACTION_TIME_STAMP])
      logger.debug("Timestamp validated")
      int(jsonObj[Interaction.INTERACTION_DURATION])
      logger.debug("Duration validated")
      float(jsonObj[Interaction.INTERACTION_COORDS][Coords.COORDS_LATITUDE])
      logger.debug("Latitude validated")
      float(jsonObj[Interaction.INTERACTION_COORDS][Coords.COORDS_LONGITUDE])
      logger.debug("Longitude validated")
      logger.debug("Coords validated")
    except (KeyError, ValueError):
      return False
    return True