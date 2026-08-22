"""
script_python.py

A deliberately unusual collection of Python machinery.

This file is intentionally Python-heavy.
It does not require third-party packages.
"""

from __future__ import annotations

import asyncio
import contextlib
import functools
import hashlib
import itertools
import math
import random
import statistics
import string
import sys
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Iterator,
    TypeVar,
    Generic,
)


# ============================================================
# 1. GLOBAL PYTHON WEIRDNESS
# ============================================================

T = TypeVar("T")
R = TypeVar("R")


MAGIC_NUMBER = 0xC0FFEE
PHRASE = "Python is hiding in the repository."


def xor_shuffle(value: str, key: int = MAGIC_NUMBER) -> str:
    """Turn a string into a deterministic sequence of characters."""
    return "".join(
        chr(ord(char) ^ (key & 0xFF))
        for char in value
    )


def reverse_without_reverse(value: str) -> str:
    """Reverse a string using slicing."""
    return value[::-1]


def fibonacci() -> Generator[int, None, None]:
    """Infinite Fibonacci generator."""
    first, second = 0, 1

    while True:
        yield first
        first, second = second, first + second


# ============================================================
# 2. ENUMS
# ============================================================

class Mood(Enum):
    CURIOUS = auto()
    CHAOTIC = auto()
    CALM = auto()
    OVERENGINEERED = auto()
    PYTHONIC = auto()


class Signal(Enum):
    ZERO = 0
    ONE = 1
    MAYBE = 2


# ============================================================
# 3. DATACLASSES
# ============================================================

@dataclass(slots=True)
class PythonArtifact:
    name: str
    weight: int
    mood: Mood = Mood.PYTHONIC
    metadata: dict[str, Any] = field(default_factory=dict)

    def fingerprint(self) -> str:
        payload = (
            f"{self.name}|"
            f"{self.weight}|"
            f"{self.mood.name}|"
            f"{sorted(self.metadata.items())}"
        )

        return hashlib.sha256(
            payload.encode("utf-8")
        ).hexdigest()


# ============================================================
# 4. DECORATORS
# ============================================================

def loudly(function: Callable[..., R]) -> Callable[..., R]:
    """Decorator that announces function execution."""

    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        print(f"[LOUD] entering {function.__name__}")
        result = function(*args, **kwargs)
        print(f"[LOUD] leaving {function.__name__}")
        return result

    return wrapper


def memoize(function: Callable[..., R]) -> Callable[..., R]:
    """Tiny hand-rolled memoization decorator."""

    cache: dict[tuple[Any, ...], R] = {}

    @functools.wraps(function)
    def wrapped(*args: Any) -> R:
        if args not in cache:
            cache[args] = function(*args)

        return cache[args]

    return wrapped


@loudly
def multiply(a: int, b: int) -> int:
    return a * b


@memoize
def strange_power(base: int, exponent: int) -> int:
    if exponent == 0:
        return 1

    return base * strange_power(base, exponent - 1)


# ============================================================
# 5. METACLASS
# ============================================================

class DramaticMeta(type):
    """A metaclass that adds a dramatic identity to classes."""

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:

        namespace["dramatic_name"] = (
            f"THE_{name.upper()}_OF_PYTHON"
        )

        return super().__new__(
            cls,
            name,
            bases,
            namespace,
        )


class QuantumPython(metaclass=DramaticMeta):

    def __init__(self, value: int) -> None:
        self.value = value

    def collapse(self) -> str:
        if self.value % 2 == 0:
            return "The Python state collapsed into EVEN."

        return "The Python state collapsed into ODD."


# ============================================================
# 6. GENERIC CONTAINER
# ============================================================

class Box(Generic[T]):

    def __init__(self, value: T):
        self.value = value

    def map(
        self,
        function: Callable[[T], R],
    ) -> "Box[R]":

        return Box(function(self.value))

    def unwrap(self) -> T:
        return self.value

    def __repr__(self) -> str:
        return f"Box({self.value!r})"


