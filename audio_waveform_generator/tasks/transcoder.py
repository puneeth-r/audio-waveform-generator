from audio_waveform_generator.tasks.static import TempColumns
import subprocess
import shlex
from pathlib import Path
import os
import shutil
import stat


def transcode_as_wav_pcm32(source_audio_path: str):
    """
    :param source_audio_path: str
    :return: str transcoded wav file path
    Transcodes the input audio file into PCM-32le formatted wav audio
    """
    with open(source_audio_path, 'rb') as f:
        content = f.read()
    path = prepare_ffmpeg()
    source_suffix = Path(source_audio_path).suffix
    temp_path = path + f"{TempColumns.TEMP_VOICE_FILE_PREFIX}{source_suffix}"
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(content)
    wav_path = path + TempColumns.TEMP_VOICE_FILE_PREFIX
    subprocess.run(shlex.split(f"{path}/ffmpeg -y -i {temp_path} -c:a pcm_s32le {wav_path}"))
    delete_temp_file(temp_path)
    return wav_path


def delete_temp_file(file: str):
    """
    :param file: str
    :return: None
    Deletes temp file if it exists
    """
    if os.path.exists(file):
        os.remove(file)


def prepare_ffmpeg() -> str:
    """
    :return: str
    """
    path = '/tmp'
    ffmpeg_bin = path + '/ffmpeg'
    shutil.copyfile(os.getcwd() + '/ffmpeg_exec', ffmpeg_bin)
    os.chmod(ffmpeg_bin, os.stat(ffmpeg_bin).st_mode | stat.S_IEXEC)
    return path
