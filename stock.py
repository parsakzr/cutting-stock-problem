class Stock:
    """
    A stock is a rectangular sheet of paper that can be cut into smaller
    rectangles. The stock has a width and a height
    """

    def __init__(self, width: int, height: int, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def getVertices(self) -> list:
        """
        Get the vertices of the stock
        """
        return [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height),
        ]

    def getArea(self) -> int:
        """
        Get the area of the stock
        """
        return self.width * self.height

    def rotate90(self):
        """
        Rotate the stock by 90 degrees
        """
        self.width, self.height = self.height, self.width

    def setLoc(self, x: int, y: int):
        """
        Set the x and y coordinates of the stock
        """
        self.x = x
        self.y = y

    def setLoc(self, point: tuple):
        """
        Set the x and y coordinates of the stock
        """
        self.x = point[0]
        self.y = point[1]

    def getLoc(self) -> tuple:
        """
        Get the x and y coordinates of the stock
        """
        return (self.x, self.y)

    def intersects(self, stock2) -> bool:
        """
        Check if the stock is intersecting with another stock
        """
        if (
            self.x < stock2.x + stock2.width
            and self.x + self.width > stock2.x
            and self.y < stock2.y + stock2.height
            and self.y + self.height > stock2.y
        ):
            return True

        return False

    def __str__(self) -> str:
        return f"Stock: {self.width}x{self.height} @ ({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Stock(w={self.width}, h={self.height}, x={self.x}, y={self.y})"


class Sheet:
    """
    A sheet is a rectangular space that can be filled with stocks
    """

    def __init__(self, width, height, stocks: list = []) -> None:
        self.width = width
        self.height = height
        self.packed_stocks = []
        self.unpacked_stocks = stocks
        self.sortStocks()

    def addStock(self, stock: Stock) -> None:
        """
        Add a stock to the sheet, sorted by area
        """
        ## dont sort the whole list, just insert the stock in the right place
        # calculate the area of the stock
        area = stock.getArea()
        # find the index to insert the stock
        index = 0
        for i in range(len(self.unpacked_stocks)):
            if self.unpacked_stocks[i].getArea() < area:
                index = i
                break
        # insert the stock
        self.unpacked_stocks.insert(index, stock)

    def addStocks(self, stocks: list) -> None:
        """
        Add a list of stocks to the sheet
        """
        self.unpacked_stocks.extend(stocks)
        self.sortStocks()  # lazy way. just sorting from scratch

    def sortStocks(self) -> None:
        """
        Sort the stocks by area
        """
        self.unpacked_stocks.sort(key=lambda stock: stock.getArea(), reverse=True)

    def pack(self, stock: Stock, loc: tuple) -> bool:
        """
        Pack the stock into the sheet

        Args:
            stock (Stock): The stock to be packed.
            loc (tuple): The new location of the stock within the sheet. (x, y)

        Returns:
            bool: True if the packing step is valid, False otherwise.
        """
        if not self.validate_pack_step(stock, loc):
            return False

        # ok to pack the stock
        stock.setLoc(loc)  # Place the stock in the location
        self.packed_stocks.append(stock)
        self.unpacked_stocks.remove(stock)
        return True

    def packNext(self, loc: tuple) -> bool:
        """
        Pack the next stock into the sheet

        Args:
            loc (tuple): The new location of the stock within the sheet. (x, y)

        Returns:
            bool: True if the packing step is valid, False otherwise.
        """
        if len(self.unpacked_stocks) == 0:
            return False

        # Assuming the unpacked stocks are sorted by area
        return self.pack(self.unpacked_stocks[0], loc)

    def validate_pack_step(self, stock: Stock, loc: tuple) -> bool:
        """
        Validate the packing step.

        The validation is done by checking if the stock is intersecting with
        any of the stocks in the pattern and if the stock is within the sheet.

        Args:
            stock (Stock): The stock to be validated.
            loc (tuple): The new location of the stock within the sheet. (x, y)

        Returns:
            bool: True if the packing step is valid, False otherwise.
        """
        stock_new = Stock(stock.width, stock.height, loc[0], loc[1])

        # Check if the stock is within the sheet
        if (
            stock_new.x < 0
            or stock_new.y < 0
            or stock_new.x + stock_new.width > self.width
            or stock_new.y + stock_new.height > self.height
        ):
            return False

        # Check if the stock intersects with any of the stocks in the pattern
        for stock2 in self.packed_stocks:
            if stock_new.intersects(stock2):
                return False

        del stock_new  # free up memory
        return True

    def __str__(self) -> str:
        return f"Sheet: {self.width}x{self.height}"


# Tests


def test_validateIntersections(pattern: list) -> None:
    """
    Test if the pattern has any intersections
    """
    has_intersections = False
    for i in range(len(pattern)):
        for j in range(i + 1, len(pattern)):
            if pattern[i].intersects(pattern[j]):
                has_intersections = True

    assert not has_intersections, "The pattern has intersections"
