PyRend Documentation
====================

Welcome to the PyRend documentation. This page will guide you through the main features and how to use them.

.. note::

   THIS DOCUMENTATION IS CURRENTLY A SKELETON. IT WILL BE PROPERLY EDITED SOON.

.. contents::
   :local:
   :depth: 2
   :backlinks: none

Overview
========

PyRend allows you to create audio/video overlays, automate keyboard input, and manage windows/files.

Getting Started
===============

This section explains how to get started with PyRend.

Installation
------------

Use pip to install PyRend:

.. code-block:: bash

    pip install pyrend

Basic Usage
-----------

Here is an example of basic usage:

.. code-block:: python

    import pyrend
    pyrend.overlay.shape(False, (200, 200), (400, 400))
    pyrend.overlay.start()

Audio and Video Overlay
=======================

Learn how to draw shapes, images, and videos as overlays.

Keyboard Input Automation
=========================

How to simulate keyboard and mouse inputs.

Window and File Management
==========================

Controlling windows and running files.
