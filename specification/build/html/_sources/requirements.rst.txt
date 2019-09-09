.. _sec_requirements:

Requirements
============

This section describes the functional, mathematical and software requirements.

General description
-------------------

The software is a graphical user interface for editing Modelica models.
In this respect it must comply with the Modelica language specification :cite:`Modelica2017` for every aspect relating to (the chapter numbers refer to :cite:`Modelica2017`):

* validating the syntax of the user inputs: see *Chapter 2 Lexical Structure* and *Chapter 3 Operators and Expressions*,

* the connection between objects: see *Chapter 9 Connectors and Connections*,

* the structure of packages: see *Chapter 13 Packages*,

* `to be updated`.


Software Environment
********************

.. _tab_environment:

.. table:: Requirements for software integration

      ============================================== ============================================================================================
      Feature                                        Support
      ============================================== ============================================================================================
      Platform (minimum version)                      Windows (10), Linux Ubuntu (16.04), OS X (10.10)
      Web browser                                     Chrome, Firefox, Safari
      Offline version                                 Running on local server with access to resources hosted on the file system
      ============================================== ============================================================================================



Modelica Graphical User Interface
---------------------------------

Structure
*********

See figure :numref:`screen_conf_1`:

* Left panel: library navigator

* Main panel: diagram view of the model

* Right panel:

      * Configuration widget
      * Connection widget
      * Annotation widget
      * Parameters widget

* Menu bar

* Bottom panel: console

Functionalities
***************

.. _tab_gui_func:

.. list-table:: Functionalities of the user interface -- R: required, P: required partially, O: optional, N: not required
      :widths: 40 20 20 100
      :header-rows: 1

      *     - Feature
            - V1
            - V2
            - Comment

      *     - **IO**
            -
            -
            -

      *     - Load ``mo`` file
            - R
            -
            - Simple Modelica model or full package

      *     - Translate model
            - P
            -
            - The software settings allow the user to specify a command for translating the model with a third party Modelica tool e.g. JModelica.

      *     - Simulate model
            - P
            -
            - The software settings allow the user to specify a command for simulating the model with a third party Modelica tool e.g. JModelica.

      *     - Export simulation results
            - R
            -
            - Export in the following format: ``mat, csv``

      *     - Variables browser
            - P
            - R
            - Query selection of model variables based on regular expression (V1) or Brick tag :cite:`Brick` (V2)

      *     - Plot simulation results
            - N
            - O
            -

      *     - Text editor
            - N
            - O
            -

      *     - **Object manipulation**
            -
            -
            -

      *     - Vectorized instances
            - R
            -
            -

      *     - Expandable connectors
            - R
            -
            -

      *     - Navigation in object composition
            - R
            -
            - Right clicking an icon in the diagram view offers the option to open the model in another tab

      *     - **Graphical features**
            -
            -
            -

      *     - Support of Modelica graphical annotations
            - R
            -
            -

      *     - Icon layer
            - O
            - O
            -

      *     - Draw shape, text box
            - O
            - R
            -

      *     - Customize connection lines
            - O
            - R
            - Color, width and line can be specified in the `Annotation Panel`

      *     - Hover information
            - R
            -
            - Class path when hovering an object in the diagram view and tooltip for each GUI element

Generating Connections
******************************

When drawing a connection line between two connector icons:

* a ``connect`` equation with the references to the two connectors is created,

* with a graphical annotation defining the connection path as an array of points and providing an optional smoothing function e.g. Bezier.

    * When no smoothing function is specified the connection path must be rendered graphically as a set of segments.

    * The array of points is either:

        * created fully automatically when the next user's click after having started a connection is made on a connector icon. The function call ``create_new_path(connector1, connector2)`` creates the minimum number of *vertical or horizontal* segments to link the two connector icons with the constraint of avoiding overlaying any instantiated object,

        * created semi automatically based on the input points corresponding to the user clicks outside any connector icon: the function call ``create_new_path(point[i], point[i+1])`` is called to generate the path linking each pair of points together.

