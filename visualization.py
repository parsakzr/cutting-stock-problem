import matplotlib.pyplot as plt
from stock import Stock, Sheet


class VisualSheet:
    def __init__(self, sheet: Sheet):
        self.sheet = sheet
        # matplotlib figure
        # figure is a canvas for the whole visualization

        self.fig = plt.figure(
            figsize=(self.sheet.width * 2, self.sheet.height)
        )  # figure contains two subplots in one row
        # figsize=(self.sheet.width * 2, self.sheet.height)
        # figuresize

        # axes, two axes for two subplots, one for sheet, one for unpacked stocks
        self.ax = self.fig.add_subplot(121)  # with size sheet.width x sheet.height

        # the dimensions of the self.ax is sheet.width x sheet.height
        self.ax.set_xlim(0, sheet.width)
        self.ax.set_ylim(0, sheet.height)
        self.ax.set_title("Sheet")

        self.ax_unpacked = self.fig.add_subplot(122)
        self.ax_unpacked.set_xlim(0, sheet.width)
        self.ax_unpacked.set_ylim(0, sheet.height)
        self.ax_unpacked.set_title("Unpacked Stocks")
        self.ax_unpacked.set_xticks([])
        self.ax_unpacked.set_yticks([])
        self.ax_unpacked.axis("equal")

    def draw(self, unpacked=False):
        """
        Draw the sheet and the stocks

        Args:
            unpacked: whether to draw the unpacked stocks or just the sheet
        """

        # set the visibility of the unpacked stocks
        self.ax_unpacked.set_visible(unpacked)

        self.draw_sheet()

        if unpacked:
            self.draw_unpacked()

        plt.show()

    def draw_sheet(self):
        """
        Draw the sheet with the stocks packed on it
        """
        for stock in self.sheet.packed_stocks:
            self._draw_stock(self.ax, stock)

    def draw_unpacked(self):
        """
        Draw the unpacked stocks,
        Since the location of the unpacked stocks are all (0,0),
        it's better to draw them on a grid. The drawing algorithm is as follows:
        1. gather the max_width and max_height of the unpacked stocks
        2. calculate the number of rows and columns needed to draw the unpacked stocks
        3. draw the unpacked stocks on the grid
        """

        def _draw_stocks_staggered(canvas_width, canvas_height, stocks, margin):
            """Draws rectangles in a staggered layout within the given canvas."""

            max_width = max([stock.width for stock in self.sheet.unpacked_stocks])
            # Calculate columns assuming maximum width rectangles
            columns = canvas_width // (max_width + 2 * margin)

            column_baselines = [0] * columns  # Track baseline for each column

            for stock in stocks:
                # Find the column with the lowest baseline
                shortest_column = column_baselines.index(min(column_baselines))

                # Calculate x and y coordinates
                x = shortest_column * (max_width + margin) + margin
                y = column_baselines[shortest_column]

                # Draw the stock
                self._draw_stock(self.ax_unpacked, stock, custom_xy=(x, y))

                # Update the baseline for that column
                column_baselines[shortest_column] += stock.height + margin

        _draw_stocks_staggered(
            self.sheet.width, self.sheet.height, self.sheet.unpacked_stocks, margin=1
        )

        # --------
        """
        max_width = max([stock.width for stock in self.sheet.unpacked_stocks])
        max_height = max([stock.height for stock in self.sheet.unpacked_stocks])

        MARGIN = 1  # margin between stocks
        max_width += 2 * MARGIN
        max_height += 2 * MARGIN
        # calculate the number of rows and columns needed to draw the unpacked stocks
        num_rows = self.sheet.height // max_height
        num_cols = self.sheet.width // max_width

        # draw the unpacked stocks on the grid
        # keep track of the current row and column
        current_row = 0
        current_column = 0
        for stock in self.sheet.unpacked_stocks:
            # calculate the x and y coordinates of the stock
            x = current_column * max_width + MARGIN
            y = current_row * max_height + MARGIN
            # draw the stock
            self._draw_stock(self.ax_unpacked, stock, custom_xy=(x, y))

            # update the current row and column
            current_column += 1
            if current_column == num_cols:
                current_column = 0
                current_row += 1
        """

    def _draw_stock(self, ax, stock, *, custom_xy: tuple = None) -> None:
        """
        Draw a stock using matplotlib Rectangle

        Args:
            ax: axes to draw the stock on (sheet or unpacked)
            stock: stock to draw
        """

        def _draw_rectangle(
            ax, x, y, width, height, *, color="black", lw=2, fill=False, text=None
        ) -> None:
            ax.add_patch(
                plt.Rectangle((x, y), width, height, fill=fill, facecolor=color, lw=2)
            )
            if text or text != "":
                ax.text(x + width / 2, y + height / 2, text, ha="center", va="center")

        # draw the stock
        if custom_xy:
            x, y = custom_xy
        else:
            x, y = stock.x, stock.y

        _draw_rectangle(
            ax,
            x,
            y,
            stock.width,
            stock.height,
            text=f"{stock.width}x{stock.height}",
        )

    # draw the rectangle in a canvas
