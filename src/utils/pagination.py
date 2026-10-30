from math import ceil


def make_pagination_range(
    page_range: list[int],
    page_quantity: int,
    current_page: int,
) -> list[int]:
    # Calculates the smaller integer of the page total quantity.
    middle_range = ceil(page_quantity / 2)

    # Get the start range based on the current page - middle range. This will
    # cause an error on the stop range later because the first start range will
    # be negative (-1 for instance).
    start_range = current_page - middle_range

    # This is the pages quantity limit that will be shown.
    stop_range = current_page + middle_range

    # When the start range is negative, like in the first loop rotation, we save
    # this number on another variable transforming it in positive to fix the
    # stop range later.
    start_range_offset = abs(start_range) if start_range < 0 else 0

    # When the start range is negative we fix the range variables setting the
    # start to 0 and adding the offset range on the stop range.
    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    return page_range[start_range:stop_range]