Configuration Widget
--------------------

Functionalities
***************

The configuration widget allows the user to generate a model of an HVAC system by filling up a simple form.

The form is provided by the developer as a JSON file or a dictionary within a Python script (easier to program the modeling logic).
It provides for each field:

* the HTML widget and populating data to be used for user input,
* the modeling data required to instantiate, position and set up the parameters of the different components,
* some tags to be used to automatically generate the connections between the different components connectors.

The user interface logic is illustrated in figures :numref:`screen_conf_0` and :numref:`screen_conf_1`.

.. _screen_conf_0:

.. figure:: img/screen_conf_0.svg

      Configuration widget -- Configuring a new model

.. _screen_conf_1:

.. figure:: img/screen_conf_1.svg

   Configuration widget -- Configuring an existing model

The envisioned schema supporting this logic is illustrated in listing :ref:`code_conf_ahu`.

.. code-block:: json
      :caption: Partial example of the configuration data model for an air handling unit
      :name: code_conf_ahu

      {
            "system": {
                  "description": "System type",
                  "value": "AHU"
            },

            "icon": "path of icon.mo",

            "diagram": {
                  "configuration": [20, 20],
                  "modelica": [[-120,-200], [120,120]]
            },

            "name": {
                  "description": "Model name",
                  "widget": "Text",
                  "value": "AHU_#i"
            },

            "type": {
                  "description": "Type of AHU",
                  "widget": "Dropdown",
                  "options": ["VAV", "DOA"]
            },

            "medium": {
                  "air": "Buildings.Media.Air",
                  "hotWater": "Buildings.Media.Water",
                  "chilledWater": "Buildings.Media.Water"
            },

            "equipment": [
                  {
                        "name": "heaRec",
                        "description": "Heat recovery",
                        "widget": "Dropdown",
                        "condition": [
                              {"#type": "DOA"}
                        ],
                        "options": ["None", "Fixed plate", "Enthalpy wheel", "Sensible wheel"],
                        "value": "None",
                        "model": [
                              null,
                              "Buildings.Fluid.HeatExchangers.PlateHeatExchangerEffectivenessNTU",
                              "Buildings.Fluid.HeatExchangers.EnthalpyWheel",
                              "Buildings.Fluid.HeatExchangers.EnthalpyWheel(sensible=true)"
                        ],
                        "icon_transformation": "flipHorizontal",
                        "placement": [12, 9],
                        "connect_tags": {"connectors": {
                              "port_a1": "air_return_inlet", "port_a2": "air_supply_inlet", "port_b1": "air_return_outlet", "port_b2": "air_supply_outlet"
                        }}
                  },
                  {
                        "name": "eco",
                        "description": "Economizer",
                        "widget": "Dropdown",
                        "options": ["None", "Separate dedicated OA dampers", "Single common OA damper"],
                        "condition": [
                              {"#type": "VAV"}
                        ],
                        "model": [
                              null,
                              "Buildings.Fluid.Actuators.Dampers.MixingBoxMinimumFlow",
                              "Buildings.Fluid.Actuators.Dampers.MixingBox"
                        ],
                        "icon_transformation": "flipVertical",
                        "placement": [12, 6],
                        "connect_tags": {"connectors": {
                              "port_Out": "air_supply_junction", "port_OutMin": "air_supply_junction", "port_Sup": "air_supply_outlet",
                              "port_Exh": "air_return_outlet", "port_Ret": "air_return_inlet"
                        }}
                  },
                  {
                        "name": "supFan",
                        "description": "Supply fan",
                        "widget": "Dropdown",
                        "options": ["None", "Draw through", "Blow through"],
                        "value": "Draw through",
                        "model": "Buildings.Fluid.Movers.SpeedControlled_y",
                        "icon_transformation": null,
                        "placement": [null, [16, 11], [16, 18]],
                        "connect_tags": {"fluid_path": "air_supply"}
                  },
                  {
                        "name": "retFan",
                        "description": "Return/Relief fan",
                        "widget": "Dropdown",
                        "options": ["None", "Return", "Relief"],
                        "value": "Relief",
                        "model": "Buildings.Fluid.Movers.SpeedControlled_y",
                        "icon_transformation": "flipHorizontal",
                        "placement": [null, [16, 11], [16, 18]],
                        "connect_tags": {"fluid_path": "air_return"}
                  }
            ],

            "controls": [
                  {
                        "description": "Economizer",
                        "widget": "Dropdown",
                        "condition": [
                              {"#equipment[id=economizer].value": "True"}
                        ],
                        "options": ["ASHRAE 2006", "ASHRAE G36"]
                  }
            ],

            "parameters": [
                  {
                        "name": "v_flowSup_nominal",
                        "description": "Nominal supply air volumetric flow rate",
                        "value": 0,
                        "unit": "m3/h"
                  },
                  {
                        "name": "v_flowRet_nominal",
                        "description": "Nominal return air volumetric flow rate",
                        "value": 0,
                        "unit": "m3/h"
                  }
            ]
      }

