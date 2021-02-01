.. _sec_annex:

#####
Annex
#####

This annex is informative only. It presents various validation cases and additional information for the development of the templates in Phase 1 and the future development of a diagram editor in Phase 2.

*****************************************
Using Expandable Connectors in Templates
*****************************************

.. admonition:: Revision Note
   :class: danger

   This paragraph is moved from the *Requirements* section to the *Annex* section.


General Principles
==================

The ``connect`` equations for signal variables in the Modelica templates rely on expandable connectors (also referred to as control bus), see *§9.1.3 Expandable Connectors* in :cite:`Modelica2017`.

The following features of the expandable connectors are leveraged. They are illustrated with minimal examples in :numref:`sec_annex_bus_example`.

#. All components in an expandable connector are seen as connector instances even if they are not declared as such. In comparison to a non expandable connector, that means that each variable (even of type ``Real``) can be connected i.e. be part of a ``connect`` equation.

   .. note::

      Connecting a non connector variable to a connector variable with ``connect(non_connector_var, connector_var)`` yields a warning but not an error in Dymola. It is considered bad practice though and a standard equation should be used in place ``non_connector_var = connector_var``.

      Using a ``connect`` equation allows to draw a connection line which makes the model structure explicit to the user. Furthermore it avoids mixing ``connect`` equations and standard equations within the same equation set, which has been adopted as a best practice in the Modelica Buildings library.

#. The causality (input or output) of each variable inside an expandable connector is not predefined but rather set by the ``connect`` equation where the variable is first being used. For instance when the variable of an expandable connector is first connected to an inside connector ``Modelica.Blocks.Interfaces.RealOutput`` it gets the same causality i.e. output. The same variable can then be connected to another inside connector  ``Modelica.Blocks.Interfaces.RealInput``.

#. Potentially present but not connected variables are eventually considered as undefined i.e. a tool may remove them or set them to the default value (Dymola treat them as not declared: they are not listed in ``dsin.txt``): all variables need not be connected so the control bus does not have to be reconfigured depending on the model structure.

#. The variables set of a class of type expandable connector is augmented whenever a new variable gets connected to any *instance* of the class. Though that feature is not needed by the configuration widget (we will have a predefined control bus with declared variables), it is needed to allow the user further modifying the control sequence. Adding new control variables is simply done by connecting them to the control bus.

#. Expandable connectors can be used in arrays, as any other Modelica type. A typical use case is the connection of control input signals from a set of terminal units to a supervisory controller at the AHU or at the plant level. This use case has been validated on minimal examples in :numref:`sec_annex_bus_array`.


.. _sec_connect_ui_req:

Additional Requirements for the UI in Phase 2
=============================================

:numref:`dymola_bus` presents the Dymola pop-up window displayed when connecting the sub-bus of input control variables to the main control bus (based on the validation case in :numref:`sec_annex_bus_valid`).
A similar view of the connections set must be implemented with the additional requirements listed below. That view is displayed in the connections tab of the right panel.

.. figure:: img/dymola_bus.png
   :name: dymola_bus

   Dymola pop-up window when connecting the sub-bus of input control variables (left) to the main control bus (right) -- case of outside connectors

The variables listed immediately after the bus name are either

* *declared variables* that are not connected, for instance ``ahuBus.yTest`` (declared as ``Real`` in the bus definition): those variables are only *potentially present* and eventually considered as *undefined* when translating the model (treated by Dymola as if they were never declared) or,

* *present variables* i.e. variables that appear in a connect equation, for instance ``ahuSubBusI.TZonHeaSet``: the icon next to each variable then indicates the causality. Those variables can originally be either declared variables or variables elaborated by the augmentation process for *that instance* of the expandable connector i.e. variables that are declared in another component and connected to the connector's instance.

The variables listed under ``Add variable`` are the remaining *potentially present variables* (in addition to the declared but not connected variables). Those variables are elaborated by the augmentation process for *all instances* of the expandable connector, however they are not connected in that instance of the connector.

In addition to Dymola's features for handling the bus connections, Linkage Phase 2 will require the following.

