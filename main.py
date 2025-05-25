import replay

filename = "test"

delay = 25

initX = 21
initY = 62
initD = 90

robotWidth = 11
robotLength = 13


if __name__ == "__main__":
    window = replay.Main(filename, delay, initX, initY, initD, robotWidth, robotLength)
    window.start()
