#############################################################################
# Author: parenti
# Created on December 11, 2019, 12:02 PM
# Copyright (C) European XFEL GmbH Hamburg. All rights reserved.
#############################################################################
from karabo.common.scenemodel.api import (
    BoxLayoutModel, DisplayCommandModel, DisplayLabelModel,
    DisplayStateColorModel, DoubleLineEditModel, EvaluatorModel,
    LabelModel, LineModel, SceneModel, WebCamGraphModel, write_scene
)


def get_scene(deviceId):
    scene0 = DisplayStateColorModel(
        height=31.0, keys=[
            f'{deviceId}.state'], parent_component='DisplayComponent',
        show_string=True, width=180.0, x=590.0, y=10.0)
    scene1 = WebCamGraphModel(
        colormap='viridis', height=455.0,
        keys=[f'{deviceId}.output.schema.data.image'],
        parent_component='DisplayComponent', width=461.0, x=10.0, y=60.0)
    scene20 = LabelModel(
        font='Source Sans Pro,11,-1,5,75,0,0,0,0,0',
        foreground='#000000', height=31.0,
        parent_component='DisplayComponent', text='DeviceID',
        width=68.0, x=10.0, y=10.0)
    scene21 = DisplayLabelModel(
        font_size=10, font_weight='bold', height=31.0,
        keys=[f'{deviceId}.deviceId'],
        parent_component='DisplayComponent',
        width=383.0, x=78.0, y=10.0)
    scene2 = BoxLayoutModel(
        height=31.0, width=451.0,
        x=10.0, y=10.0, children=[scene20, scene21])
    scene3 = LabelModel(
        font='Source Sans Pro,11,-1,5,75,0,0,0,0,0', foreground='#000000',
        height=31.0, parent_component='DisplayComponent', text='State',
        width=51.0, x=530.0, y=10.0)
    scene4 = LineModel(
        stroke='#000000', stroke_width=2.0,
        x=10.0, x1=10.0, x2=770.0, y=50.0, y1=50.0, y2=50.0)
    scene5 = LabelModel(
        font='Source Sans Pro,10,-1,5,50,0,0,0,0,0',
        foreground='#000000', height=31.0,
        parent_component='DisplayComponent', text='Camera Frame Rate',
        width=116.0, x=510.0, y=80.0)
    scene6 = LineModel(
        stroke='#000000', stroke_width=2.0,
        x=490.0, x1=490.0, x2=770.0, y=280.0, y1=280.0, y2=280.0)
    scene70 = LabelModel(
        font='Source Sans Pro,10,-1,5,50,0,0,0,0,0',
        foreground='#000000', height=27.0,
        parent_component='DisplayComponent', text='Exposure Time',
        width=90.0, x=490.0, y=290.0)
    scene710 = DisplayLabelModel(
        font_size=10, height=27.0, keys=[f'{deviceId}.exposureTime'],
        parent_component='DisplayComponent', width=86.0, x=580.0, y=290.0)
    scene711 = DoubleLineEditModel(
        height=27.0, keys=[f'{deviceId}.exposureTime'],
        parent_component='EditableApplyLaterComponent',
        width=85.0, x=666.0, y=290.0)
    scene71 = BoxLayoutModel(
        height=27.0, width=171.0,
        x=580.0, y=290.0, children=[scene710, scene711])
    scene7 = BoxLayoutModel(
        height=27.0, width=261.0,
        x=490.0, y=290.0, children=[scene70, scene71])
    scene8 = EvaluatorModel(
        expression='"{:.2f}".format(x)', font_size=11, font_weight='bold',
        height=31.0, keys=[f'{deviceId}.frameRate'],
        parent_component='DisplayComponent', width=85.0, x=626.0, y=80.0)
    scene9 = DisplayCommandModel(
        height=37.0, keys=[f'{deviceId}.reset'],
        parent_component='DisplayComponent',
        width=151.0, x=480.0, y=190.0)
    scene100 = DisplayCommandModel(
        height=37.0, keys=[f'{deviceId}.acquire'],
        parent_component='DisplayComponent',
        width=151.0, x=480.0, y=150.0)
    scene101 = DisplayCommandModel(
        height=37.0, keys=[
            f'{deviceId}.stop'],
        parent_component='DisplayComponent',
        width=151.0, x=631.0, y=150.0)
    scene10 = BoxLayoutModel(
        height=37.0, width=302.0,
        x=480.0, y=150.0, children=[scene100, scene101])
    scene11 = LabelModel(
        font='Source Sans Pro,11,-1,5,75,0,0,0,0,0', height=22.0,
        parent_component='DisplayComponent', text='Parameters',
        width=86.0, x=494.0, y=249.0)
    scene = SceneModel(
        height=530.0, width=800.0, children=[
            scene0, scene1, scene2, scene3, scene4, scene5,
            scene6, scene7, scene8, scene9, scene10, scene11])
    return write_scene(scene)
