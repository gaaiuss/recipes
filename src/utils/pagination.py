from math import ceil


def make_pagination_range(
    page_range: list[int],
    page_quantity_per_range: int,
    current_page: int,
) -> dict[str, list[int] | int | bool]:
    """
    Return a "window" of page numbers to display around the current page.

    Example: with 10 pages, page_quantity_per_range=4 and current_page=5,
    the window is [3, 4, 5, 6] -> roughly 2 pages on each side.
    """
    total_pages = len(page_range)

    # Half of the window size, rounded up. This is how many pages we try to
    # show on each side of the current page.
    # Example: page_quantity_per_range=5 -> ceil(2.5) = 3
    middle_range = ceil(page_quantity_per_range / 2)

    # Initial window boundaries, centered on the current page.
    # `stop_range` is exclusive because it is used in a slice at the end.
    start_range = current_page - middle_range
    stop_range = current_page + middle_range

    # Problem 1: the window starts before the first page.
    # Example: current_page=1, middle_range=3 -> start_range=-2, which is
    # not a valid index. We shift the whole window to the right so it
    # still shows the same number of pages.
    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0  # Clamp the start to the first page.
        stop_range += start_range_offset  # Push the end forward to compensate.

    # Problem 2: the window goes past the last page.
    # `stop_range - total_pages` is how far we overshot, so we move the start
    # back by that amount to keep the window size consistent.
    # Example: total_pages=10, stop_range=12 -> overshoot of 2 -> start moves
    # back by 2. (Slicing already ignores indexes past the end of the list.)
    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]

    return {
        "pagination": pagination,
        "page_range": page_range,
        "page_quantity_per_range": page_quantity_per_range,
        "current_page": current_page,
        "total_pages": total_pages,
        "start_range": start_range,
        "stop_range": stop_range,
        "first_page_out_of_range": current_page > middle_range,
        "last_page_out_of_range": stop_range < total_pages,
    }
