import numpy as np
from audio_waveform_generator.tasks.static import TempColumns, TargetColumns, OUTPUT_FILE_PATH
import matplotlib.pyplot as plt
import json
import os
import shutil
import stat

def plot_waveform(x: np.ndarray, y: np.ndarray) -> None:
    """
    :param x: np.ndarray
    :param y: np.ndarray
    :return: None
    Plots waveform
    """
    plt.plot(x, y)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.show()


def write_json_output(time_data: np.ndarray, audio_data: np.ndarray, duration: float) -> None:
    """
    :param time_data: np.ndarray
    :param audio_data: np.ndarray
    :param duration: float
    :return: None
    Writes waveform data as a json output file
    """
    result = []
    for time, audio_buffer in zip(time_data, audio_data):
        d = {TargetColumns.TIME: time, TargetColumns.AUDIO_BUFFER: audio_buffer[1] if isinstance(audio_buffer, np.ndarray) else audio_buffer}
        result.append(d)
    with open(OUTPUT_FILE_PATH, "w") as f_out:
        json.dump({TargetColumns.WAVEFORM_DATA: result, TargetColumns.DURATION_IN_SECONDS: duration}, f_out)
