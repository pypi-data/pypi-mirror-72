import collections.abc
import datetime
import h5py
import pandas as pd


def find_available_channels(file):
    if type(file) != h5py.File:
        file = h5py.File(file, "r")
    available_channels = {}
    for ch in file["Waveforms"].keys():
        ch_type = ch.split()[0]
        ch_num = int(ch.split()[1])
        available_channels[ch_type] = available_channels.get(ch_type, []) + [ch_num]
    return available_channels


def get_frame(file):
    """Return a dictionary with the composite file's Frame metadata"""
    if type(file) != h5py.File:
        file = h5py.File(file, "r")
    frame = file["Frame"]["TheFrame"]
    metadata = {}
    for col in frame.dtype.fields.keys():
        metadata[col] = frame[col]
    if "Date" in metadata:
        metadata["Date"] = datetime.datetime.strptime(
            metadata["Date"].decode(), "%d-%b-%Y %H:%M:%S"
        )
    return metadata


def read_ch_data(group):
    """Return a Series containing data from a single channel"""
    x_inc = group.attrs["XInc"]
    x_org = group.attrs["XOrg"]
    y_inc = group.attrs.get("YInc", 1)
    y_org = group.attrs.get("YOrg", 0)
    if group.attrs["NumSegments"] == 0:
        y_data = y_inc * list(group.values())[0][()] + y_org
        x_data = x_inc * range(0, len(y_data)) + x_org
    else:
        raise AttributeError("Segmented memory is not supported")
    return pd.Series(index=x_data, data=y_data)


def to_dataframe(file):
    """Return a DataFrame with one column per channel of data"""
    if type(file) != h5py.File:
        file = h5py.File(file, "r")
    data = pd.DataFrame()
    for ch in file["Waveforms"]:
        group = file["Waveforms"][ch]
        data[ch] = read_ch_data(group)
    return data


def get_metadata(file, convert_bytes=True):
    if type(file) != h5py.File:
        file = h5py.File(file, "r")
    metadata = {}
    metadata = {ch: dict(file["Waveforms"][ch].attrs) for ch in file["Waveforms"]}
    metadata["Oscilloscope"] = get_frame(file)
    if convert_bytes:
        metadata = update_bytes_to_str_recursive(metadata)
    return metadata


def update_bytes_to_str_recursive(metadata):
    """Recursively scan a dict, converting any byte values to str"""
    for key, value in metadata.items():
        if isinstance(value, collections.abc.Mapping):
            metadata[key] = update_bytes_to_str_recursive(value)
        elif isinstance(value, bytes):
            metadata[key] = value.decode()
    return metadata
