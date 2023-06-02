#############################################################################
# Author: parenti
# Created on November 27, 2019, 02:12 PM
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################

from karabo.bound import KARABO_CLASSINFO, VECTOR_STRING_ELEMENT, Hash
from karabo.common.api import KARABO_SCHEMA_DISPLAY_TYPE_SCENES as DT_SCENES

from .ImageSource import ImageSource
from .scenes import get_scene


@KARABO_CLASSINFO("CameraImageSource", "2.7")
class CameraImageSource(ImageSource):
    """
    Base class for camera devices.

    It is derived from the ImageSource class, and provides a default scene.
    """

    @staticmethod
    def expectedParameters(expected):
        (
            VECTOR_STRING_ELEMENT(expected).key('availableScenes')
            .setSpecialDisplayType(DT_SCENES)
            .readOnly().initialValue(['scene'])
            .commit()
        )

    def __init__(self, configuration):
        # always call PythonDevice constructor first!
        super(CameraImageSource, self).__init__(configuration)
        self.KARABO_SLOT(self.requestScene)

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
            payload.set('data', get_scene(self.getInstanceId()))
        self.reply(Hash('type', 'deviceScene', 'origin', self.getInstanceId(),
                        'payload', payload))
