import scipy.io
import scipy.io.wavfile
import numpy as np
import scipy.signal as sps
from audio_waveform_generator.tasks.transcoder import transcode_as_wav_pcm32, delete_temp_file
from audio_waveform_generator.tasks.io import plot_waveform, write_json_output


NUMBER_OF_SAMPLES = 2000
# audio_file = "/Users/puneethr/Downloads/zoom_test/test_2/attachments/93048b2d-ee8b-4b54-98ba-62fdbff7ba63/call_recording_93048b2d-ee8b-4b54-98ba-62fdbff7ba63_20220628090903.mp3"
# audio_file = "/Users/puneethr/Downloads/19409a8e-6e35-46c8-8954-3be734ab531a_(20211210155940142)_updated.wav"
audio_file = "/Users/puneethr/Downloads/f6bc43cd-1a34-472d-9e5c-7b257aa01fe8-1656344547836.wav"


def main(source_audio_path):
    try:
        if source_audio_path.endswith(".wav"):
            sample_rate, audio_buffer = scipy.io.wavfile.read(source_audio_path)
        else:
            audio_path = transcode_as_wav_pcm32(source_audio_path=source_audio_path)
            sample_rate, audio_buffer = scipy.io.wavfile.read(audio_path)
            delete_temp_file(audio_path)
    except ValueError:
        audio_path = transcode_as_wav_pcm32(source_audio_path=source_audio_path)
        sample_rate, audio_buffer = scipy.io.wavfile.read(audio_path)
        delete_temp_file(audio_path)

    duration = audio_buffer.shape[0] / sample_rate

    # resample to limit number of samples to NUMBER_OF_SAMPLES
    data = sps.resample(audio_buffer, NUMBER_OF_SAMPLES)
    time_vector = np.linspace(0, duration, NUMBER_OF_SAMPLES)

    # normalize values so that it is in the range 0-1
    normalized_time = normalize_nd_array(time_vector)
    normalized_audio_buffer = normalize_nd_array(data)

    # plot waveform
    plot_waveform(normalized_time, normalized_audio_buffer)

    # write json output
    write_json_output(time_data=normalized_time, audio_data=normalized_audio_buffer, duration=duration)


def normalize_nd_array(array: np.ndarray) -> np.ndarray:
    """
    :param array: np.ndarray
    :return: np.ndarray
    Normalizes input ndarray to a range (0-1) and returns the normalized array.
    Base Formula used to normalize:
    ((Input - InputLow) / (InputHigh - InputLow)) * (OutputHigh - OutputLow) + OutputLow
    Reference: https://gamedev.stackexchange.com/questions/33441/how-to-convert-a-number-from-one-min-max-set-to-another-min-max-set/33445#33445
    """
    min_x = np.min(array)
    max_x = np.max(array)
    normalized_array = np.array([(x - min_x) / (max_x - min_x) for x in array])
    return normalized_array


main(audio_file)
