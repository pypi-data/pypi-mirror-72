from wowpy.constants import WSC_API_ENDPOINT, logger
from wowpy.utils import wowza_query

class Recording:
  recordings_base = WSC_API_ENDPOINT + 'recordings'
  recordings_single = recordings_base + '/{recording_id}'         # recording delete, get

  @classmethod
  def get_recording(cls, recording_id):
    # Get recording info
    endpoint = cls.recordings_single.format(
      recording_id=recording_id
    )
    response = wowza_query(endpoint=endpoint, method='get')
    recording = response['recording']
    logger.debug('Recording info is {}'.format(recording))
    return recording