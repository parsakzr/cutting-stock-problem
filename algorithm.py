from stock import Stock, Sheet
from visualization import VisualSheet
import logging, sys


# Auxiliary functions
def is_intersecting(rect1, rect2):
    """
    Check if two rectangles are intersecting
    :param rect1: tuple of (x, y, width, height)
    :param rect2: tuple of (x, y, width, height)
    :return: True if the two rectangles are intersecting, False otherwise
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)


# def intersecting_direction(rect1, rect2):
#     """
#     Check if two rectangles are intersecting
#     :param rect1: tuple of (x, y, width, height)
#     :param rect2: tuple of (x, y, width, height)
#     :return: 'x' if the two rectangles are intersecting on the x axis, 'y' if on the y axis
#     """
#     x1, y1, w1, h1 = rect1
#     x2, y2, w2, h2 = rect2
#     if x1 + w1 <= x2 or x2 + w2 <= x1:
#         return "x"
#     if y1 + h1 <= y2 or y2 + h2 <= y1:
#         return "y"
#     return None


def cutting_stock_problem(sheet):
    # Sort the rectangles in descending order of height
    stocks = sorted(sheet.unpacked_stocks, key=lambda s: s.height, reverse=True)
    # stocks.sort(key=lambda s: s.height, reverse=True)

    # Initialize the sheet with the first stock
    sheet.packNext((0, 0))

    # Iterate through the stocks
    while len(sheet.unpacked_stocks) > 0:
        # Get the next stock
        stock = sheet.unpacked_stocks[0]

        x, y = None, None

        # Iterate through the sheet
        for i, packed_stock in enumerate(sheet.packed_stocks):
            # Pack the stock in the current location
            if sheet.validate_pack_step(
                stock, (packed_stock.x + packed_stock.width, packed_stock.y)
            ):
                x, y = packed_stock.x + packed_stock.width, packed_stock.y
                break
            if sheet.validate_pack_step(
                stock, (packed_stock.x, packed_stock.y + packed_stock.height)
            ):
                x, y = packed_stock.x, packed_stock.y + packed_stock.height
                break

            # if still not packed, rotate the stock
            stock.rotate90()

            # try again
            if sheet.validate_pack_step(
                stock, (packed_stock.x + packed_stock.width, packed_stock.y)
            ):
                x, y = packed_stock.x + packed_stock.width, packed_stock.y
                break
            if sheet.validate_pack_step(
                stock, (packed_stock.x, packed_stock.y + packed_stock.height)
            ):
                x, y = packed_stock.x, packed_stock.y + packed_stock.height
                break

        # Pack the stock in the current location
        if x is None and y is None:
            print("Cannot pack the stock")
            return False
        # then it was successfully packed, so pack it and go to the next stock
        sheet.pack(stock, (x, y))

    return True


