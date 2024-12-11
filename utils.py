from collections.abc import Callable
from typing import Generator
from pathlib import Path
import os
from typing import Generic, TypeVar

T = TypeVar('T')
K = TypeVar('K')


def read_lines(path: str | Path) -> Generator[str, None, None]:
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            yield line.strip()

class Option(Generic[T]):
    __GUARD = object()

    __slots__ = ('__value',)

    def __init__(self):
        raise RuntimeError('Option can only be instantiated using Option.some(value) or Option.none()')

    @classmethod
    def some(cls, value: T) -> "Option[T]":
        ret = super().__new__(cls)
        ret.__value = value
        return ret

    @classmethod
    def none(cls) -> "Option[K]":
        ret = super().__new__(cls)
        ret.__value = Option.__GUARD
        return ret

    def is_some(self) -> bool:
        return self.__value != Option.__GUARD

    def is_none(self) -> bool:
        return self.__value == Option.__GUARD

    def unwrap(self) -> T:
        if self.is_none():
            raise RuntimeError('cannot unwrap Option.none')
        return self.__value

    def unwrap_or(self, default: T) -> T:
        if self.is_none():
            return default
        return self.__value

    def map(self, mapper: Callable[[T], K]) -> "Option[K]":
        if self.is_none():
            return Option.none()
        return Option.some(mapper(self.__value))

    def __repr__(self) -> str:
        if self.is_none():
            return f'Option.none()'
        return f'Option.some({self.__value!r})'

    @classmethod
    def wrap(cls, value: K | None) -> "Option[K]":
        if value is None:
            return Option.none()
        return Option.some(value)


if __name__ == '__main__':
    DAY = 7
    os.mkdir(f'./day{DAY}')
    with open(f'./day{DAY}/day{DAY}.py', 'w+', encoding='utf-8') as file:
        pass
    with open(f'./day{DAY}/input.txt', 'w+', encoding='utf-8') as file:
        pass
    with open(f'./day{DAY}/test.txt', 'w+', encoding='utf-8') as file:
        pass

