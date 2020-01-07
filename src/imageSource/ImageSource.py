#############################################################################
# Author: parenti
# Created on November 27, 2019, 02:12 PM
# Copyright (C) European XFEL GmbH Hamburg. All rights reserved.
#############################################################################

from karabo.bound import (
    DaqDataType, Hash, ImageData, IMAGEDATA_ELEMENT, KARABO_CLASSINFO,
    NODE_ELEMENT, OUTPUT_CHANNEL, PythonDevice, Schema, VECTOR_STRING_ELEMENT
)

from karabo.common.api import KARABO_SCHEMA_DISPLAY_TYPE_SCENES as DT_SCENES

from .scenes import get_base_scene, get_camera_scene


@KARABO_CLASSINFO("ImageSource", "2.7")
class ImageSource(PythonDevice):
    """
    Base class for image sources.

    It provides two output channels - 'output' and 'daqOutput' - for sending
    out images, and two functions - 'update_output_schema' and
    'write_channels'.

    The function 'update_output_schema' will update the schema for the output
    channels and make it fit for the DAQ.

    The function 'write_channels' will write the input data to both the
    output channels, taking care of reshaping them for the DAQ.
    """

    @staticmethod
    def expectedParameters(expected):
        output_data = Schema()
        (
            NODE_ELEMENT(output_data).key("data")
            .displayedName("Data")
            .setDaqDataType(DaqDataType.TRAIN)
            .commit(),

            IMAGEDATA_ELEMENT(output_data).key("data.image")
            .displayedName("Image")
            .commit(),

            OUTPUT_CHANNEL(expected).key("output")
            .displayedName("Output")
            .dataSchema(output_data)
            .commit(),

            # Second output channel for the DAQ
            OUTPUT_CHANNEL(expected).key("daqOutput")
            .displayedName("DAQ Output")
            .dataSchema(output_data)
            .commit(),

            VECTOR_STRING_ELEMENT(expected).key('availableScenes')
            .setSpecialDisplayType(DT_SCENES)
            .readOnly().initialValue(['scene'])
            .commit()
        )

    def __init__(self, configuration):
        # always call PythonDevice constructor first!
        super(ImageSource, self).__init__(configuration)
        self.KARABO_SLOT(self.requestScene)

    def update_output_schema(self, shape, encoding, k_type):
        """
        Update the schema of 'output' and 'daqOutput' channels

        :param shape: the shape of image, e.g. (height, width)
        :param encoding: the encoding of the image. e.g. Encoding.GRAY
        :param k_type: the data type, e.g. Types.UINT16
        :return:
        """
        schema_update = Schema()

        def schema_update_helper(node_key, displayed_name):
            data_schema = Schema()
            (
                NODE_ELEMENT(data_schema).key("data")
                .displayedName("Data")
                .setDaqDataType(DaqDataType.TRAIN)
                .commit(),

                IMAGEDATA_ELEMENT(data_schema).key("data.image")
                .displayedName("Image")
                .setDimensions(list(shape))
                .setType(k_type)
                .setEncoding(encoding)
                .commit(),

                OUTPUT_CHANNEL(schema_update).key(node_key)
                .displayedName(displayed_name)
                .dataSchema(data_schema)
                .commit(),
            )

        schema_update_helper("output", "Output")

        # NB DAQ wants shape in CImg order, eg (width, height)
        shape = tuple(reversed(shape))
        schema_update_helper("daqOutput", "DAQ Output")

        self.appendSchema(schema_update)

    def write_channels(self, data, binning=None, bpp=None, encoding=None,
                       roi_offsets=None, timestamp=None):
        """
        Write an image to 'output' and 'daqOutput' channels

        :param data: the image data as numpy.ndarray
        :param binning: the image binning, e.g. (1, 1)
        :param bpp: the bits-per-pixel, e.g. 12
        :param encoding: the image encoding, e.g. Encoding.GRAY
        :param roi_offsets: the ROI offset, e.g. (0, 0)
        :param timestamp: the image timestamp - if none the current timestamp
        will be used
        :return:
        """

        def write_channel(node_key):
            image_data = ImageData(data)
            if binning:
                image_data.setBinning(binning)
            if bpp:
                image_data.setBitsPerPixel(bpp)
            if encoding:
                image_data.setEncoding(encoding)
            if roi_offsets:
                image_data.setROIOffsets(roi_offsets)
            self.writeChannel(node_key, Hash("data.image", image_data),
                              timestamp)

        write_channel('output')

        # Reshaped image for DAQ
        # NB DAQ wants shape in CImg order, eg (width, height)
        data = data.reshape(*reversed(data.shape))
        write_channel('daqOutput')

    def get_scene(self, device_id):
        return get_base_scene(device_id)

    def requestScene(self, params):
        """Fulfill a scene request from another device.

         NOTE: Required by Scene Supply Protocol, which is defined in KEP 21.
               The format of the reply is also specified there.

        :param params: A `Hash` containing the method parameters
        """
        payload = Hash('success', False)

        name = params.get('name', default='')
        if name == 'scene':
            payload.set('success', True)
            payload.set('name', name)
            payload.set('data', self.get_scene(self.getInstanceId()))
        self.reply(Hash('type', 'deviceScene', 'origin', self.getInstanceId(),
                        'payload', payload))


@KARABO_CLASSINFO("CameraImageSource", "2.7")
class CameraImageSource(ImageSource):
    """
    Base class for camera devices.

    It is derived from the ImageSource class.
    """

    def get_scene(self, device_id):
        return get_camera_scene(device_id)