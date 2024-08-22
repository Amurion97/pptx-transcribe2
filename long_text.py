from google.cloud import speech
from upload import upload_name

dir2='D:\\Download\\testststs.wav'
uri=f'gs://aimetalk/{upload_name}'

def transcribe_gcs(gcs_uri: str) -> str:
    """Asynchronously transcribes the audio file from Cloud Storage
    Args:
        gcs_uri: The Google Cloud Storage path to an audio file.
            E.g., "gs://storage-bucket/file.flac".
    Returns:
        The generated transcript from the audio file provided.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ja-JP",
        enable_automatic_punctuation=True,
        audio_channel_count=2,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    # response = operation.result(timeout=90)
    response = operation.result(timeout=1000)

    transcript_builder = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    rs = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # transcript_builder.append(f"\nTranscript: {result.alternatives[0].transcript}")
        rs.append(result.alternatives[0].transcript)
        # transcript_builder.append(f"\nConfidence: {result.alternatives[0].confidence}")

    # transcript = "".join(transcript_builder)
    # print(transcript)

    return "".join(rs)

if __name__ == '__main__':
    print(transcribe_gcs(uri))