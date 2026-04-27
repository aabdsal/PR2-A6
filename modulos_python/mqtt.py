from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

import paho.mqtt.client as mqtt  # type: ignore[reportMissingImports]

import RobotController as rc  # type: ignore[reportMissingImports]

broker="mqtt.dsic.upv.es"
port=1883
user="giirob"
passwd="UPV2024"
base_topic="giirob/pr2/station/"
station_name="demo"
station_commands_topic=base_topic+station_name+"/commands"
station_status_topic=base_topic+station_name+"/status"


def on_message(mqttc, obj, msg):
    payload = msg.payload.decode('utf-8')
    topic = msg.topic
    qos = msg.qos
    rc.handle_message(mqttc, topic, payload)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message

mqttc.username_pw_set(username=user, password=passwd)
mqttc.connect(broker, port, 60)
mqttc.subscribe(station_commands_topic, 0)

mqttc.publish(station_status_topic, "ready")

mqttc.loop_forever()


def handle_message(mqttc, topic, payload):

    if topic == "giirob/pr2/demo/commands":
        move_robot(payload)

def move_robot(position):
    robot = RDK.Item("myRobotUR", robolink.ITEM_TYPE_ROBOT)
    target = RDK.Item(position).setAsCartesianTarget()
    if robot.Valid() and target.Valid():
        robot.MoveJ(target)
        #robot.MoveL(target)



