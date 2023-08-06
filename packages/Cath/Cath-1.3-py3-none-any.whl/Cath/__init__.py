import time
import zmq


class Cath:
    def __init__(self):
        self.__Address = "tcp://localhost:12346"
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.REQ)
        self.__socket.connect(self.__Address)
        self.__TIMEOUT = 10000
        time.sleep(0.5)

    def __send(self, msg):
        self.__socket.send_string(msg)
        poller = zmq.Poller()
        poller.register(self.__socket, zmq.POLLIN)
        evt = dict(poller.poll(self.__TIMEOUT))
        if evt:
            if evt.get(self.__socket) == zmq.POLLIN:
                rep = self.__socket.recv(zmq.NOBLOCK)

    def pensize(self, size):
        """
        펜 굵기를 설정합니다.

        :param size: 펜 굵기 (float)
        """
        msg = "pensize " + str(size)
        self.__send(msg)

    def pencolor(self, color):
        """
        펜 색상을 헥스코드를 사용하여 설정합니다.
        마지막에 투명도(Alpha) 값을 추가하여 설정 할 수 있습니다.

        :param color: 펜 색상 "#RRGGBB" 또는 "#RRGGBBAA" (string)
        """
        msg = "pencolor " + color
        self.__send(msg)

    def penup(self):
        """
        펜을 들어 올립니다.
        """
        msg = "penup"
        self.__send(msg)

    def pendown(self):
        """
        펜을 내립니다.
        """
        msg = "pendown"
        self.__send(msg)

    def translate(self, x, y, z):
        """
        고양이를 특정 좌표로 이동시킵니다.

        :param x: X 좌표 (float)
        :param y: Y 좌표 (float)
        :param z: Z 좌표 (float)
        """
        msg = "translate " + str(x) + " " + str(y) + " " + str(z)
        self.__send(msg)

    def forward(self, distance):
        """
        고양이를 앞쪽으로 distance 만큼 이동시킵니다.

        :param distance: 이동거리 (float)
        """
        msg = "forward " + str(distance)
        self.__send(msg)

    def backward(self, distance):
        """
        고양이를 뒤쪽으로 distance 만큼 이동시킵니다.

        :param distance: 이동거리 (float)
        """
        msg = "backward " + str(distance)
        self.__send(msg)

    def leftward(self, distance):
        """
        고양이를 왼쪽으로 distance 만큼 이동시킵니다.

        :param distance: 이동거리 (float)
        """
        msg = "leftward " + str(distance)
        self.__send(msg)

    def rightward(self, distance):
        """
        고양이를 오른쪽으로 distance 만큼 이동시킵니다.

        :param distance: 이동거리 (float)
        """
        msg = "rightward " + str(distance)
        self.__send(msg)

    def up(self, distance):
        """
        고양이를 위쪽으로 distance 만큼 이동시킵니다.

        :param distance: 이동거리 (float)
        """
        msg = "up " + str(distance)
        self.__send(msg)

    def down(self, distance):
        """
        고양이를 아래쪽으로 distance 만큼 이동시킵니다.

        :param distance: 이동거리 (float)
        """
        msg = "down " + str(distance)
        self.__send(msg)

    def rotate_x(self, angle):
        """
        고양이를 X축으로 angle 만큼 회전시킵니다.

        :param angle: 각도 (float)
        """
        msg = "rotate_x " + str(angle)
        self.__send(msg)

    def rotate_y(self, angle):
        """
        고양이를 X축으로 angle 만큼 회전시킵니다.

        :param angle: 각도 (float)
        """
        msg = "rotate_y " + str(angle)
        self.__send(msg)

    def rotate_z(self, angle):
        """
        고양이를 X축으로 angle 만큼 회전시킵니다.

        :param angle: 각도 (float)
        """
        msg = "rotate_z " + str(angle)
        self.__send(msg)

    def clear(self):
        """
        고양이를 초기화 시킵니다.
        :return:
        """
        msg = "clear"
        self.__send(msg)