# ============================================================
# 7. CUSTOM ITERATOR
# ============================================================

class SpiralNumbers(Iterator[int]):

    def __init__(self, limit: int):
        self.limit = limit
        self.current = 0
        self.step = 1

    def __iter__(self) -> "SpiralNumbers":
        return self

    def __next__(self) -> int:
        if self.current >= self.limit:
            raise StopIteration

        value = self.current

        self.current += self.step
        self.step += 1

        return value


# ============================================================
# 8. CONTEXT MANAGER
# ============================================================

@contextlib.contextmanager
def python_dimension(name: str):
    start = time.perf_counter()

    print(f"\n>>> entering dimension: {name}")

    try:
        yield
    finally:
        elapsed = time.perf_counter() - start

        print(
            f"<<< leaving dimension: {name} "
            f"after {elapsed:.6f}s"
        )


# ============================================================
# 9. PROPERTY MAGIC
# ============================================================

class Temperature:

    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:

        if value < -273.15:
            raise ValueError(
                "Temperature cannot go below absolute zero."
            )

        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        return (self.celsius * 9 / 5) + 32

    @property
    def kelvin(self) -> float:
        return self.celsius + 273.15


# ============================================================
# 10. STRUCTURAL PATTERN MATCHING
# ============================================================

def interpret_signal(signal: Signal) -> str:

    match signal:

        case Signal.ZERO:
            return "Nothing happened."

        case Signal.ONE:
            return "Something happened."

        case Signal.MAYBE:
            return "Something theoretically happened."

        case _:
            return "Unknown quantum situation."


# ============================================================
# 11. ASYNC PYTHON
# ============================================================

async def asynchronous_counter(
    limit: int,
) -> list[int]:

    values: list[int] = []

    for number in range(limit):

        await asyncio.sleep(0)

        values.append(number)

    return values


async def parallel_python() -> list[list[int]]:

    jobs = [
        asynchronous_counter(5),
        asynchronous_counter(8),
        asynchronous_counter(3),
    ]

    return await asyncio.gather(*jobs)


# ============================================================
# 12. CUSTOM DESCRIPTOR
# ============================================================

class LoggedAttribute:

    def __init__(self, default: Any = None):
        self.default = default
        self.private_name: str | None = None

    def __set_name__(
        self,
        owner: type,
        name: str,
    ) -> None:

        self.private_name = f"_{name}"

    def __get__(
        self,
        instance: Any,
        owner: type | None = None,
    ) -> Any:

        if instance is None:
            return self

        if self.private_name is None:
            return self.default

        return getattr(
            instance,
            self.private_name,
            self.default,
        )

    def __set__(
        self,
        instance: Any,
        value: Any,
    ) -> None:

        if self.private_name is None:
            return

        print(
            f"descriptor assignment -> "
            f"{self.private_name} = {value!r}"
        )

        setattr(
            instance,
            self.private_name,
            value,
        )


class StrangeObject:

    value = LoggedAttribute("initial")

    def __init__(self):
        self.value = "Python"


# ============================================================
# 13. FUNCTION FACTORY
# ============================================================

def create_multiplier(
    factor: int,
) -> Callable[[int], int]:

    def multiplier(value: int) -> int:
        return value * factor

    return multiplier


double = create_multiplier(2)
triple = create_multiplier(3)
sevenfold = create_multiplier(7)


# ============================================================
# 14. RECURSIVE TREE
# ============================================================

@dataclass
class Node:
    value: int
    children: list["Node"] = field(default_factory=list)

    def walk(self) -> Generator[int, None, None]:

        yield self.value

        for child in self.children:
            yield from child.walk()


def build_tree(depth: int, seed: int = 1) -> Node:

    node = Node(seed)

    if depth <= 0:
        return node

    node.children = [
        build_tree(depth - 1, seed * 2),
        build_tree(depth - 1, seed * 2 + 1),
    ]

    return node


