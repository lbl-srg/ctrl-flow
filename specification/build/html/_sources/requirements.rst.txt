.. _sec_requirements:

Requirements
============

.. note::

   Most of the concepts used to develop that specification are defined in the Modelica Language Specification :cite:`Modelica2017`.


.. _sec_general_description:

General Description
-------------------

Main Requirements
*****************

The following requirements apply to both the configuration widget (first phase of the development) and the diagram editor (second phase of the development).

* The software must rely on client side JS code with minimal dependencies and must be built down to a single page HTML document (SPA).

* A widget structure is required that allows seamless embedding into:

  * a desktop app -- with standard access to the local file system,

  * a standalone web app -- with access to the local file system limited to Download & Upload functions of the web browser (potentially with an additional sandbox file system to secure backup in case the app enters an unknown state),

  * any third-party application with the suitable framework to serve a single page HTML document executing JS code -- with access to the local file system through the API of the third-party application:

    * For the first development phase pertaining to the configuration widget, the third-party application for the widget integration is the existing graphical editor for Modelica. The widget must be integrated into this editor. That requires for the editor to be able to serve a single page HTML document executing JS code.

    * For the second development phase, the primary integration target is `OpenStudio® <https://www.openstudio.net>`_ (OS) while the widget to be integrated is now the full-featured editor (including the configuration widget).
      An example of a JS application embedded in OS is `FloorspaceJS <https://nrel.github.io/OpenStudio-user-documentation/reference/geometry_editor>`_. The standalone SPA lives here: `https://nrel.github.io/floorspace.js <https://nrel.github.io/floorspace.js>`_. FloorspaceJS may be considered as a reference for the development.

  .. note::

     Those three integration targets are actual deliverables.

     For the first development phase pertaining to the configuration widget, the exact functionalities (configuration only, or configuration plus minimal editing functionalities) of the standalone web app and desktop app versions shall be further discussed with the provider.

* The diagram editor must consume and return Modelica models formatted into JSON. LBL has developed a `Modelica to JSON translator <https://lbl-srg.github.io/modelica-json/>`_ that should be used for these formatting tasks.

* A specific data model must be devised for the configuration widget. The recommended format is JSON but alternative formats may be proposed. A minimum requirement is the ability to validate the configuration data against a well documented schema that LBL can maintain. The configuration widget must return Modelica models formatted into JSON, see previous item.

* A Python or Ruby API is required to access the data model and leverage the main functionalities of the software in a programmatic way, e.g., by means of `OpenStudio measures <http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/>`_.


Software Compatibility
**********************

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
*******************

A responsive design is required.

A minimal mockup of the UI is presented :numref:`screen_mockup`.

.. figure:: img/screen_mockup.*
   :name: screen_mockup

   UI Visual Structure

The minimum requirements are as follows.

* Left panel: library navigator

* Main panel: model editor with diagram, icon, documentation or code view

* Right panel:

  * Configuration tab, see :numref:`sec_configuration_widget`
  * Connections tab, see :numref:`sec_connect_ui_req`
  * Parameters tab, see :numref:`sec_parameters`

* Menu bar

* Bottom panel: console

The placement of the different UI elements may differ from the one proposed here above (especially the right panel tabs may be relocated into the left panel) but the user must have access to all those elements.

Ideally a toggle feature should be implemented to show or hide each side panel, either by user click if the panel is pinned or automatically.

Optionally a fully customizable workspace may be implemented.


.. _sec_functionalities:

Detailed Functionalities
------------------------

:numref:`tab_gui_func` provides a list of the functionalities that the software must support. Phase 1 refers to the configuration widget, phase 2 refers to the full-featured editor.

.. _tab_gui_func:

