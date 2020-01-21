from timeit import default_timer as timer
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from ColorOfPicture import *


class MakePicture:
    """ Создание выходной картинки. """

    def __init__(self, width=300, height=300):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("Ray Tracing")
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, bg='white', width=self.width, height=self.height)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.redraw()
        self.root.mainloop()

    def erase(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def redraw(self):
        self.erase()

        start_time = timer()
        gui = ColorOfPicture(camera=Point(0, 0, 0), width=self.width, height=self.height)
        duration = timer() - start_time

        bitmap = gui.bitmap

        for y in range(self.image.height):
            for x in range(self.image.width):
                self.draw.point([(y, x)], bitmap[x][y])

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

        print("\nDuration: {:g} secs".format(duration))