# ============================================================
# 15. FUNCTIONAL PYTHON
# ============================================================

numbers = list(range(1, 101))

squares = [
    number ** 2
    for number in numbers
]

cubes = [
    number ** 3
    for number in numbers
]

even_squares = [
    value
    for value in squares
    if value % 2 == 0
]

odd_cubes = [
    value
    for value in cubes
    if value % 2
]

mapping = {
    number: number ** 2
    for number in range(20)
}

filtered_mapping = {
    key: value
    for key, value in mapping.items()
    if value % 3 == 0
}


# ============================================================
# 16. LAMBDA CHAOS
# ============================================================

operations: dict[str, Callable[[int, int], int]] = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "power": lambda a, b: a ** b,
    "modulo": lambda a, b: a % b,
}


# ============================================================
# 17. ITERTOOLS
# ============================================================

letters = "PYTHON"

permutations = list(
    itertools.permutations(
        letters,
        2,
    )
)

combinations = list(
    itertools.combinations(
        letters,
        3,
    )
)

cyclic_letters = itertools.cycle(
    letters
)


# ============================================================
# 18. RANDOM BUT DETERMINISTIC
# ============================================================

random.seed(1337)

random_numbers = [
    random.randint(0, 999)
    for _ in range(25)
]

random_average = statistics.mean(
    random_numbers
)


# ============================================================
# 19. STRING ALCHEMY
# ============================================================

alphabet = string.ascii_letters

encoded_phrase = "".join(
    alphabet[
        (alphabet.index(char) + 7)
        % len(alphabet)
    ]
    if char in alphabet
    else char
    for char in PHRASE
)


# ============================================================
# 20. PATHLIB
# ============================================================

CURRENT_FILE = Path(__file__).resolve()

CURRENT_DIRECTORY = CURRENT_FILE.parent

FILE_NAME = CURRENT_FILE.name

FILE_EXTENSION = CURRENT_FILE.suffix


# ============================================================
# 21. HASHING
# ============================================================

def digest(value: str) -> str:

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


HASH_OF_PYTHON = digest(
    "Python lives here."
)


# ============================================================
# 22. PRIME NUMBER GENERATOR
# ============================================================

def primes(limit: int) -> Generator[int, None, None]:

    for candidate in range(2, limit + 1):

        is_prime = all(
            candidate % divisor != 0
            for divisor in range(
                2,
                int(math.sqrt(candidate)) + 1,
            )
        )

        if is_prime:
            yield candidate


PRIME_NUMBERS = list(
    primes(250)
)


# ============================================================
# 23. MATRIX-LIKE PYTHON
# ============================================================

matrix = [
    [
        (row + column) ** 2
        for column in range(10)
    ]
    for row in range(10)
]

transposed = [
    list(column)
    for column in zip(*matrix)
]


# ============================================================
# 24. EXCEPTION HANDLING
# ============================================================

class ImpossiblePythonError(RuntimeError):
    pass


def dangerous_math(value: int) -> float:

    try:
        return math.sqrt(value)

    except ValueError as error:

        raise ImpossiblePythonError(
            "The number escaped mathematics."
        ) from error


# ============================================================
# 25. GENERATOR PIPELINE
# ============================================================

def source_numbers() -> Generator[int, None, None]:

    yield from range(1, 51)


def doubled(
    values: Iterable[int],
) -> Generator[int, None, None]:

    for value in values:
        yield value * 2


def only_large(
    values: Iterable[int],
) -> Generator[int, None, None]:

    for value in values:

        if value > 50:
            yield value


pipeline = only_large(
    doubled(
        source_numbers()
    )
)


PIPELINE_RESULT = list(pipeline)


# ============================================================
# 26. XOR DATA TRANSFORMATION
# ============================================================

def xor_bytes(
    data: bytes,
    key: int,
) -> bytes:

    return bytes(
        byte ^ key
        for byte in data
    )


