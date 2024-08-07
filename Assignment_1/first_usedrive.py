import robomaster
from robomaster import robot
import time

tof_distance = None
adc_1 = None
MAX_SPEED = 2
WALL_DISTANCE_THRESHOLD = 200


def tof_data_handler(sub_info):
    global tof_distance, status_tof
    tof_distance = sub_info[0]
    if 150 < tof_distance < 250:
        status_tof = True
    else:
        status_tof = False
    # print(f"ToF distance: {tof_distance} mm")

    global adc_1, status_ss_1
    adc_1 = ep_sensor_adaptor.get_adc(id=1, port=2)
    adc_2 = (adc_1 * 3) / 1023  # process to cm unit

    if adc_2 > 1.4:
        adc_cm = (adc_2 - 4.2) / -0.31
    elif 1.4 >= adc_2 >= 0.6:
        adc_cm = (adc_2 - 2.03) / -0.07
    else:
        adc_cm = (adc_2 - 0.95) / -0.016

    print("distance from front wall:", adc_cm, "cm")

    if 16.5 > adc_cm > 5.5:
        status_ss_1 = True
    else:
        status_ss_1 = False
    # print(f"ToF distance: {adc_1} mm")
    print(f"status_tof {status_tof} , status_ss_1 {status_ss_1}")
    time.sleep(1)


print("****************************")

if __name__ == "__main__":
    ep_robot = robot.Robot()
    print("Initializing robot...")
    ep_robot.initialize(conn_type="ap")
    time.sleep(2)  # รอ 2 วินาทีหลังการเชื่อมต่อ
    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal
    ep_sensor_adaptor = ep_robot.sensor_adaptor
    ep_sensor.sub_distance(freq=10, callback=tof_data_handler)
    ep_gimbal.recenter().wait_for_completed()

    try:
        while True:
            print("************")
            ep_gimbal.moveto(
                pitch=0, yaw=90, pitch_speed=0, yaw_speed=30
            ).wait_for_completed()
            time.sleep(0.5)
            if tof_distance is None or adc_1 is None:
                print("Waiting for sensor data...")
                time.sleep(1)
                continue

            gap = abs(WALL_DISTANCE_THRESHOLD - tof_distance)

            walk_y = gap / 1000

            if status_tof == True and status_ss_1 == True:
                time.sleep(1)
                print("Left")
                ep_chassis.move(x=0, y=0, z=90, xy_speed=MAX_SPEED).wait_for_completed()
                ep_gimbal.recenter().wait_for_completed()
                time.sleep(1)
            elif status_tof == False and status_ss_1 == True:
                if tof_distance > 500:
                    ep_chassis.move(
                        x=0.2, y=0, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                    print("Right")
                    ep_chassis.move(
                        x=0, y=0, z=-90, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                    ep_gimbal.recenter().wait_for_completed()
                    ep_chassis.move(
                        x=0.4, y=0, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                    time.sleep(1)
                else:
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
            elif status_tof == True and status_ss_1 == False:
                print("Drive forward")

                ep_chassis.drive_wheels(w1=40, w2=40, w3=40, w4=40)
                time.sleep(0.1)
                ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
            elif status_tof == False and status_ss_1 == False:
                print("tof distance: {} cms")
                if tof_distance > 500:
                    ep_chassis.move(
                        x=0.20, y=0, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                    print("Right")
                    ep_chassis.move(
                        x=0, y=0, z=-90, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                    ep_gimbal.recenter().wait_for_completed()
                    ep_chassis.move(
                        x=0.4, y=0, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                    time.sleep(1)
                else:
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
            # time.sleep(2)
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
