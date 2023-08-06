Changelog
---------

v0.6.4 (2020-06-26)
~~~~~~~~~~~~~~~~~~~

* Enhancements

  * Added support for parametric (ie. symbolic) argument for some gates (e.g. Rx, Ry, Rz, TimeEvolution, QubitOperator)
    See documentation for more information.
  * Update Travis CI configuration to allow building of binaries on all platforms

..

* Bug Fixes

  * Fix potential test failures on Travis CI due to reference counting
  * QubitOperator invalid comparison to empty tuple

v0.6.3 (2020-06-05)
~~~~~~~~~~~~~~~~~~~

Update to ProjectQ v0.5.1


v0.6.2 (2020-04-02)
~~~~~~~~~~~~~~~~~~~

* Enhancements

  * Added JSONBackend

..

* Bug Fixes

  * Fix libs/histogram under Python 2.7

v0.6.1 (2020-03-20)
~~~~~~~~~~~~~~~~~~~

* Enhancements

  * Migrated HiQ-ProjectQ to a namespace package for compatibility with other HiQ packages.

v0.6.0 (2020-03-17)
~~~~~~~~~~~~~~~~~~~

* Update HiQ-ProjectQ with ProjectQ v0.5.0
