import robomaster
from robomaster import robot
import time

tof_distance = None
MAX_SPEED = 1
WALL_DISTANCE_THRESHOLD = 300


def tof_data_handler(sub_info):
    global tof_distance, status_tof
    tof_distance = sub_info[0]
    if 250 < tof_distance < 350:
        status_tof = True
    else:
        status_tof = False
    # print(f"ToF distance: {tof_distance} mm")
    print(f"status_tof {status_tof}")


print("****************************")


def sub_data_handler(sub_info):
    global io_data, status_io
    io_data, ad_data = sub_info
    if io_data[0] == 1:
        status_io = True
    else:
        status_io = False
    # print(f"front sensor: {io_data[0]}")
    print(f"status_io {status_io}")


if __name__ == "__main__":
    ep_robot = robot.Robot()
    print("Initializing robot...")
    ep_robot.initialize(conn_type="ap")
    time.sleep(2)  # รอ 2 วินาทีหลังการเชื่อมต่อ

    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    print("Subscribing to ToF data...")
    ep_sensor.sub_distance(freq=10, callback=tof_data_handler)
    print("Subscribing to adapter data...")
    ep_sensor_adaptor.sub_adapter(freq=10, callback=sub_data_handler)

    print("Recentering gimbal...")
    ep_gimbal.recenter().wait_for_completed()

    try:

        print("Starting main loop...")
        while True:
            adc_1 = ep_sensor_adaptor.get_adc(id=1, port=1)
            ep_gimbal.moveto(
                pitch=0, yaw=90, pitch_speed=0, yaw_speed=30
            ).wait_for_completed()
            time.sleep(0.5)

            if tof_distance is None:
                print("Waiting for sensor data...")
                time.sleep(1)
                continue

            gap = abs(WALL_DISTANCE_THRESHOLD - tof_distance)
            walk_y = gap / 1000

            if status_io == False:
                if tof_distance < WALL_DISTANCE_THRESHOLD - 50:
                    print("Turn left")
                    ep_chassis.move(
                        x=0, y=-walk_y, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                elif tof_distance > WALL_DISTANCE_THRESHOLD + 50:
                    print("Turn right")
                    ep_chassis.move(
                        x=0, y=walk_y, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                else:
                    print("Drive forward")
                    ep_chassis.move(
                        x=0.1, y=0, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
            elif status_io == True:
                if tof_distance < WALL_DISTANCE_THRESHOLD - 50:
                    print("Turn left")
                    ep_chassis.move(
                        x=0, y=-walk_y, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                elif tof_distance > WALL_DISTANCE_THRESHOLD + 50:
                    print("Turn right")
                    ep_chassis.move(
                        x=0, y=walk_y, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                elif status_tof == True:
                    print("Left")
                    ep_chassis.move(
                        x=0, y=0, z=90, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                    ep_gimbal.recenter().wait_for_completed()
                    status_io == False

            # if status_tof == Truwe

            time.sleep(2)

    except KeyboardInterrupt:
        print("Program stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up...")
        ep_sensor.unsub_distance()
        ep_sensor.unsub_adapter()
        ep_chassis.drive_speed(x=0, y=0, z=0)
        ep_robot.close()
        print("Program ended.")
