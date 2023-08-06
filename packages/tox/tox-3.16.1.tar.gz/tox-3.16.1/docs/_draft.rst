*Changes in master, but not released yet are under the draft section*.

vDRAFT (2020-06-26)
-------------------


Features
^^^^^^^^

- Allow skipping the package and installation step when passing the ``--skip-pkg-install``. This should be used in pair with the ``--notest``, so you can separate environment setup and test run:

   .. code-block:: console

      tox -e py --notest
      tox -e py --skip-pkg-install

  by :user:`gaborbernat`.
  `#1605 <https://github.com/tox-dev/tox/issues/1605>`_


Miscellaneous
^^^^^^^^^^^^^

- Improve config parsing performance by precompiling commonly used regular expressions - by :user:`brettlangdon`
  `#1603 <https://github.com/tox-dev/tox/issues/1603>`_

