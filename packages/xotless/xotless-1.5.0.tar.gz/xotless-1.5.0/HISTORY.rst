=========
 History
=========

First releases 1.0
==================

2020-06-24.  Release 1.5.0
--------------------------

- Make the hash of an ImmutableWrapper without overrides be the same as the
  underlying object.


2020-06-05.  Release 1.4.0
--------------------------

- Don't cache Odoo instances in `xotless.picablenv.PickableRecordset`:class:,
  but also prefer the current HTTP Odoo Environment to avoid looking for an
  arbitrary one.

  This solves a `couple <xhg2#979>`_ of `bugs <xhg2#939>`_ in Mercurio 2018

  .. _xhg2#979: https://gitlab.merchise.org/mercurio-2018/xhg2/-/issues/979
  .. _xhg2#939: https://gitlab.merchise.org/mercurio-2018/xhg2/-/issues/939


2020-05-26.  Release 1.3.0
--------------------------

- Add module `xotless.walk`:mod:.


2020-05-19.  Release 1.2.0
--------------------------

- `xotless.immutables.ImmutableWrapper`:class: now accepts argument
  `wraps_descriptors` to apply wrapper on while invoking descriptors.


2020-04-30.  Release 1.1.0
--------------------------

- Use ``__slots__`` in `xotless.trees.IntervalTree`:class:.  We don't expect
  instances of this class to need additional attributes.


2020-04-29.  Release 1.0.1
--------------------------

This release only contains packaging fixes to make the distribution compliant
with PEP :pep:`561`.


2020-04-29.  Release 1.0.0
--------------------------

The first release including the code extracted from a bigger project.  Modules
available are `xotless.ranges`:mod:, `xotless.tress`:mod:,
`xotless.domains`:mod:, `xotless.itertools`:mod:, `xotless.immutables`:mod:,
and `xotless.pickablenv`:mod:.
