.. _sec_annex:

Annex
=====

.. _sec_annex_json:

Example of the Configuration Data Structure
-------------------------------------------

.. literalinclude:: json/ahu_example.json
   :language: json
   :caption: Partial example of the configuration data structure for an air handling unit (pseudo-code, especially for autoreferencing the data structure and writing conditional statements)
   :name: code_conf_ahu


.. _sec_annex_bus_example:

Main Features of the Expandable Connectors
------------------------------------------

The main features of the expandable connectors (as described in :numref:`sec_signal_connectors`) are illustrated with a minimal example described in the figures below where:

* a controlled system consisting in a sensor (idealized with a real expression) and an actuator (idealized with a simple block passing through the value of the input control signal) is connected with,

* a controller system which divides the input variable (measurement) by itself and thus outputs a control variable equal to one.

* The same model is first implemented with an expandable connector and then with a standard connector.

.. figure:: img/BusTestExp.*
   :name: BusTestExp
   :width: 50%

   Minimal example illustrating the connection scheme with an expandable connector -- Top level

.. code:: modelica

   model BusTestExp
   BusTestControllerExp controllerSystem;
   BusTestControlledExp controlledSystem;
   equation
         connect(controllerSystem.ahuBus, controlledSystem.ahuBus);
   end BusTestExp;

.. figure:: img/BusTestControlledExp.*
   :name: BusTestControlledExp
   :width: 50%

   Minimal example illustrating the connection scheme with an expandable connector -- Controlled component sublevel

.. code:: modelica

   model BusTestControlledExp
   Modelica.Blocks.Sources.RealExpression sensor(y=2 + sin(time*3.14));
   Buildings.Experimental.Templates.BaseClasses.AhuBus ahuBus;
   Modelica.Blocks.Routing.RealPassThrough actuator;
   equation
         connect(sensor.y, ahuBus.yMea);
         connect(ahuBus.yAct, actuator.u);
   end BusTestControlledExp;

.. code:: modelica

   expandable connector AhuBus
   extends Modelica.Icons.SignalBus;
   end AhuBus;

.. note::

   The definition of ``AhuBus`` in the code snippet here above does not include any variable declaration. However the variables ``ahuBus.yAct`` and ``ahuBus.yMea`` are used in ``connect`` equations. That is only possible with an expandable connector.

.. figure:: img/BusTestControllerExp.*
   :name: BusTestControllerExp
   :width: 50%

   Minimal example illustrating the connection scheme with an expandable connector -- Controller component sublevel

.. code:: modelica

   model BusTestControlledExp
         Modelica.Blocks.Sources.RealExpression sensor(y=2 + sin(time*3.14));
         Buildings.Experimental.Templates.BaseClasses.AhuBus ahuBus;
         Modelica.Blocks.Routing.RealPassThrough actuator;
   equation
         connect(ahuBus.yAct, actuator.u);
         connect(sensor.y, ahuBus.yMea)
   end BusTestControlledExp;

.. figure:: img/BusTestNonExp.*
   :name: BusTestNonExp
   :width: 50%

   Minimal example illustrating the connection scheme with a standard connector -- Top level

.. code:: modelica

   model BusTestNonExp
   BusTestControllerNonExp controllerSystem;
   BusTestControlledNonExp controlledSystem;
   equation
         connect(controllerSystem.nonExpandableBus, controlledSystem.nonExpandableBus);
   end BusTestNonExp;

.. figure:: img/BusTestControlledNonExp.*
   :name: BusTestControlledNonExp
   :width: 50%

   Minimal example illustrating the connection scheme with a standard connector -- Controlled component sublevel

.. code:: modelica

   model BusTestControlledNonExp
   Modelica.Blocks.Sources.RealExpression sensor(y=2 + sin(time*3.14));
   Modelica.Blocks.Routing.RealPassThrough actuator;
   BaseClasses.NonExpandableBus nonExpandableBus;
   equation
         nonExpandableBus.yMea = sensor.y;
         actuator.u = nonExpandableBus.yAct;
   end BusTestControlledNonExp;

.. code:: modelica

   connector NonExpandableBus
   // The following declarations are required.
   // The variables are not considered as connectors: they cannot be part of connect equations.
   Real yMea;
   Real yAct;
   end NonExpandableBus;

.. figure:: img/BusTestControllerNonExp.*
  :name: BusTestControllerNonExp
  :width: 50%

  Minimal example illustrating the connection scheme with a standard connector -- Controller component sublevel

.. code:: modelica

   model BusTestControllerNonExp
   Controls.OBC.CDL.Continuous.Division controller;
   Modelica.Blocks.Routing.RealPassThrough realPassThrough;
   BaseClasses.NonExpandableBus nonExpandableBus;
   equation
         connect(realPassThrough.y, controller.u1);
         controller.u2 = nonExpandableBus.yMea;
         nonExpandableBus.yAct = controller.y;
         realPassThrough.u = nonExpandableBus.yMea;
   end BusTestControllerNonExp;


.. _sec_annex_bus_valid:

Validating the Use of Expandable Connectors
-------------------------------------------

The use of expandable connectors (control bus) is validated in case of a complex controller (``Buildings.Controls.OBC.ASHRAE.G36_PR1.AHUs.MultiZone.VAV.Controller``).

The validation is performed:

* with Dymola (Version 2020, 64-bit, 2019-04-10) and JModelica (revision numbers from svn: JModelica 12903, Assimulo 873);
* first with a single instance of the controller and then with multiple instances corresponding to different parameters set up (see validation cases of the original controller ``Validation.Controller`` and ``Validation.ControllerConfigurationTest``),
* with nested expandable connectors: a top-level control bus composed of a first sub-level control bus for control output variables and another for control input variables.

Simulation succeeds for the two tests cases with the two simulation tools.
The results comparison to the original test case (without control bus) is presented in :numref:`annex_valid_bus` for Dymola.

.. figure:: img/annex_valid_bus.*
   :name: annex_valid_bus
   :width: 800px

   G36 AHU controller model: comparison of simulation results (Dymola) between implementation without (``origin``) and with (``new_bus``) expandable connectors

.. _sec_annex_bus_array:

Validating the Use of Expandable Connector Arrays
-------------------------------------------------

