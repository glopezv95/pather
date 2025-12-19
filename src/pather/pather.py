from pathlib import Path
from typing import TypeVar, overload, Iterable, Literal, Optional, Generator, Union
import re
from stringmop.normalization import normalize

from .constants import RED, RESET

T_str_path = TypeVar('T_str_path', str, Path)

@overload
def _create_generator(
        iterable: Iterable[T_str_path],
        enum: Literal[True],
        include: Iterable[str],
        exclude: Optional[Iterable[str]] = ...
    ) -> Generator[int, None, None]: ...

@overload
def _create_generator(
        iterable: Iterable[T_str_path],
        enum: Literal[False],
        include: Iterable[str],
        exclude: Optional[Iterable[str]] = ...
    ) -> Generator[T_str_path, None, None]: ...

def _val_to_str(val: T_str_path) -> str:
    return val.name if isinstance(val, Path) else val

def _create_enum_generator(
        iterable: Iterable[T_str_path],
        include: Iterable[str],
        exclude: Optional[Iterable[str]]
) -> Generator[int, None, None]:
    
    return (
        i for i, val in enumerate(iterable)
        if all(
            re.search(normalize(s), normalize(_val_to_str(val)))
            for s in include
        )
        and not any(
            re.search(normalize(s), normalize(_val_to_str(val)))
            for s in exclude or []
        )
    )

def _create_non_enum_generator(
        iterable: Iterable[T_str_path],
        include: Iterable[str],
        exclude: Optional[Iterable[str]]
) -> Generator[T_str_path, None, None]:
    
    return (
        val for val in iterable
        if all(
            re.search(normalize(s), normalize(_val_to_str(val)))
            for s in include
        )
        and not any(
            re.search(normalize(s), normalize(_val_to_str(val)))
            for s in exclude or []
        )
    )

def _create_generator(
        iterable: Iterable[T_str_path],
        enum: bool,
        include: Iterable[str],
        exclude: Optional[Iterable[str]] = None,
    ):

    if enum:
        return _create_enum_generator(
            iterable=iterable,
            include=include,
            exclude=exclude
        )
    else:
        return _create_non_enum_generator(
            iterable=iterable,
            include=include,
            exclude=exclude
        )

def _get_part_idx(
        path_src: Path,
        include: Iterable[str],
        exclude: Optional[Iterable[str]]
    ) -> int:

    return next(
        _create_generator(
            iterable=path_src.parts, enum=True,
            include=include, exclude=exclude
        )
    )

def get_home_path() -> Path:
    return Path().home()

def get_parent_path(
        path_src: Union[Path, str],
        include: Iterable[str],
        exclude: Optional[Iterable[str]] = None
    ) -> Path:

    path_src = (
        path_src.resolve()
        if isinstance(path_src, Path)
        else Path(path_src).resolve()
    )

    try:
        path_dst = Path(
            *path_src.parts[
                :_get_part_idx(path_src=path_src, include=include, exclude=exclude) +1
            ]
        )
    except StopIteration:
        raise StopIteration(
            f"{RED}\n\nNo path found with patterns provided in 'include' and without patterns provided in 'exclude' on 'path_src'.\n{'-' * 100}\n{path_src=}\n{include=}\n{exclude=}\n{RESET}"
        )
    
    return path_dst

def get_child_path(
        path_src: Union[Path, str],
        include: Iterable[str],
        exclude: Optional[Iterable[str]] = None
    ) -> Path:

    path_src = (
        path_src.resolve()
        if isinstance(path_src, Path)
        else Path(path_src).resolve()
    )

    try:
        path_dst = next(
            _create_generator(
                iterable=path_src.iterdir(), enum=False,
                include=include, exclude=exclude
            )
        ).resolve()
    except StopIteration:
        raise StopIteration(
            f"{RED}\n\nNo path found with patterns provided in 'include' and without patterns provided in 'exclude' on 'path_src'.\n{'-' * 100}\n{path_src=}\n{include=}\n{exclude=}\n{RESET}"
        )
    
    return path_dst

if __name__ == '__main__':

    path_home = get_child_path(path_src=Path(), include=[r'project'], exclude=[r'toml'])
    print(path_home)