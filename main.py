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

path = "Replays/" + replayID + ".txt"
poses = []

with open(path, 'r') as f:
    entry = f.readline()

    while entry:
        poses.append(tuple(map(float, entry.split())))
        entry = f.readline()

duration = DELAY * len(poses) / 1000  # in seconds


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
        self.timeElapsed = 0  # divided by 1000 for seconds
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

            # Note that if during auto, pose is ever reset, this will break

            self.robot.center_x = VIEWSCALE * (initX + x)
            self.robot.center_y = VIEWSCALE * (initY + y)
            self.robot.angle = initD + math.degrees(t)

            self.step += 1
            self.timeElapsed += DELAY
        else:
            self.pause()

    def goToTime(self, time):
        pass

    def goToStep(self, step):
        pass

    def draw_ring(self, x, y, color):
        pass

    def draw_goal(self, x, y):
        pass

    def on_key_press(self, key, modifiers):
        if key == ar.key.ESCAPE:
            ar.close_window()
        elif key == ar.key.SPACE:
            if self.isPlaying:
                self.pause()
            else:
                self.play()

    def on_draw(self):
        self.clear()
        self.sl.draw()

        # Field
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

        # Ladder
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

# Features:
# Playback
# Speed Customization
# Real-Time Graph
