.. _sec_requirements:

############
Requirements
############

.. _sec_general_description:

*******************
General Description
*******************

Main Requirements
==================

The following requirements apply to both the configuration widget (Phase 1 of the development) and the diagram editor (future phase of the development).

* The software must rely on client side JS code with minimal dependencies and must be built down to a single page HTML document (SPA).

* A widget structure is required that allows seamless embedding into:

  * a desktop app—with standard access to the local file system,

  * a standalone web app—with access to the local file system limited to Download & Upload functions of the web browser (potentially with an additional sandbox file system to secure backup in case the app enters an unknown state),

  * any third-party application with the suitable framework to serve a single page HTML document executing JS code—with access to the local file system through the API of the third-party application:

    * For the first development phase pertaining to the configuration widget, the third-party application for the widget integration is an existing graphical editor for Modelica.
      To demonstrate the feasibility of this integration, a proof of concept shall be developed, together with the documentation describing how this workflow can be accomplished.
      This will include the creation of a prototype where the host application may be an actual Modelica editor or a rudimentary emulator of such.

    * For the second development phase, the primary integration target is `OpenStudio® <https://www.openstudio.net>`_ (OS) while the widget to be integrated is now the full-featured editor (including the configuration widget).
      An example of a JS application embedded in OS is `FloorspaceJS <https://nrel.github.io/OpenStudio-user-documentation/reference/geometry_editor>`_. The standalone SPA lives here: `https://nrel.github.io/floorspace.js <https://nrel.github.io/floorspace.js>`_. FloorspaceJS may be considered as a reference for the development.

.. admonition:: Revision Note
  :class: danger

  The following part is modified to make it clearer that the execution of the Modelica to JSON translator must be handled by the configuration widget.

* The core components parsing and generating Modelica classes must rely on JSON-formatted Modelica.
  For this purpose, LBL has developed a `Modelica to JSON translator <https://lbl-srg.github.io/modelica-json/>`_, based on the definition of two JSON schemas:

  * `Schema-modelica.json <https://lbl-srg.github.io/modelica-json/modelica.html>`_ validates the JSON files parsed from Modelica.

  * `Schema-CDL.json <https://lbl-srg.github.io/modelica-json/CDL.html>`_ validates the JSON files parsed from `CDL <http://obc.lbl.gov/specification/cdl>`_ (subset of Modelica language used for control sequence implementation).

  The software should call the Modelica to JSON translator for interfacing with native Modelica code.


Software Compatibility
======================

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
===================

A responsive design is required.

.. admonition:: Revision Note
  :class: danger

  The following part is modified to add the library navigator into the scope. See also :numref:`sec_class_workflow`.


A mockup of the UI for the full-featured editor is presented :numref:`screen_mockup`.
For Phase 1, only the graphical features pertaining to the configuration widget in the right panel and the library navigator in the left panel (see :numref:`sec_class_workflow`) should be considered.

.. figure:: img/screen_mockup.*
  :name: screen_mockup

  UI Visual Structure


.. _sec_functionalities:

**************************
High-Level Functionalities
**************************

The configuration widget allows the user to generate a Modelica model of an HVAC system and its controls by filling up a simple input form.

.. note::

   `CtrlSpecBuilder <https://www.ctrlspecbuilder.com/ctrlspecbuilder/home.do;jsessionid=4747144EA3E61E9B82B9E0B463FF2E5F>`_ is a tool widely used in the HVAC industry for specifying control systems. It may be used as a reference for the development in terms of user experience minimal functionalities. Note that this software does not provide any Modelica modeling functionality.

The implementation of control sequences must comply with OpenBuildingControl requirements, see *§7 Control Description Language* and *§8 Code Generation* in :cite:`OBC`. Especially:

* It is required that the CDL part of the model can be programmatically isolated from the rest of the model in order to be translated into vendor-specific code (by means of a third-party translator).