Fluid Connectors
................

Natural mapping for a model with two fluid ports (most common case):

* ``Modelica.Fluid.Interfaces.FluidPort_a``: inlet
* ``Modelica.Fluid.Interfaces.FluidPort_b``: outlet

For more than two fluid ports e.g. coil we could use the variable name:

* ``Modelica.Fluid.Interfaces.FluidPort_a port_a1``: primary fluid (liquid) inlet
* ``Modelica.Fluid.Interfaces.FluidPort_a port_a2``: secondary fluid (air) inlet

However that logic fails when the ports correspond to the same medium e.g.:

* ``Buildings.Fluid.Actuators.Dampers.MixingBox``: ``port_Out, port_Exh, port_Ret, port_Sup``
* ``Buildings.Fluid.Actuators.Valves.ThreeWayEqualPercentageLinear``: ``port_1, port_2, port_3``
* ``Buildings.Fluid.HeatExchangers.PlateHeatExchangerEffectivenessNTU``: ``port_a1, port_a2, port_b1, port_b2``

For the configuration script:

* By default ``port_a`` and ``port_b`` will be tagged as ``inlet`` and ``outlet`` respectively.

* An optional tag is provided at the instance level to specify the fluid path e.g. ``air_supply`` or ``air_return``.

* All fluid connectors are then tagged by concatenating the previous tags e.g. ``air_supply_inlet`` or ``air_return_outlet``.

We need an additional mechanism to allow tagging each fluid port individually. Typically for a three way valve, the bypass port should be on a different fluid path than the inlet and outlet ports see :numref:`linkage_connect_3wv`. Hence we need a mapping dictionary at the connector level which, if provided, takes precedence on the default logic specified above.
Furthermore a fluid connector can be connected to more than one other fluid connector. To support that feature another connector tag value is needed: ``junction``.
For a three way valve without any flow splitter to explicitly model the fluid junction the mapping dictionary could be:

``{"port_1": "hotwater_return_inlet", "port_2": "hotwater_return_outlet", "port_3": "hotwater_supply_junction"}``

.. figure:: img/linkage_connect_3wv.svg
      :name: linkage_connect_3wv

      Connection scheme with a fluid junction not modeled explicitly, using the connector tag ``junction``

The conversion script throws an exception if the instantiated class has some fluid ports that cannot be tagged with the previous logic e.g. non default names and no (or incomplete) mapping dictionary provided.

If the tagging is resolved for all fluid connectors of the instantiated objects the connector tags are stored in a hierarchical vendor annotation at the model level e.g. ``__Linkage_connect(Tags(object_name1={connector_name1=air_supply_inlet, connector_name2=air_supply_outlet, ...}, ...))``. This is done when updating the model.

