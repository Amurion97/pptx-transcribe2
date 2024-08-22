from pydub import AudioSegment

# m4a_file = 'sample-1.m4a' # I have downloaded sample audio from this link https://getsamplefiles.com/sample-audio-files/m4a
# wav_filename = 'output.wav'
def convert_m4a_to_wav(m4a_file: str, wav_filename: str):
    # sound = AudioSegment.from_file(upload_dir, format='m4a')
    sound = AudioSegment.from_file(m4a_file, format='m4a')
    # file_handle = sound.export(wav_filename, format='wav')
    file_handle = sound.export(wav_filename, format='wav')