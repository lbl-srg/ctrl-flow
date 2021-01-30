.. _sec_requirements:

##################
Requirements
##################

.. note::

   Most of the concepts used to develop that specification are defined in the Modelica Language Specification :cite:`Modelica2017`.


.. _sec_general_description:

***************************
General Description
***************************

Main Requirements
==================

The following requirements apply to both the configuration widget (Phase 1 of the development) and the diagram editor (future phase of the development).

* The software must rely on client side JS code with minimal dependencies and must be built down to a single page HTML document (SPA).

* A widget structure is required that allows seamless embedding into:

  * a desktop app—with standard access to the local file system,

  * a standalone web app—with access to the local file system limited to Download & Upload functions of the web browser (potentially with an additional sandbox file system to secure backup in case the app enters an unknown state),

  * any third-party application with the suitable framework to serve a single page HTML document executing JS code—with access to the local file system through the API of the third-party application:

    .. admonition:: Revision Note (10/2020)
       :class: danger

       The following bullet point is modified to require “proof of concept” for third party integration through a demonstration and not through a completed integration.

    * For the first development phase pertaining to the configuration widget, the third-party application for the widget integration is an existing graphical editor for Modelica.
      To demonstrate the feasibility of this integration, a proof of concept shall be developed, together with the documentation describing how this workflow can be accomplished.
      This will include the creation of a prototype where the host application may be an actual Modelica editor or a rudimentary emulator of such.

    * For the second development phase, the primary integration target is `OpenStudio® <https://www.openstudio.net>`_ (OS) while the widget to be integrated is now the full-featured editor (including the configuration widget).
      An example of a JS application embedded in OS is `FloorspaceJS <https://nrel.github.io/OpenStudio-user-documentation/reference/geometry_editor>`_. The standalone SPA lives here: `https://nrel.github.io/floorspace.js <https://nrel.github.io/floorspace.js>`_. FloorspaceJS may be considered as a reference for the development.

.. admonition:: Revision Note (01/2021)
   :class: danger

   The following bullet point is modified to specify Modelica as the language supporting the templating.

* The core components parsing and generating Modelica classes must rely on JSON-formatted Modelica. LBL has developed a `Modelica to JSON translator <https://lbl-srg.github.io/modelica-json/>`_ that should be used for interfacing those core components with native Modelica code.

.. admonition:: Revision Note (10/2020)
   :class: danger

   The Python API, if required, will be developed in a subsequent phase.


Software Compatibility
===========================

The software requirements regarding platform and environment compatibility are presented in :numref:`tab_environment`.

.. _tab_environment:

.. table:: Requirements for software compatibility

   ============================================== =================================================
   Feature                                        Support
   ============================================== =================================================
   Platform (minimum version)                      Windows (10), Linux Ubuntu (18.04), OS X (10.10)
   Mobile device                                   The software may support iOS and Android
                                                   integration though this is not an absolute
                                                   requirement.
   Web browser                                     Chrome, Firefox, Safari
   ============================================== =================================================


UI Visual Structure
===========================

.. admonition:: Revision Note (11/2020)
   :class: danger

   Only the requirements pertaining to the configuration widget are retained.

A responsive design is required.

For the record, a mockup of the UI for the full featured editor is presented :numref:`screen_mockup`.
For Phase 1, only the graphical features pertaining to the configuration widget in the right panel should be considered.

.. figure:: img/screen_mockup.*
   :name: screen_mockup

   UI Visual Structure

.. admonition:: Revision Note (01/2021)
   :class: danger

   The paragraph below is added.

Using the Modelica language for the templating implies that the configuration widget must comply with most of the specification of the *parameter dialog* from :cite:`Modelica2017` §18.7.
However, part of the specification is only optional in Phase 1 because only a subset of all the user inputs of a Modelica model are needed in the control specification workflow. For instance the type of medium, the nominal values of physical quantities, various modeling assumptions, etc. are only needed in the modeling and simulation workflow.

The features of the Modelica specification that are required for Phase 1 are detailed in :numref:`tab_gui_add`.

In addition, the configuration widget must include a mechanism to select the subset of user inputs that must be exposed in the UI. For this purpose a vendor-specific annotation at the declaration level is specified.

Eventually, the core components developed in Phase 1 must be reusable when developing a full featured parameter dialog widget in Phase 2, with the ability to switch between a control specification mode—where only a subset of the user inputs being exposed—and a modeling and simulation workflow—with the complete set of the user inputs being exposed.


