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
        self.unpacked_stocks = stocks
        self.packed_stocks = []
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

    # useful methods after packing
    def getArea(self) -> int:
        """
        Get the area of the sheet
        """
        return self.width * self.height

    def getLowerBoundHeight(self) -> int:
        """
        Get the lower bound of height of the sheet
        Which is the maximum height that the packed stocks has been placed
        """
        return max([stock.y + stock.height for stock in self.packed_stocks])

    def getAreaUsed(self) -> int:
        """
        Get the area of the sheet that is used by the stocks.
        Sum of the areas of the packed stocks
        """
        return sum([stock.getArea() for stock in self.packed_stocks])

    def getEfficiency(self) -> float:
        """
        Get the efficiency of the sheet
        Efficiency = AreaUsed / Total area
        """
        return self.getAreaUsed() / self.getArea()

    def getStats(self) -> dict:
        """
        Get the stats of the sheet
        """
        stats = {
            "width": self.width,
            "height": self.height,
            "lower_bound_height": self.getLowerBoundHeight(),
            "area": self.getArea(),
            "area_used": self.getAreaUsed(),
            "efficiency": self.getEfficiency(),
            "num_unpacked_stocks": len(self.unpacked_stocks),
            # convert list of stocks to json serializable list
            # "unpacked_stocks": [
            #     {"width": stock.width, "height": stock.height}
            #     for stock in self.unpacked_stocks
            # ],
        }
        return stats

    def exportSheet(self, filename: str = "output/sheet.txt") -> None:
        """
        Export the sheet data to a file
        Template of file.txt:
            width height
            stock_width stock_height x y
            ...

        """
        with open(filename, "w") as f:
            print(f"Exporting sheet to {filename}")
            f.write(f"{self.width} {self.height}\n")
            for stock in self.packed_stocks:
                f.write(f"{stock.x} {stock.y} {stock.width} {stock.height}\n")

    @staticmethod
    def importSheet(filename: str = "output/sheet.txt") -> "Sheet":
        """
        Import the sheet data from a file
        Template of file.txt:
            width height
            stock_width stock_height x y
            ...

        """
        with open(filename, "r") as f:
            width, height = map(int, f.readline().split())
            sheet = Sheet(width, height)
            for line in f.readlines():
                x, y, w, h = map(int, line.split())
                sheet.addStock(Stock(w, h))
                sheet.packNext((x, y))
            return sheet

    def __del__(self):
        del self.unpacked_stocks[:]
        del self.packed_stocks[:]
        del self

    def __str__(self) -> str:
        return f"Sheet: {self.width}x{self.height}"

    def __repr__(self) -> str:
        return f"Sheet(w={self.width}, h={self.height})"


if __name__ == "__main__":
    # Test the sheet class
    # sheet = Sheet(10, 10)
    # sheet.addStock(Stock(3, 3))
    # sheet.addStock(Stock(5, 4))
    # print(sheet.unpacked_stocks)
    """
    20 20
    4 1
    4 5
    9 4
    3 5
    3 9
    1 4
    5 3
    4 1
    5 5
    7 2
    9 3
    3 13
    2 8
    15 4
    5 4
    10 6
    7 2
    """
    sheet = Sheet(20, 20)
    stocks = [
        Stock(4, 1),
        Stock(4, 5),
        Stock(9, 4),
        Stock(3, 5),
        Stock(3, 9),
        Stock(1, 4),
        Stock(5, 3),
        Stock(4, 1),
        Stock(5, 5),
        Stock(7, 2),
        Stock(9, 3),
        Stock(3, 13),
        Stock(2, 8),
        Stock(15, 4),
        Stock(5, 4),
        Stock(10, 6),
        Stock(7, 2),
    ]
    sheet.addStocks(stocks)
    sheet.packNext((0, 0))
    sheet.packNext((5, 0))

    sheet.exportSheet()
    sheet2 = Sheet.importSheet()

    # from visualization import VisualSheet

    # VisualSheet(sheet2).draw()