* Color code to distinguish between

  * Variables connected only once (within the entire augmentation set): those variables should be listed first and in red color. This is needed so that the user immediately identify which connections are still required for the model to be complete.

    .. Note::

       Dymola does not throw any exception when a *declared* bus variable is connected to an input (resp. output) variable but not connected to any other non input (resp. non output) variable. It then uses the default value (0 for ``Real``) to feed the connected variable.

       That is not the case if the variable is not declared i.e. elaborated by augmentation: in that case it has to be connected in a consistent way.

       JModelica throws an exception in any case with the message ``The following variable(s) could not be matched to any equation``.

  * Declared variables which are only potentially present (not connected): those variables should be listed last (not first as in Dymola) and in light grey color. That behavior is also closer to :cite:`Modelica2017` *§9.1.3 Expandable Connectors*: "variables and non-parameter array elements declared in expandable connectors are marked as only being potentially present. [...] elements that are only potentially present are not seen as declared."

* View the "expanded" connection set of an expandable connector in each level of composition -- that covers several topics:

  * The user can view the connection set of a connector simply by selecting it and without having to make an actual connection (as in Dymola).

  * The user can view the name of the component and connector variable to which the expandable connector's variables are connected: similar to Dymola's function ``Find Connection`` accessible by right-clicking on a connection line.

  * | From :cite:`Modelica2017` *§9.1.3 Expandable Connectors*: "When two expandable connectors are connected, each is augmented with the variables that are only declared in the other expandable connector (the new variables are neither input nor output)."
    | That feature is illustrated in the minimal example :numref:`bus_minimal` where a sub-bus ``subBus`` with declared variables ``yDeclaredPresent`` and ``yDeclaredNotPresent`` is connected to the declared sub-bus ``bus.ahuI`` of a bus. ``yDeclaredPresent`` is connected to another variable so it is considered present. ``yDeclaredNotPresent`` is not connected so it is only considered potentially present. Finally ``yNotDeclaredPresent`` is connected but not declared which makes it a present variable. :numref:`subbus_outside` to :numref:`bus_inside` then show which variables are exposed to the user. In consistency with :cite:`Modelica2017` the declared variables of ``subBus`` are considered declared variables in ``bus.ahuI`` due to the connect equation between those two instances and they are neither input nor output. Furthermore the present variable ``yNotDeclaredPresent`` appears in ``bus.ahuI`` under ``Add variable``, i.e., as a potentially present variable whereas it is a present variable in the connected sub-bus ``subBus``.

    * This is an issue for the user who will not have the information at the bus level of the connections which are required by the sub-bus variables e.g. Dymola will allow connecting an output connector to ``bus.ahuI.yDeclaredPresent`` but the translation of the model will fail due to ``Multiple sources for causal signal in the same connection set``.
    * Directly connecting variables to the bus (without intermediary sub-bus) can solve that issue for outside connectors but not for inside connectors, see below.

  * | Another issue is illustrated :numref:`bus_inside` where the connection to the bus is now made from an outside component for which the bus is considered as an inside connector. Here Dymola only displays declared variables of the bus (but not of the sub-bus) but without the causality information and even if it is only potentially present (not connected). Present variables of the bus or sub-bus which are not declared are not displayed. Contrary to Dymola, Linkage requires that the "expanded" connection set of an expandable connector be exposed, independently from the level of composition. That means exposing all the variables of the *augmentation set* as defined in :cite:`Modelica2017` *9.1.3 Expandable Connectors*. In our example the same information displayed in :numref:`subbus_outside` for the original sub-bus should be accessible when displaying the connection set of ``bus.ahuI`` whatever the current status (inside or outside) of the connector ``bus``. A typical view of the connection set of expandable connectors for Linkage could be:

    .. list-table:: Typical view of the connection set of expandable connectors -- visible from outside component (connector is inside), "Present" and "I/O" columns display the connection status over the full augmentation set
       :widths: 40 10 10 20 20
       :header-rows: 1

       * - Variable
         - Present
         - Declared
         - I/O
         - Description

       * - **bus**
         -
         -
         -
         -

       * - ``var1`` (present variable connected only once: red color)
         - x
         - O
         - :math:`\rightarrow` ``comp1.var1``
         - ...

       * - ``var2``  (present variable connected twice: default color)
         - x
         - O
         - ``comp2.var1`` :math:`\rightarrow` ``comp1.var2``
         - ...

       * - ``var3`` (declared variable not connected: light grey color)
         - O
         - x
         -
         - ...

       * - *Add variable*
         -
         -
         -
         -

       * - ``var4`` (variable elaborated by augmentation from *all instances* of the connector: light grey color)
         - O
         - O
         -
         - ...

       * - **subBus**
         -
         -
         -
         -

       * - ``var5`` (present variable connected only once: red color)
         - x
         - O
         - ``comp3.var5`` :math:`\rightarrow`
         - ...

       * - *Add variable*
         -
         -
         -
         -

       * - ``var6`` (variable elaborated by augmentation from *all instances* of the connector: light grey color)
         - O
         - O
         -
         - ...

