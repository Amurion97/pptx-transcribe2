import win32com.client as win32
import pythoncom
import librosa


def get_length(pptx_path: str):
    pythoncom.CoInitialize()
    powerpoint = win32.gencache.EnsureDispatch('PowerPoint.Application')
    presentationInstance = powerpoint.Presentations.Open(pptx_path, True, True, False)
    results = []
    if presentationInstance is not None:
        numOfSlides = presentationInstance.Slides.Count
        for i in range(numOfSlides):
            print(f'Getting notes and shapes\' info from Slide {i}')
            slide = presentationInstance.Slides.Item(i + 1)
            print(f'This slide has {slide.Shapes.Count} shapes')
            for shape in slide.Shapes:
                if shape.Type == 16:  # If shape is a media (video) object
                    print(f'Slide {i} has video of type {shape.MediaType}')
                    results.append(shape.MediaFormat.Length)
    del presentationInstance
    return results

def get_audio_length(file: str):
    return librosa.get_duration(path=file)