* The expandable connectors (control bus) are not part of CDL specification. Those are used to connect

  * control blocks and equipment models within a composed sub-system model, e.g., AHU or terminal unit,

  * different sub-system models together to compose a whole system model, e.g., VAV system serving different rooms.

  This is consistent with OpenBuildingControl requirement to provide control sequence specification at the equipment level only (controller programming), not for system level applications (system programming).


:numref:`tab_gui_func` provides a list of the functionalities that the software must support. Phase 1 refers to the configuration widget, future work refers to the full-featured editor and is provided for informative purposes only.

.. admonition:: Revision Note
  :class: danger

  The requirement for automatic medium propagation between connected components is removed.
  The requirement for executing the conversion scripts is removed.

.. _tab_gui_func:

.. list-table:: Functionalities of the software -- R: required, P: required partially, O: optional, N: not required
  :widths: 30 10 10 50
  :header-rows: 1
  :class: longtable

  * - Feature
    - Phase 1
    - Future
    - Comment

  * - **Main functionalities**
    -
    -
    - See :numref:`sec_general_description` for reference.

  * - Diagram editor for Modelica classes
    - N
    - R
    - In the first phase, the configuration widget must be integrated into an existing diagram editor for Modelica, but only as a proof a concept of such an integration. Such an editor must be developed in the second phase.

  * - Configuration widget
    - R
    - R
    -

  * - **I/O**
    -
    -
    -

  * - Modelica export
    - R
    - R
    - See :numref:`sec_modelica_export`

  * - Documentation export
    - R
    - R
    - Control points, sequence of operation description (based on CDL to Word translator developed by LBL), and equipment schematic see :numref:`sec_documentation_export`

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
    - P
    - R
    - If a loaded class contains the Modelica annotation ``uses`` (e.g., ``uses(Buildings(version="6.0.0")``) the software checks the version number of the stored library. If the version number does not match, the tool simply alerts the user of version incompatibility.

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


*************************
Modelica-Based Templating
*************************

.. admonition:: Revision Note
  :class: danger

  This paragraph is added. It replaces the former paragraph *Configuration Widget*.


The templates used by the configuration widget will be developed in Modelica.

A prototype of a template for an air handling unit is available in the feature branch ``issue1374_templateVAV`` of `Modelica Buildings Library <https://github.com/lbl-srg/modelica-buildings>`_ within the package ``Buildings.Experimental.Templates.AHUs``.

To support the use of Modelica, the software must comply with the language specification :cite:`Modelica2017` for every aspect pertaining to (the chapter numbers refer to :cite:`Modelica2017`):

* validating the syntax of the user inputs: see *Chapter 2 Lexical Structure* and *Chapter 3 Operators and Expressions*,

  * In Phase 1, only literals, operations with literals and arrays constructors with literals need to be supported.

* the class names: see *Chapter 5 Scoping, Name Lookup, and Flattening*,

  * In Phase 1, short class names may be used in the templates and must be supported.

* the structure of packages: see *Chapter 13 Packages*,

  * In Phase 1, the tool generates a package ``UserProject`` which structure must comply with the specification.

* the annotations: see *Chapter 18 Annotations*.

  * In Phase 1, this is required since the UI relies on the annotations specified in :numref:`sec_dialog_annotations` and :numref:`sec_vendor_annotations`.

Furthermore, in a control specification workflow only a subset of all the user inputs of a Modelica model are needed. For instance the type of medium, the nominal values of physical quantities, various modeling assumptions, etc. are only needed in the modeling and simulation workflow.
Therefore, the configuration widget must include a mechanism to select the subset of user inputs that must be exposed in the UI.
For this purpose a vendor-specific annotation should be used, see :numref:`sec_vendor_annotations`.

Eventually, the core components developed in Phase 1 must be reusable for the development of a full-featured parameter dialog widget in Phase 2, with the ability to switch between a control specification mode—with only a subset of the user inputs being exposed—and a modeling and simulation workflow—with the complete set of the user inputs being exposed.


Input Fields
============

Each input field described in this paragraph must be rendered in the UI with the description string provided at the declaration level.
Optionally a software setting parameter (accessible to the user) should enable hiding the instance name, which is not needed in the control specification workflow.

`TODO: Flesh out the requirement for highlighting missing parameter values (no default) or best-guess (or default?) values that need to be further specified (based on user selection?). How the latter is supported since a declaration annotation cannot be added/modified when redeclaring the enclosing class? Maybe through a class annotation referencing the instance name?`


Validation
----------

Values entered by the user must be validated *upon submit* against the Modelica language specification :cite:`Modelica2017`—syntax and type check, with an additional dimension check for arrays—and parameter attributes such as ``min`` and ``max``. In Phase 1, only literals, operations with literals and arrays constructors with literals need to be supported.

A color code may be used to identify the fields with incorrect values that will be discarded upon save, and the corresponding error message may be displayed on hover.

`TODO: Specify how manual edits of the control description can be added by the user.` For instance, store them in a ``String`` variable for each part (such as supply temperature control, duct pressure control, etc.) of the control block, with a specific annotation so that they are highlighted in the generated documentation.

Variables
---------

Each variable declared as a parameter without a ``final`` modifier must have a corresponding input field in the UI.

If the variable has the type Boolean a dropdown menu must be used and populated with ``true``, ``false`` and ``Unspecified`` (no default). The latter option may be simply rendered as blank.

If the variable has the type of an enumeration a dropdown menu must be used.
The dropdown menu must display the description string of each enumeration element and fallback to the name of each element. In addition an ``Unspecified`` (no default) option must be included, which may be simply rendered as blank.

If the variable is an array, a minimum requirement is that its value can be input using any array constructor specified in :cite:`Modelica2017`.
Optionally a tailored input field for arrays may be made available *in addition*, for instance to allow the input of each array element within a cell of a table.
However, the previous input logic based on a literal array constructor must always be available.


Record Type
-----------

All the declarations within a parameter of type record, and recursively of all the enclosed record parameters, must have a corresponding input field in the UI.
An indentation may be used to show the different levels of composition.


Replaceable Keyword
-------------------

Each declaration with the keyword ``replaceable`` and a choices annotation—either from the Modelica specification or a vendor-specific annotation, see :numref:`sec_vendor_annotations`—must have a corresponding dropdown menu in the UI.
See :numref:`tab_param_dialog` for additional requirements for how to populate the dropdown menu.

In addition, if the declaration corresponds to the instantiation of a model, a block, or a record, the previous logic must be applied recursively at each level of composition.
An indentation may be used to show the different levels of composition.

Note that each variable may potentially be declared as replaceable. So the dropdown menu logic shall be not exclusive of the input field logic. Typically a user may specify the type through the dropdown menu and enter the value through the input field.


Final Keyword
-------------

The ``final`` prefix must result in no item being rendered in the UI for the corresponding declaration.


.. _sec_dialog_annotations:

Parameter Dialog Annotations
============================

The UI of the configuration widget must comply with the specification of the *parameter dialog annotations* from :cite:`Modelica2017` §18.7.
:numref:`tab_param_dialog` specifies how each feature of this part of the Modelica specification must be addressed.

.. _tab_param_dialog:

.. list-table:: Parameter dialog annotations
   :widths: 30 70
   :header-rows: 1

   * - Feature
     - Comment

   * - **Modelica annotations for the GUI**
     - See :cite:`Modelica2017` §18.7 for reference.

   * - ``Dialog(tab|group)``
     - The UI must render the structure in groups and tabs as specified by this annotation. The groups may be collapsible with a button to expand or collapse all the groups.

   * - ``Dialog(enable)``
     - ``Dialog(enable=false)`` must result in no item being rendered in the UI for the corresponding declaration—as opposed to being only greyed out but still visible in Dymola.

   * - ``Dialog(showStartAttribute)``
     - The configuration widget should not display the input for the start value of a variable, this is not required in Phase 1.

   * - ``Dialog(colorSelector)``
     - This is not required in Phase 1.

   * - ``Dialog(loadSelector|saveSelector)`` and ``Selector(filter|caption)``
     - A mechanism to display a file dialog to select a file is required. The ``filter`` and ``caption`` attributes must also be interpreted as specified in :cite:`Modelica2017`.


   * - **Annotation Choices for Modifications and Redeclarations**
     - See :cite:`Modelica2017` §18.11 and §7.3.4 for reference.

   * - ``choicesAllMatching``
     - A discovery mechanism is required to enumerate all class subtypes (where subtyping is possible through multiple inheritances or nested function calls to a class constructor, such as ``class A = B(...);``) given a constraining class. The enumeration must display the description string of the class and fallback to the simple name of the class. Once a selection is made by the user, the UI must display the description string of the redeclared class (as opposed to the literal redeclare statement in Dymola), with the same fallback logic as before.

       In Phase 1, this discovery mechanism will be implemented in the Modelica to JSON translator that will convert the ``choicesAllMatching`` annotation into a ``choices(choice)`` annotation when a specific flag is set to true. (Note that the tool in Phase 1 is an application tool, not a development tool: it works with static libraries that cannot be edited. So the list of allowable classes may be precomputed.)

   * - ``choices(choice)``
     - The enumeration must display the description string provided within each inner ``choice`` and fallback to the description string of the redeclared class, and ultimately fallback to the simple name of the redeclared class. Once a selection is made by the user, the UI must display the description string of the redeclared class (as opposed to the literal redeclare statement in Dymola), with the same fallback logic as before.


.. _sec_vendor_annotations:

Vendor-Specific Annotations
===========================

Some vendor-specific annotations are required to facilitate the use of the templates.
Those annotations are specified below using the lexical conventions from :cite:`Modelica2017` Appendix B.1.

Note that some annotations require to interpret some redeclare statements prior to compile time, in order to "visit" the redeclared classes and evaluate clauses like ``coiCoo.typHex <> Types.HeatExchanger.None``—which Dymola does not support, see for instance ``annotation(Dialog(enable=typHex<>Types.HeatExchanger.None))`` which has no effect.
The UI must dynamically evaluate such clauses and update the parameter dialog accordingly.


Declaration Annotation
----------------------

Each declaration may have a hierarchical vendor-specific annotation ``"__Linkage" class-modification`` that must be interpreted, with the following possible attributes.

``"choicesConditional" "(" [ "condition" "=" logical-expression "," choices-annotation ] { "," "condition" "=" logical-expression "," choices-annotation } ")"``

  Description: This annotation enables specifying a Modelica choices annotation (see :cite:`Modelica2017` §7.3.4) *conditionally* to any logical expression. Both the logical expression and the argument specified within the choices annotation must be valid in the variable scope of the class where they are used. This annotation takes precedence on Modelica ``choices`` and ``choicesAllMatching`` annotation. The UI must render the choices corresponding to the condition evaluated as true, with the same logic as the one described for the choices annotation in :numref:`tab_param_dialog`. If no condition is evaluated as true of if ``choices()`` is empty for the condition evaluated as true, no enumeration shall be rendered. If multiple conditions are evaluated as true, no enumeration shall be rendered and a message shall be printed to the standard error.

  Example: See the declaration ``replaceable Economizers.None eco`` in `VAVSingleDuct.mo <https://github.com/lbl-srg/modelica-buildings/blob/issue1374_templateVAV/Buildings/Experimental/Templates/AHUs/VAVSingleDuct.mo>`_.

``"modification" "(" [ "condition" "=" logical-expression "," argument ] { "," "condition" "=" logical-expression "," argument } ")"``

  Description: This annotation enables a programmatic element modification or redeclaration based on any logical expression. Both the logical expression and the argument must be valid in the variable scope of the class where they are used. This annotation takes precedence on Modelica ``choices`` and ``choicesAllMatching`` annotation. No enumeration shall be rendered in the UI for any declaration containing this annotation.

  Example: See the declaration ``replaceable record RecordEco = Economizers.Data.None`` in `VAVSingleDuct.mo <https://github.com/lbl-srg/modelica-buildings/blob/issue1374_templateVAV/Buildings/Experimental/Templates/AHUs/VAVSingleDuct.mo>`_.

``"display" "=" logical-expression``

  Description: This annotation enables displaying (or hiding) some input fields in the UI. It takes precedence on Modelica ``Dialog(enable)`` annotation, and must be interpreted with the same logic as the one described for the latter in :numref:`tab_param_dialog`. This annotation adds another level of flexibility to the built-in Modelica ``Dialog(enable)`` annotation, typically needed to render only a subset of the user input fields in a control specification workflow.

``"displayOrder" "=" UNSIGNED-INTEGER``

  Description: This annotation enables specifying how to order the input fields in the UI, independently from the declaration order. The input fields of all the declarations with this annotation should be positioned at the top of each group—or at the top of the parameter dialog if no group is specified—and ordered according to the value of ``UNSIGNED-INTEGER``.

  `Is it really needed? Alternatively, and specifically for the templates, we could allow declaring parameters after instantiating replaceable components (those replaceable components must often appear at the top of a group as they often define the equipment type)`.


Class Annotation
----------------

``"__LinkageTemplate"``

  Description: This annotation identifies either a template or a package containing templates. It is used by the tool to simplify the tree view of the loaded libraries and only display the templates, see :numref:`sec_class_workflow`.


.. _sec_class_workflow:

Class Manipulation and Workflow
===============================

From the original template classes, the configuration workflow enables generating classes representing specific system configurations.
Those specific classes must be organized in a package structure (the user projects) complying with the Modelica specification.
Note that according to the specification, a package can be either a single file (for instance ``NameOfPackage.mo``) or a directory containing a ``package.mo`` file, and the package file may itself include some definitions of subpackages.

The UI must provide a means to explore both the package containing the template classes and the package containing the specific classes (the user projects).

* A file explorer with a tree view should reveal the package structure in a left panel.

* Only the classes defined in the package file, or enumerated in the ``package.order`` file shall be displayed. And they shall be displayed in the same order as the one specified by those two files.

* The left panel is divided vertically in two parts: the upper part for the templates, the lower part for the user projects.

* The description string of each class must be displayed, for instance when hovering a package or a model in the file explorer.

The following example illustrates typical package structures and the way they should be displayed in the UI.

.. code-block:: bash
   :name: code_packages_system
   :caption: Example of the package structure for the templates and user projects (in the file system)

   Buildings
   ├── Templates
   │   ├── AHUs
   │   │   ├── Data
   │   │   ├── package.mo        # Contains __Linkage_Template annotation.
   │   │   ├── package.order
   │   │   └── VAVSingleDuct.mo  # Contains __Linkage_Template annotation.
   │   ├── BoilerPlants
   │   │   └── ...               # Enclosed file package.mo contains __Linkage_Template annotation.
   │   ├── ChillerPlants
   │   │   └── ...               # Enclosed file package.mo contains __Linkage_Template annotation.
   │   ├── TerminalUnits
   │   │   └── ...               # Enclosed file package.mo contains __Linkage_Template annotation.
   │   ├── package.mo
   │   └── package.order
   ├── ...
   ├── package.mo
   └── package.order

   UserProjects
   ├── Project_1
   │   ├── AHUs
   │   │   ├── Data
   │   │   ├── package.mo
   │   │   ├── package.order
   │   │   └── VAV_1.mo
   │   ├── BoilerPlants
   │   │   └── ...
   │   ├── ChillerPlants
   │   │   └── ...
   │   ├── TerminalUnits
   │   │   └── ...
   │   ├── package.mo
   │   └── package.order
   ├── {Project_i}
   │   └── ...
   ├── package.mo
   └── package.order

This should be rendered in the UI as follows.

.. code-block:: bash
   :name: code_packages_ui
   :caption: Example of the rendering of the package structure in the UI

   Buildings
   ├── AHUs
   │   └── VAVSingleDuct
   ├── BoilerPlants
   │   └── ...
   ├── ChillerPlants
   │   └── ...
   └── TerminalUnits
       └── ...

   UserProjects
   ├── Project_1
   │   ├── AHUs
   │   │   ├── VAV_1
   │   │   └── Data
   │   ├── BoilerPlants
   │   │   └── ...
   │   ├── ChillerPlants
   │   │   └── ...
   │   └── TerminalUnits
   │       └── ...
   └── {Project_i}
       └── ...


The suggested workflow is as follows.

#. The template package of the Modelica Buildings Library is preloaded. The tool provides the option to load additional template packages from third-party libraries. A template package is identified by the class annotation ``__Linkage_Template`` in the package file.

   * Only the classes with the annotation ``__Linkage_Template`` should be displayed in the template file explorer.

#. The user can select whether to create a ``UserProjects`` from scratch or to load a package stored locally on the device.

   * If a new package is created, it must contain the class annotation ``uses(Buildings(version="..."), ...)`` with the version of all loaded libraries.

   * When loading a package with the class annotation ``uses(Buildings(version="..."), ...)`` refer to :numref:`tab_gui_func` for the library version management.

#. The user can create a new project, for instance by right clicking on ``UserProjects`` which renders a menu with the options *Add New*, etc.

#. The user can select the working project to save the new specific classes, for instance by right clicking on ``Project_1`` which renders a menu with the options *Set Working Project*, *Rename*, *Delete*, etc.

   * The current working project must be clearly highlighted in the user projects file explorer.

#. The user selects a template to start the configuration workflow, for instance by right clicking on ``VAVSingleDuct`` which renders a menu with the option *Start Configuring*, etc.

#. A specific class is created under the corresponding subpackage (for instance ``AHUs``) of the current working project in the ``UserProjects`` package.

   * The new class is constructed by extending the original template ``extends type-specifier [ class-modification ] [annotation]``.
   * The parameter dialog of the template class is generated in the configuration panel. In addition, two input fields allows specifying the simple name and the description string of the specific class to be generated.
   * The tree view of the ``UserProjects`` package is updated dynamically, based on the class name and the class description string input by the user.
   * Any user input leads to updating the specific class definition. The full composed name (dot notation starting from the top-level library package, for instance ``Buildings``) shall be used to reference each class used in the class definition.

#. Optionally, a record class with the same simple name is created under the corresponding subpackage, for instance ``AHUs.Data``. The record contains the same class modifications as the ones applied to the records of the specific class. This will allow the user to further use this record to propagate the parameters of an instance of the specific class to a top-level simulation model.

#. At least two action buttons *Save* and *Cancel* are required in the configuration panel. The class within the ``UserProjects`` package is only modified upon *Save*. All the modifications are reset to the last saved state upon *Cancel*.

#. Once created, the user can select each specific class from the user projects file explorer and further modify it, for instance by right clicking on the corresponding class which renders a menu with the options *Edit Class*, *Delete*, *Rename*, *Duplicate*, etc.

#. Export functionalities (Modelica code, see :numref:`sec_modelica_export`, or documentation, see :numref:`sec_documentation_export`) are available from the user projects file explorer, at the level of the package and at the level of the specific class.


**********************************
Standard Streams and Error Logging
**********************************

.. admonition:: Revision Note
   :class: danger

   This paragraph is added.


An error logging mechanism is required.

Standard output and standard error streams must support redirecting to any file descriptor when integrating the widget into a third party application.


.. _sec_modelica_export:

***************
Modelica Export
***************

.. admonition:: Revision Note
   :class: danger

   This paragraph is added.


Exporting Modelica code requires the following steps.

#. Converting the JSON-formatted Modelica into Modelica code. This should be done by calling `Modelica to JSON translator <https://lbl-srg.github.io/modelica-json/>`_.

#. Formatting the generated Modelica code. This should be done by calling `<https://github.com/urbanopt/modelica-fmt>`_.
   `Implemented in Go: can it run on client side? With WebAssembly?`.

#. Optional compression. File compression is only required for exporting a package. A single class should be exported as a single uncompressed ``mo`` file.
#. Launch downloading on the client.


.. _sec_documentation_export:

********************
Documentation Export
********************

The documentation export encompasses three items.

#. Engineering schematic of the system including all control points

#. Control point list

#. Control sequence description

The composition level at which the functionality will typically be used is the same as the one considered for the configuration widget, for instance primary plant, air handling unit, terminal unit, etc. No specific mechanism to guard against an export call at different levels is required.

:numref:`screen_schematics_output` provides an example of the documentation to be generated in case of an air handling unit. The documentation may be exported as three different files but must contain all the material described in the following paragraphs.

.. figure:: img/screen_schematics_output.*
   :name: screen_schematics_output

   Mockup of the documentation export


Engineering Schematic
======================

SVG is the required output format, DXF or DWG is optional.

It is expected that Linkage will eventually be used to generate design documents included in the invitation to tender for HVAC control systems.
As such, the exported graphics should meet the industry standards and have a pixel perfect precision.
They should also allow for further editing in CAD softwares, e.g., AutoCAD®.

.. note::

   All the examples hereafter are based on the commit |611c2de|_ of MBL.

.. |611c2de| replace:: ``611c2de``
.. _611c2de: https://github.com/lbl-srg/modelica-buildings/commit/611c2de06d28b507146f591df50f8b89d594fbab

The top-level template class (such as ``Templates.AirHandlersFans.VAVMultiZone``) provides the necessary information to build the system schematic corresponding to a specific configuration.
That information is attached to the `diagram layer <https://specification.modelica.org/maint/3.5/annotations.html#annotations-for-graphical-objects>`_ of the class, in the form of `Modelica graphical primitives <https://specification.modelica.org/maint/3.5/annotations.html#graphical-primitives>`_, either directly provided in the
``Diagram`` annotation of the class, or through the icons of the subcomponents.

To process that information,

* the tool must traverse

  * one level of the instance tree to access the graphical primitives of the ``Icon`` annotation of the subcomponents,
  * the whole inheritance tree as the graphical primitives may be specified in any parent class (of the top-level class and of any class instantiated within),

* the tool must interpret

  * component redeclarations and other class modifications that are used to specify the system configuration,
  * parameter assignments based on expressions that are typically not literal and involve parameters from any other component (possibly with ``inner`` and ``outer`` references),

* the tool must render

  * SVG files provided as URIs through ``Bitmap`` annotations such as ``Bitmap(fileName="modelica://Buildings/Resources/Images/Templates/**/*.svg", ...)``,
  * native Modelica graphical primitives using the ``Line``, ``Polygon``, ``Rectangle``, ``Ellipse``, or ``Text`` annotations,
  * and ultimately the diagram and icon layers of the used classes, which are composed of the two previous types of graphical objects, the position and visibility of the objects being specified with the ``Placement`` annotation.

The process is as follows.

* From the top-level configuration class (such as ``Templates.AirHandlersFans.Validation.UserProject.AHUs.CompleteAHU`` which extends the template class ``Templates.AirHandlersFans.VAVMultiZone``) interpret all ``redeclare`` statements and build the list of all instantiated classes.

* Exclude from that list all classes that do not belong to the ``Templates`` package, all objects with the declaration annotation ``Placement(visible=false)``, and all objects with the vendor specific annotation ``__Linkage_visible=false``. The latter annotation may be either a class annotation or a declaration annotation (which takes precedence over the class annotation).

* Iterate over the resulting list of class names and build the icon view by processing the ``Icon`` annotation of that class and all parent classes. For instance, this may require to evaluate expressions such as

  .. code-block::

     Bitmap(
       visible=typDamOutMin<>Buildings.Templates.Components.Types.Damper.None and
         (typCtrEco==Buildings.Templates.AirHandlersFans.Types.ControlEconomizer.FixedEnthalpyWithFixedDryBulb or
         typCtrEco==Buildings.Templates.AirHandlersFans.Types.ControlEconomizer.DifferentialEnthalpyWithFixedDryBulb,
        ...)

  defined in the parent class ``Templates.AirHandlersFans.Components.OutdoorReliefReturnSection.Interfaces.PartialOutdoorReliefReturnSection``, where some parameters are assigned within the derived class ``Templates.AirHandlersFans.Components.OutdoorReliefReturnSection.Economizer`` as below.

  .. code-block::

     model Economizer "Air economizer"
       extends Buildings.Templates.AirHandlersFans.Components.OutdoorReliefReturnSection.Interfaces. PartialOutdoorReliefReturnSection(
         final typDamOutMin=secOut.typDamOutMin,
         ...)

* Build the diagram view by processing the ``Diagram`` annotation of the configuration class and all parent classes (including the original template class). The connection lines specified as annotations of ``connect`` clauses must be disregarded and *not included* in the generated schematic.

* Place the icons of all visible objects and the additional graphical objects from the ``Diagram`` annotation on the diagram canvas, using the ``Placement`` annotation of each object.

  Note that the system schematic may include "standalone" graphical objects that are not related to any component (for instance the AHU casing), and may exclude components that are required in the Modelica model but pruned from the schematic (for instance boundary conditions).

* Optionally: generate an index tag based on the object position, from top to bottom and left to right. Use those tags to order the :ref:`Control Point List`. The expected result is illustrated on :numref:`screen_schematics_output`. The mapping between the graphical objects and the control points may be implemented using a ``__cdl__annotation`` as specified at `https://obc.lbl.gov/specification/cdl.html#tagged-properties <https://obc.lbl.gov/specification/cdl.html#tagged-properties>`_. `TODO: Further specify the annotation mechanism and the placement of the generated tag.`

* Resize the diagram canvas to the minimum and maximum x and y coordinates of the visible graphical objects, output the SVG file.

  As a fallback, the template developer may specify the actual limiting coordinates of the schematic by means of a vendor annotation.


.. note::

   **Graphical feedback involving parameter evaluation**: With Dymola (version 2022), graphical feedback involving parameter evaluation (such as ``visible=typDamOutMin<>Buildings.Templates.Components.Types.Damper.None`` in the example here above) seems to be effective only when using full class names, i.e., when no class name lookup is needed. Therefore, such parameter assignments in the ``Templates`` package should rely on full class names.

   **Code reusability**: The functionalities that are described here above to generate the system schematic basically boil down to the ones needed by a viewer of the icon and diagram layers of Modelica classes.
   The code should be structured so that potential future developments of such a viewer can easily reuse the implementation within the Linkage tool, or access functions like ``generateIconView`` and ``generateDiagramView`` through the Linkage API (not within the current scope).


.. _Control Point List:

Control Point List
===================

Generating the control point list is done by calling a module developed by LBL (ongoing development) which returns an HTML or Word document.


Control Sequence Description
============================

Generating the control sequence description is done by calling a `module developed by LBL <https://lbl-srg.github.io/modelica-json/>`_ which returns an HTML or Word document.


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
