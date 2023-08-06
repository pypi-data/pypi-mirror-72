"""Package init."""

from public import public as _public
from flufl.lock._lockfile import (
    SEP, Lock, LockError, LockState, TimeOutError, NotLockedError,
    AlreadyLockedError)


__version__ = '4.0'


_public(
    AlreadyLockedError=AlreadyLockedError,
    Lock=Lock,
    LockError=LockError,
    LockState=LockState,
    NotLockedError=NotLockedError,
    SEP=SEP,
    TimeOutError=TimeOutError,
    __version__=__version__,
    )


del _public
