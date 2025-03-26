import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE

def detect_audio_quality(file_path):
    try:
        audio = mutagen.File(file_path)
        if audio is None:
            return {'format': 'Unknown', 'bitrate': None, 'lossless': False}
        if isinstance(audio, MP3):
            bitrate = getattr(audio.info, 'bitrate', None)
            if bitrate is not None:
                bitrate = int(bitrate // 1000)
            return {'format': 'MP3', 'bitrate': bitrate, 'lossless': False}
        elif isinstance(audio, FLAC):
            return {'format': 'FLAC', 'bitrate': None, 'lossless': True}
        elif isinstance(audio, WAVE):
            return {'format': 'WAV', 'bitrate': None, 'lossless': True}
        else:
            ext = file_path.split('.')[-1].lower()
            if ext in ['m4a', 'alac']:
                return {'format': ext.upper(), 'bitrate': None, 'lossless': True}
            else:
                return {'format': ext.upper(), 'bitrate': None, 'lossless': False}
    except Exception as e:
        return {'format': 'Unknown', 'bitrate': None, 'lossless': False}
# def detect_audio_quality(file_path):
#     """
#     Detects audio quality for a given file.
    
#     Returns a dictionary with:
#       - 'format': The detected audio format (e.g., 'MP3', 'FLAC', 'WAV')
#       - 'bitrate': For MP3 files, the bitrate in kbps (integer); for lossless files, None
#       - 'lossless': Boolean indicating whether the file is lossless
#     """
#     try:
#         audio = mutagen.File(file_path)
#         if audio is None:
#             return {'format': 'Unknown', 'bitrate': None, 'lossless': False}

#         # Check if the file is an MP3.
#         if isinstance(audio, MP3):
#             bitrate = getattr(audio.info, 'bitrate', None)
#             if bitrate is not None:
#                 bitrate = int(bitrate // 1000)  # Convert bps to kbps
#             return {'format': 'MP3', 'bitrate': bitrate, 'lossless': False}
        
#         # Check for FLAC (lossless).
#         elif isinstance(audio, FLAC):
#             return {'format': 'FLAC', 'bitrate': None, 'lossless': True}
        
#         # Check for WAV (typically lossless).
#         elif isinstance(audio, WAVE):
#             return {'format': 'WAV', 'bitrate': None, 'lossless': True}
        
#         # Fallback: use file extension to guess format.
#         else:
#             ext = file_path.split('.')[-1].lower()
#             if ext in ['m4a', 'alac']:
#                 # Assume ALAC or similar lossless format.
#                 return {'format': ext.upper(), 'bitrate': None, 'lossless': True}
#             else:
#                 return {'format': ext.upper(), 'bitrate': None, 'lossless': False}
#     except Exception as e:
#         # On error, return Unknown info.
#         return {'format': 'Unknown', 'bitrate': None, 'lossless': False}