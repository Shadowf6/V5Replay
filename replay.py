import math
import arcade

WIDTH = 144
HEIGHT = 144
BORDER = 3
VIEWSCALE = 5

INITX = 0
INITY = 0
INITD = 0

ROBOTWIDTH = 0
ROBOTLENGTH = 0

DELAY = 25
REPLAYID = ""

windowWidth = VIEWSCALE * (WIDTH + BORDER * 2)
windowHeight = VIEWSCALE * (HEIGHT + BORDER * 2)

poses = []
duration = 0


def verticalLine(x, start, length, color=(255, 255, 255), width=0.8):
    arcade.draw_line(VIEWSCALE * (BORDER + x), VIEWSCALE * (BORDER + start),
                     VIEWSCALE * (BORDER + x), VIEWSCALE * (BORDER + start + length), color, VIEWSCALE * width)

def horizontalLine(y, start, length, color=(255, 255, 255), width=0.8):
    arcade.draw_line(VIEWSCALE * (BORDER + start), VIEWSCALE * (BORDER + y),
                     VIEWSCALE * (BORDER + start + length), VIEWSCALE * (BORDER + y), color, VIEWSCALE * width)

def block(x, y, color):
    x = VIEWSCALE * (BORDER + x)
    y = VIEWSCALE * (BORDER + y)
    radius = VIEWSCALE * 1.625

    points = [(x + radius * math.cos(math.radians(angle)),
               y + radius * math.sin(math.radians(angle))) for angle in range(0, 360, 60)]

    arcade.draw_polygon_filled(points, color)

def dispenser(x, y):
    arcade.draw_circle_outline(VIEWSCALE * (BORDER + x), VIEWSCALE * (BORDER + y),
                               VIEWSCALE * 3, (196, 150, 18), VIEWSCALE)

def longGoal(left, right, bottom, top):
    arcade.draw_lrbt_rectangle_filled(VIEWSCALE * (BORDER + left + 1.75), VIEWSCALE * (BORDER + right - 1.75),
                                      VIEWSCALE * (BORDER + bottom - 0.1), VIEWSCALE * (BORDER + top + 0.1),
                                      (206, 127, 38))
    arcade.draw_lrbt_rectangle_filled(VIEWSCALE * (BORDER + left), VIEWSCALE * (BORDER + right),
                                      VIEWSCALE * (BORDER + bottom), VIEWSCALE * (BORDER + top),
                                      (193, 191, 192, 100))
    arcade.draw_lrbt_rectangle_filled(VIEWSCALE * (BORDER + left + 3.5), VIEWSCALE * (BORDER + right - 3.5),
                                      VIEWSCALE * (BORDER + bottom), VIEWSCALE * (BORDER + top),
                                      (193, 191, 192, 100))
    arcade.draw_lrbt_rectangle_filled(VIEWSCALE * (BORDER + left), VIEWSCALE * (BORDER + left + 3.5),
                                      VIEWSCALE * (BORDER + bottom), VIEWSCALE * (BORDER + bottom + 0.3),
                                      (193, 191, 192, 100))
    arcade.draw_lrbt_rectangle_filled(VIEWSCALE * (BORDER + right - 3.5), VIEWSCALE * (BORDER + right),
                                      VIEWSCALE * (BORDER + bottom), VIEWSCALE * (BORDER + bottom + 0.3),
                                      (193, 191, 192, 100))
    arcade.draw_lrbt_rectangle_filled(VIEWSCALE * (BORDER + left), VIEWSCALE * (BORDER + left + 3.5),
                                      VIEWSCALE * (BORDER + top - 0.3), VIEWSCALE * (BORDER + top),
                                      (193, 191, 192, 100))
    arcade.draw_lrbt_rectangle_filled(VIEWSCALE * (BORDER + right - 3.5), VIEWSCALE * (BORDER + right),
                                      VIEWSCALE * (BORDER + top - 0.3), VIEWSCALE * (BORDER + top),
                                      (193, 191, 192, 100))
    arcade.draw_line(VIEWSCALE * (BORDER + 65.5), VIEWSCALE * (BORDER + bottom - 0.2),
                     VIEWSCALE * (BORDER + 65.5), VIEWSCALE * (BORDER + top + 0.2),
                     (255, 255, 255), 4)
    arcade.draw_line(VIEWSCALE * (BORDER + 78.5), VIEWSCALE * (BORDER + bottom - 0.2),
                     VIEWSCALE * (BORDER + 78.5), VIEWSCALE * (BORDER + top + 0.2),
                     (255, 255, 255), 4)