.. figure:: img/bus_minimal.*
   :name: bus_minimal
   :width: 800px

   Minimal example of sub-bus to bus connection illustrating how the bus variables are exposed in Dymola -- case of outside connectors

.. figure:: img/subbus_outside.png
   :name: subbus_outside
   :width: 400px

   Sub-bus variables being exposed in case the sub-bus is an outside connector

.. figure:: img/bus_outside.png
   :name: bus_outside
   :width: 400px

   Bus variables being exposed in case the bus is an outside connector

.. figure:: img/bus_inside.png
   :name: bus_inside
   :width: 400px

   Bus variables being exposed in case the bus is an inside connector


.. _sec_annex_bus_example:

******************************************
Main Features of the Expandable Connectors
******************************************

The main features of the expandable connectors are illustrated with a minimal example described in the figures below where

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

*******************************************
Validating the Use of Expandable Connectors
*******************************************

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

.. note::

   Connectors with conditional instances must be connected to the bus variables with the same conditional statement e.g.

   .. code:: modelica

      if have_occSen then
          connect(ahuSubBusI.nOcc[1:numZon], nOcc[1:numZon])
      end if;

   With Dymola, bus variables cannot be connected to array connectors without explicitly specifying the indices range.
   Using the unspecified ``[:]`` syntax yields the following translation error.

   .. code:: modelica

      Failed to expand conAHU.ahuSubBusI.nOcc[:] (since element does not exist) in connect(conAHU.ahuSubBusI.nOcc[:], conAHU.nOcc[:]);

   Providing an explicit indices range e.g. ``[1:numZon]`` like in the previous code snippet only causes a translation warning: Dymola seems to allocate a default dimension of **20** to the connector, the unused indices (from 3 to 20 in the example hereunder) are then removed since they are not used in the model.

   .. code:: modelica

      Warning: The bus-input conAHU.ahuSubBusI.VDis_flow[3] matches multiple top-level connectors in the connection sets.

      Bus-signal: ahuI.VDis_flow[3]

      Connected bus variables:
      ahuSubBusI.VDis_flow[3] (connect) "Connector of Real output signal"
      conAHU.ahuBus.ahuI.VDis_flow[3] (connect) "Primary airflow rate to the ventilation zone from the air handler, including   outdoor air and recirculated air"
      ahuBus.ahuI.VDis_flow[3] (connect)
      conAHU.ahuSubBusI.VDis_flow[3] (connect)

   This is a strange behavior in Dymola. On the other hand JModelica:

   * allows the unspecified ``[:]`` syntax and,
   * does not generate any translation warning when explicitly specifying the indices range.

   JModelica's behavior seems more aligned with :cite:`Modelica2017` *§9.1.3 Expandable Connectors* that states: "A non-parameter array element may be declared with array dimensions “:” indicating that the size is unknown."
   The same logic as JModelica for array variables connections to expandable connectors is required for Linkage.


.. _sec_annex_bus_array:

*************************************************
Validating the Use of Expandable Connector Arrays
*************************************************

Minimum examples illustrate that arrays of expandable connectors are differentially supported between Dymola and OCT. None of the tested Modelica tools seems to have a fully robust support. However, by reporting those bugs, it seems as a feature we can leverage for Linkage.

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
=========================================================================

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
==================================================================================

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


Passing on a Scalar Variable to an Array of System Models
=========================================================

The typical use case is a schedule, set point, or central system status value that is used as a common input to a set of terminal units.
Two programmatic options are obviously available.

1. Instantiating a replicator (routing) component to connect the variable to the expandable connector array. After discussion with the team, it seems like the best approach to use in production.

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

However that syntax is against the Modelica language specification.
It is indeed equivalent to an equation, and equations are not allowed in an expandable connector class.

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