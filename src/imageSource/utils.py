import numpy as np


def unpack_mono12_packed(in_buffer, lock=None):
    """
    Unpack the input MONO12PACKED data to MONO12.

    In MONO12PACKED pixel data format, every 3 bytes contain data for 2 pixels,
    according to the following table:

    +------+---------------------+
    | Byte |  Pixel - Data bits  |
    +------+---------------------+
    |  B0  |      P0 11...4      |
    |  B1  | P1 3...0 | P0 3...0 |
    |  B2  |      P1 11...4      |
    +------+---------------------+


    :param in_buffer: the input packed data
    :param lock: an optional lock
    :return: the output unpacked data
    """
    if lock:
        lock.acquire()

    dataframe_size = 3
    buf_size = in_buffer.nbytes

    if in_buffer.nbytes % dataframe_size:
        raise RuntimeError(f"{buf_size} must be multiple of {dataframe_size}")

    height = buf_size // 3
    packed = np.ndarray(shape=(height, 3), dtype=np.uint8, buffer=in_buffer)
    unpacked = np.zeros(shape=(height, 4), dtype=np.uint8)

    unpacked[:, 0] = (packed[:, 0] << 4) + (packed[:, 1] & 0xF)
    unpacked[:, 1] = packed[:, 0] >> 4
    unpacked[:, 2] = (packed[:, 1] >> 4) + (packed[:, 2] << 4)
    unpacked[:, 3] = (packed[:, 2] >> 4)

    if lock:
        lock.release()

    return unpacked.data