.. list-table:: Functionalities of the software -- R: required, P: required partially, O: optional, N: not required
   :widths: 30 10 10 50
   :header-rows: 1

   * - Feature
     - Phase 1
     - Phase 2
     - Comment

   * - **Main functionalities**
     -
     -
     - (as per :numref:`sec_general_description`)

   * - Diagram editor for Modelica models
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

   * - Variables tagging
     - N
     - R
     - See :numref:`sec_tagged_variables`.

   * - **I/O**
     -
     -
     -

   * - Load ``mo`` file
     - N
     - R
     - Simple Modelica model or full package ``Package.mo`` with recursive parsing

       If the model contains annotations specific to the configuration widget (see :numref:`sec_configuration_widget`), the corresponding data must be loaded in memory for further configuration.

       If the model contains the Modelica annotation ``uses`` the corresponding library must be loaded.

       If a package is loaded, the structure of the package and sub packages should be checked against *Chapter 13 Packages*.

   * - Export simulation results
     - N
     - R
     - Export in the following format: ``mat``, ``csv``.

       All variables or selection based on variable browser (see below).

   * - Variable browser
     - N
     - R
     - Selection of model variables based on regular expression (R)

       Or Brick/Haystack query :cite:`Brick` :cite:`Haystack4` (O)

   * - Plot simulation results
     - N
     - R
     - HTML plots of variables selected within the variable browser

       Pan, zoom and value display at hover must be available.

       The independent variable on the X-axis must be chosen by the user, with the time variable as default.

   * - Export documentation
     - R
     - R
     - Control points, sequence of operation description (based on CDL to Word translator developed by LBL), and equipment schematics see :numref:`sec_documentation_export`

   * - Import/Export data sheet
     - N
     - R
     - Additional module to

       1) generate a file in CSV or JSON format from the configuration data,

       2) populate the configuration data based on a file input in CSV or JSON format.


   * - **Modelica features**
     -
     -
     -

   * - Checking the compliance with Modelica specification
     - N
     - R
     - Real-time checking of syntax for component names

       Real-time checking of connections

   * - Translate model
     - N
     - R
     - The software settings allow the user to specify a command for translating the model with a third-party Modelica tool e.g. JModelica.

       The output of the translation routine is logged in LinkageJS console.

   * - Simulate model
     - N
     - R
     - The software settings allow the user to specify a command for simulating the model with a third-party Modelica tool, e.g., JModelica.

       The output of the simulation routine is logged in LinkageJS console.

   * - Automatic medium propagation between connected components
     - R
     - O
     - Only the configuration widget integrates this feature as a minimum requirement.

       When generating ``connect`` equations manually within the diagram editor, a similar approach as the *fluid path* used by the configuration widget may be developed, see components with four ports and two media.

   * - Support of Modelica graphical annotations
     - N
     - R
     -

   * - Modelica code editor
     - N
     - R
     - Raw text editor with linter and Modelica specification checking upon save

       Note that this functionality requires translation and reverse translation of JSON to Modelica (those translators are developed by LBL).

   * - Icon editor
     - N
     - R
     - Editing functionalities similar to diagram editor

   * - Documentation view
     - N
     - R
     - Rendering of the documentation section of the model annotation (HTML format)

   * - Library version management
     - R
     - R
     - If a loaded model contains the Modelica annotation ``uses`` (e.g., ``uses(Buildings(version="6.0.0")``) the software checks the version number of the stored library, prompts the user for update if the version number does not match, executes the conversion script per user request.

   * - Path discovery
     - R
     - R
     - A routine to reconstruct the path or URL of a referenced resource within the loaded Modelica libraries is required. Typically a resource can be referenced with the following syntax ``modelica://Buildings.Air.Systems.SingleZone.VAV``.

   * - **Object manipulation**
     -
     -
     -

   * - Vectorized instances
     - N
     - R
     - An array dimension descriptor appending the name of an object is interpreted as an array declaration. Further  connections to the connectors of that object must comply with the array structure.

   * - Expandable connectors
     - N
     - R
     -

   * - Navigation in object composition
     - N
     - R
     - Right clicking an icon in the diagram view offers the option to open the model in another tab

   * - Multiple objects selection for setting the value of common parameters
     - N
     - R
     - If several objects are selected only their common parameters are listed in the Parameters panel. If a parameter value is modified, all the selected objects will have their parameter value updated.

   * - Avoiding duplicate names
     - R
     - R
     - When instantiating a component or assigning a name through the configuration widget, if the default name is already used in the model the software automatically appends the name with the lowest integer value that would ensure uniqueness.

       When copying and pasting a set of objects connected together, the set of connect equations is updated to ensure  consistency with the appended object names.

   * - **Graphical features**
     -
     -
     - A user experience similar to modern web based diagramming applications is expected e.g. `draw.io <https:// w.draw.io>`_.

   * - Tab view
     - R
     - R
     - The UI is organized in tabs that can be manipulated, created and deleted typically as navigation tabs in a web browser.

   * - Diagram split view
     - N
     - R
     - The diagram view can be split (horizontally and vertically) into several views. Each tab can be dragged and dropped from one view to another. The views are synchronized so that if the same model is open in different views and gets modified, all the views of the model are updated to reflect the modifications.

   * - Copy/Paste objects
     - R
     - R
     - Copying and pasting a set of objects connected together copies the objects declarations and the corresponding connect  equations.

   * - Pan and zoom on mouse actions
     - N
     - R
     -

   * - Undo/Redo
     - R
     - R
     - Available through buttons and standard keyboard shortcuts

   * - Draw shape, text box
     - N
     - R
     -

   * - Start connection line when hovering connectors
     - N
     - R
     -

   * - Connection line jumps
     - N
     - R
     - Gap jump at crossing

   * - Customize connection lines
     - N
     - R
     - Color, width and line can be specified in the annotations panel

   * - Hover information
     - R
     - R
     - Class path when hovering an object in the diagram view and tooltip help for each GUI element

   * - Color and style of connection lines
     - N
     - R
     - Allow the user to manually specify (right click menu) the style of the connections lines.

       When generating a ``connect`` equation automatically select a line style based on some heuristic to be further specified.

   * - Drawing guides
     - N
     - R
     - Snap to grid and alignment lines with neighbor objects with the option to enable/disable those guides.

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


.. _sec_modelica_gui:

Modelica Graphical User Interface
---------------------------------

Modelica Language
*****************

The software must comply with the Modelica language specification :cite:`Modelica2017` for every aspect relating to (the chapter numbers refer to :cite:`Modelica2017`):

* validating the syntax of the user inputs: see *Chapter 2 Lexical Structure* and *Chapter 3 Operators and Expressions*,

* the connection between objects: see *Chapter 9 Connectors and Connections*,

* the structure of packages: see *Chapter 13 Packages*,

* the annotations: see *Chapter 18 Annotations*.


JSON Representation
*******************

LBL has already developed a `Modelica to JSON translator <https://lbl-srg.github.io/modelica-json/>`_.
This development includes the definition of two JSON schemas:

#. `Schema-modelica.json <https://lbl-srg.github.io/modelica-json/modelica.html>`_ validates the JSON files parsed from Modelica.

#. `Schema-CDL.json <https://lbl-srg.github.io/modelica-json/CDL.html>`_ validates the JSON files parsed from `CDL <http://obc.lbl.gov/specification/cdl>`_ (subset of Modelica language used for control sequence implementation).

Those developments should be leveraged to define a JSON-based native format for LinkageJS.


Connection Lines
****************

When drawing a connection line between two connector icons in the diagram view

* a ``connect`` equation with the references to the two connectors must be created,

* with a graphical annotation defining the connection path as an array of points and providing an optional smoothing function e.g. Bezier.

* When no smoothing function is specified the connection path must be rendered graphically as a set of segments.

* The array of points must be either:

  * created fully automatically when the next user's click after having started a connection is made on a connector icon. The function call ``create_new_path(connector1, connector2)`` creates the minimum number of *vertical or horizontal* segments to link the two connector icons with the constraint of avoiding overlaying any instantiated object,

  * created semi automatically based on the input points corresponding to the user clicks outside any connector icon: the function call ``create_new_path(point[i], point[i+1])`` is called to generate the path linking each pair of points together.

* The first and last couple of points must be so that the connection line does not overlap the component icon but rather grows the distance to it, see :numref:`linkage_connect_distance`.


.. figure:: img/linkage_connect_distance.*
   :name: linkage_connect_distance

   Logic for generating a connection line in the neighborhood of a connector


.. _sec_configuration_widget:

Configuration Widget
--------------------

Functionalities
***************

The configuration widget allows the user to generate a Modelica model of an HVAC system and its controls by filling up a simple input form.
It is mostly needed for integrating advanced control sequences that can have dozens of I/O variables.
The intent is to reduce the complexity to the mere definition of the system layout and the selection of standard control sequences already transcribed in Modelica :cite:`OBC`.

.. note::

   `CtrlSpecBuilder <https://www.ctrlspecbuilder.com/ctrlspecbuilder/home.do;jsessionid=4747144EA3E61E9B82B9E0B463FF2E5F>`_ is a tool widely used in the HVAC industry for specifying control systems. It may be used as a reference for the development in terms of user experience minimal functionalities. Note that this software does not provide any Modelica modeling functionality.

There are fundamental requirements regarding the Modelica model generated by the configuration widget:

1. It must be "graphically readable" (both within LinkageJS and within any third-party Modelica GUI e.g. Dymola): this is a strong constraint regarding the placement of the composing objects and the connections that must be generated automatically.

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


Equipment and controller models are connected together by means of a *control bus*, see :numref:`screen_schematics_modelica`. The upper-level Modelica model including the equipment and controls models is the ultimate output of the configuration widget: see :numref:`screen_conf_1` where the component named ``AHU_1_01_02`` represents an instance of the upper-level model ``AHU_1`` generated by the widget. That component exposes the outside fluid connectors as well as the top level control bus.

The logic for instantiating classes from the library is straightforward. Each field of the form specifies

* the reference of the class (library path) to be instantiated depending on the user input,

* the position of the component in simplified grid coordinates to be converted in diagram view coordinates.

:numref:`sec_fluid_connectors` and :numref:`sec_signal_connectors` address how the connections between the connectors of the different components are generated automatically based on this initial model structure.

.. _sec_data_model:

Data Model
**********

.. warning::

  This paragraph proposes a data model that may be used to support the configuration workflow. This part of the specification is not hard and fast, we are rather trying to illustrate a possible implementation path. Alternative approaches are welcome but they must at least provide the same level of functionalities as the proposed approach and meet the minimum requirements that are expressed.


The envisioned data structure supporting the configuration process consists in

* placement coordinates provided relatively to a simplified grid, see :numref:`grid` -- those must be mapped to Modelica diagram coordinates by the widget,

* an ``equipment`` section referencing the components that must be connected together with fluid connectors, see :numref:`sec_fluid_connectors`,

* a ``controls`` section referencing the components that must connected together with signal connectors, including schedules, set points, optimal start, etc., see :numref:`sec_signal_connectors`,

* a ``dependencies`` section referencing additional components with the following characteristics:

  * They typically correspond to sensors and outside fluid connectors.
  * The model completeness depends on their presence.
  * The requirements for their presence can be deduced from the equipment and controls options.
  * They do not need additional fields in the user form of the configuration widget.

Format
``````
A robust syntax is a minimum requirement for

* auto-referencing the data structure, for instance ``#type.value`` refers to the value of the field ``value`` of the object which ``$id`` is ``type``, and it must be interpreted by the configuration widget and replaced by the actual value when generating the model,

* conditional statements: potentially every field may require a conditional statement -- either data fields (e.g., the model to be instantiated and its placement) or UI fields (e.g., the condition to enable a widget itself or the different options of a menu widget).

Ideally the syntax should also allow iteration ``for`` loops to instantiate a given number (as parameter) of objects with an offset applied to the placement coordinates, for instance a chiller plant with ``n`` chillers. Backup strategy: define a maximum number of instances and enable only the first ``n`` ones based on a condition.

Possible formats:

* JSON: recommended format but expensive syntax especially for boolean conditions or auto-referencing the data structure: is there any standard syntax?

* Specific format to be defined in collaboration with the UI developer and depending on the selected UI framework


Parameters Exposed by the Configuration Widget
``````````````````````````````````````````````

The template developer must have the ability to declare in the template any parameter of the composing components e.g. ``V_flowSup_nominal`` and reference them in any declaration e.g. ``Buildings.Fluid.Movers.SpeedControlled_y(m_flow_nominal=(#air_supply.medium).rho_default / 3600 * #V_flowSup_nominal.value)``. The configuration widget must replace the referenced names by their actual values (literal or numerical). The user will be able to override those values in the parameters panel e.g. if he wants to specify a different nominal air flow rate for the heating or cooling coil. See additional requirements regarding the persistence of those references in :numref:`sec_persisting_data`.

Some parameters must be integrated in the template (examples below are provided in reference to ``Buildings.Controls.OBC.ASHRAE.G36_PR1.AHUs.MultiZone.VAV.Controller``)

* when they impact the model structure e.g. ``use_enthalpy`` requires an additional enthalpy sensor: in that case the model declaration must use the ``final`` qualifier to prevent the user from overriding those values in the parameters panel,

* when no default value is provided e.g. ``AFlo`` cf. requirement that the model generated by the configuration widget must be ready to simulate.


.. figure:: img/grid.png
   :name: grid

   Simplified grid providing placement coordinates for all objects to be instantiated when configuring an AHU model


Configuration Schema
````````````````````

A well documented schema must be developed, to support the development of the configuration files by third parties and the validation of the configuration data input by the user.

In the definitions provided here below

* when the type of a field is specified as a string marked with (C), it may correspond to

  * a conditional statement provided as a string that must be interpreted by the UI engine,

  * a reference to another field value of type boolean (that may itself correspond to a conditional statement provided as a string).

* references to other fields of the data structure may be of two kinds:

  * LinkageJS references prefixed by ``#`` which must be interpreted by the configuration widget and replaced by their actual value e.g. ``"declaration": "Modelica.Fluid.Interfaces.FluidPort_a (redeclare package Medium=#air_supply.medium)"`` for the object ``"$id": "id_value"`` leads to ``Modelica.Fluid.Interfaces.FluidPort_a id_value(redeclare package Medium=Buildings.Media.Air)`` in the generated model.

  * Modelica references provided as literal variables e.g. ``"declaration": "Buildings.Fluid.Movers.SpeedControlled_y (m_flow_nominal=m_flowRet_nominal)"`` for the object if ``"$id": "id_value"`` leads to ``Buildings.Fluid.Movers.SpeedControlled_y id_value(m_flow_nominal=m_flowRet_nominal)`` in the generated model.

* The syntax supporting those features shall be specified in collaboration with the UI developer. The syntax must support e.g. ``(#air_supply.medium).rho_default`` where the first dot is used to access the property ``medium`` of the configuration object with ``$id == #air_supply`` (which must be replaced by its value) while the second dot is used to access Modelica property ``rho_default`` of the class ``Medium`` (which must be kept literal).


.. _Configuration data:

**Definitions**

  ``type`` : object : required

    | Type of system to configure, e.g., air handling unit, chilled water plant.
    | Object defined as `elementary object`_.

    *required* : ``[$id, description, value]``

  ``subtype`` : object : required

    | Subtype of system, e.g., for an air handling unit: variable air volume or dedicated outdoor air.
    | Object defined as `elementary object`_.

    *required* : ``[$id, description, widget, value]``

  ``name`` : object : required

    | Name of the component. Must be stored in the Modelica annotation ``defaultComponentName``.
    | Object defined as `elementary object`_.

    *required* : ``[$id, description, widget, value]``

  ``fluid_paths`` : array : required

    *items* : object

    | Definition of all *main fluid paths* of the model, see :numref:`sec_heuristic`.
    | Object defined as follows.

    *required* : ``[$id, direction, medium]``

      ``$id`` : string : required

        Unique string identifier starting with ``#``.

      ``direction`` : string : required

        *enum* : ``["north", "south", "east", "west"]``

        Direction indicating the order in which the components must be connected along the path.

      ``medium`` : string : required

        Common medium for that fluid path and all derived paths, e.g., ``"Buildings.Media.Air"``

  ``icon`` : string : required

    Path to icon file.

  ``diagram`` : object : required

    Size of the diagram layout.

    Object defined as follows.

    ``configuration`` : array : required

      *items* : integer

      Array on length 2, providing the number of lines and columns of the simplified grid layout.

    ``model`` : array : required

      *items* : array

      Array on length 2 providing the coordinates tuples of two opposite corners of the diagram rectangular layout.

        *items* : integer

        Array on length 2 providing the coordinates of one corner of the diagram rectangular layout.

  ``equipment`` : array : optional

    *items* : object

    Object defined as `elementary object`_.

  ``controls`` : array : optional

    *items* : object

    Object defined as `elementary object`_.

  ``dependencies`` : array : optional

    *items* : object

    Object defined as `elementary object`_.

.. _elementary object:

**Elementary Object Definition**

  ``$id`` : string : required

    | Unique string identifier.
    | Used for referencing the object properties in other configuration objects: references are prefixed with ``#`` in the examples, e.g., ``#id_value.property``.
    | If the object has a ``declaration`` field, the name of the declared component is the value of ``$id``.
    | Must be suffixed with brackets e.g. ``[2]`` in case of array variables.

  ``description`` : string : required

    | Descriptive string.
    | If the object has a ``declaration`` field, the descriptive string appends the component declaration in the Modelica source file (referred to as *comment* in *§4.4.1 Syntax and Examples of Component Declarations* of :cite:`Modelica2017`).

  ``enabled`` : boolean, string (C) : optional, default ``true``

    Indicates if the object must be used or not. If not, the UI does not display the corresponding widget, no modification to the model is done and the object field ``value`` is assigned its default value.

  ``widget`` : object : optional

    Object defined as follows.

    ``type`` : string : required

      Type of UI widget.

    ``options`` : array : optional

      *items* : string

      Options to be displayed by certain widgets, e.g., dropdown menu.

    ``options.enabled`` : array : optional

      *items* : boolean, string (C)

      Indicates which option can be selected by the user. Must be the same size as ``widget.options``.

  ``value`` : string (C), number, boolean, null : required

    [*enum* : ``widget.options`` (if provided)]

    | Value of the object (default value prior to user input).
    | May be provided as a literal expression in which all literal references to object properties (prefixed with ``#``) must be replaced by their actual value.

  ``unit`` : string : optional

    Unit of the value. Must be displayed in the UI.

  ``declaration`` : array, string (C), null : optional

    [*items* : string (C)]

    Any valid Modelica declaration(*) (component or parameter) or an array of those that has the same size as ``widget.options`` if the latter is provided (in which case the elements of ``declaration`` get mapped with the elements of ``widget.options`` based on their indices).

    .. note::

       (*) The name of the instance is not included in the declaration but provided with the ``$id`` entry: it must be inserted between the class reference and the optional parameters of the instance (specified within parenthesis).

       If one option requires multiple declarations, the first one should typically be specified here and the other ones as dependencies.

  ``placement`` : array, string (C) : optional

    [*items* : array, integer]

      [*items* : integer]

    | Placement of the component icon provided in simplified grid coordinates ``[line, column]`` to be mapped with the model diagram coordinates.
    | Can be an array of arrays where the main array must have the same size as ``widget.options`` if the latter is provided (in which case the elements of ``placement`` get mapped with the elements of ``widget.options`` based on their indices).

  ``connect`` : object : optional

    | Data required to generate the connect equations involving the connectors of the component, see :numref:`sec_fluid_connectors`.
    | Object defined as follows.

    ``type`` : string : optional, default ``path``

      *enum* : ``["path", "tags", "explicit"]``

      Type of connection logic.

    ``value`` : string (C), object : required

      | If ``type == "path"``: fluid path (string) that must be used to generate the tags in case of two connectors only. It must not be used if the component has more than two connectors or a non standard connectors scheme (different from one instance of ``Modelica.Fluid.Interfaces.FluidPort_a`` and one instance of ``Modelica.Fluid.Interfaces.FluidPort_b``).
      | If ``type == "tags"``: object providing for each connector (referenced by its instance name) the tag to be applied.
      | If ``type == "explicit"``: object providing for each connector (referenced by instance name) the connector to be connected to, using explicit names e.g. ``fanSup.port_a``.

  ``annotation`` : array, string (C), null : optional

    [*items* : string (C)]

    Any valid Modelica annotation or an array of those which must have the same size as ``widget.options`` if the latter is provided (in which case the elements of ``annotation`` get mapped with the elements of ``widget.options`` based on their indices).

  ``protected`` : boolean : optional, default ``false``

    | Indicates if the declaration should be public or protected.
    | All protected declarations must be grouped together at the end of the declaration section in the Modelica model (to avoid multiple ``protected`` and ``public`` specifiers in the source file).

  ``symbol_path`` : string (C) : optional

    Path of the SVG file containing the engineering symbol of the component. This is needed for the schematics export functionality, see :numref:`sec_documentation_export`. That path is specified by the template developer and not in the class definition because the same class can be used to represent different equipment parts e.g. a flow resistance model can be used to represent either a filter (SVG symbol needed) or a duct section (no SVG symbol needed).

  ``icon_transformation`` : string (C) : optional

    Graphical transformation that must be applied to the component icon e.g. ``"flipHorizontal"``.


An example of the resulting data structure is provided in annex, see :numref:`sec_annex_json`.


.. _sec_persisting_data:

Persisting Data
```````````````

**Path of the Configuration File**

The path (relative to the library entry path, see *Path discovery* in :numref:`tab_gui_func`) must be stored in a hierarchical vendor annotation at the model level e.g. ``__Linkage(path="modelica://Buildings.Configuration.AHU")``.


**Configuration Objects**

The ``value`` of all objects must be stored with their ``$id`` in a serialized format within a hierarchical vendor annotation at the model level. (This is done at the model level since some configuration data may be linked to some model declarations indirectly using dependencies so annotations at the declaration level would not cover all use cases.)

This is especially needed so that the references to the configuration data in the object declarations persist when saving and loading a model. Unless specified as ``final`` those references may be overwritten by the user. When loading a model the configuration widget must parse the ``$id`` and ``value`` of the stored configuration data and reconstruct the corresponding model declarations using the configuration file (and interpreting the references prefixed by ``#``). Those declarations are compared to the ones present in the model: if they differ, the ones in the model take precedence.


**Engineering Symbol SVG File path**

The path (``symbol_path`` in `Configuration data`_) is stored in a vendor annotation at the declaration level e.g. ``annotation(__Linkage(symbol_path="value of symbol_path"))``.


.. _sec_fluid_connectors:

Fluid Connectors
****************

.. warning::

  This paragraph proposes an algorithm that may be used to support the generation of ``connect`` statements between fluid connectors. This part of the specification is not hard and fast, we are rather trying to illustrate a possible implementation path. Alternative approaches are welcome but they must at least provide the same level of functionalities as the proposed approach and meet the minimum requirements that are expressed.


The fluid connections (``connect`` equations involving two fluid connectors) is generated based on either:

* an explicit connection logic relying on one-to-one relationships between connectors (see :numref:`sec_explicit`) or,

* a heuristic connection logic (see :numref:`sec_heuristic`) based on:

  * the coordinates of the components in the diagram layout, i.e., after converting the coordinates provided relatively to the simplified grid,

  * a tag applied to the fluid connectors (or fluid ports) of the components.

.. _sec_explicit:

Explicit Connection Logic
``````````````````````````

In certain cases it may be convenient to specify explicitly a one-to-one connection scheme between the connectors of the model, for instance a differential pressure sensor to be connected with the outlet port of a fan model and a port of a fluid source providing the reference pressure.

That logic is activated at the component level by the keyword ``connect.type == "explicit"``.

The user provides for each connector the name of the component instance and connector instance to be connected to e.g. ``"port_1": "component1.connector2``.


.. _sec_heuristic:

Heuristic Connection Logic
``````````````````````````

That logic relies on connectors tagging which supports two modes.

1. Default mode (``connect.type == "path"`` or ``null``)

   * By default an instance of ``Modelica.Fluid.Interfaces.FluidPort_a`` (resp. ``Modelica.Fluid.Interfaces.FluidPort_b``) must be tagged with the suffix ``inlet`` (resp. ``outlet``).

   * The tag prefix is provided at the component level to specify the fluid path, for instance ``air_supply`` or ``air_return``.

   * The fluid connectors are then tagged by concatenating the previous strings, for instance ``air_supply_inlet`` or ``air_return_outlet``.

2. Detailed mode (``connect.type == "tags"``)

   * An additional mechanism is required to allow tagging each fluid port individually. Typically for a three way valve, the bypass port should be on a different fluid path than the inlet and outlet ports see :numref:`linkage_connect_3wv`. Hence we need a mapping dictionary at the connector level which, if provided, takes precedence on the default logic specified above.

   * Furthermore a fluid connector may be connected to more than one other fluid connector (fork configuration). To support that feature the concept of *derived path* is introduced: if ``fluid_path`` is the name of a fluid path, each fluid path named ``/^fluid_path_((?!_).)*$/gm`` is considered a *derived path*. The original (derived from) path is the *parent path*. A path with no parent path is referred to as *main path*.

     For instance in case of a three way valve the mapping dictionary may be:

     ``{"port_1": "hotwater_return_inlet", "port_2": "hotwater_return_outlet", "port_3": "hotwater_supply_bypass_inlet"}`` where ``hotwater_supply_bypass`` is a derived path from ``hotwater_supply``.

.. figure:: img/linkage_connect_3wv.*
   :name: linkage_connect_3wv

   Example of the connection scheme for a three-way valve. The first diagram does not include an explicit model of the fluid junction whereas the second does (and represents the highly recommended modeling approach). This example illustrates how the fluid connection logic allows for both modeling approaches. In the first case the bypass and direct branches are derived paths from ``fluid_path0`` which consists only in one connector. In the second case they are different main paths, the bypass branch having a different direction than the direct branch (the user could also use an "explicit" connection logic to avoid the definition of an additional main fluid path).

The conversion script throws an exception if an instantiated class has ``connect.type != "explicit"`` and some fluid ports that cannot be tagged nor connected with the previous logic e.g. non default names and no (or incomplete) mapping dictionary provided.
Once the tagging is resolved for all fluid connectors of the instantiated objects with ``connect.type != "explicit"``, the connector tags are stored in a list, furthered referred to as "tagged connectors list".
All object names in that list thus reference instantiated objects with fluid ports that have to be connected to each other.

To build the full connection set, the direction (north, south, east, west) along which the objects must be connected needs to be provided for all main (not derived) fluid paths.

.. note::

   The direction (as well as the fluid medium) of a derived path are inherited from the parent path.

   Modelica ``connect`` construct is symmetric so at first glance only the vertical / horizontal direction of a fluid path seems enough. However the actual orientation along the fluid path is needed in order to identify the start and end connectors, see below.

The connection logic is then as follows:

* List all the different fluid paths in the tagged connectors list as obtained by truncating ``_inlet`` and ``_outlet`` from each connector name. Get the direction of the main fluid paths in the configuration data and finally reconstruct the tree structure of the fluid paths based on their names:

  .. code-block::

     └── fluid_path0 (direction: east): [connectors list]
       ├── fluid_path0_0 (inherited direction: east): [connectors list]
       └── fluid_path0_1 (inherited direction: east): [connectors list]
         ├── fluid_path0_1_0 (inherited direction: east): [connectors list]
         └── fluid_path0_1_1 (inherited direction: east): [connectors list]
     ├── fluid_path1 (direction: west): [connectors list]
     ├── fluid_path3 (direction: north): [connectors list]
     └── fluid_path4 (direction: south): [connectors list]

* For each fluid path:

  * Order all the connectors in the connectors list according to the direction of the fluid path and based on the position of the corresponding *objects* (not connectors) with the constraint that for each object ``inlet`` has to be listed first and ``outlet`` last.

  * For each derived path find the start and end connectors as described hereunder and prepend / append the connectors list.

    * If the first (resp. last) connector in the ordered list is an outlet (resp. inlet), it is the start (resp. end) connector. (Note that the reciprocal is not true: a start port can be either an inlet or an outlet see :numref:`linkage_connect_multi`.)

    * Otherwise the start (resp. end) connector is the outlet (resp. inlet) connector of the object in the parent path placed immediately before (resp. after) the object corresponding to the first (resp. last) connector -- where before and after are relative to the direction and orientation of the fluid path (which are the same for the parent path).

  *  For each *parent path* split the path into several *sub paths* whenever a connector corresponds to the start or end port of a derived path.

  * Throw an exception if one of the following rules is not verified:

    * Derived paths must start *or* end with a connector from a parent path.
    * Each branch of a fork must be a derived path, it cannot belong to the parent path: so no object from the parent path can be positioned between the objects corresponding to the first and last connector of any derived path.

  * Generate the ``connect`` equations by iterating on the ordered list of connectors and generate the connection path and the corresponding graphical annotation. The only valid connection along a fluid path is ``outlet`` with ``inlet``.

  * Populate the ``iconTransformation`` annotation of each outside connector instantiated as a dependency so that, in the icon layer, they belong to the same border (top, left, bottom, right) as in the diagram layer and be evenly positioned considering the icon's dimensions. The bus connector is an exception and must always be positioned at the top center of the icon.

That logic implies that within the same fluid path, objects are connected in one given direction only: to represent a fluid loop (graphically) at least two fluid paths must be defined, typically ``supply`` and ``return``.

:numref:`linkage_connect_multi` to :numref:`linkage_connect_duct` further illustrate the connection logic on different test cases.

.. figure:: img/linkage_connect_multi.*
   :name: linkage_connect_multi

   Connection scheme with nested fluid junctions not modeled explicitly (using derived paths)

.. figure:: img/linkage_connect_multi_exp.*
   :name: linkage_connect_multi_exp

   Connection scheme with nested fluid junctions modeled explicitly (recommended modeling approach)

.. figure:: img/linkage_connect_duct.*
   :name: linkage_connect_duct

   Connection scheme with fluid branches with different directions e.g. VAV duct system. Here a flow splitter is used to start several main fluid paths with a vertical connection direction.


.. _sec_signal_connectors:

Signal Connectors
*****************

.. warning::

  This paragraph proposes an algorithm that may be used to support the generation of ``connect`` statements between signal (or block) connectors. This part of the specification is not hard and fast, we are rather trying to illustrate a possible implementation path. Alternative approaches are welcome but they must at least provide the same level of functionalities as the proposed approach and meet the minimum requirements that are expressed.


General Principles
``````````````````

Generating the ``connect`` equations for signal variables relies on:

* a (fuzzy) string matching principle applied to the names of the connector variables and their components e.g. ``com.y`` for the output connector ``y`` of the component ``com``,

* a so-called *control bus* which has the type of an *expandable connector*, see *§9.1.3 Expandable Connectors* in :cite:`Modelica2017`.

The following features of the expandable connectors are leveraged. They are illustrated with minimal examples in annex, see :numref:`sec_annex_bus_example`.

#. All components in an expandable connector are seen as connector instances even if they are not declared as such. In comparison to a non expandable connector, that means that each variable (even of type ``Real``) can be connected i.e. be part of a ``connect`` equation.

   .. note::

      Connecting a non connector variable to a connector variable with ``connect(non_connector_var, connector_var)`` yields a warning but not an error in Dymola. It is considered bad practice though and a standard equation should be used in place ``non_connector_var = connector_var``.

      Using a ``connect`` equation allows to draw a connection line which makes the model structure explicit to the user. Furthermore it avoids mixing ``connect`` equations and standard equations within the same equation set, which has been adopted as a best practice in the Modelica Buildings library.

#. The causality (input or output) of each variable inside an expandable connector is not predefined but rather set by the ``connect`` equation where the variable is first being used. For instance when the variable of an expandable connector is first connected to an inside connector ``Modelica.Blocks.Interfaces.RealOutput`` it gets the same causality i.e. output. The same variable can then be connected to another inside connector  ``Modelica.Blocks.Interfaces.RealInput``.

#. Potentially present but not connected variables are eventually considered as undefined i.e. a tool may remove them or set them to the default value (Dymola treat them as not declared: they are not listed in ``dsin.txt``): all variables need not be connected so the control bus does not have to be reconfigured depending on the model structure.

#. The variables set of a class of type expandable connector is augmented whenever a new variable gets connected to any *instance* of the class. Though that feature is not needed by the configuration widget (we will have a predefined control bus with declared variables), it is needed to allow the user further modifying the control sequence. Adding new control variables is simply done by connecting them to the control bus.

#. Expandable connectors can be used in arrays, as any other Modelica type. A typical use case is the connection of control input signals from a set of terminal units to a supervisory controller at the AHU or at the plant level. This use case has been validated on minimal examples in :numref:`sec_annex_bus_array`.


Generating Connections by Approximate String Matching
`````````````````````````````````````````````````````

.. note::

   The module implementing the string matching algorithm will be developed by LBL.


To support automatic connections of signal variables a predefined control bus will be defined for each type of system (e.g. AHU, CHW plant) with a set of predeclared variables. The names of the variables must allow a one-to-one correspondence between:

* the control sequence input variables and the outputs of the equipment model e.g. sensed quantities and actuators returned positions,

* the control sequence output variables and the inputs of the equipment model e.g. actuators commanded positions.

Thus the control bus variables are used as "gateways" to stream values between the controlled system and the controller system.

However an exact string matching is not conceivable. An approximate (or fuzzy) string matching algorithm must be used instead. Such an algorithm has been tested in the case of an advanced control sequence implementation in CDL (``Buildings.Controls.OBC.ASHRAE.G36_PR1.AHUs.MultiZone.VAV.Controller``): see :numref:`code_string_match` and results in :numref:`fig_string_match`. The main conclusions of that test are the following:

* Strict naming conventions solve most of the mismatch cases with a satisfying confidence (end score > 60).

* There is still a need to specify a convention to determine which array element should be connected to a scalar variable.

* There is one remaining mismatch (``busAhu.TZonHeaSet``) for which a logic consisting in using only the variable name if it is descriptive enough (test on length of suffix of standard variables names) and the initial matching score is low (below 50).


.. code-block:: python
   :caption: Example of a Python function used for fuzzy string matching
   :name: code_string_match

    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    import itertools as it
    import re


    def return_best(string, choices, sys_type='Ahu'):
        # Constrain array to array and scalar (or array element) to scalar.
        # Need to specify a logic for tagging scalar variables that should be connected to array elements e.g. '*_zon*.y'.
        # But allow a single array element to be connected to a scalar variable: not bool(re.search('\[\d+\]', string))
        if bool(re.search('\[.+\]|_zon.*\.', string)) and not bool(re.search('\[\d+\]', string)):
            choices = [el for el in choices if re.search('\[.+\]', el)]
            # Replace [.*] by [:]
            string = re.sub('\[.*\]', '[:]', string, flags=re.I)
            string = re.sub('_zon.*\.', '[:].', string, flags=re.I)
        else:
            choices = [el for el in choices if not re.search('\[.+\]', el)]

        # Replace pre by p and tem by t.
        string = re.sub('pre', 'P', string, flags=re.I)
        string = re.sub('tem', 'T', string, flags=re.I)

        # Do not consider controller and bus component names.
        # Remark: has only little impact.
        string = re.sub('^(con|bus){}\.'.format(sys_type), '', string)
        choices = [re.sub('^(con|bus){}\.'.format(sys_type), '', c) for c in choices]

        # Perform comparison.
        res = process.extract(string, choices, limit=2, scorer=fuzz.token_sort_ratio)

        return list(it.chain(*res))


.. raw:: html
   :file: _static/string_match.html

.. raw:: html

   <span style="display:block; margin-bottom:-20px;"></span>

.. figure:: img/string_match.*
   :name: fig_string_match

   Fuzzy string matching test case -- G36 VAV AHU Controller.
   ``match`` (resp. ``match_to``) is the bus variable with the highest matching score when compared to ``Controller variable`` (resp. ``Variable to connect to``). ``score`` (resp. ``score_to``) is the corresponding matching score and 	``sec_score`` (resp. ``sec_score_to``) is the second highest score. Variables highlighted in red show when the algorithm fails. Rows highlighted in grey show the effect of renaming the variables based on strict naming conventions e.g. quantity first with standard abbreviation, etc.


Validation and Additional Requirements
``````````````````````````````````````

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

   Providing an explicit indices range e.g. ``[1:numZon]`` like in the previous code snippet only causes a translation warning: Dymola seems to allocate a default dimension of **20** to the connector, the unused indices (from 3 to 20 in the example hereunder) are then removed from the simulation problem since they are not used in the model.

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
   The same logic as JModelica for array variables connections to expandable connectors is required for LinkageJS.


.. _sec_connect_ui_req:

Additional Requirements for the UI
``````````````````````````````````

Based on the previous validation case, :numref:`dymola_bus` presents the Dymola pop-up window displayed when connecting the sub-bus of input control variables to the main control bus.
A similar view of the connections set must be implemented with the additional requirements listed below. That view is displayed in the connections tab of the right panel.


.. figure:: img/dymola_bus.png
   :name: dymola_bus

   Dymola pop-up window when connecting the sub-bus of input control variables (left) to the main control bus (right) -- case of outside connectors


The variables listed immediately after the bus name are either

* *declared variables* that are not connected, for instance ``ahuBus.yTest`` (declared as ``Real`` in the bus definition): those variables are only *potentially present* and eventually considered as *undefined* when translating the model (treated by Dymola as if they were never declared) or,

* *present variables* i.e. variables that appear in a connect equation, for instance ``ahuSubBusI.TZonHeaSet``: the icon next to each variable then indicates the causality. Those variables can originally be either declared variables or variables elaborated by the augmentation process for *that instance* of the expandable connector i.e. variables that are declared in another component and connected to the connector's instance.

The variables listed under ``Add variable`` are the remaining *potentially present variables* (in addition to the declared but not connected variables). Those variables are elaborated by the augmentation process for *all instances* of the expandable connector, however they are not connected in that instance of the connector.

In addition to Dymola's features for handling the bus connections, LinkageJS requires the following.

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

  * | Another issue is illustrated :numref:`bus_inside` where the connection to the bus is now made from an outside component for which the bus is considered as an inside connector. Here Dymola only displays declared variables of the bus (but not of the sub-bus) but without the causality information and even if it is only potentially present (not connected). Present variables of the bus or sub-bus which are not declared are not displayed. Contrary to Dymola, LinkageJS requires that the "expanded" connection set of an expandable connector be exposed, independently from the level of composition. That means exposing all the variables of the *augmentation set* as defined in :cite:`Modelica2017` *9.1.3 Expandable Connectors*. In our example the same information displayed in :numref:`subbus_outside` for the original sub-bus should be accessible when displaying the connection set of ``bus.ahuI`` whatever the current status (inside or outside) of the connector ``bus``. A typical view of the connection set of expandable connectors for LinkageJS could be:

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
******************************

In principle the configuration widget as specified previously should allow building custom control sequences based on elementary control blocks (e.g. from the `CDL Library <https://github.com/lbl-srg/modelica-buildings/tree/master/Buildings/Controls/OBC/CDL>`_) and automatically generating connections between those blocks. However

* this would require to distinguish between low-level control blocks (e.g. ``Buildings.Controls.OBC.CDL.Continuous.LimPID``) composing a system controller -- which must be connected with direct connect equations and not with expandable connectors variables that are not part of the CDL specification -- and high-level control blocks (e.g. ``Buildings.Controls.OBC.ASHRAE.G36_PR1.AHUs.MultiZone.VAV.Controller``) -- which can be connected to other high-level controllers (e.g. ``Buildings.Controls.OBC.ASHRAE.G36_PR1.TerminalUnits.Controller``) using expandable connectors variables (the CDL translation will be done for each high-level controller individually),

* the complexity of some sequences makes it hard to validate the reliability of such an approach without extensive testing.

Therefore in practice, and at least for the first version of LinkageJS, it has been decided to rely on pre-assembled high-level control blocks. For each system type (e.g., AHU) one (or a very limited number) of control block(s) should be instantiated by the configuration widget for which the connections can be generated using expandable connectors as described before.

The example of the configuration file for a VAV system in :numref:`sec_annex_json` illustrates that use case.


.. _sec_parameters:

Parameters Setting
------------------

The parameters tab must expose the parameters of the objects selected in the diagram view, except if the parameters are declared as *protected* or have a *final* modifier. The name, unit and comment (description string) from the parameter declaration must be displayed.

Multiple Selection
******************

When multiple objects are selected in the diagram view the parameters tab must expose only common parameters (the intersection of the multiple parameters sets). The dimensionality of the parameters is not updated e.g. if the user selects an instance ``comp`` of the class ``Component`` and an instance ``obj`` of the class ``Object`` where both classes declare  a ``Real`` scalar parameter ``par`` (dimensionality 0) then the parameters tab must display an input field for ``par`` (dimensionality 0) and the user input will be used to assign the same value to ``par`` in both instances.

Array Selection
***************

When an array of instances is selected the parameters tab must update the dimensionality of each parameter e.g. if the user selects an array ``comp[n]`` of instances of the class ``Component`` which declares a ``Real`` scalar parameter ``parSca`` (dimensionality 0) and a ``Real`` array parameter ``parArr[m]`` (dimensionality 1) then the parameters tab must display input fields for ``parSca[n]`` (dimensionality 1) and ``parArr[m][n]`` (dimensionality 2).


Enumeration and Boolean
***********************

For parameters of type *enumeration* or *Boolean* a dropdown menu should be displayed in the parameters tab and populated by the enumeration items or ``true`` and ``false``.


Record
******

The parameters tab must allow exploring the inner structure of a parameter *record* and setting the lower level parameters values.


Grouped Parameters
******************

A declaration annotation may be used by the model developer to specify how parameters should be divided up in different *tabs* and *groups* e.g. ``annotation(Dialog(tab="General", group="Nominal condition"))``. The parameters tab must reflect that structure.


Validation
**********

Values entered by the user must be validated *upon submit* against Modelica language specification :cite:`Modelica2017` and parameter attributes e.g. ``min``, ``max``. (The sizes of array dimensions may be validated at run-time only by the simulation tool.)

A color code is required to identify the fields with incorrect values and the corresponding error message must be displayed on hover.


.. _sec_documentation_export:

Documentation Export
--------------------

The documentation export encompasses three items.

#. Engineering schematics of the equipment including the controls points

#. Control points list

#. Control sequence description

The composition level at which the functionality will typically be used is the same as the one considered for the configuration widget, for instance primary plant, air handling unit, terminal unit, etc. No specific mechanism to guard against an export call at different levels is required.

:numref:`screen_schematics_modelica` provides the typical diagram view of the Modelica model generated by the configuration widget and :numref:`screen_schematics_output` mocks up the corresponding documentation that must be exported. The documentation export may consist in three different files but must contain all the material described in the following paragraphs.


.. figure:: img/screen_schematics_modelica.*
   :name: screen_schematics_modelica

   Diagram view of the Modelica model generated by the configuration widget

.. figure:: img/screen_schematics_output.*
   :name: screen_schematics_output

   Mockup of the documentation export


Engineering Schematics
**********************

Objects of the original model to be included in the schematics export must have a declaration annotation providing the SVG file path for the corresponding engineering symbol e.g. ``annotation(__Linkage(symbol_path="value of symbol_path"))``. That annotation may be

* specified in the configuration file, see ``symbol_path`` in `Configuration data`_,
* specified manually by the user for potentially any instantiated component.

.. note::

   It is expected that LinkageJS will eventually be used to generate design documents included in the invitation to tender for HVAC control systems. The exported schematics should meet the industry standards and they must allow for further editing in CAD softwares, e.g., AutoCAD®.

   Due to geometry discrepancies between Modelica icons and engineering symbols a perfect alignment of the latter is not expected by simply mapping the diagram coordinates of the former to the SVG layout. A mechanism should be developed to automatically correct small alignment defaults.

For the exported objects

* the connectors connected to the control input and output sub-buses must be split into two groups depending on their type -- boolean or numeric,
* an index tag is then generated based on the object position, from top to bottom and left to right,
* eventually connection lines are drawn to link those tags to the four different control points buses (AI, AO, DI, DO). The line must be vertical, with an optional horizontal offset from the index tag to avoid overlapping any other object.

SVG is the required output format.

See :numref:`screen_schematics_output` for the typical output of the schematics export process.


Control Points List
**********************************

Generating the control points list is done by calling a module developed by LBL (ongoing development) which returns an HTML or Word document.


Control Sequence Description
**********************************

Generating the control sequence description is done by calling a `module developed by LBL <https://lbl-srg.github.io/modelica-json/>`_ which returns an HTML or Word document.


.. _sec_tagged_variables:

Working with Tagged Variables
-----------------------------

The requirements for tagging variables (based on :cite:`Brick` or :cite:`Haystack4`) and performing some queries on the set of tagged variables will be specified by LBL in a later version of this document.

Those additional requirements should at least address the following typical use cases.

* Setting parameters values with OpenStudio measures, for instance e.g. nominal electrical loads or boiler efficiency

* Plotting variables selected by a description string, for instance "indoor air temperature for all zones of the first floor"

* Mapping with equipment characteristics and sizing from data sheets or equipment schedules

An algorithm based on the variable names (similar to the one proposed for generating automatic connections for signal variables, see :numref:`sec_signal_connectors`) is envisioned.


OpenStudio Integration
----------------------

LinkageJS must eventually be integrated as a specific *tab* in the `OpenStudio <https://nrel.github.io/OpenStudio-user-documentation/>`_ (OS) modeling platform. This will provide editing capabilities of HVAC equipment and control systems models in the future `Spawn of EnergyPlus <https://lbl-srg.github.io/soep/>`_ (SOEP) workflow. (In the current EnergyPlus workflow those capabilities are provided by the `HVAC Systems tab <https://nrel.github.io/OpenStudio-user-documentation/tutorials/creating_your_model/#air-plant-and-zone-hvac-systems>`_.)

In SOEP workflow a multi-zone building model (EnergyPlus input file ``idf``) is configured within OpenStudio. The OpenStudio model ``osm`` exposes functions to access ``idf`` parameters e.g. zone names and characteristics. Modelica classes are created by extending the SOEP zone model and referencing the ``idf`` file and the zone names. Instances of those classes allow the user to select the thermal zone (as an item of an enumeration) and connect its fluid ports to the HVAC system model that is edited with LinkageJS.

The only requirement to embed in OS app is for LinkageJS to be built down to a single page HTML document.

An API must also be developed to access LinkageJS functionalities and data model in a programmatic way. The preferred language is Python (largely used in the Modelica users' community) or Ruby (largely used in the OpenStudio users' community).

Iterations between the UI developer, NREL (OpenStudio developer) and LBL will be required to

* devise the read and write access to the local file system, for instance by means of OS API (functions to be developed by LBL or NREL),

* specify LinkageJS API (to be developed by the UI developer).

This is illustrated in :numref:`linkage_architecture_os`.


Interface with URBANopt GeoJSON
-------------------------------

A seamless integration of LinkageJS in `URBANopt <https://www.nrel.gov/buildings/urbanopt.html>`_ modeling workflow is required. To support that feature additional requirements will be specified by LBL in a later version of this document.

The URBANopt-Modelica project has adopted the Modelica language to interface the upstream UI-GeoJSON workflow and the downstream Modelica-LinkageJS workflow. Therefore the requirements should only relate to the persistence of modeling data and the shared resources between the two processes.


Licensing
---------

The software is developed under funding from the U.S. Department of Energy and the U.S. Government consequently retains certain rights. As such, the U.S. Government has been granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software to reproduce, distribute copies to the public, prepare derivative works, and perform publicly and display publicly, and to permit other to do so.

The main software components built as part of this development project must be open sourced, e.g., under BSD 3 or 4-clause, with possible additions to make it easy to accept improvements.

Different licensing options are then envisioned depending on the integration target and the engagement of third-party developers and distributors. The minimum requirement is that at least one integration target be made available as a free software.

* Desktop app

  Subscription-based

* Standalone web app

  * Free account allowing access to Modelica libraries preloaded by default, for instance Modelica Standard and Buildings: the user can only upload and download single Modelica files (not a package).

  * Pro account allowing access to server storage of Modelica files (packages uploaded and models saved by the user): the user can update the stored libraries and reopen saved models between sessions.

* Third-party application embedding

  Licensing will depend on the application distribution model.

  For OpenStudio there is currently a shift in the `licensing strategy <https://www.openstudio.net/new-future-for-openstudio-application>`_. The specification will be updated to comply with the distribution options after the transition period (no entity has yet announced specific plans to continue support for the OS app).

