from unittest import TestCase
from distutils.version import LooseVersion

from vortexasdk.utils import (
    convert_to_list,
    convert_values_to_list,
    get_latest_sdk_version,
)


class TestUtils(TestCase):
    def test_single_item_list(self):
        assert convert_to_list("a") == ["a"]

    def test_multiple_items_list(self):
        actual = convert_to_list(["a", "b"])
        assert actual == ["a", "b"] or actual == ["b", "a"]

    def test_convert_values_to_list(self):
        d = {1: None, 2: "b", 3: ["c"]}

        expected = {1: [], 2: ["b"], 3: ["c"]}

        assert convert_values_to_list(d) == expected

    def test_get_latest_sdk_version(self):
        sdk_old_version = "0.18.0"

        lv = get_latest_sdk_version()

        assert lv > LooseVersion(sdk_old_version)
