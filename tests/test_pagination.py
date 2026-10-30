from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def assert_pagination_range(
        self,
        desired_range: list[int],
        pagination: list[int] | int,
    ) -> None:
        if desired_range != pagination:
            msg = f"The desired range '{desired_range}' != '{pagination}'"
            raise AssertionError(msg)

    def setup_default_pagination(self, current_page: int) -> list[int] | int:
        page_range = list(range(1, 21))
        page_quantity_per_range = 4

        return make_pagination_range(
            page_range=page_range,
            page_quantity_per_range=page_quantity_per_range,
            current_page=current_page,
        )["pagination"]

    def test_make_pagination_range_returns_a_pagination_range(self) -> None:
        current_page = 1
        pagination = self.setup_default_pagination(current_page)
        desired_range = [1, 2, 3, 4]

        self.assert_pagination_range(desired_range, pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(
        self,
    ) -> None:
        current_page = 1
        pagination = self.setup_default_pagination(current_page)
        desired_range = [1, 2, 3, 4]

        self.assert_pagination_range(desired_range, pagination)

        current_page = 2
        pagination = self.setup_default_pagination(current_page)
        desired_range = [1, 2, 3, 4]

        self.assert_pagination_range(desired_range, pagination)

        # ------------------- Range should change here -----------------------
        current_page = 3
        pagination = self.setup_default_pagination(current_page)
        desired_range = [2, 3, 4, 5]

        self.assert_pagination_range(desired_range, pagination)

        current_page = 4
        pagination = self.setup_default_pagination(current_page)
        desired_range = [3, 4, 5, 6]

        self.assert_pagination_range(desired_range, pagination)

    def test_make_pagination_range_makes_sure_middle_ranges_are_correct(
        self,
    ) -> None:
        # Tests if middle range page numbers are correct.
        current_page = 10
        pagination = self.setup_default_pagination(current_page)
        desired_range = [9, 10, 11, 12]

        self.assert_pagination_range(desired_range, pagination)

        current_page = 12
        pagination = self.setup_default_pagination(current_page)
        desired_range = [11, 12, 13, 14]

        self.assert_pagination_range(desired_range, pagination)

    def test_make_pagination_range_is_static_if_last_pages(self) -> None:
        current_page = 18
        pagination = self.setup_default_pagination(current_page)
        desired_range = [17, 18, 19, 20]

        self.assert_pagination_range(desired_range, pagination)

        current_page = 19
        pagination = self.setup_default_pagination(current_page)
        desired_range = [17, 18, 19, 20]

        self.assert_pagination_range(desired_range, pagination)

        current_page = 20
        pagination = self.setup_default_pagination(current_page)
        desired_range = [17, 18, 19, 20]

        self.assert_pagination_range(desired_range, pagination)

        current_page = 21
        pagination = self.setup_default_pagination(current_page)
        desired_range = [17, 18, 19, 20]

        self.assert_pagination_range(desired_range, pagination)
