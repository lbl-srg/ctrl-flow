.. _sec_architecture:

#####################
Software Architecture
#####################

:numref:`linkage_architecture_legend` to :numref:`linkage_architecture_spa` provide architecture diagrams for the various integration targets.

.. warning::

   These diagrams are informative only and do not constitute requirements. They rather aim at illustrating the data workflow and describing the main modules to develop, and how they interface with LBL or third-party developments.

.. admonition:: Revision Note (11/2020)
   :class: danger

   The diagrams for the desktop app and the third-party application are removed.

The following definitions and conventions are used.

  Model data: pieces of data used by the graphical editor to allow manipulating a Modelica model. Those correspond to the Modelica code as interpreted by the editor according to its specific data model.

  Return *<arg>*: describes the translating task from one language (e.g. Modelica or Brick) or one data model (e.g. Modelica raw code or JSON) to another, specified by *<arg>*.

  Input: describes the user action of setting a parameter value through mouse or keyboard input.

  Call >> return *<arg>*: describes a bidirectional task where a component A calls another component B, and B returns *<arg>* to A.


.. figure:: img/linkage_architecture_legend.*
   :name: linkage_architecture_legend

   Software architecture legend


.. figure:: img/linkage_architecture_plugin.*
   :name: linkage_architecture_plugin

   Software architecture for the configuration widget integrated into an existing graphical editor for Modelica


.. figure:: img/linkage_architecture_spa.*
   :name: linkage_architecture_spa

   Software architecture for the full-featured graphical editor embedding the configuration widget - Standalone web app

