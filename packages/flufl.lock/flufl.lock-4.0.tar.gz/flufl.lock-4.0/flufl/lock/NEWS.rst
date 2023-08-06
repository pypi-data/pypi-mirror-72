===================
NEWS for flufl.lock
===================

4.0 (2020-06-30)
================

API
---
* **Breaking change** - In ``Lock.refresh()`` and ``Lock.unlock()`` the
  ``unconditionally`` flag is now a keyword-only argument.  (GL#13)
* **Breaking change** - Removed ``Lock.__del__()`` and ``Lock.finalize()``.
  It's impossible to make ``__del__()`` work properly, and this is obsoleted
  by context manager protocol support anyway.  Since ``finalize()`` only
  existed to help with ``__del__()`` and its functionality is identical to
  ``.unlock(unconditionally=True)``, this method is also removed.  (GL#7)
* Added a ``Lock.expiration`` property. (GL#15)
* Added a ``Lock.lockfile`` property. (GL#16)
* Added a ``Lock.state`` property and the ``LockState`` enum. (GL#12)
* In all APIs, the ``lifetime`` parameter can now also be an integer number of
  seconds, in addition to the previously allowed ``datetime.timedelta``.  The
  ``lifetime`` property always gives you a ``datetime.timedelta``.
* The API is now properly type annotated.
* Some library-defined exceptions support exception chaining.

Behavior
--------
* Getting the ``repr()`` of a lock no longer refreshes it (GL#11)

Other
-----
* Add support for Python 3.7 and 3.8; drop support for Python 3.4 and 3.5.
* We now run the test suite on both Linux and Windows.
* The LICENSE file is now included in the sdist tarball.
* API documentation is now built automatically.
* Numerous quality improvements and modernizations.

3.2 (2017-09-03)
================
* Expose the host name used in the ``.details`` property, as a property.
  (Closes #4).

3.1 (2017-07-15)
================
* Expose the ``SEP`` as a public attribute.  (Closes #3)

3.0 (2017-05-31)
================
* Drop Python 2.7, add Python 3.6.  (Closes #2)
* Added Windows support.
* Switch to the Apache License Version 2.0.
* Use flufl.testing for nose2 and flake8 plugins.
* Allow the claim file separator to be configurable, to support file systems
  where the vertical bar is problematic.  Defaults to ``^`` on Windows and
  ``|`` everywhere else (unchanged).  (Closes #1)

2.4.1 (2015-10-29)
==================
* Fix the MANIFEST.in so that tox.ini is included in the sdist.

2.4 (2015-10-10)
================
* Drop Python 2.6 compatibility.
* Add Python 3.5 compatibility.

2.3.1 (2014-09-26)
==================
* Include MANIFEST.in in the sdist tarball, otherwise the Debian package
  won't built correctly.

2.3 (2014-09-25)
================
* Fix documentation bug.  (LP: #1026403)
* Catch ESTALE along with ENOENT, as NFS servers are supposed to (but don't
  always) throw ESTALE instead of ENOENT.  (LP: #977999)
* Purge all references to ``distribute``.  (LP: #1263794)

2.2.1 (2012-04-19)
==================
* Add classifiers to setup.py and make the long description more compatible
  with the Cheeseshop.
* Other changes to make the Cheeseshop page look nicer.  (LP: #680136)
* setup_helper.py version 2.1.

2.2 (2012-01-19)
================
* Support Python 3 without the use of 2to3.
* Make the documentation clear that the ``flufl.test.subproc`` functions are
  not part of the public API.  (LP: #838338)
* Fix claim file format in ``take_possession()``.  (LP: #872096)
* Provide a new API for dealing with possible additional unexpected errnos
  while trying to read the lock file.  These can happen in some NFS
  environments.  If you want to retry the read, set the lock file's
  ``retry_errnos`` property to a sequence of errnos.  If one of those errnos
  occurs, the read is unconditionally (and infinitely) retried.
  ``retry_errnos`` is a property which must be set to a sequence; it has a
  getter and a deleter too.  (LP: #882261)

2.1.1 (2011-08-20)
==================
* Fixed TypeError in .lock() method due to race condition in _releasetime
  property.  Found by Stephen A. Goss. (LP: #827052)

2.1 (2010-12-22)
================
* Added lock.details.

2.0.2 (2010-12-19)
==================
* Small adjustment to doctest.

2.0.1 (2010-11-27)
==================
* Add missing exception to __all__.

2.0 (2010-11-26)
================
* Package renamed to flufl.lock.

Earlier
=======

Try ``bzr log lp:flufl.lock`` for details.
