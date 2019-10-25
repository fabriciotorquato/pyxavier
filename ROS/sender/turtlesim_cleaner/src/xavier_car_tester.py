from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from picar import front_wheels
from picar import back_wheels
import xavier_command
import time
import picar
import random


class XavierCar(object):
    def __init__(self):
        # 0 = random direction, 1 = force left, 2 = force right, 3 = orderdly
        self.force_turning = 0
        picar.setup()

        self.ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
        self.fw = front_wheels.Front_Wheels(db='config')
        self.bw = back_wheels.Back_Wheels(db='config')
        self.default_turning_max = self.fw.turning_max
        self.fw.turning_max = 60

        self.forward_speed = 45
        self.backward_speed = 45

        self.back_distance = 10
        self.turn_distance = 20

        self.timeout = 10
        self.last_angle = 90
        self.last_dir = 0

        self.step = 20

        self.command = xavier_command.STOP

    def _rand_dir(self):
        if self.force_turning == 0:
            _dir = random.randint(0, 1)
        elif self.force_turning == 3:
            _dir = not self.last_dir
            self.last_dir = _dir
            print('last dir  %s' % self.last_dir)
        else:
            _dir = self.force_turning - 1
        angle = (90 - self.fw.turning_max) + (_dir * 2 * self.fw.turning_max)
        self.last_angle = angle
        return angle

    def _opposite_angle(self):
        if self.last_angle < 90:
            angle = self.last_angle + 2 * self.fw.turning_max
        else:
            angle = self.last_angle - 2 * self.fw.turning_max
        self.last_angle = angle
        return angle

    def _left_angle(self):
        angle = 180
        print(self.last_angle,angle)
        self.last_angle = angle
        return angle

    def _right_angle(self):
        angle = 0
        print(self.last_angle,angle)
        self.last_angle = angle
        return angle

    def start_avoidance(self):
        print('start_avoidance')
        self.count = 0
        self._update_status()

    def send_command(self, command):
         self.command = command.data
         self._update_status()

    def _update_status(self):
        distance = self.ua.get_distance()
        print("distance: %scm" % distance)
        if distance > 0:
            self.fw.turning_max = 60
            self.count = 0
            if distance < self.back_distance:  # backward
                print("[Comando Autonomo] parado")
                self.fw.turn(90)
                self.bw.stop()
            elif distance < self.turn_distance:  # turn
                print("[Comando Autonomo] parado")
                self.fw.turn(90)
                self.bw.stop()
            else:
                self.fw.turning_max = self.default_turning_max
                if self.command == xavier_command.STOP:
                    print("[Comando Autonomo] parado")
                    self.fw.turn(90)
                    self.bw.stop()
                else:
                    if self.command == xavier_command.FORWARD:
                        print('[Comando Xavier] Frente')
                        self.fw.turn(90)
                        self.bw.forward()
                        self.bw.speed = self.forward_speed
                    
                    elif self.command == xavier_command.TURN_LEFT:
                        print("[Comando Xavier] Rotacionar Esquerda")
                        self.fw.turn(90-self.step)
                        self.bw.forward()
                        self.bw.speed = self.forward_speed    

                    elif self.command == xavier_command.TURN_RIGHT:
                        print("[Comando Xavier] Rotacionar Direita")
                        self.fw.turn(90+self.step)
                        self.bw.forward()
                        self.bw.speed = self.forward_speed  
        else:  # forward
            print("[Comando Autonomo] Reiniciando")
            self.fw.turn_straight()
            if self.count > self.timeout:  # timeout, stop;
                self.bw.stop()
            else:
                self.count += 1

    def stop(self):
        print("[Comando Autonomo] Desligando")
        self.bw.stop()
        self.fw.turn_straight()

