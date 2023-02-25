import pygame
import time

# set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class Element():
    def __init__(self, _id: str = "", _color: tuple[int, int, int] = BLACK):
        self.id = _id
        self.color = _color

    def Print_Id(self):
        print(self.id)

    def draw(self, _scale: tuple[int, int]):
        pass


class Point(Element):
    def __init__(self, _X: int, _Y: int, id: str = "", _color: tuple[int, int, int] = BLACK):
        super().__init__(id, _color)
        self.X = _X
        self.Y = _Y

    def __iter__(self):
        for i in range(0, 2):
            if i == 0:
                yield self.X
            else:
                yield self.Y

    def __mul__(self, other: tuple[int, int]):
        return Point(self.X * other[0], self.Y * other[1])

    def __add__(self, other: tuple[int, int]):
        return Point(self.X + other[0], self.Y + other[1])

    def __sub__(self, other: tuple[int, int]):
        return Point(self.X - other[0], self.Y - other[1])

    def __div__(self, other: tuple[int, int]):
        return Point(self.X / other[0], self.Y / other[1])


class Line(Element):
    def __init__(self, _point1: Point, _point2: Point, _width: int = 5, _id: str = "", _color: tuple[int, int, int] = BLACK):
        super().__init__(_id, _color)
        self.point1 = _point1
        self.point2 = _point2
        self.width = _width

    def draw(self, _screen, _scale: tuple[int, int]):
        pygame.draw.line(_screen, self.color, tuple(
            self.point1 * _scale), tuple(self.point2 * _scale), self.width)


class Display:

    def __init__(self, _size: tuple[int, int], _caption: str, _scaleable: bool = True, _maintainAspectRatio = True):
        # set up a window
        pygame.init()
        self.size = _size
        self.scaleable = _scaleable
        self.maintainAspectRatio = _maintainAspectRatio
        self.scale: tuple[int, int] = (1, 1)
        self.screen = pygame.display.set_mode(
            self.size, pygame.RESIZABLE if self.scaleable else 0)
        pygame.display.set_caption(_caption)

        self.elements = []

    def add(self, _element: Element):
        _element.draw(self.screen, self.scale if not self.maintainAspectRatio else (min(self.scale),) * 2)
        self.elements.append(_element)
        pygame.display.flip()

    def update(self):
        pygame.display.set_mode(
            (self.size[0] * self.scale[0], self.size[1] * self.scale[1]), pygame.RESIZABLE)
        for element in self.elements:
            element.draw(self.screen, self.scale if not self.maintainAspectRatio else (min(self.scale),) * 2)
        pygame.display.flip()


class Polygon(Element):
    def __init__(self, _points: list[Point] = [], _id: str = "", _color: tuple[int, int, int] = BLACK, _outlineWidth: int = 5):
        super().__init__(_id, _color)
        self.points = _points
        self.outlineWidth = _outlineWidth

    def __iter__(self):
        for point in self.points:
            yield tuple(point)

    def __mul__(self, other):
        return Polygon([point * other for point in self.points])

    def __add__(self, other):
        return Polygon([point + other for point in self.points])

    def __sub__(self, other):
        return Polygon([point - other for point in self.points])

    def __div__(self, other):
        return Polygon([point / other for point in self.points])

    def draw(self, _screen, _scale: tuple[int, int]):
        pygame.draw.polygon(_screen, self.color, list(
            self * _scale), self.outlineWidth)


class Quadralateral(Polygon):
    def __init__(self, _points: list[Point, Point, Point, Point] = [], _id: str = "", _color: tuple[int, int, int] = BLACK, _outlineWidth: int = 5):
        if not len(_points) == 4:
            raise Exception("Quadralaterial must have four points")
        super().__init__(_points, _id, _color, _outlineWidth)
        self.points = _points
        self.outlineWidth = _outlineWidth


def main():
    print("Starting...")

    # initialize Pygame

    display = Display((500, 500), "Testing")

    polygon = Quadralateral(_points=[Point(100, 100), Point(
        200, 100), Point(200, 200), Point(100, 200)], _color=GREEN, _outlineWidth=0)

    display.add(polygon)

    # wait for the user to close the window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resizing
                display.scale = (
                    event.size[0] / display.size[0], event.size[1] / display.size[1])
                pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)

                display.update()

    # quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