def bin_packing_BLF(sheet, rotation=False):
    """
    Bin Packing Algorithm: Bottom Left Fill
    Consists of two steps:
    1. Try to pack the item in available rectangles
    2.1. If packed, update the available rectangles
    2.2. If not packed, create a new rectangle

    :param sheet: Sheet object that contains the stocks
    """

    def update_available_rectangles(
        available_rectangles, packed_rectangle_index, packed_stock
    ):
        """
        Update the available rectangles after packing a stock
        :param available_rectangles: list of available rectangles
        :param packed_stock: Stock object that was packed
        :return: updated available rectangles with the required changes applied.
        """
        # Get the packed rectangle
        xr, yr, wr, hr = available_rectangles[packed_rectangle_index]
        packed_stock_rect = (
            packed_stock.x,
            packed_stock.y,
            packed_stock.width,
            packed_stock.height,
        )
        # Create the new top and right rectangles
        right_rectangle = (xr + packed_stock.width, yr, wr - packed_stock.width, hr)
        top_rectangle = (xr, yr + packed_stock.height, wr, hr - packed_stock.height)
        # Add the new top and right rectangles
        if wr > packed_stock.width:  # if there's space for a right rectangle
            available_rectangles.append(right_rectangle)
        if hr > packed_stock.height:  # top rectangle
            available_rectangles.append(top_rectangle)

        # Remove the packed rectangle from the available rectangles
        available_rectangles.pop(packed_rectangle_index)

        # check collision with other rectangles and update the rectangles
        for i, (xr, yr, wr, hr) in enumerate(available_rectangles):
            # TODO Think: should the new rectangles be checked upon or the original packed one?
            if is_intersecting(right_rectangle, (xr, yr, wr, hr)):
                # if it's on the same plane, then it's eaten by the bottom rectangle
                if xr == right_rectangle[0] and yr != right_rectangle[1]:
                    logging.info(
                        f"{right_rectangle} Eaten by the bottom rectangle {(xr, yr, wr, hr)}"
                    )  # DEBUG
                    available_rectangles.remove(
                        right_rectangle
                    )  # remove the right rectangle
                else:
                    available_rectangles[i] = (
                        xr,
                        yr,
                        right_rectangle[0] + right_rectangle[2] - xr,
                        hr,
                    )
            if is_intersecting(top_rectangle, (xr, yr, wr, hr)):
                # if it's on the same plane, then it's eaten by the left rectangle
                if yr == top_rectangle[1] and xr != top_rectangle[0]:
                    logging.info(
                        f"{top_rectangle} Eaten by the left rectangle {(xr, yr, wr, hr)}"
                    )  # DEBUG
                    available_rectangles.remove(top_rectangle)
                else:
                    available_rectangles[i] = (
                        xr,
                        yr,
                        wr,
                        top_rectangle[1] + top_rectangle[3] - yr,
                    )
            if is_intersecting(packed_stock_rect, (xr, yr, wr, hr)):
                # update the rectangle so it's cut by the packed stock
                # example: rect(0, 6, 20, 5) and stock(6, 5, 3, 5) -> cut vertically
                # example: rect(16, 5, 4, 3) and stock(19, 0, 1, 10) -> cut horizontally
                # cut the rectangle with the packed stock
                available_rectangles[i] = (
                    (xr, yr, wr, packed_stock.y - yr)
                    if packed_stock.y > yr  # is on the top, cutting horizontally
                    else (xr, yr, packed_stock.x - xr, hr)
                )

            # Remove the rectangles with zero width or height
            if available_rectangles[i][2] == 0 or available_rectangles[i][3] == 0:
                available_rectangles.pop(i)

        # Sort the rectangles in descending order of height
        # old: sort by height, if equal then by width, then by x, then by y: r[3], r[2], r[0], r[1]
        # new: sort by lower y, if equal then by lower x, then by higher height, then by higher width
        available_rectangles.sort(
            key=lambda r: (r[1], r[0], -r[3], -r[2]), reverse=False
        )

        return available_rectangles

    # Beginning of the main algorithm
    # Sort the stocks in descending order of height
    # stocks.sort(key=lambda s: s.height, reverse=True)
    stocks = sorted(sheet.unpacked_stocks, key=lambda s: s.height, reverse=True)
    logging.info(stocks)  # DEBUG

    available_rectangles = [
        (0, 0, sheet.width, sheet.height)  # xr, yr, wr, hr
    ]  # initial the sheet as one available rectangle
    for stock in stocks:
        is_packed = False
        # Find the first rectangle that can fit the stock
        for i, (xr, yr, wr, hr) in enumerate(available_rectangles):
            if wr >= stock.width and hr >= stock.height:
                # Pack the stock in the current location
                logging.info(f"Packing Stock: {stock}")  # DEBUG
                is_packed = sheet.validate_pack_step(stock, (xr, yr))

                if rotation == True:
                    # in this block, we try to rotate the stock and see if it fits
                    # if a better choice, we replace the stock with the rotated one
                    stock_rotated = Stock(
                        stock.height, stock.width
                    )  # a copy of stock rotated 90 degrees
                    is_packed_rotated = sheet.validate_pack_step(
                        stock_rotated, (xr, yr)
                    )
                    if is_packed_rotated and not is_packed:
                        stock.rotate90()
                        is_packed = True
                    if is_packed_rotated and is_packed:
                        # if both rotations are valid, choose the one with center lower and right
                        if (
                            stock.width < stock.height
                        ):  # if the original stock is taller than it is wide
                            stock.rotate90()
                    is_packed = (
                        is_packed or is_packed_rotated
                    )  # if either one is true, then it's packable

                if is_packed:  # if valid, actually pack it
                    sheet.pack(stock, (xr, yr))
                    available_rectangles = update_available_rectangles(
                        available_rectangles, i, stock
                    )
                    logging.info(f"Packed: {is_packed}")  # DEBUG
                    logging.info(f"Rectangles: {available_rectangles}")  # DEBUG
                    break

        # after all the rectangles, if still not packed, then it's not packable
        if not is_packed:
            logging.info(f"Cannot pack the stock {stock}")  # DEBUG
            # return False  # if cannot pack a stock, halt the algorithm

        # VisualSheet(sheet).draw(unpacked=True)  # DEBUG
    # Algorithm finished
    if len(sheet.unpacked_stocks) > 0:
        return False
    return True


def test_and_visualize_BLF():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    # C2_1
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

    is_success = bin_packing_BLF(sheet, rotation=False)
    print(f"Did it succeed?: {is_success}")  # DEBUG
    print(f"Packing efficiency: {sheet.getEfficiency()}")  # DEBUG
    # VisualSheet(sheet).draw(unpacked=True) # DEBUG
    VisualSheet(sheet).draw(unpacked=True)
    print(sheet.getStats())  # DEBUG


if __name__ == "__main__":
    test_and_visualize_BLF()