All object names in ``__Linkage_tags(Tags())`` annotation reference instantiated objects with fluid ports that have to be connected to each other. To build the full connection set, two additional inputs are needed:

1. The names of the start port and the end port for each fluid path. Note that those ports may be part of a different fluid path see figure.

2. The direction (horizontal or vertical) of the connection path.

Those are stored in ``__Linkage_connect(Direction(fluid_path1={start_connector_name, end_connector_name, horizontal_or_vertical}))``.

The connection logic is then as follows:

* List all the different fluid paths in ``__Linkage_connect(Tags())`` corresponding to each tuple ``{fluid}_{path}`` in all the connector tags ``{fluid}_{path}_{port}``.

* For each fluid path:

      * Find the position of the objects corresponding to the start and end ports specified in ``__Linkage_connect(Direction(fluid_path1={start_connector_name, end_connector_name}))``. Those are further referred to as start and end position.

      * | Find the orientation (up, down, right, left) of the direction (horizontal, vertical) of the connection path by comparing the ``x`` (resp. ``y``) coordinate values of the start and end position if the direction is horizontal (resp. vertical).

        | Throw an exception if the orientation cannot be resolved due to identical coordinate values.

      * Order all the connectors belonging to that fluid path according to the orientation defined here above and based on the position of the corresponding objects with the constraint that for each object ``inlet`` has to be listed first and ``outlet`` last. Prepend / append that list with the start and end connectors.

      * Generate the ``connect`` equations by iterating on the ordered list of connectors as illustrated in the pseudo code below. And generate the connection path and the corresponding graphical annotation::

            i = 1
            while i < n
            j = i + 1
            if type(ordered_connector[i]) == "junction"
                  while type(ordered_connector[j]) == "junction"
                        connect(ordered_connector[i], ordered_connector[j])
                        annotation(Line(points=create_new_path(ordered_connector[i], ordered_connector[j])))
                        j = j + 1
                  i = j
            else
                  connect(ordered_connector[i], ordered_connector[j])
                  annotation(Line(points=create_new_path(ordered_connector[i], ordered_connector[j])))
                  i = j + 1

        :numref:`linkage_connect_junction` further illustrates the logic for connecting ``junction`` ports.

.. figure:: img/linkage_connect_junction.svg
      :name: linkage_connect_junction
      :align: center

      Logic of ports connection in case of ``inlet`` and ``outlet`` ports (top) and ``junction`` ports (bottom)

The implications of that logic are the following:

* Within the same fluid path, objects are connected in a given direction and orientation: to represent a fluid loop (graphically) at least two fluid paths must be defined, typically ``supply`` and ``return``.

* A same fluid path does not necessarily imply a uniform flow rate.

Signal Connectors
.................

Generating the ``connect`` equations for signal variables relies on the expandable connector type, see *§9.1.3
Expandable Connectors* in :cite:`Modelica2017`. For the `Configuration widget` we will define classes of this type with a predefined set of control variables: such a class will be further referred to as `control bus`.

Three main features of the expandable connector are leveraged:

#. All components in an expandable connector are seen as connector instances even if they are not declared as such. In comparison to a non expandable connector, that means that each variable (even of type ``Real``) can be connected i.e. be part of a ``connect`` equation.

   .. note::

      * Connecting a non connector variable to a connector variable with ``connect(non_connector_var, connector_var)`` yields a warning but no error. It is considered bad practice though and a standard equation should be used in place ``non_connector_var = connector_var``.

      * Using a ``connect`` equation allows to draw a connection line which makes the model structure more obvious to the user. Furthermore it avoids mixing ``connect`` equations and standard equations within the same equation set, which has been adopted as a best practice ine Modelica Buildings library.

