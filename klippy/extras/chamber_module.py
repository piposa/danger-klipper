from . import controller_fan
import util
import logging


class ChamberModule:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.full_section = config.get_name()
        self.gcode_id = config.get("gcode_id")
        self.heater_pin = config.get("heater_pin")
        self.chamber_max_power = config.getfloat(
            "chamber_max_power", 1.0, above=0.0, maxval=1.0
        )
        self.chamber_sensor_type = config.get("chamber_sensor_type")
        self.chamber_sensor_pin = config.get("chamber_sensor_pin")
        self.chamber_smooth_time = config.getfloat(
            "chamber_smooth_time", 1.0, minval=0.0
        )
        self.chamber_min_temp = config.getfloat(
            "chamber_min_temp", 0.0, minval=0.0
        )
        self.chamber_max_temp = config.getfloat(
            "chamber_max_temp", 100.0, minval=0.0
        )
        self.heater_control = config.get("heater_control")
        self.pid_Kp = config.getfloat("pid_Kp", 0.0, minval=0.0)
        self.pid_Ki = config.getfloat("pid_Ki", 0.0, minval=0.0)
        self.pid_Kd = config.getfloat("pid_Kd", 0.0, minval=0.0)
        self.pwm_cycle_time = config.getfloat("pwm_cycle_time", 0.0, minval=0.0)
        self.chamber_sensor_pullup = config.getfloat(
            "pullup_resistor", 4700.0, above=0.0
        )
        self.chamber_sensor_inline_resistor = config.getfloat(
            "inline_resistor", 0.0, minval=0.0
        )
        self.min_extrude_temp = config.getfloat(
            "min_extrude_temp",
            170.0,
            minval=self.chamber_min_temp,
            maxval=self.chamber_max_temp,
        )
        self.hysteresis = config.getfloat("hysteresis", 5.0, minval=0.0)
        self.max_error = config.getfloat("max_error", 120.0, minval=0.0)
        self.heating_gain = config.getfloat("heating_gain", 2.0, above=0.0)
        default_gain_time = 60.0
        self.check_gain_time = config.getfloat(
            "check_gain_time", default_gain_time, minval=1.0
        )

        self.fan_pin = config.get("fan_pin")
        self.fan_max_power = config.getfloat(
            "fan_max_power", 1.0, above=0.0, maxval=1.0
        )
        self.fan_shutdown_speed = config.getfloat(
            "fan_shutdown_speed", 0.0, minval=0.0
        )
        self.fan_cycle_time = config.getfloat("fan_cycle_time", 0.0, minval=0.0)
        self.fan_hardware_pwm = config.get("fan_hardware_pwm", False)
        self.fan_kick_start_time = config.getfloat(
            "fan_kick_start_time", 0.0, minval=0.0
        )
        self.fan_min_power = config.getfloat("fan_min_power", 0.0, minval=0.0)
        self.fan_tachometer_pin = config.get("fan_tachometer_pin", None)
        self.fan_tachometer_ppr = config.getint(
            "fan_tachometer_ppr", 0, minval=0
        )
        self.fan_tachometer_poll_interval = config.getfloat(
            "fan_tachometer_poll_interval", 0.0, minval=0.0
        )
        self.fan_enable_pin = config.get("fan_enable_pin", None)
        self.fan_speed = config.getfloat(
            "fan_speed", 1.0, minval=0.0, maxval=1.0
        )
        self.fan_idle_timeout = config.getint("fan_idle_timeout", 30, minval=0)
        self.fan_idle_speed = config.getfloat(
            "fan_idle_speed", self.fan_speed, minval=0.0, maxval=1.0
        )
        self.fan_off_below = config.getfloat(
            "fan_off_below", default=None, minval=0.0, maxval=1.0
        )

        self.heater = [
            config.get("heater", self.full_section.split()[-1]),
        ]
        self.stepper_names = "extruder"

        self.hconfig = util.FakeConfig(
            self.printer,
            self.full_section,
            config,
            gcode_id=self.gcode_id,
            heater_pin=self.heater_pin,
            max_power=self.chamber_max_power,
            sensor_type=self.chamber_sensor_type,
            sensor_pin=self.chamber_sensor_pin,
            smooth_time=self.chamber_smooth_time,
            min_temp=self.chamber_min_temp,
            max_temp=self.chamber_max_temp,
            control=self.heater_control,
            pid_Kp=self.pid_Kp,
            pid_Ki=self.pid_Ki,
            pid_Kd=self.pid_Kd,
            pwm_cycle_time=self.pwm_cycle_time,
            pullup_resistor=self.chamber_sensor_pullup,
            inline_resistor=self.chamber_sensor_inline_resistor,
            min_extrude_temp=self.min_extrude_temp,
            hysteresis=self.hysteresis,
            max_error=self.max_error,
            heating_gain=self.heating_gain,
            check_gain_time=self.check_gain_time,
        )

        self.fconfig = util.FakeConfig(
            self.printer,
            self.full_section,
            config,
            pin=self.fan_pin,
            max_power=self.fan_max_power,
            shutdown_speed=self.fan_shutdown_speed,
            cycle_time=self.fan_cycle_time,
            hardware_pwm=self.fan_hardware_pwm,
            kick_start_time=self.fan_kick_start_time,
            min_power=self.fan_min_power,
            tachometer_pin=self.fan_tachometer_pin,
            tachometer_ppr=self.fan_tachometer_ppr,
            tachometer_poll_interval=self.fan_tachometer_poll_interval,
            enable_pin=self.fan_enable_pin,
            fan_speed=self.fan_speed,
            idle_timeout=self.fan_idle_timeout,
            idle_speed=self.fan_idle_speed,
            stepper=self.stepper_names,
            off_below=self.fan_off_below,
            heater=self.heater,
        )

    def get_max_power(self):
        return self.chamber_max_power

    def get_smooth_time(self):
        return self.chamber_smooth_time


def load_config_prefix(config):
    obj = ChamberModule(config)
    logging.error("hit load_config_prefix")
    pheaters = config.get_printer().load_object(obj.hconfig, "heaters")
    pheaters.setup_heater(obj.hconfig)

    config.get_printer().add_object(
        "controller_fan", controller_fan.ControllerFan(obj.fconfig)
    )

    return obj
