from stock import Stock, Sheet


def cutting_stock_problem(sheet):
    # Sort the rectangles in descending order of height
    stocks.sort(key=lambda s: s.height, reverse=True)

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


# Example usage
sheet = Sheet(10, 10)
stocks = [Stock(4, 3), Stock(2, 5), Stock(3, 2), Stock(1, 4)]
sheet.addStocks(stocks)

result = cutting_stock_problem(sheet)
print(result)
