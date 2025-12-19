from typing import Generator
import pytest

from pather.pather import _create_generator

class TestCreateGenerator:

    def test_empty_false(self) -> None:
        result = _create_generator([], False, [])

        assert isinstance(result, Generator)
        with pytest.raises(StopIteration):
            next(result)

    def test_empty_true(self) -> None:
        result = _create_generator([], True, [])

        assert isinstance(result, Generator)
        with pytest.raises(StopIteration):
            next(result)

    def test_generic_correct_nenum(self) -> None:
        result = _create_generator(
            iterable=['acbcd', 'ácdr', 'bc', '\tacd', 'c'],
            enum=False,
            include=['ac', 'cd'],
            exclude=['b']
        )

        assert isinstance(result, Generator)
        assert next(result) == 'ácdr'
        assert next(result) == '\tacd'
        with pytest.raises(StopIteration):
            assert next(result)

    def test_generic_correct_enum(self) -> None:
        result = _create_generator(
            iterable=['acbcd', 'ácdr', 'bc', '\tacd', 'c'],
            enum=True,
            include=['ac', 'cd'],
            exclude=['b']
        )

        assert isinstance(result, Generator)
        assert next(result) == 1
        assert next(result) == 3
        with pytest.raises(StopIteration):
            assert next(result)

    def test_generic_incorrect_nenum(self) -> None:
        result = _create_generator(
            iterable=['acbcd', 'ácdr', 'bc', '\tacd', 'c'],
            enum=False,
            include=['37', 'cd'],
            exclude=['b']
        )

        assert isinstance(result, Generator)
        with pytest.raises(StopIteration):
            assert next(result)

    def test_generic_incorrect_enum(self) -> None:
        result = _create_generator(
            iterable=['acbcd', 'ácdr', 'bc', '\tacd', 'c'],
            enum=True,
            include=['37', 'cd'],
            exclude=['b']
        )

        assert isinstance(result, Generator)
        with pytest.raises(StopIteration):
            assert next(result)

    def test_generic_correct_nenum(self) -> None:
        result = _create_generator(
            iterable=['acbcd', 'ácdr', 'bc', '\tacd', 'c'],
            enum=False,
            include=['ac', 'cd'],
            exclude=['b']
        )

        assert isinstance(result, Generator)
        assert next(result) == 'ácdr'
        assert next(result) == '\tacd'
        with pytest.raises(StopIteration):
            assert next(result)

    def test_exclude_nenum(self) -> None:
        result = _create_generator(
            iterable=['acbcd', 'ácdr', 'bc', '\tacd', 'c'],
            enum=False,
            include=['ac', 'cd']
        )

        assert isinstance(result, Generator)
        assert next(result) == 'acbcd'
        assert next(result) == 'ácdr'
        assert next(result) == '\tacd'
        with pytest.raises(StopIteration):
            assert next(result)

    def test_exclude_enum(self) -> None:
        result = _create_generator(
            iterable=['acbcd', 'ácdr', 'bc', '\tacd', 'c'],
            enum=True,
            include=['ac', 'cd']
        )

        assert isinstance(result, Generator)
        assert next(result) == 0
        assert next(result) == 1
        assert next(result) == 3
        with pytest.raises(StopIteration):
            assert next(result)