def middleGoal(left, right, bottom, top, angle):
    def rotate(l, r, b, t):
        init = [
            (VIEWSCALE * (BORDER + l), VIEWSCALE * (BORDER + b)),
            (VIEWSCALE * (BORDER + r), VIEWSCALE * (BORDER + b)),
            (VIEWSCALE * (BORDER + r), VIEWSCALE * (BORDER + t)),
            (VIEWSCALE * (BORDER + l), VIEWSCALE * (BORDER + t))
        ]

        c = math.cos(math.radians(angle))
        s = math.sin(math.radians(angle))

        cx = VIEWSCALE * (BORDER + (l + r) / 2)
        cy = VIEWSCALE * (BORDER + (b + t) / 2)

        points = []
        for x, y in init:
            dx, dy = x - cx, y - cy
            rx = dx * c - dy * s
            ry = dx * s + dy * c
            points.append((cx + rx, cy + ry))

        return points

    arcade.draw_polygon_filled(rotate(left, right, bottom, top), (193, 191, 192, 100))
    arcade.draw_polygon_filled(rotate(left + 3.5, right - 3.5, bottom, top), (193, 191, 192, 100))

def leftParking(top, bottom, left, right, color):
    horizontalLine(top + 3, left + 0.5, right + 3, color, 2)
    horizontalLine(bottom - 3, left + 0.5, right + 3, color, 2)
    verticalLine(right + 3, bottom - 4, top - bottom + 8, color, 2)

def rightParking(top, bottom, left, color):
    horizontalLine(top + 3, left - 3, WIDTH - left + 2.5, color, 2)
    horizontalLine(bottom - 3, left - 3, WIDTH - left + 2.5, color, 2)
    verticalLine(left - 3, bottom - 4, top - bottom + 8, color, 2)