.. _sec_functionalities:

***************************
Detailed Functionalities
***************************

:numref:`tab_gui_func` provides a list of the functionalities that the software must support. Phase 1 refers to the configuration widget, future work refers to the full-featured editor.

.. admonition:: Revision Note
   :class: danger

   * **(10/2020)** The features "Copy/Paste Objects" and "Undo/Redo" are optional and not required for Phase 1.

   * **(11/2020)** :numref:`tab_gui_func` is edited to focus on requirements pertaining to Phase 1.

.. _tab_gui_func:

.. list-table:: Functionalities of the software -- R: required, P: required partially, O: optional, N: not required
   :widths: 30 10 10 50
   :header-rows: 1

   * - Feature
     - Phase 1
     - Future
     - Comment

   * - **Main functionalities**
     -
     -
     - (as per :numref:`sec_general_description`)

   * - Diagram editor for Modelica classes
     - N
     - R
     - In the first phase, the configuration widget must be integrated into an existing diagram editor for Modelica. Such an editor must be developed in the second phase.

   * - Configuration widget
     - R
     - R
     -

   * - Documentation export
     - R
     - R
     - See :numref:`sec_documentation_export`.

   * - **I/O**
     -
     -
     -

   * - Export documentation
     - R
     - R
     - Control points, sequence of operation description (based on CDL to Word translator developed by LBL), and equipment schematics see :numref:`sec_documentation_export`

   * - **Modelica features**
     -
     -
     -

   * - Modelica code editor
     - N
     - R
     - Raw text editor with linter and Modelica specification checking upon save

       Note that this functionality requires translation and reverse translation of JSON to Modelica (those translators are developed by LBL).

   * - Library version management
     - R
     - R
     - If a loaded class contains the Modelica annotation ``uses`` (e.g., ``uses(Buildings(version="6.0.0")``) the software checks the version number of the stored library, prompts the user for update if the version number does not match, executes the conversion script per user request.

   * - Path discovery
     - R
     - R
     - A routine to reconstruct the path or URL of a referenced resource within the loaded Modelica libraries is required. Typically a resource can be referenced with the following syntax ``modelica://Buildings.Air.Systems.SingleZone.VAV``.

   * - **Object manipulation**
     -
     -
     -

   * - Avoiding duplicate names
     - R
     - R
     - When instantiating a component or assigning a name through the configuration widget, if the default name is already used in the class the software automatically appends the name with the lowest integer value that would ensure uniqueness.

       When copying and pasting a set of objects connected together, the set of connect equations is updated to ensure  consistency with the appended object names.

   * - **Graphical features**
     -
     -
     - A user experience similar to modern web apps is expected e.g. `tranedesignassist.com <https://tranedesignassist.com/>`_.

   * - Pan and zoom on mouse actions
     - N
     - R
     -

   * - Help tooltip
     - R
     - R
     - Provide contextual help information to the user during each step of the workflow

   * - **Miscellaneous**
     -
     -
     -

   * - Internationalization
     - R
     - R
     - The software will be delivered in US English only, but it must be architectured to allow seamless integration of additional languages in the future.

       The choice between I-P and SI units must be possible. The mechanism supporting different units will be specified by LBL in a later version of this document.

   * - User documentation
     - R
     - R
     - User manual of the GUI and the corresponding API

       Both an HTML version and a PDF version are required (may rely on Sphinx).

   * - Developer documentation
     - R
     - R
     - All classes, methods, free functions, and schemas must be documented with an exhaustive description of the functionalities, parameters, return values, etc.

       UML diagrams should also be provided.

       At least an HTML version is required, PDF version is optional (may rely on Sphinx or VuePress).



.. _tab_gui_add:

.. list-table:: Additional functionalities for Modelica-based templating -- R: required, P: required partially, O: optional, N: not required
   :widths: 30 10 10 50
   :header-rows: 1

   * - Feature
     - Phase 1
     - Future
     - Comment

   * - **Modelica annotations for the GUI**
     -
     -
     - (As per :cite:`Modelica2017` §18.7)

   * - ``Dialog(tab|group)``
     - R
     - R
     - The UI must render the structure in groups and tabs as specified by this annotation. The groups may be collapsable with a button to expand or collapse all the groups.

   * - ``Dialog(enable)``
     - R
     - R
     - ``Dialog(enable=false)`` should result in the input field not being rendered in the UI—as opposed to being only greyed out but still visible in Dymola.

   * - ``Dialog(showStartAttribute)``
     - N
     - R
     - The configuration widget should not display the input for the start value of a variable, this is not required in Phase 1.

   * - ``Dialog(colorSelector)``
     - N
     - R
     -

   * - ``Dialog(loadSelector|saveSelector)`` and ``Selector(filter|caption)``
     - R
     - R
     - A mechanism to display a file dialog to select a file is required. The ``filter`` and ``caption`` attributes must also be interpreted as specified in :cite:`Modelica2017`.


   * - **Annotation Choices for Modifications and Redeclarations**
     -
     -
     - (As per :cite:`Modelica2017` §18.11 and §7.3.4)

   * - ``choicesAllMatching``
     - R
     - R
     - A discovery mechanism is required to enumerate all class subtypes (where subtyping is possible through multiple inheritances or nested function calls to a record constructor, such as ``record A = B(...);``) given a constraining class. The enumeration must display the class description string and default to the class simple name.

   * - ``choices(choice)``
     - R
     - R
     - The enumeration must display the description string provided within each inner ``choice`` and default to the description string of the redeclared class, and ultimately default to the simple name of the redeclared class.


.. _sec_modelica_gui:

******************************************************
Requirements Related to the Modelica Language
******************************************************

.. admonition:: Revision Note (11/2020)
   :class: danger

   This paragraph replaces the paragraph "Modelica Graphical User Interface" and only retains the requirements pertaining to the configuration widget.


Language Specification
===========================

The software must comply with the Modelica language specification :cite:`Modelica2017` for every aspect relating to (the chapter numbers refer to :cite:`Modelica2017`):

* validating the syntax of the user inputs: see *Chapter 2 Lexical Structure* and *Chapter 3 Operators and Expressions*,

* the connection between objects: see *Chapter 9 Connectors and Connections*,

* the structure of packages: see *Chapter 13 Packages*,

* the annotations: see *Chapter 18 Annotations*.

JSON Representation
===========================

LBL has already developed a `Modelica to JSON translator <https://lbl-srg.github.io/modelica-json/>`_.
This development includes the definition of two JSON schemas:

#. `Schema-modelica.json <https://lbl-srg.github.io/modelica-json/modelica.html>`_ validates the JSON files parsed from Modelica.

#. `Schema-CDL.json <https://lbl-srg.github.io/modelica-json/CDL.html>`_ validates the JSON files parsed from `CDL <http://obc.lbl.gov/specification/cdl>`_ (subset of Modelica language used for control sequence implementation).

Linkage should leverage those developments by consuming and outputting Modelica files formatted into JSON, without having to parse the Modelica syntax.


Vendor-Specific Annotations
===========================




Declaration Level




Class Level



``"__Linkage" class-modification``

* TODO: validate that ``class-modification`` is actually valid in the scope of the class where the redeclaration happens (similar issue with ``choices`` annotation).

  Example: The syntax of ``select`` in ``Buildings.Experimental.Templates.AHUs.Main.VAVSingleDuct.datEco`` is valid.

  Check ``datCoi(redeclare parameter Buildings.Experimental.Templates.AHUs.Coils.HeatExchangers.Data.Discretized datHex)`` in ``Buildings.Experimental.Templates.AHUs.Main.VAVSingleDuct_outer``

* ``"choicesConditional" "(" [ "condition" "=" logical-expression "," choices-annotation ] { "," "condition" "=" logical-expression "," choices-annotation } ")"``

  Example: see declaration of ``Buildings.Experimental.Templates.AHUs.Main.VAVSingleDuct.eco``.

  Takes precedence on Modelica ``choices`` and ``choicesAllMatching`` annotation. Choices are rendered in Linkage UI based on the vendor-specific annotation. Note that ``choices()`` annotation can be empty in which case no enumeration shall be rendered.

  Solves: Modelica ``choices`` annotation does not allow conditional specification of the choices to be rendered.

* ``"select" "(" [ "condition" "=" logical-expression "," class-modification ] { "," "condition" "=" logical-expression "," class-modification } ")"``

  Takes precedence on Modelica ``choices`` and ``choicesAllMatching`` annotation. No enumeration is rendered in Linkage UI.

  Solves: Modelica does not allow conditional ``element-redeclaration``.

* ``"display" "=" logical-expression``

  To display/hide some parameters from the UI in a control configuration mode (TODO: specify how this mode is enabled), for instance the medium, dynamics, etc.

  Note that Modelica annotation ``Dialog(enable=false)`` should result in the input field not being rendered at all in the UI—as opposed to being only greyed out but still visible in Dymola.

Note that the above requires to interpret the redeclare statements before compile time in order to "visit" the redeclared classes and evaluate clauses like ``coiCoo.typHex <> Types.HeatExchanger.None``—which Dymola does not do for instance with ``annotation(Dialog(enable=typHex<>Types.HeatExchanger.None))``.



.. _sec_configuration_widget:

*****************************************************
Configuration Widget
*****************************************************

Package Structure for the Templates and User Projects
======================================================






Functionalities
===============

The configuration widget allows the user to generate a Modelica model of an HVAC system and its controls by filling up a simple input form.
It is mostly needed for integrating advanced control sequences that can have dozens of I/O variables.
The intent is to reduce the complexity to the mere definition of the system layout and the selection of standard control sequences already transcribed in Modelica :cite:`OBC`.

.. note::

   `CtrlSpecBuilder <https://www.ctrlspecbuilder.com/ctrlspecbuilder/home.do;jsessionid=4747144EA3E61E9B82B9E0B463FF2E5F>`_ is a tool widely used in the HVAC industry for specifying control systems. It may be used as a reference for the development in terms of user experience minimal functionalities. Note that this software does not provide any Modelica modeling functionality.

There are fundamental requirements regarding the Modelica model generated by the configuration widget:

1. It must be "graphically readable" (both within Linkage and within any third-party Modelica GUI e.g. Dymola): this is a strong constraint regarding the placement of the composing objects and the connections that must be generated automatically.

2. It must be ready to simulate: no additional modeling work or parameters setting is needed outside the configuration widget.

3. It must contain all annotations needed to regenerate the HTML input form when loaded, with all entries corresponding to the actual state of the model.

   * Manual modifications of the Modelica model made by the user are not supported by the configuration widget: an additional annotation should be included in the Modelica file to flag that the model has deviated from the template. In this case the configuration widget is disabled when loading that model.

4. The implementation of control sequences must comply with OpenBuildingControl requirements, see *§7 Control Description Language* and *§8 Code Generation* in :cite:`OBC`. Especially:

   * It is required that the CDL part of the model can be programmatically isolated from the rest of the model in order to be translated into vendor-specific code (by means of a third-party translator).

   * The expandable connectors (control bus) are not part of CDL specification. Those are used by the configuration widget to connect

     * control blocks and equipment models within a composed sub-system model, e.g., AHU or terminal unit,

     * different sub-system models together to compose a whole system model, e.g., VAV system serving different rooms.

     This is consistent with OpenBuildingControl requirement to provide control sequence specification at the equipment level only (controller programming), not for system level applications (system programming).

The input form is provided by the template developer (e.g., LBL) in a data model with a format that is to be further specified in collaboration with the software developer. The minimum requirement is the ability to validate the configuration data against a well documented schema that LBL can maintain.

The data model should typically provide for each entry

* the HTML widget and populating data to be used for requesting user input,
* the modeling data required to instantiate, position and set the parameters values of the different components,
* some tags to be used to automatically generate the connections between the different components connectors.

The user interface logic is illustrated in figures :numref:`screen_conf_0` and :numref:`screen_conf_1`: the comments in those figures are part of the requirements.

.. figure:: img/screen_conf_0.*
   :name: screen_conf_0

   Configuration widget -- Configuring a new model

.. figure:: img/screen_conf_1.*
   :name: screen_conf_1

   Configuration widget -- Configuring an existing model


Equipment and controller models are connected together by means of a *control bus*, see :numref:`screen_schematics_modelica`. The upper-level Modelica class including the equipment models and control blocks is the ultimate output of the configuration widget: see :numref:`screen_conf_1` where the component named ``AHU_1_01_02`` represents an instance of the upper-level class ``AHU_1`` generated by the widget. That component exposes the outside fluid connectors as well as the top level control bus.

The logic for instantiating classes from the library is straightforward. Each field of the form specifies

* the reference of the class (library path) to be instantiated depending on the user input,

* the position of the component in simplified grid coordinates to be converted in diagram view coordinates.

:numref:`sec_fluid_connectors` and :numref:`sec_signal_connectors` address how the connections between the connectors of the different components are generated automatically based on this initial model structure.

.. _sec_data_model:

Data Model
==========

.. admonition:: Revision Note (01/2021)
   :class: danger

   The paragraph *Data Model* is removed as the templating is now based on the Modelica language specification.


.. _sec_fluid_connectors:

Fluid Connectors
================

.. admonition:: Revision Note (01/2021)
   :class: danger

   The paragraph *Fluid Connectors* is removed as the templating is now based on the Modelica language specification. The connect clauses between fluid connectors are fully specified in the templates.


.. _sec_signal_connectors:

Signal Connectors
=================

.. admonition:: Revision Note (01/2021)
   :class: danger

   The paragraph *Signal Connectors* is removed as the templating is now based on the Modelica language specification. The connect clauses between signal variables are fully specified in the templates.


Validation and Additional Requirements
--------------------------------------

The use of expandable connectors (control bus) is validated in case of a complex controller, see :numref:`sec_annex_bus_valid`.

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


.. _sec_connect_ui_req:

Additional Requirements for the UI
----------------------------------

Based on the previous validation case, :numref:`dymola_bus` presents the Dymola pop-up window displayed when connecting the sub-bus of input control variables to the main control bus.
A similar view of the connections set must be implemented with the additional requirements listed below. That view is displayed in the connections tab of the right panel.


.. figure:: img/dymola_bus.png
   :name: dymola_bus

   Dymola pop-up window when connecting the sub-bus of input control variables (left) to the main control bus (right) -- case of outside connectors


The variables listed immediately after the bus name are either

* *declared variables* that are not connected, for instance ``ahuBus.yTest`` (declared as ``Real`` in the bus definition): those variables are only *potentially present* and eventually considered as *undefined* when translating the model (treated by Dymola as if they were never declared) or,

* *present variables* i.e. variables that appear in a connect equation, for instance ``ahuSubBusI.TZonHeaSet``: the icon next to each variable then indicates the causality. Those variables can originally be either declared variables or variables elaborated by the augmentation process for *that instance* of the expandable connector i.e. variables that are declared in another component and connected to the connector's instance.

The variables listed under ``Add variable`` are the remaining *potentially present variables* (in addition to the declared but not connected variables). Those variables are elaborated by the augmentation process for *all instances* of the expandable connector, however they are not connected in that instance of the connector.

In addition to Dymola's features for handling the bus connections, Linkage requires the following.

* Color code to distinguish between

  * Variables connected only once (within the entire augmentation set): those variables should be listed first and in red color. This is needed so that the user immediately identify which connections are still required for the model to be complete.

    .. Note::

       Dymola does not throw any exception when a *declared* bus variable is connected to an input (resp. output) variable but not connected to any other non input (resp. non output) variable. It then uses the default value (0 for ``Real``) to feed the connected variable.

       That is not the case if the variable is not declared i.e. elaborated by augmentation: in that case it has to be connected in a consistent way.

       JModelica throws an exception in any case with the message ``The following variable(s) could not be matched to any equation``.

  * Declared variables which are only potentially present (not connected): those variables should be listed last (not first as in Dymola) and in light grey color. That behavior is also closer to :cite:`Modelica2017` *§9.1.3 Expandable Connectors*: "variables and non-parameter array elements declared in expandable connectors are marked as only being potentially present. [...] elements that are only potentially present are not seen as declared."

* View the "expanded" connection set of an expandable connector in each level of composition—that covers several topics:

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


Control Sequence Configuration
==============================

In principle the configuration widget as specified previously should allow building custom control sequences based on elementary control blocks (e.g. from the `CDL Library <https://github.com/lbl-srg/modelica-buildings/tree/master/Buildings/Controls/OBC/CDL>`_) and automatically generating connections between those blocks. However

* this would require to distinguish between low-level control blocks (e.g. ``Buildings.Controls.OBC.CDL.Continuous.LimPID``) composing a system controller—which must be connected with direct connect equations and not with expandable connectors variables that are not part of the CDL specification—and high-level control blocks (e.g. ``Buildings.Controls.OBC.ASHRAE.G36_PR1.AHUs.MultiZone.VAV.Controller``)—which can be connected to other high-level controllers (e.g. ``Buildings.Controls.OBC.ASHRAE.G36_PR1.TerminalUnits.Controller``) using expandable connectors variables (the CDL translation will be done for each high-level controller individually),

* the complexity of some sequences makes it hard to validate the reliability of such an approach without extensive testing.

Therefore in practice, and at least for the first version of Linkage, it has been decided to rely on pre-assembled high-level control blocks. For each system type (e.g., AHU) one (or a very limited number) of control block(s) should be instantiated by the configuration widget for which the connections can be generated using expandable connectors as described before.


.. _sec_parameters:

Parameters Setting
------------------

.. admonition:: Revision Note (11/2020)
   :class: danger

   This paragraph is modified to retain only the requirements pertaining to the configuration widget.

Enumeration and Boolean
=======================

For parameters of type *enumeration* or *Boolean* a dropdown menu should be displayed and populated by the enumeration items or ``true`` and ``false``.

Validation
==========

Values entered by the user must be validated *upon submit* against Modelica language specification :cite:`Modelica2017` and parameter attributes e.g. ``min``, ``max``.

A color code is required to identify the fields with incorrect values and the corresponding error message must be displayed on hover.


.. _sec_documentation_export:

********************
Documentation Export
********************

The documentation export encompasses three items.

#. Engineering schematics of the equipment including the controls points

#. Control points list

#. Control sequence description

The composition level at which the functionality will typically be used is the same as the one considered for the configuration widget, for instance primary plant, air handling unit, terminal unit, etc. No specific mechanism to guard against an export call at different levels is required.

:numref:`screen_schematics_output` provides an example of the documentation to be generated in case of an air handling unit. The documentation export may consist in three different files but must contain all the material described in the following paragraphs.

.. figure:: img/screen_schematics_output.*
   :name: screen_schematics_output

   Mockup of the documentation export


Engineering Schematics
======================

Objects of the original model to be included in the schematics export must have a declaration annotation providing the SVG file path for the corresponding engineering symbol e.g. ``annotation(__Linkage(symbol_path="value of symbol_path"))``.

.. note::

   It is expected that Linkage will eventually be used to generate design documents included in the invitation to tender for HVAC control systems. The exported schematics should meet the industry standards and they must allow for further editing in CAD softwares, e.g., AutoCAD®.

   Due to geometry discrepancies between Modelica icons and engineering symbols a perfect alignment of the latter is not expected by simply mapping the diagram coordinates of the former to the SVG layout. A mechanism should be developed to automatically correct small alignment defaults.

For the exported objects

* the connectors connected to the control input and output sub-buses must be split into two groups depending on their type—Boolean or numeric,
* an index tag is then generated based on the object position, from top to bottom and left to right,
* eventually connection lines are drawn to link those tags to the four different control points buses (AI, AO, DI, DO). The line must be vertical, with an optional horizontal offset from the index tag to avoid overlapping any other object.

SVG is the required output format.

See :numref:`screen_schematics_output` for the typical output of the schematics export process.


Control Points List
===================

Generating the control points list is done by calling a module developed by LBL (ongoing development) which returns an HTML or Word document.


Control Sequence Description
============================

Generating the control sequence description is done by calling a `module developed by LBL <https://lbl-srg.github.io/modelica-json/>`_ which returns an HTML or Word document.


.. admonition:: Revision Note (10/2020)
   :class: danger

   The paragraphs "Working with Tagged Variables", "OpenStudio Integration" and "Interface with URBANopt GeoJSON" are removed.

*********
Licensing
*********

The software is developed under funding from the U.S. Department of Energy and the U.S. Government consequently retains certain rights. As such, the U.S. Government has been granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software to reproduce, distribute copies to the public, prepare derivative works, and perform publicly and display publicly, and to permit other to do so.

The main software components built as part of this development project must be open sourced under BSD 3 or 4-clause, with possible additions to make it easy to accept improvements. Licensing under GPL or LGPL will not be accepted.

Different licensing options are then envisioned depending on the integration target and the engagement of third-party developers and distributors. The minimum requirement is that at least one integration target be made available as a free software.

* Desktop app

  Subscription-based

* Standalone web app

  * Free account allowing access to Modelica libraries preloaded by default, for instance Modelica Standard and Buildings: the user can only upload and download single Modelica files (not a package).

  * Pro account allowing access to server storage of Modelica files (packages uploaded and models saved by the user): the user can update the stored libraries and reopen saved models between sessions.

* Third-party application embedding

  Licensing will depend on the application distribution model.

  For OpenStudio there is currently a shift in the `licensing strategy <https://www.openstudio.net/new-future-for-openstudio-application>`_. The specification will be updated to comply with the distribution options after the transition period (no entity has yet announced specific plans to continue support for the OS app).

