import robomaster
from robomaster import robot
import time

tof_distance = None
adc_1 = None
use_left_sensor = False
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


def main():
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
            global adc_1, status_ss, adc_2
            adc_1 = ep_sensor_adaptor.get_adc(id=1, port=1)
            adc_2 = ep_sensor_adaptor.get_adc(id=1, port=2)
            if status_tof == True and not use_left_sensor:
                use_left_sensor = True

            if use_left_sensor:
                adc_value = adc_2
            else:
                adc_value = adc_1

            if 250 < adc_value < 350:
                status_ss = True
            else:
                status_ss = False

            print(f"Using {'left' if use_left_sensor else 'right'} sensor")
            print(f"status_ss {status_ss}")

            print("****************************")

            if tof_distance is None or adc_1 is None:
                print("Waiting for sensor data...")
                time.sleep(1)
                continue

            gap = abs(WALL_DISTANCE_THRESHOLD - tof_distance)
            walk_y = gap / 1000

            if status_tof == True and status_ss == True:
                print("กลับหลังหัน!!")
                ep_chassis.move(
                    x=0, y=0, z=180, xy_speed=MAX_SPEED
                ).wait_for_completed()
                ep_gimbal.recenter().wait_for_completed()
                time.sleep(1)

            elif status_tof == True and status_ss == False:
                if tof_distance < WALL_DISTANCE_THRESHOLD - 50:
                    print("กระเถิบ left")
                    ep_chassis.move(
                        x=0, y=-walk_y, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                elif tof_distance > WALL_DISTANCE_THRESHOLD + 50:
                    print("กระเถิบ right")
                    ep_chassis.move(
                        x=0, y=walk_y, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()

            elif status_tof == False and status_ss == True:
                print("Drive forward")
                ep_chassis.move(
                    x=0.1, y=0, z=0, xy_speed=MAX_SPEED
                ).wait_for_completed()
                time.sleep(1)

            elif status_tof == False and status_ss == False:
                if tof_distance < WALL_DISTANCE_THRESHOLD - 50:
                    print("กระเถิบ left")
                    ep_chassis.move(
                        x=0, y=-walk_y, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
                elif tof_distance > WALL_DISTANCE_THRESHOLD + 50:
                    print("กระเถิบ right")
                    ep_chassis.move(
                        x=0, y=walk_y, z=0, xy_speed=MAX_SPEED
                    ).wait_for_completed()
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


if __name__ == "__main__":
    main()
