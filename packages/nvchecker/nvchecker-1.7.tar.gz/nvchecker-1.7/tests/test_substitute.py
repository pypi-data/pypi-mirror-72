# MIT licensed
# Copyright (c) 2013-2017 lilydjwg <lilydjwg@gmail.com>, et al.

import pytest
pytestmark = pytest.mark.asyncio

async def test_substitute_prefix(get_version):
    assert await get_version("example", {"manual": "v1.0", "prefix": "v"}) == "1.0"

async def test_substitute_prefix_missing_ok(get_version):
    assert await get_version("example", {"manual": "1.0", "prefix": "v"}) == "1.0"

async def test_substitute_regex(get_version):
    assert await get_version("example", {"manual": "r15c", "from_pattern": r"r(\d+)([a-z])", "to_pattern": r"r\1.\2"}) == "r15.c"

async def test_substitute_regex_missing_ok(get_version):
    assert await get_version("example", {"manual": "r15", "from_pattern": r"r(\d+)([a-z])", "to_pattern": r"r\1.\2"}) == "r15"

async def test_substitute_prefix_has_higher_priority(get_version):
    assert await get_version("example", {"manual": "r15", "prefix": "r", "from_pattern": r"r(\d+)", "to_pattern": r"R\1"}) == "15"
