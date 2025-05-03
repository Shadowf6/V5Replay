import arcade as ar
import math

WIDTH = 144
HEIGHT = 144
BORDER = 12

VIEWSCALE = 5

DELAY = 25

initX = BORDER + 16
initY = (HEIGHT + BORDER) / 2 - 9
initD = 90

ROBOTWIDTH = 18
ROBOTLENGTH = 24

replayID = "test"


WINDOWWIDTH = VIEWSCALE * (WIDTH + BORDER * 2)
WINDOWHEIGHT = VIEWSCALE * (HEIGHT + BORDER * 2)

path = replayID + ".txt"
poses = []

with open(path, 'r') as f:
    entry = f.readline()

    while entry:
        poses.append(tuple(map(float, entry.split())))
        entry = f.readline()

duration = DELAY * len(poses)  # in seconds


class Replay(ar.Window):
    def __init__(self):
        super().__init__(WINDOWWIDTH, WINDOWHEIGHT, replayID)
        ar.set_background_color(ar.color.GRAY)

        self.robot = ar.SpriteSolidColor(VIEWSCALE * ROBOTWIDTH, VIEWSCALE * ROBOTLENGTH)
        self.robot.center_x = VIEWSCALE * initX
        self.robot.center_y = VIEWSCALE * initY
        self.robot.color = ar.color.BLACK
        self.robot.angle = initD

        self.sl = ar.SpriteList()
        self.sl.append(self.robot)

        self.step = 0
        self.timeElapsed = 0
        self.isPlaying = False

    def play(self):
        if not self.isPlaying:
            self.isPlaying = True
            ar.schedule(self.replay, DELAY / 1000.0)

    def pause(self):
        if self.isPlaying:
            self.isPlaying = False
            ar.unschedule(self.replay)

    def replay(self, delta_time):
        if self.step < len(poses):
            x, y, t = poses[self.step]

            # Note that if during auto, pose is ever reset to (0, 0, 0), this will break

            self.robot.center_x = VIEWSCALE * (initX + x)
            self.robot.center_y = VIEWSCALE * (initY + y)
            self.robot.angle = initD + math.degrees(t)

            self.step += 1
            self.timeElapsed += DELAY
        else:
            self.pause()

    def update(self):
        x, y, t = poses[self.step]
        self.robot.center_x = VIEWSCALE * (initX + x)
        self.robot.center_y = VIEWSCALE * (initY + y)
        self.robot.angle = initD + math.degrees(t)

    def on_key_press(self, key, modifiers):
        if key == ar.key.ESCAPE:
            ar.close_window()
        elif key == ar.key.SPACE:
            if self.isPlaying:
                self.pause()
            else:
                self.play()
        elif key == ar.key.LEFT:
            self.step = math.floor(max(0, self.timeElapsed - 1000) / DELAY)
            self.timeElapsed = self.step * DELAY
            self.update()
        elif key == ar.key.RIGHT:
            self.step = math.floor(min(duration, self.timeElapsed + 1000) / DELAY)
            self.timeElapsed = self.step * DELAY
            self.update()
        elif key == ar.key.J:
            self.step = math.floor(max(0, self.timeElapsed - 5000) / DELAY)
            self.timeElapsed = self.step * DELAY
            self.update()
        elif key == ar.key.L:
            self.step = math.floor(min(duration, self.timeElapsed + 5000) / DELAY)
            self.timeElapsed = self.step * DELAY
            self.update()
        elif key == ar.key.COMMA:
            self.step -= 1
            self.timeElapsed -= DELAY
            self.update()
        elif key == ar.key.PERIOD:
            self.step += 1
            self.timeElapsed += DELAY
            self.update()

    def on_draw(self):
        self.clear()
        self.sl.draw()

        ar.draw_lrbt_rectangle_outline(VIEWSCALE * BORDER, WINDOWWIDTH - VIEWSCALE * BORDER,
                                       VIEWSCALE * BORDER, WINDOWHEIGHT - VIEWSCALE * BORDER,
                                       (255, 255, 255), 4)
        ar.draw_line(VIEWSCALE * (BORDER + 6), VIEWSCALE * BORDER,
                     VIEWSCALE * (BORDER + 6), WINDOWHEIGHT - VIEWSCALE * BORDER,
                     (255, 255, 255), 4)
        ar.draw_line(WINDOWWIDTH - VIEWSCALE * (BORDER + 6), VIEWSCALE * BORDER,
                     WINDOWWIDTH - VIEWSCALE * (BORDER + 6), WINDOWHEIGHT - VIEWSCALE * BORDER,
                     (255, 255, 255), 4)
        ar.draw_line(VIEWSCALE * BORDER, VIEWSCALE * (BORDER + 6),
                     WINDOWWIDTH - VIEWSCALE * BORDER, VIEWSCALE * (BORDER + 6),
                     (255, 255, 255), 4)
        ar.draw_line(VIEWSCALE * BORDER, WINDOWHEIGHT - VIEWSCALE * (BORDER + 6),
                     WINDOWWIDTH - (VIEWSCALE * BORDER), WINDOWHEIGHT - VIEWSCALE * (BORDER + 6),
                     (255, 255, 255), 4)
        ar.draw_line(WINDOWWIDTH / 2 - VIEWSCALE, VIEWSCALE * BORDER,
                     WINDOWWIDTH / 2 - VIEWSCALE, WINDOWHEIGHT - VIEWSCALE * BORDER,
                     (255, 255, 255), 4)
        ar.draw_line(WINDOWWIDTH / 2 + VIEWSCALE, VIEWSCALE * BORDER,
                     WINDOWWIDTH / 2 + VIEWSCALE, WINDOWHEIGHT - VIEWSCALE * BORDER,
                     (255, 255, 255), 4)

        w, h = VIEWSCALE * 12 * math.sqrt(2), VIEWSCALE * 12 * math.sqrt(2)
        a = math.sqrt(2) / 2
        x = WINDOWWIDTH / 2
        y = WINDOWHEIGHT / 2
        corners = [(x + a * (w - h), y + a * (w + h)), (x + a * (-w - h), y + a * (h - w)),
                   (x + a * (h - w), y + a * (-w - h)), (x + a * (w + h), y + a * (w - h))]
        ar.draw_polygon_outline(corners, (255, 255, 0), 6)


if __name__ == "__main__":
    replay = Replay()
    ar.run()
    ar.start_render()
