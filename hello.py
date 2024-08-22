from spire.presentation import *
# import assemblyai as aai
import json

from add_punctuation import add_punctuation
from convert import convert_m4a_to_wav
from get_length import get_audio_length
from long_text import transcribe_gcs
from short_text import transcribe_file_with_auto_punctuation
from upload import upload_blob

# $env:GOOGLE_APPLICATION_CREDENTIALS="D:\Projects\PyCharm\testSpire\pythonProject1\aimetalk-gapi-key.json"

if __name__ == '__main__':
    # config = aai.TranscriptionConfig(language_code="ja",punctuate = True,format_text = True)
    # transcriber = aai.Transcriber(config=config)

    presentation = Presentation()

    folder_no = 14
    # dir = 'D:/Download/aimetalk_customer/１．情報セキュリティとは.pptx'
    # dir = 'D:/Download/aimetalk_customer/２．リスクアセスメントについて.pptx'
    # dir = 'D:/Download/aimetalk_customer/３．情報資産台帳（文書管理）.pptx'
    # dir = 'D:/Download/aimetalk_customer/１．情報セキュリティとは - Copy (2).pptx'
    # dir = 'D:/Download/aimetalk_customer/４．事業継続計画.pptx'
    # dir = 'D:/Download/aimetalk_customer/５．CSIRTとは.pptx'
    # dir = 'D:/Download/aimetalk_customer/６．マルウェア対策・脆弱性対策.pptx'
    # dir = 'D:/Download/aimetalk_customer/７．情報セキュリティマネジメントシステム（ISMS）.pptx'
    # dir = 'D:/Download/aimetalk_customer/８．メール、Web、SNSセキュリティ、アクセス管理.pptx'
    # dir = 'D:/Download/aimetalk_customer/９．ITに関わるセキュリティ対策.pptx'
    dir = 'D:/Download/aimetalk_customer/１０．その他セキュリティ全般.pptx'
    presentation.LoadFromFile(dir)

    notes = []
    is_long = []
    # Initialize a counter
    i = 1
    for slide in presentation.Slides:
        for shape in slide.Shapes:
            if isinstance(shape, IAudio):
                AudioData = shape.Data
                file_path = f"ExtractAudio_folder_no_{str(folder_no)}_{str(i)}.m4a"
                AudioData.SaveToFile(file_path)
                new_name = f"ExtractAudio_folder_no_{str(folder_no)}_{str(i)}.wav"
                convert_m4a_to_wav(file_path, new_name)

                length = get_audio_length(new_name)
                print(f'this {i} audio has length in seconds {length}')
                if length < 50:
                    is_long.append(0)
                    # file_path_short = "ExtractAudio_2_" + str(i) + ".wav"
                    # AudioData.SaveToFile(file_path_short)
                    # transcript = transcribe_file_with_auto_punctuation(file_path_short)
                    transcript = transcribe_file_with_auto_punctuation(new_name)
                    print(f'transcript of Slide {i}\n')
                    print(transcript)
                    notes.append(transcript)
                else:
                    is_long.append(1)
                    uploaded_name = f'slide_{folder_no}_audio_{i}.wav'
                    upload_blob('aimetalk', new_name, uploaded_name)
                    uri = f'gs://aimetalk/{uploaded_name}'
                    transcript = transcribe_gcs(uri)
                    print(f'long transcript of Slide {i}\n')
                    print(transcript)
                    print(f'punctuated transcript of Slide {i}\n')
                    refined = add_punctuation(transcript)
                    print(refined)
                    notes.append(refined)

                i = i + 1

                # transcript = transcriber.transcribe(file_path)
                # print(f'transcript of Slide {i}\n')
                # print(transcript.text)
                # notes.append(transcript.text)

    presentation.Dispose()

    with open(f'{folder_no}/your_file.txt', 'w', encoding='utf8') as f:
        for line in notes:
            f.write(f"{line}\n")
    with open(f'{folder_no}/data.json', 'wb') as fp:
        fp.write(json.dumps(notes, ensure_ascii=False).encode("utf8"))
    with open(f'{folder_no}/status.json', 'wb') as fp:
        fp.write(json.dumps(is_long, ensure_ascii=False).encode("utf8"))
