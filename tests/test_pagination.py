from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self) -> None:
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_quantity=4,
            current_page=1,
        )
        desired_range = [1, 2, 3, 4]

        if desired_range != pagination:
            msg = f"The desired range '{desired_range}' is not in pagination"
            raise AssertionError(msg)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(
        self,
    ) -> None:
        page_range = list(range(1, 21))
        page_quantity = 4

        current_page = 1
        pagination = make_pagination_range(
            page_range=page_range,
            page_quantity=page_quantity,
            current_page=current_page,
        )
        desired_range = [1, 2, 3, 4]

        current_page = 2
        pagination = make_pagination_range(
            page_range=page_range,
            page_quantity=page_quantity,
            current_page=current_page,
        )
        desired_range = [1, 2, 3, 4]

        # ------------------- Range should change here -----------------------
        current_page = 3
        pagination = make_pagination_range(
            page_range=page_range,
            page_quantity=page_quantity,
            current_page=current_page,
        )
        desired_range = [2, 3, 4, 5]

        current_page = 4
        pagination = make_pagination_range(
            page_range=page_range,
            page_quantity=page_quantity,
            current_page=current_page,
        )
        desired_range = [3, 4, 5, 6]

        if desired_range != pagination:
            msg = f"The desired range '{desired_range}' is not equal to pagination"
            raise AssertionError(msg)
