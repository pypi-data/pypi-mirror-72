from wowpy.livestreams import LiveStream
from wowpy.recordings import Recording
from wowpy.transcoders import Transcoder
from wowpy.constants import logger
from wowpy.exceptions import DeleteRecordingException

class Mapper:

  @classmethod
  def map_live_streams(cls):
    document_batch = []
    live_streams = LiveStream.get_live_streams()
    for live_stream in live_streams:
      live_stream_id = live_stream['id']
      live_stream_name = live_stream['name']
      document = {
        'live_stream_name': live_stream_name,
        'live_stream_id': live_stream_id
      }
      document_batch.append(document)
    return document_batch
    
  @classmethod
  def map_recordings(cls):
    document_batch = []
    recordings = Recording.get_recordings()
    for recording in recordings:
      try:
        recording_id = recording['id']
        transcoder_id = recording['transcoder_id']
        transcoder_name = Transcoder.get_transcoder(transcoder_id)
        document = {
          'transcoder_id': transcoder_id,
          'transcoder_name': transcoder_name,
          'recording_id': recording_id
        }
        document_batch.append(document)
      except DeleteRecordingException as err:
        logger.warning(err)
    return document_batch
