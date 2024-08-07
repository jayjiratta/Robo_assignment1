from robomaster import robot
import time


if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_sensor_adaptor = ep_robot.sensor_adaptor

    # # 获取传感器转接板adc值
    # adc = ep_sensor_adaptor.get_adc(id=1, port=1)
    # print("sensor adapter id1-port1 adc is {0}".format(adc))

    # # 获取传感器转接板io电平
    # io = ep_sensor_adaptor.get_io(id=1, port=1)
    # print("sensor adapter id1-port1 io is {0}".format(io))

    # # 获取传感器转接板io电平持续时间
    # duration = ep_sensor_adaptor.get_pulse_period(id=1, port=1)
    # print("sensor adapter id1-port1 duration is {0}ms".format(duration))

    # adc = ep_sensor_adaptor.get_adc(id=1, port=2)
    # print("sensor adapter id1-port1 adc is {0}".format(adc))
    # io = ep_sensor_adaptor.get_io(id=1, port=2)
    # print("sensor adapter id1-port1 io is {0}".format(io))
    # duration = ep_sensor_adaptor.get_pulse_period(id=1, port=2)
    # print("sensor adapter id1-port1 duration is {0}ms".format(duration))

    try:
        while True:
            adc_1 = ep_sensor_adaptor.get_adc(id=1, port=1)
            adc_2 = ep_sensor_adaptor.get_adc(id=1, port=2)

            print("id1-port1 adc is {0} id1-port2 adc is {1}".format(adc_1, adc_2))
            time.sleep(1)
    except KeyboardInterrupt:
        ep_robot.close()