#. The causality (input or output) of each variable inside an expandable connector is not predefined but rather depends on the ``connect`` equation where the variable is being used. So the same variable can be connected to an instance of ``Modelica.Blocks.Interfaces.RealOutput`` (and treated as an input) or an instance of ``Modelica.Blocks.Interfaces.RealInput`` (and treated as an output).

#. The variables set of a class of type expandable connector is expanded whenever a new variable gets connected to any *instance* of the class. Though that feature is not needed by the `Configuration widget` (we will have a predefined `Control bus` with declared variables corresponding to the control sequences implemented for each system), it is needed to allow the user further modifying the control sequence. Adding new control variables is simply done by connecting them to the `control bus`.

Those features are illustrated with a minimal example in the figures below where:

* a controlled system consisting in a sensor (idealized with a real expression) and an actuator (idealized with a simple block passing through the value of the input control signal) is connected with,

* a controller system which divides the input variable (measurement) by itself and outputs a control variable equal to one.

The same model is first implemented with an expandable connector and then with a standard connector.

.. figure:: img/BusTestExp.svg
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

.. figure:: img/BusTestControlledExp.svg
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

      expandable connector AhuBus
      extends Modelica.Icons.SignalBus;
      end AhuBus;

.. note::

      The definition of ``AhuBus`` in the code snippet here above does not include any variable declaration. However the variables ``ahuBus.yAct`` and ``ahuBus.yMea`` are used in ``connect`` equations. That is only possible with an expandable connector.

      For the `Configuration widget` we will have predeclared variables with names allowing a one-to-one correspondence between:

      * the control sequence input variables (outputs of the equipment model e.g. measured quantities and actuators returned positions),

      * the control sequence output variables (inputs of the equipment model e.g. actuators commanded positions).

      The control bus variable is used as a "gateway" to stream values between the controlled and controller systems.

.. figure:: img/BusTestControllerExp.svg
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

.. figure:: img/BusTestNonExp.svg
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

.. figure:: img/BusTestControlledNonExp.svg
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

      connector NonExpandableBus
      // The following declarations are required.
      Real yMea;
      Real yAct;
      end NonExpandableBus;

.. figure:: img/BusTestControllerNonExp.svg
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

Issues
======

We have a linked modelica model residing on disk. When loading that model, LinkageJS must be able to:

* identify which object and ``connect`` statement can be modified with the template script: declaration/statement annotation ``__Linkage_modify=true``

* generate the JSON configuration file:

      * automatically from the model structure? Non working examples:

      * Supply fan/Draw through: if the user has modified the ``Placement`` we have no one-to-one correspondance with JSON file. Also relying on the ``connect`` statements involving the object seems to complex.


Questions
=========

* Validation upon submit (export/generate) VS real-time
* Routine to add sensors for control sequences
* Routine to add fluid ports: part of data model?

Choice of units: SI / IP

Launch simulation integrated

* At least compilation required to validate the model?
* For control sequence configuration the model may not need to be fully specified.

Visualize results: variable browser (with Brick/Haystack option similar as ``re`` option)

No icon layer: just diagram layer showing graphical objects, component icons, connectors and connection lines

Automatic medium propagation between connected components

* Expected as a future enhancement of Modelica standard: should we anticipate or wait and see?

.. note::

      Brick and tagging

      Set up parameters values like OS measures enable cf. electrical loads...

      From Taylor Eng.

      For standard systems, it might be possible to simply include in their specifications a table of ASHRAE Guideline 36 sequences with check boxes for the paragraph numbers that are applicable to their project.

      From https://build.openmodelica.org/Documentation/Modelica.Fluid.UsersGuide.ComponentDefinition.FluidConnectors.html

      With the current library design, it is necessary to explicitly select the medium model for each component in a circuit. This model is then propagated to the ports, and a Modelica translator will check that the quantity and unit attributes of connected interfaces are identical. Therefore, an error occurs, if connected FluidPorts do not have a medium with the same medium name. In the future, automatic propagation of fluid models through the ports will be introduced, but this still not possible with Modelica 3.0.
