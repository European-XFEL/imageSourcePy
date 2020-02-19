#############################################################################
# Author: parenti
# Created on December 11, 2019, 12:02 PM
# Copyright (C) European XFEL GmbH Hamburg. All rights reserved.
#############################################################################

from karabo.common.scenemodel.api import (
    BoxLayoutModel, DisplayCommandModel, DisplayLabelModel,
    DisplayStateColorModel, DoubleLineEditModel, EvaluatorModel,
    FixedLayoutModel, LabelModel, RectangleModel, SceneModel,
    WebCamGraphModel, write_scene
)


def get_scene(device_id):
    scene0 = RectangleModel(
        height=452.0, stroke='#000000', width=814.0, x=6.0, y=16.0)
    scene1 = LabelModel(
        font='Sans Serif,11,-1,5,75,0,0,0,0,0', foreground='#000000',
        height=27.0, parent_component='DisplayComponent', text='DeviceID',
        width=74.0, x=60.0, y=31.0)
    scene2 = EvaluatorModel(
        expression="x.split('/')[-1]", height=27.0,
        keys=[f'{device_id}.deviceId'], parent_component='DisplayComponent',
        width=480.0, x=140.0, y=31.0)
    scene300 = DoubleLineEditModel(
        height=32.0, keys=[f'{device_id}.exposureTime'],
        parent_component='EditableApplyLaterComponent', width=235.0,
        x=575.0, y=370.0)
    scene301 = DisplayLabelModel(
        height=32.0, keys=[f'{device_id}.exposureTime'],
        parent_component='DisplayComponent', width=235.0, x=575.0, y=411.0)
    scene302 = LabelModel(
        font='Sans Serif,11,-1,5,50,0,0,0,0,0', foreground='#000000',
        height=27.0, parent_component='DisplayComponent', text='Exposure Time',
        width=115.0, x=450.0, y=371.0)
    scene30 = FixedLayoutModel(
        height=32.0, width=366.0, x=456.0, y=370.0,
        children=[scene300, scene301, scene302])
    scene310 = LabelModel(
        font='Sans Serif,11,-1,5,50,0,0,0,0,0', foreground='#000000',
        height=28.0, parent_component='DisplayComponent', width=10.0)
    scene311 = DisplayCommandModel(
        height=24.0, keys=[f'{device_id}.acquire'],
        parent_component='DisplayComponent', width=69.0)
    scene31 = BoxLayoutModel(
        height=52.0, width=330.0, x=465.0, y=133.0,
        children=[scene310, scene311])
    scene320 = LabelModel(
        font='Sans Serif,11,-1,5,50,0,0,0,0,0', foreground='#000000',
        height=28.0, parent_component='DisplayComponent', width=10.0)
    scene321 = DisplayCommandModel(
        height=24.0, keys=[f'{device_id}.trigger'],
        parent_component='DisplayComponent', width=67.0)
    scene32 = BoxLayoutModel(
        height=51.0, width=330.0, x=465.0, y=185.0,
        children=[scene320, scene321])
    scene330 = LabelModel(
        font='Sans Serif,11,-1,5,50,0,0,0,0,0', foreground='#000000',
        height=28.0, parent_component='DisplayComponent', width=10.0)
    scene331 = DisplayCommandModel(
        height=24.0, keys=[f'{device_id}.stop'],
        parent_component='DisplayComponent', width=47.0)
    scene33 = BoxLayoutModel(
        height=52.0, width=330.0, x=465.0, y=236.0,
        children=[scene330, scene331])
    scene340 = LabelModel(
        font='Sans Serif,11,-1,5,50,0,0,0,0,0', foreground='#000000',
        height=28.0, parent_component='DisplayComponent', width=10.0)
    scene341 = DisplayCommandModel(
        height=24.0, keys=[f'{device_id}.reset'],
        parent_component='DisplayComponent', width=55.0)
    scene34 = BoxLayoutModel(
        height=51.0, width=330.0, x=465.0, y=288.0,
        children=[scene340, scene341])
    scene35 = DisplayStateColorModel(
        height=30.0, keys=[f'{device_id}.state'],
        parent_component='DisplayComponent', width=310.0, x=480.0, y=75.0)
    scene36 = DisplayLabelModel(
        height=30.0, keys=[f'{device_id}.state'],
        parent_component='DisplayComponent', width=310.0, x=480.0, y=75.0)
    scene37 = WebCamGraphModel(
        colormap='viridis', height=400.0,
        keys=[f'{device_id}.output.schema.data.image'],
        parent_component='DisplayComponent', width=450.0, x=11.0, y=76.0)
    scene3 = FixedLayoutModel(
        height=365.0, width=810.0, x=11.0, y=76.0,
        children=[scene30, scene31, scene32, scene33, scene34, scene35,
                  scene36, scene37])
    scene = SceneModel(
        height=484.0, width=844.0, children=[scene0, scene1, scene2, scene3])
    return write_scene(scene)
