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
    frame = file["Frame"]["TheFrame"]
    metadata = {}
    for col in frame.dtype.fields.keys():
        metadata[col] = frame[col]

    if "Date" in metadata:
        metadata["Date"] = datetime.datetime.strptime(
            metadata["Date"].decode(), "%d-%b-%Y %H:%M:%S"
        )
    return metadata


def read_ch_data(file, group):
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
    if type(file) != h5py.File:
        file = h5py.File(file, "r")

    metadata = {}
    metadata["Oscilloscope"] = get_frame(file)
    data = pd.DataFrame()
    for ch in file["Waveforms"]:
        group = file["Waveforms"][ch]
        data[ch] = read_ch_data(file, group)
        metadata[ch] = dict(group.attrs)
    metadata = updates_bytes_to_str_recursive(metadata)
    return data, metadata


def updates_bytes_to_str_recursive(metadata):
    for key, value in metadata.items():
        if isinstance(value, collections.abc.Mapping):
            metadata[key] = updates_bytes_to_str_recursive(value)
        elif isinstance(value, bytes):
            metadata[key] = value.decode()
    return metadata
