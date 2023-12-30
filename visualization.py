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
        self.ax.set_title("Sheet")
        self.ax.set_xlim(0, sheet.width)
        self.ax.set_ylim(0, sheet.height)
        self.ax.set_xticks([0, sheet.width])
        self.ax.set_yticks([0, sheet.height])
        self.ax.axis("scaled")

        self.ax_unpacked = self.fig.add_subplot(122)
        self.ax_unpacked.set_title("Unpacked Stocks")
        self.ax_unpacked.set_xlim(0, sheet.width)
        self.ax_unpacked.set_ylim(0, sheet.height)
        self.ax_unpacked.set_xticks([])
        self.ax_unpacked.set_yticks([])
        self.ax_unpacked.axis("scaled")

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
        #
        xticks_set = set(self.ax.get_xticks())
        yticks_set = set(self.ax.get_yticks())
        print(xticks_set, yticks_set)

        for stock in self.sheet.packed_stocks:
            self._draw_stock(self.ax, stock)
            # add to x and y ticks for better visualization
            xticks_set.update((stock.x, stock.x + stock.width))
            yticks_set.update((stock.y, stock.y + stock.height))
        self.ax.set_xticks(list(xticks_set))
        self.ax.set_yticks(list(yticks_set))

    def draw_unpacked(self):
        """
        Draw the unpacked stocks,
        Since the location of the unpacked stocks are all (0,0),
        it's better to draw them on a grid. The drawing algorithm is as follows:
        1. gather the max_width and max_height of the unpacked stocks
        2. calculate the number of rows and columns needed to draw the unpacked stocks
        3. draw the unpacked stocks on the grid
        """

        def _draw_stocks_staggered(
            canvas_width, canvas_height, stocks, margin, scale=1.0
        ):
            """Draws rectangles in a staggered layout within the given canvas."""

            max_width = max(
                [stock.width * scale for stock in self.sheet.unpacked_stocks]
            )
            # Calculate columns assuming maximum width rectangles
            columns = canvas_width // (max_width + 2 * margin)

            column_baselines = [0] * columns  # Track baseline for each column

            for stock in stocks:
                # Find the column with the lowest baseline
                shortest_column = column_baselines.index(min(column_baselines), 0)

                # Calculate x and y coordinates
                x = shortest_column * (max_width + margin) + margin
                y = column_baselines[shortest_column]

                # Draw the stock
                self._draw_stock(
                    self.ax_unpacked,
                    Stock(stock.width * scale, stock.height * scale, x, y),
                    custom_text=f"{stock.width}x{stock.height}",
                )

                # Update the baseline for that column
                column_baselines[shortest_column] += stock.height * scale + margin

        def _draw_stocks_grid(canvas_width, canvas_height, stocks, margin, scale=1.0):
            """Draws rectangles in a grid layout within the given canvas."""

            max_width = max([stock.width for stock in stocks]) * scale
            max_height = max([stock.height for stock in stocks]) * scale

            # Calculate columns and rows assuming maximum width and height rectangles
            num_cols = canvas_width // (max_width + 2 * margin) or 1
            num_rows = canvas_height // (max_height + 2 * margin) or 1

            for i, stock in enumerate(stocks):
                # Calculate x and y coordinates
                x = (i % num_cols) * (max_width + margin) + margin
                y = (i // num_cols) * (max_height + margin) + margin

                # Draw the stock
                self._draw_stock(
                    self.ax_unpacked,
                    Stock(stock.width * scale, stock.height * scale, x, y),
                    custom_text=f"{stock.width}x{stock.height}",
                )

        def _draw_stocks_horizontal(
            canvas_width, canvas_height, stocks, margin, scale=1.0
        ):
            """Draws rectangles in only one axis next to each other within the given canvas."""
            last_x = 0
            for i, stock in enumerate(stocks):
                # Calculate x and y coordinates
                x = last_x + margin
                y = margin
                last_x += stock.width + margin

                # Draw the stock
                self._draw_stock(
                    self.ax_unpacked,
                    Stock(stock.width * scale, stock.height * scale, x, y),
                    custom_text=f"{stock.width}x{stock.height}",
                )

        # Choose a drawing style for the unpacked
        _draw_stocks_grid(
            self.sheet.width,
            self.sheet.height,
            self.sheet.unpacked_stocks,
            margin=1,
            scale=0.5,
        )

    def _draw_stock(
        self, ax, stock, *, custom_xy: tuple = None, custom_text=None
    ) -> None:
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
            text=f"{stock.width}x{stock.height}" if not custom_text else custom_text,
        )

    # draw the rectangle in a canvas