original_data = b"PYTHON"

encrypted_data = xor_bytes(
    original_data,
    42,
)

decrypted_data = xor_bytes(
    encrypted_data,
    42,
)


# ============================================================
# 27. WEIRD BOOLEAN LOGIC
# ============================================================

truth_table = {
    (a, b): {
        "and": a and b,
        "or": a or b,
        "xor": bool(a) ^ bool(b),
        "equal": a == b,
    }
    for a in (False, True)
    for b in (False, True)
}


# ============================================================
# 28. ARTIFACT FACTORY
# ============================================================

def manufacture_artifacts(
    count: int,
) -> list[PythonArtifact]:

    moods = list(Mood)

    return [
        PythonArtifact(
            name=f"artifact_{index:04d}",
            weight=(index * 17) % 101,
            mood=moods[index % len(moods)],
            metadata={
                "index": index,
                "square": index ** 2,
                "cube": index ** 3,
            },
        )
        for index in range(count)
    ]


ARTIFACTS = manufacture_artifacts(30)


# ============================================================
# 29. MAIN DEMONSTRATION
# ============================================================

def main() -> None:

    print("=" * 70)
    print(" PYTHON DIMENSION INITIALIZED ")
    print("=" * 70)

    print(f"Current file: {CURRENT_FILE}")
    print(f"Current directory: {CURRENT_DIRECTORY}")
    print(f"File name: {FILE_NAME}")
    print(f"Extension: {FILE_EXTENSION}")

    print("\n--- Decorators ---")
    print("3 × 9 =", multiply(3, 9))
    print("2^10 =", strange_power(2, 10))

    print("\n--- Metaclass ---")
    quantum = QuantumPython(42)
    print(quantum.dramatic_name)
    print(quantum.collapse())

    print("\n--- Generic Box ---")
    boxed = Box(21)
    transformed = boxed.map(lambda x: x * 10)
    print(transformed.unwrap())

    print("\n--- Spiral Iterator ---")
    print(list(SpiralNumbers(100)))

    print("\n--- Context Manager ---")
    with python_dimension("GitHub Python dimension"):
        time.sleep(0.001)

    print("\n--- Temperature ---")
    temperature = Temperature(25)
    print("Celsius:", temperature.celsius)
    print("Fahrenheit:", temperature.fahrenheit)
    print("Kelvin:", temperature.kelvin)

    print("\n--- Pattern Matching ---")
    for signal in Signal:
        print(signal.name, "=>", interpret_signal(signal))

    print("\n--- Functions ---")
    print("double(50):", double(50))
    print("triple(50):", triple(50))
    print("sevenfold(10):", sevenfold(10))

    print("\n--- Tree ---")
    tree = build_tree(4)
    print("Tree values:", list(tree.walk()))

    print("\n--- Descriptor ---")
    strange = StrangeObject()
    print("Stored:", strange.value)
    strange.value = "GitHub"

    print("\n--- Pipeline ---")
    print(PIPELINE_RESULT)

    print("\n--- Prime Numbers ---")
    print(PRIME_NUMBERS)

    print("\n--- Hash ---")
    print(HASH_OF_PYTHON)

    print("\n--- XOR ---")
    print("Original :", original_data)
    print("Encrypted:", encrypted_data)
    print("Decoded  :", decrypted_data)

    print("\n--- Random Statistics ---")
    print("Numbers:", random_numbers)
    print("Average:", random_average)

    print("\n--- Artifacts ---")
    for artifact in ARTIFACTS[:5]:
        print(
            artifact.name,
            artifact.mood.name,
            artifact.fingerprint()[:16],
        )

    print("\n--- Async Python ---")

    async_results = asyncio.run(
        parallel_python()
    )

    print(async_results)

    print("\n" + "=" * 70)
    print(" PYTHON HAS ENTERED THE REPOSITORY ")
    print("=" * 70)


# ============================================================
# 30. PYTHON ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()