class Stock:
    """
    A stock is a rectangular sheet of paper that can be cut into smaller
    rectangles. The stock has a width and a height
    """

    def __init__(self, width, height, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def rotate(self):
        """
        Rotate the stock by 90 degrees
        """
        self.width, self.height = self.height, self.width

    def set_loc(self, x, y):
        """
        Set the x and y coordinates of the stock
        """
        self.x = x
        self.y = y

    def set_loc(self, point):
        """
        Set the x and y coordinates of the stock
        """
        self.x = point[0]
        self.y = point[1]

    def get_loc(self):
        """
        Get the x and y coordinates of the stock
        """
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"Stock: {self.width}x{self.height} @ ({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Stock(w={self.width}, h={self.height}, x={self.x}, y={self.y})"
