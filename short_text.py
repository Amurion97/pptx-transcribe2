from google.cloud import speech
dir2='D:\\Download\\testststs.wav'

def transcribe_file_with_auto_punctuation(audio_file: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file with auto punctuation enabled.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
    Returns:
        speech.RecognizeResponse: The response containing the transcription results.
    """
    client = speech.SpeechClient()
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ja-JP",
        enable_automatic_punctuation=True,
        audio_channel_count=2,
    )

    response = client.recognize(config=config, audio=audio)
    rs = ''
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")
        rs = rs + alternative.transcript

    return rs
if __name__ == '__main__':
    transcribe_file_with_auto_punctuation(dir2)