import robomaster
from robomaster import robot
import time

tof_distance = None
MAX_SPEED = 0.5  # Adjust as needed
WALL_DISTANCE_THRESHOLD = 300  # mm, adjust as needed


def tof_data_handler(sub_info):
    global tof_distance
    tof_distance = sub_info[0]  # Assuming the first value is the distance
    print(f"ToF distance: {tof_distance} mm")


def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis
    ep_gimbal = ep_robot.gimbal

    ep_sensor.sub_distance(freq=10, callback=tof_data_handler)
    ep_gimbal.recenter().wait_for_completed()

    try:
        while True:
            # Turn gimbal to the right to measure wall distance
            ep_gimbal.moveto(
                pitch=0, yaw=90, pitch_speed=30, yaw_speed=30
            ).wait_for_completed()
            time.sleep(0.5)  # Wait for stable reading

            if tof_distance is None:
                print("Waiting for ToF data...")
                continue

            gap = abs(WALL_DISTANCE_THRESHOLD - tof_distance)
            walk_y = gap / 1000
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
                    x=0.2, y=0, z=0, xy_speed=MAX_SPEED
                ).wait_for_completed()

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        ep_sensor.unsub_distance()
        ep_robot.close()


if __name__ == "__main__":
    main()
