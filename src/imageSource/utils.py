import numpy as np


def unpack_mono12_packed(in_buffer, lock=None):
    """
    Unpack the input MONO12PACKED data to MONO12.

    In MONO12PACKED pixel data format, every 3 bytes contain data for 2 pixels,
    according to the following table:

    +------+---------------------+
    | Byte |  Pixel - Data bits  |
    +======+=====================+
    |  B0  |      P0 11...4      |
    +------+---------------------+
    |  B1  | P1 3...0 | P0 3...0 |
    +------+---------------------+
    |  B2  |      P1 11...4      |
    +------+---------------------+
    |  ... |         ...         |
    +------+---------------------+
    |  Bm  |      Pn 11...4      |
    +------+---------------------+

    :param in_buffer: the input packed data
    :param lock: an optional lock
    :return: the output unpacked data
    """
    if lock:
        lock.acquire()

    dataframe_size = 3
    buf_size = in_buffer.nbytes

    if buf_size % dataframe_size:
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


def unpack_mono_xx_p(in_buffer, bpp, lock=None):
    """
    Unpack the input MonoXXp data to MONO12, where XX is usually 10 or 12.

    Use with caution! The function can be quite slow on large images.

    In MONOXXp pixel data format, XX-bit pixel data are packed, with no
    padding bits in between. Padding 0s are added to the MSB if needed.
    For example Mono10p pixels are packed this way:

    +------+---------------------+
    | Byte |  Pixel - Data bits  |
    +======+=====================+
    |  B0  |      P0 7...0       |
    +------+---------------------+
    |  B1  | P1 5...0 | P0 9...8 |
    +------+---------------------+
    |  B2  | P2 3...0 | P1 9...6 |
    +------+---------------------+
    |  B3  | P4 1...0 | P3 9...4 |
    +------+---------------------+
    |  ... |         ...         |
    +------+---------------------+

    :param data: the input packed data
    :param bpp: the bits-per-pixel, normally 10 or 12
    :param lock: an optional lock
    :return: the output unpacked data
    """
    if lock:
        lock.acquire()

    if bpp < 9 or bpp > 15:
        raise ValueError(f"Invalid bpp value: {bpp}. It must be in [9, 15].")

    buf_size = in_buffer.nbytes
    mask = 0xFFFF >> (16 - bpp)
    image_size = int(buf_size * 8 / bpp)  # size of the unpacked data

    packed = np.ndarray(shape=(buf_size), dtype=np.uint8, buffer=in_buffer)
    unpacked = np.zeros(shape=(image_size), dtype=np.uint16)

    bits = 0
    px = 0
    while px < image_size:
        idx = bits // 8
        shift = bits % 8

        unpacked[px] = (
            (packed[idx] | packed[idx + 1] << 8) >> shift) & mask

        bits += bpp
        px += 1

    if lock:
        lock.release()

    return unpacked.data


def unpack_mono10_p(in_buffer, lock=None):
    return unpack_mono_xx_p(in_buffer, 10, lock)


def unpack_mono12_p(in_buffer, lock=None):
    # XXX A faster implemenation could be written, starting from the
    # unpack_mono12_packed code
    return unpack_mono_xx_p(in_buffer, 12, lock)
