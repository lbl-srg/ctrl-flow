########
Overview
########

The software to develop is a graphical user interface for editing Modelica models of HVAC and control systems.

The development targets two main categories of end users, also seen as two main use cases.

#. Heating Ventilating and Air Conditioning (HVAC) engineers and designers who will utilize the software to specify the controls of HVAC systems in commercial buildings. In terms of use case, we will refer to this category as the *control specification workflow*.

#. Building Energy Modeling (BEM) engineers who will use it to assess the energy use of HVAC systems based on a detailed representation of the equipment and controls that the tool will enable, and simulations that will be run using third party Modelica tools. In terms of use case, we will refer to this category as the *modeling and simulation workflow*.

The software relies on two main components.

#. A graphical user interface for editing Modelica classes in a diagrammatic form.

#. A configuration widget supporting assisted modeling based on a simple HTML input form. This widget is mostly needed for integrating advanced control sequences that can have dozens of I/O variables. The intent is to reduce the complexity to the mere definition of the system layout and the selection of standard control sequences already transcribed in Modelica.

We plan a phased development where

#. the configuration widget will be first implemented as part of Phase 1 and integrated into an existing graphical editor for Modelica—the *control specification workflow* is the prioritized use case,

#. the full-featured editor will be developed in a future phase, providing diagrammatic editing capabilities and integrating the configuration widget natively—the *modeling and simulation workflow* is the prioritized use case.


.. admonition:: Revision Note (11/2020)
   :class: danger

   The current version of the specification is limited to Phase 1. Each part related to the full-featured editor is provided for informative purposes only.


.. raw:: html

   <iframe src="_static/overview.html" width="100%" height="800px" frameBorder="0">


.. only:: latex

   .. figure:: img/overview_1.*

   .. figure:: img/overview_2.*

   .. figure:: img/overview_3.*

