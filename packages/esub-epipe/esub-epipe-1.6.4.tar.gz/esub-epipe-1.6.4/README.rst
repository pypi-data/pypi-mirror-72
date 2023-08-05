=================================
esub-epipe - Version 1.6.4 STABLE
=================================

.. image:: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/esub-epipe/badges/master/coverage.svg
  		:target: https://cosmo-gitlab.phys.ethz.ch/esub-epipe/NGSF

.. image:: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/esub-epipe/badges/master/pipeline.svg
        :target: https://cosmo-gitlab.phys.ethz.ch/cosmo_public/esub-epipe


.. image:: http://img.shields.io/badge/arXiv-2006.12506-orange.svg?style=flat
        :target: https://arxiv.org/abs/2006.12506



esub-epipe is part of the Non-Gaussian Statistics Framework (`NGSF <https://cosmo-gitlab.phys.ethz.ch/cosmo_public/NGSF>`_).

If you use this package in your research please cite Zuercher et al. 2020. (`arXiv-2006.12506 <https://arxiv.org/abs/2006.12506>`_).

`Source <https://cosmo-gitlab.phys.ethz.ch/cosmo_public/esub-epipe>`_

`Documentation <http://cosmo-docs.phys.ethz.ch/esub-epipe>`_

Introduction
============

- Are you tired of rewriting the same kind of submission scripts to sumbit your code to a computer cluster?

- Do you not want to rewrite different versions of your code for serial, parallel or MPI execution?

- Do you wish there would be an easy way to submit large numbers of dependent jobs to a computer cluster without writing the same kind of pipeline scripts and worrying about resource allocation every time?

If any of these points applies to you, you have come to the right place!

When using this package you will only need to write a single python executable file. The same file can then be used to run your code
serially, in parallel or in an MPI environement on your local machine. You can also use the same file to submit your code to a
computer cluster.

Even more, if you are building large pipelines with many dependent jobs, or even tasks which have to be executed multiple times
you will just have to write a single YAML file in which you state what you want to run and esub will submit all those
jobs to the computer cluster such that you can continue working on your amazing projects while waiting for the results :)

Getting Started
===============

The easiest and fastest way to learn about esub is to have a look at the Examples Section in the documentation.
If you wish to learn more also have a look at the Usage Section in the documenation in which we documented all the things you can do with esub.

Disclaimer
==========

At the moment only IBMs bsub system is supported but we hope to include other queing systems in the future.

Credits
=======

This package was created on May 12 2019 by Dominik Zuercher (PhD student at ETH Zurich in Alexandre Refregiers `Comsology Research Group <https://cosmology.ethz.ch/>`_)
It is inspired by the jobchainer code written by Tomasz Kacprzak.

The package is maintained by Dominik Zuercher dominik.zuercher@phys.ethz.ch.

Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.
