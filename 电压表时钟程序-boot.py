import machine
import network
import ntptime
import time
from machine import RTC

# 配置WiFi
SSID = 'SYG'
PASSWORD = '12345678'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    pass

print("WiFi connected")
print("Getting network time...")

# 获取网络时间
ntptime.settime()
time.sleep(8)  # 等待时间同步

# 配置PWM引脚
pwm_hour = machine.PWM(machine.Pin(2), freq=1000)  # D2
pwm_minute = machine.PWM(machine.Pin(4), freq=1000)  # D4
pwm_second = machine.PWM(machine.Pin(5), freq=1000)  # D5

try:
    while True:
        # 获取当前时间
        current_time = time.localtime(time.time() + 8 * 3600)
        hour = current_time[3]  # 小时（24小时制）
        minute = current_time[4]  # 分钟
        second = current_time[5]  # 秒

        # 将时间转换为0-1023范围内的PWM值（10位分辨率）
        pwm_hour_value = int(hour / 24.0 * 980)
        pwm_minute_value = int(minute / 60.0 * 980)
        pwm_second_value = int(second / 60.0 * 980)

        # 设置PWM占空比
        pwm_hour.duty(pwm_hour_value)
        pwm_minute.duty(pwm_minute_value)
        pwm_second.duty(pwm_second_value)

        # 打印当前时间和PWM值（调试用）
        print(f"Time: {hour:02}:{minute:02}:{second:02}, PWM: H={pwm_hour_value}, M={pwm_minute_value}, S={pwm_second_value}")

        # 等待一秒
        time.sleep(1)

except KeyboardInterrupt:
    # 停止PWM
    pwm_hour.deinit()
    pwm_minute.deinit()
    pwm_second.deinit()
    print("PWM stopped")
