from libServo import *


class ServoProcess(Process):
    def __init__(self):
        # Shared memory elements
        self.activate_rotation = Value('b', 0)
        self.currentPos_V = Value('I', 0)
        self.desiredPos_V = Value('I', 0)

        self.currentPos_H = Value('I', 0)
        self.desiredPos_H = Value('I', 0)

        self.acquired_data = Value('L', 0)
        self.last_data_epoch = Value('d', 0)
        self.keep_running = Value('b', 0)

        # Local elements
        self._servo_H = None
        self._servo_V = None
        self._servo_V_Connected = None
        self._tempPos_V = None
        self._servo_H_Connected = None
        self._tempPos_H = None
        self._initPos = 90
        self._sleep_at_initialize = 0.2

        Process.__init__(self, target=self.target, args=())

    def __del__(self):
        self.stop()

    def stop(self):

        self.keep_running.value = 0

        sys.stdout.flush()
        self.join()

    def get_Servo_pos(self):
        return self.currentPos_V.value, self.currentPos_H.value

    def target(self, *args, **kwargs):
        print(f"## Starting Servo process with PID: {os.getpid()} ##")

        signal.signal(signal.SIGINT, signal.SIG_IGN)
        self._initialize_Servo()

        while self.keep_running.value == 1:
            try:
                if self.activate_rotation.value == 1:

                    self._tempPos_V = self._servo_V.moveServo(self._servo_V_Connected, self.currentPos_V.value,
                                                              self.desiredPos_V.value)
                    # time.sleep(0.1)
                    self._tempPos_H = self._servo_H.moveServo(self._servo_H_Connected, self.currentPos_H.value,
                                                              self.desiredPos_H.value)
                    # time.sleep(0.1)
                    self.currentPos_V.value, self.currentPos_H.value = self._tempPos_V, self._tempPos_H
                    self.activate_rotation.value = 0

                elif self.keep_running.value == 0:
                    # time.sleep(1)
                    self._servo_V.stopServoAt(self._servo_V_Connected, self.currentPos_V.value, self._initPos)
                    self._servo_H.stopServoAt(self._servo_H_Connected, self.currentPos_H.value, self._initPos)
                    break

                else:
                    pass

            except KeyboardInterrupt:
                pass

        print(f"## Finishing Servo process with PID: {os.getpid()} ##")

        del self._servo_V
        del self._servo_H

    def _initialize_Servo(self):
        self._servo_V = ServoMotor('Servo V', self._initPos, servo_V_Pin, servo_V_minPW, servo_V_maxPW, servo_V_offset,
                                   0.03)
        self._servo_H = ServoMotor('Servo H', self._initPos, servo_H_Pin, servo_H_minPW, servo_H_maxPW, servo_H_offset,
                                   0.03)

        self._servo_V_Connected, self.currentPos_V.value = self._servo_V.initServo()
        self._servo_H_Connected, self.currentPos_H.value = self._servo_H.initServo()

        return self.INITIALIZE_OK
