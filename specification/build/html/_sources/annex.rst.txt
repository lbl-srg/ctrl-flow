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

The validation is performed

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

Minimum examples illustrate that arrays of expandable connectors are differentially supported between Dymola and OCT. None of the tested Modelica tools seems to have a fully robust support. However, by reporting those bugs, it seems as a feature we can leverage for LinkageJS.

We start with the basic definition of an expandable connector ``AhuBus`` containing the declaration of an array of expandable connectors ``ahuTer`` that will be used to connect the signal variables from the terminal unit model. In addition we build dummy models for a central system (e.g. VAV AHU) and a terminal system (e.g. VAV box) as illustrated in the figures hereafter. The input signal ``inpSig`` is typically generated by a sensor from the terminal system and must be passed on to the central system which, in response, outputs the signal ``outsig`` typically used to control an actuator position in the terminal unit.

.. code:: modelica

   expandable connector AhuBus
      extends Modelica.Icons.SignalBus;
      parameter Integer nTer=0
         "Number of terminal units";
         // annotation(Dialog(connectorSizing=true)) is not interpreted properly in Dymola.
      Buildings.Experimental.Templates.BaseClasses.TerminalBus ahuTer[nTer] if  nTer > 0
         "Terminal unit sub-bus";
   end AhuBus;

.. figure:: img/DummyCentral.*
   :name: DummyCentral
   :width: 50%

.. figure:: img/DummyTerminal.*
   :name: DummyTerminal
   :width: 50%


Connecting One Central System Model to an Array of Terminal System Models
*************************************************************************

The first test is illustrated in the figure below.

.. figure:: img/ControlBusArrayManual.*
   :name: ControlBusArrayManual
   :width: 50%

`Bug in Dymola`

Dymola GUI does not allow graphically generating the statement ``connect(dummyTerminal.terBus, dummyCentral.ahuBus.ahuTer)``. The GUI returns the error message ``Incompatible connectors``.

However, we cannot find which part of the specification :cite:`Modelica2017` this statement would violate. To the contrary, the specification states that "expandable connectors can be connected even if they do not contain the same components".

Additionally, when manually adding this ``connect`` statement in the code, the model simulates (with correct results) with OCT. Dymola fails to translate the model and returns the error message ``Connect argument was not one of the valid forms, since dummyCentral is not a connector``.

Based on various tests we performed, it seems that Dymola supports connecting *inside* expandable connectors together only when they are instances of the same class. Again, we cannot find such a requirement in Modelica specification. To allow such a connection in Dymola, we need to rely on an *outside* expandable connector as illustrated below.

.. figure:: img/ControlBusArray.*
   :name: ControlBusArray
   :width: 50%

`Bug in OCT`

With this connection layout, the model simulates with Dymola but no more with OCT which returns the following error message.

.. code::

   Error at line 296, column 5, in file '/opt/oct/ThirdParty/MSL/Modelica/Blocks/Interfaces.mo':
   Cannot find class declaration for RealInput

`Bug in Dymola`

Incidentally we observe other bugs in Dymola related to the elaboration process leading to a variable being marked as present in the expandable connector variable set.

* When connecting a non declared variable to a sub-bus, e.g., ``connect(ahuBus.ahuTer.inpSig, inpSig.u)``, the corresponding expandable connector variable list (visible in Dymola GUI under ``<Add Variable>`` when drawing a connection to the connector) does not get augmented with the variable name.

* When connecting a non declared variable directly to an array of expandable connectors as in the figure below, the dimensionality may be wrong depending on the first connection being established. Indeed, ``terBus.inpSig`` is considered as an array if ``terBus[:].inpSig`` is first connected to a one-dimensional array of scalar variables. The code needs to be updated manually to suppress the array index and simulate. If the first connection of ``inpSig`` variable to the connector is made at the terminal unit level (scalar to scalar) then the dimensionality is correctly established.

* In several use cases, we noticed similar issues related to the dimensionality of variables in presence of nested expandable connectors. In that respect OCT appears more robust.

.. figure:: img/DummyCentralBug.*
   :name: DummyCentralBug
   :width: 50%


Connecting an Array of Central System Models to an Array of Terminal System Models
**********************************************************************************

We now try to connect an one-dimensional array of central system models ``DummyCentral dummyCentral[nAhu]`` to a two-dimensional array of terminal system models ``DummyTerminal dummyTerminal[nAhu, nTerAhu]``.

`Bug in Dymola`

As explained before, in Dymola, we need to rely to an *outside* expandable connector to connect the two *inside* expandable connectors.

.. figure:: img/ControlBusArrayArray.*
   :name: ControlBusArrayArray
   :width: 50%

However, despite the connection being made properly through the GUI, the model fails to translate.

.. code::

   Unmatched dimension in connect(ahuBus.ahuTer, dummyTerminal.terBus);

   The first argument, ahuBus.ahuTer, is a connector with 1 dimensions
   and the second, dummyTerminal.terBus, is a connector with 2 dimensions.

The error message is incorrect as in this case ``ahuBus.ahuTer`` has two dimensions.

OCT also fails to translate the model but for a different reason, see error message previously mentioned.
However, when manually adding the connect statement between the two *inside* connectors ``connect(dummyTerminal.terBus, dummyCentral.ahuBus.ahuTer)``, the model simulates with OCT.


Passing a Scalar Variable to an Array of System Models
******************************************************

The typical use case is a schedule, set point, or central system status value that is used as a common input to a set of terminal units.
Two programmatic options are obviously available.

1. Instantiating a replicator (routing) component to connect the variable to the expandable connector array.
2. Looping over the expandable connector array elements to connect each of them to the variable.

The test performed here aims to provide a more "user-friendly" way of achieving the same result with only one connection being made (either graphically or programmatically).

The best approach would be a binding of the variable in the declaration of the expandable connector array.

.. code::

   expandable connector AhuBus
      parameter Integer nTer
         "Number of terminal units";
      Boolean staAhu
         "Test how a scalar variable can be passed on to an array of connected units";
      Buildings.Experimental.Templates.BaseClasses.TerminalBus ahuTer[nTer](
         each staAhu=staAhu) if nTer > 0
         "Terminal unit sub-bus";
   end AhuBus;

However that syntax is neither supported by Dymola nor by OCT.
Also an equation section is not allowed in an expandable connector class according to Modelica specification.

The approach eventually tested relies on a so-called "gateway" model composed of several instances of expandable connectors and an equation section used to establish the needed connect statements. Note that if a variable is left unconnected then it is considered undefined, so the corresponding connect statement is automatically removed by Modelica tools.

.. code ::

   model AhuBusGateway
      "Model to connect scalar variables from main bus to an array of sub-bus"
      parameter Integer nTer
         "Number of terminal units";
      AhuBus ahuBus(nTer=nTer);
      TerminalBus terBus[nTer];
   equation
      for i in 1:nTer loop
         connect(ahuBus.staAhu, ahuBus.ahuTer[i].staAhu);
      end for;
      connect(ahuBus.ahuTer, terBus);
   end AhuBusGateway;

`Bug in Dymola`

When trying to simulate a model using such a component Dymola fails to translate and returns:

.. code ::

   The bus-input dummyTerminal[1].terBus.staAhu lacks a matching non-input in the connection sets.
   This means that it lacks a source writing the signal to the bus.

However, OCT simulates the model properly.