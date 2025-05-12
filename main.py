import math
import arcade

WIDTH = 144
HEIGHT = 144
BORDER = 3
VIEWSCALE = 5

INITX = 36
INITY = 72
INITD = 90

ROBOTWIDTH = 18
ROBOTLENGTH = 18

DELAY = 25
REPLAYID = "test"

windowWidth = VIEWSCALE * (WIDTH + BORDER * 2)
windowHeight = VIEWSCALE * (HEIGHT + BORDER * 2)

poses = []

with open(REPLAYID + ".txt", "r") as f:
    entry = f.readline()

    while entry:
        poses.append(tuple(map(float, entry.split())))
        entry = f.readline()

duration = DELAY * len(poses)  # measured in milliseconds


def verticalLine(x, start, length, color=(255, 255, 255), width=0.8):
    arcade.draw_line(VIEWSCALE * (BORDER + x), VIEWSCALE * (BORDER + start),
                     VIEWSCALE * (BORDER + x), VIEWSCALE * (BORDER + start + length), color, VIEWSCALE * width)


def horizontalLine(y, start, length, color=(255, 255, 255), width=0.8):
    arcade.draw_line(VIEWSCALE * (BORDER + start), VIEWSCALE * (BORDER + y),
                     VIEWSCALE * (BORDER + start + length), VIEWSCALE * (BORDER + y), color, VIEWSCALE * width)


def block(x, y, color, radius=1.625):
    x = VIEWSCALE * (BORDER + x)
    y = VIEWSCALE * (BORDER + y)
    radius *= VIEWSCALE

    points = [(x + radius * math.cos(math.radians(angle)),
               y + radius * math.sin(math.radians(angle))) for angle in range(0, 360, 60)]

    arcade.draw_polygon_filled(points, color)


def verticalGoal(x, y):
    arcade.draw_circle_outline(VIEWSCALE * (BORDER + x), VIEWSCALE * (BORDER + y),
                               VIEWSCALE * 3, (196, 150, 18), VIEWSCALE)


def horizontalGoal(left, right, bottom, top):
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

        self.sprite = arcade.SpriteList()
        self.sprite.append(self.robot)

        self.step = 0
        self.timeElapsed = 0
        self.isPlaying = False

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
            self.robot.angle = INITD + math.degrees(t)

            self.step += 1
            self.timeElapsed += DELAY

            if self.step < len(poses):
                self.checkPoseReset()
        else:
            self.pause()

    def checkPoseReset(self):
        global INITX, INITY, INITD
        if poses[self.step - 1] != (0.000, 0.000, 0.000) and poses[self.step] == (0.000, 0.000, 0.000):
            INITX, INITY, INITD = poses[self.step - 1]

    def update(self):
        x, y, t = poses[self.step]
        self.robot.center_x = VIEWSCALE * (BORDER + INITX + x)
        self.robot.center_y = VIEWSCALE * (BORDER + INITY + y)
        self.robot.angle = INITD + math.degrees(t)

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

        arcade.draw_lrbt_rectangle_outline(VIEWSCALE * BORDER, windowWidth - VIEWSCALE * BORDER,
                                           VIEWSCALE * BORDER, windowHeight - VIEWSCALE * BORDER,
                                           (255, 255, 255), VIEWSCALE * 0.8)

        verticalLine(71, 0, 144)
        verticalLine(73, 0, 144)

        verticalGoal(4, 21)
        verticalGoal(4, 123)
        verticalGoal(140, 21)
        verticalGoal(140, 123)

        leftParking(73.625, 63.875, 0, 12, red)
        rightParking(73.625, 63.875, 132, blue)

        # Dispenser blocks
        block(4, 21, blue)
        block(4, 123, blue)
        block(140, 21, red)
        block(140, 123, red)

        # 4 vertical on sides
        block(12, 73.625, blue)
        block(12, 70.375, blue)
        block(12, 67.125, blue)
        block(12, 63.875, blue)
        block(132, 73.625, red)
        block(132, 70.375, red)
        block(132, 67.125, red)
        block(132, 63.875, red)

        # Center corners
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

        # 2 horizontal on top
        block(22.375, 141, blue)
        block(25.625, 141, blue)
        block(118.375, 141, red)
        block(121.625, 141, red)
        block(22.375, 3, blue)
        block(25.625, 3, blue)
        block(118.375, 3, red)
        block(121.625, 3, red)

        self.sprite.draw()

        horizontalGoal(47.5, 96.5, 22.25, 26)
        horizontalGoal(47.5, 96.5, 118.25, 122)


replay = Replay()
arcade.run()
arcade.start_render()
