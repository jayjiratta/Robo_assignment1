import robomaster
from robomaster import robot
import time

io_data = None


def sub_data_handler(sub_info):
    global io_data
    io_data, ad_data = sub_info
    print(f"Front: {io_data[0]} Right: {io_data[1]}")


def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_sensor = ep_robot.sensor_adaptor
    ep_chassis = ep_robot.chassis

    ep_sensor.sub_adapter(freq=10, callback=sub_data_handler)

    try:
        print("Waiting for initial IO data...")
        while io_data is None:
            time.sleep(0.1)

        print("Starting movement. Will stop when IO 1 goes high.")
        if io_data[0] == 0:
            ep_chassis.drive_speed(x=0.2, y=0, z=0)  # Continuous movement
            time.sleep(0.1)  # Short delay to prevent CPU overuse

        if io_data[1] == 1:
            ep_chassis.drive_speed(x=0, y=0.1, z=0)
            time.sleep(0.1)

        print("IO 1 went high. Stopping the robot.")
        ep_chassis.drive_speed(x=0, y=0, z=0)
        time.sleep(2)  # Wait for 2 seconds after stopping

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        ep_sensor.unsub_adapter()
        ep_chassis.drive_speed(x=0, y=0, z=0)  # Ensure the robot stops
        ep_robot.close()


if __name__ == "__main__":
    main()