class Replay(arcade.Window):
    def __init__(self):
        super().__init__(windowWidth, windowHeight, REPLAYID)
        arcade.set_background_color(arcade.color.GRAY)

        self.robot = arcade.SpriteSolidColor(VIEWSCALE * ROBOTWIDTH, VIEWSCALE * ROBOTLENGTH)
        self.robot.center_x = VIEWSCALE * (BORDER + INITX)
        self.robot.center_y = VIEWSCALE * (BORDER + INITY)
        self.robot.color = arcade.color.BLACK
        self.robot.angle = INITD

        self.robotSprite = arcade.SpriteList()
        self.robotSprite.append(self.robot)

        self.step = 0
        self.timeElapsed = 0
        self.isPlaying = False

        self.mouseX = 0
        self.mouseY = 0
        self.mouseT = 0

    def play(self):
        if not self.isPlaying:
            self.isPlaying = True
            arcade.schedule(self.pose, DELAY / 1000.0)

    def pause(self):
        if self.isPlaying:
            self.isPlaying = False
            arcade.unschedule(self.pose)

    def pose(self, delta_time):
        if self.step < len(poses):
            x, y, t = poses[self.step]

            self.robot.center_x = VIEWSCALE * (BORDER + INITX + x)
            self.robot.center_y = VIEWSCALE * (BORDER + INITY + y)
            self.robot.angle = INITD + t

            self.step += 1
            self.timeElapsed += DELAY
        else:
            self.pause()

    def update(self):
        x, y, t = poses[self.step]
        self.robot.center_x = VIEWSCALE * (BORDER + INITX + x)
        self.robot.center_y = VIEWSCALE * (BORDER + INITY + y)
        self.robot.angle = INITD + t

    def on_mouse_press(self, x, y, button, modifiers):
        if VIEWSCALE * BORDER < x < windowWidth - VIEWSCALE * BORDER and VIEWSCALE * BORDER < y < windowHeight - VIEWSCALE * BORDER:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.mouseX = round((x // VIEWSCALE) - BORDER) - INITX
                self.mouseY = round((y // VIEWSCALE) - BORDER) - INITY
                dy = round((y // VIEWSCALE) - BORDER) - INITY
                dx = round((x // VIEWSCALE) - BORDER) - INITX
                self.mouseT = round(math.degrees(math.atan2(-dy, dx)) + 90) - INITD
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                dy = round((y // VIEWSCALE) - BORDER) - INITY - self.mouseY
                dx = round((x // VIEWSCALE) - BORDER) - INITX - self.mouseX
                self.mouseT = round(math.degrees(math.atan2(-dy, dx)) + 90) - INITD

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.SPACE:
            if self.isPlaying:
                self.pause()
            else:
                self.play()
        elif key == arcade.key.LEFT:
            self.step = math.floor(max(0, self.timeElapsed - 1000) / DELAY)
            self.timeElapsed = self.step * DELAY
            self.update()
        elif key == arcade.key.RIGHT:
            self.step = math.floor(min(duration, self.timeElapsed + 1000) / DELAY) - 1
            self.timeElapsed = self.step * DELAY
            self.update()
        elif key == arcade.key.COMMA:
            self.step -= 1
            self.timeElapsed -= DELAY
            self.update()
        elif key == arcade.key.PERIOD:
            self.step += 1
            self.timeElapsed += DELAY
            self.update()

    def on_draw(self):
        self.clear()

        red = (219, 51, 81)
        blue = (16, 172, 202)

        arcade.draw_lrbt_rectangle_outline(VIEWSCALE * BORDER, VIEWSCALE * (WIDTH + BORDER),
                                           VIEWSCALE * BORDER, VIEWSCALE * (HEIGHT + BORDER),
                                           (255, 255, 255), VIEWSCALE * 0.8)

        verticalLine(71, 0, 144)
        verticalLine(73, 0, 144)

        dispenser(4, 24)
        dispenser(4, 120)
        dispenser(140, 24)
        dispenser(140, 120)

        leftParking(73.625, 63.875, 0, 12, red)
        rightParking(73.625, 63.875, 132, blue)

        block(4, 24, blue)
        block(4, 120, blue)
        block(140, 24, red)
        block(140, 120, red)
        block(12, 73.625, blue)
        block(12, 70.375, blue)
        block(12, 67.125, blue)
        block(12, 63.875, blue)
        block(132, 73.625, red)
        block(132, 70.375, red)
        block(132, 67.125, red)
        block(132, 63.875, red)
        block(49.625, 96, red)
        block(49.625, 92.75, red)
        block(52.875, 96, red)
        block(49.625, 48, red)
        block(49.625, 51.25, red)
        block(52.875, 48, red)
        block(96, 96, blue)
        block(96, 92.75, blue)
        block(92.75, 96, blue)
        block(96, 48, blue)
        block(96, 51.25, blue)
        block(92.75, 48, blue)
        block(22.375, 141, blue)
        block(25.625, 141, blue)
        block(118.375, 141, red)
        block(121.625, 141, red)
        block(22.375, 3, blue)
        block(25.625, 3, blue)
        block(118.375, 3, red)
        block(121.625, 3, red)

        self.robotSprite.draw()

        middleGoal(60, 84, 70.125, 73.875, 45)
        arcade.draw_line(VIEWSCALE * (BORDER + 69.172), VIEWSCALE * (BORDER + 72),
                         VIEWSCALE * (BORDER + 72), VIEWSCALE * (BORDER + 74.828), (206, 127, 38), VIEWSCALE * 3 / 5)
        arcade.draw_line(VIEWSCALE * (BORDER + 74.828), VIEWSCALE * (BORDER + 72),
                         VIEWSCALE * (BORDER + 72), VIEWSCALE * (BORDER + 69.172), (206, 127, 38), VIEWSCALE * 3 / 5)
        middleGoal(60, 84, 70.125, 73.875, -45)

        longGoal(47.5, 96.5, 22.25, 26)
        longGoal(47.5, 96.5, 118.25, 122)

        mousePose = arcade.Text("Mouse Pose: " + str(self.mouseX) + ", " + str(self.mouseY) + ", " + str(self.mouseT),
                                int(windowWidth - VIEWSCALE * BORDER * 13), int(VIEWSCALE * BORDER * 6), (255, 255, 255),
                                width=int(VIEWSCALE * 10), align="center", bold=True)

        c = min(self.step, len(poses) - 1)
        robotPose = arcade.Text("Robot Pose: " + str(round(poses[c][0])) + " " + str(round(poses[c][1])) + " " + str(round(poses[c][2])),
                                int(windowWidth - VIEWSCALE * BORDER * 13), int(VIEWSCALE * BORDER * 4), (255, 255, 255),
                                width=int(VIEWSCALE * 10), align="center", bold=True)

        mousePose.draw()
        robotPose.draw()

        mousePos = arcade.Text("Real Mouse Position: " + str(self.mouseX + INITX) + ", " + str(self.mouseY + INITY),
                               int(VIEWSCALE * BORDER * 4), int(VIEWSCALE * BORDER * 6), (255, 255, 255),
                               width=int(VIEWSCALE * 10), align="center", bold=True)
        robotPos = arcade.Text("Real Robot Position: " + str(round(poses[c][0] + INITX)) + " " + str(round(poses[c][1] + INITY)) + " " + str(round(poses[c][2] + INITD)),
                               int(VIEWSCALE * BORDER * 4), int(VIEWSCALE * BORDER * 4),(255, 255, 255),
                               width=int(VIEWSCALE * 10), align="center", bold=True)

        mousePos.draw()
        robotPos.draw()



class Main:
    def __init__(self, filename, delay, initX, initY, initD, robotWidth, robotLength):
        global REPLAYID, DELAY, INITX, INITY, INITD, ROBOTWIDTH, ROBOTLENGTH

        REPLAYID, DELAY, INITX, INITY, INITD, ROBOTWIDTH, ROBOTLENGTH = filename, delay, initX, initY, initD, robotWidth, robotLength

    def start(self):
        global duration

        with open(REPLAYID + ".txt", "r") as f:
            for entry in f:
                poses.append(tuple(map(float, entry.split())))

        duration = DELAY * len(poses)

        replay = Replay()
        arcade.run()
        arcade.start_render()
