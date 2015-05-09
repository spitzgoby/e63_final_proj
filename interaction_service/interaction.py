import logging

class Coords(object):
  COORDS_LATITUDE = 'latitude'
  COORDS_LONGITUDE = 'longitude'

  def __init__(self, jsonObj):
    self.latitude = float(jsonObj[Coords.COORDS_LATITUDE])
    self.longitude = float(jsonObj[Coords.COORDS_LONGITUDE])

class Interaction(object):

  INTERACTION_USER_ID = 'user_id'
  INTERACTION_TIME_STAMP = 'time_stamp'
  INTERACTION_DURATION = 'duration'
  INTERACTION_COORDS = 'coords'

  def __init__(self, jsonObj):
    self.user_id = jsonObj[Interaction.INTERACTION_USER_ID]
    self.time_stamp = float(jsonObj[Interaction.INTERACTION_TIME_STAMP])
    self.duration = float(jsonObj[Interaction.INTERACTION_DURATION])
    self.coords = Coords(jsonObj[Interaction.INTERACTION_COORDS])

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
      jsonObj[Interaction.INTERACTION_USER_ID]
      logger.debug("User id validated")
      float(jsonObj[Interaction.INTERACTION_TIME_STAMP])
      logger.debug("Timestamp validated")
      float(jsonObj[Interaction.INTERACTION_DURATION])
      logger.debug("Duration validated")
      float(jsonObj[Interaction.INTERACTION_COORDS][Coords.COORDS_LATITUDE])
      logger.debug("Latitude validated")
      float(jsonObj[Interaction.INTERACTION_COORDS][Coords.COORDS_LONGITUDE])
      logger.debug("Longitude validated")
      logger.debug("Coords validated")
    except (KeyError, ValueError):
      return False
    return True
