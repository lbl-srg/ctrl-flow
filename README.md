# Introduction

The design and delivery of high-performance control sequences is a challenge! Writing accurate and detailed sequence of operations documents requires significant skill. Even starting from an existing sequence (such as [ASHRAE Guideline 36](https://www.ashrae.org/professional-development/all-instructor-led-training/instructor-led-training-seminar-and-short-courses/guideline-36-best-in-class-hvac-control-sequences)) is tricky work and requires careful editing when done manually. The ``ctrl-flow`` High Performance Control Design Tool is a web-based tool intended to help designers develop an accurate sequence document. The tool was developed by Lawrence Berkeley National Lab under funding from the Department of Energy and is available for use at no charge.

# Tool Structure and Vision

The structure of ``ctrl-flow`` is intended to make it readily extensible to support a broad range of systems as well as deliverable options. The tool is supported by a set of “templates” that are defined in an open standard modeling language called [Modelica](https://modelica.org/modelicalanguage.html). The user can select the desired systems and how they should be configured for a project. Based on the user selections, the initial release of the tool will output a properly edited sequence of operation based on ASHRAE Guideline 36 – 2021. The use of the templates allows for expansion (in future releases) of the tool to support new system types as well as for a set of additional outputs. Examples of future outputs include not just the sequence of operation document, but also detailed points lists, system diagrams, and the specific control logic represented in the [“Control Description Language”](https://simulationresearch.lbl.gov/wetter/download/2018-americanModelica-WetterGrahovacHu.pdf)(_CDL_) and the Control eXchange Format (_CXF_) both of which will be defined in the proposed ASHRAE Standard 231P (A Controls Description Language). Finally, the tool will also provide a Modelica model of the desired HVAC system. _CDL_ will be able to be used with additional tools (such as [OpenModelica](https://openmodelica.org)) to test the control system during design. _CXF_ will be able to be used as a format to import the defined logic into tools used for setup and programming of commercial control products which comply with _ASHRAE 231P_. Finally, users will be able to utilize the _CDL_ and the Modelica systems model with tools such as [Spawn of EnergyPlus](https://www.energy.gov/eere/buildings/articles/spawn-energyplus-spawn) to do detailed energy studies of building mechanical and control systems.

# Initial Release

The initial release of the tool has both a limited number of templates supported (multi-zone air handling unit, cooling only VAV terminal, VAV terminal with reheat) and only a single deliverable (edited Guideline 36 sequence in `.docx` format). When you first enter the tool, there is a brief pop-up tutorial which lists the steps needed to use the tool. In summary:

1. __Select Project Options__: For each project you can select the units (IP or SI), relevant energy code (ASHRAE 90.1 or California Title 24), and ventilation code (ASHRAE 62.1 or California Title 24). You are also asked to select the relevant climate zone (ASHRAE Climate Zone or California Title 24 Climate Zone). These system options are used to accurately edit the Guideline 36 sequence document so that only the relevant options are shown, and all others are omitted.
2. __Select Systems__: In this initial release the systems available are multi-zone Air Handling unit, cooling only VAV terminal, and VAV terminal with reheat. Future releases will expand system options to include fan powered VAV, Single Zone Air handlers, Chiller Plants, Boiler Plants, etc.  
3. __Configure Systems__: Each system needs to be configured. Select the “Configs” option at the bottom of the page. This will show all selected systems. Clicking on “Edit” will allow you to configure the options desired for each system. If you have multiple configurations (for example, some zones have CO2 sensors and others don’t) you can create a series of configurations by clicking on “add config”. Each configuration will need a name and you can then select the desired options. Note that you will not be able to see results until you view (and edit if desired) each configuration.  
4. __Results__: Clicking on the “Results” option at the bottom of the page will bring up a dialog box which will allow you to request the download of a Word document. Note that the processing of this document takes time – so please be patient and wait for the download. If it does not download within a few minutes, there may be an issue with the system, and it should be reported.

The final edited document consists of an edited version of the ASHRAE Guideline 36, with all original document functionality maintained including active paragraph numbering, paragraph cross-references, and styles. Although paragraph numbering in the output may deviate from the original numbering in the full Guideline 36, the original paragraph numbers are noted for Level 2 headings to facilitate manual cross-referencing. Note that the document currently includes all of the informative notes within the Guideline, but instructional notes are deleted.

This document will require further review and editing prior to use on a project.

## Current Coverage of Guideline 36-2021:

Supported:
- [x] Unit System: IP, SI
- [x] Ventilation Code: 62.1, CA Title 24
- [x] Building Energy Code: ASHRAE 90.1, CA Title 24
- [x] ASHRAE and California Title 24 Climate Zones
- [x] Multiple-Zone VAV Air-Handling Unit (not including: barometric relief, relief fan with barometric damper, multiple relief fans, common relief fan inlet plenum, AFDD)
- [x] VAV Terminal Unit – Cooling Only
- [x] VAV Terminal Unit with Reheat

Not Supported:
- [ ] Dual-Fan Dual-Duct Heating VAV Air Handling Unit
- [ ] Single-Zone VAV Air-Handling Unit
- [ ] Fan-Powered Terminal Units
- [ ] Dual-Duct VAV Terminal Units
- [ ] Constant Speed Exhaust Fan
- [ ] Chilled Water Plant
- [ ] Hot Water Plant
- [ ] Fan Coil Unit

Note: Sequences from Guideline 36 that are not currently supported are not included in the software output.

# Planned Enhancements

- [ ] User accounts and ability to save projects
- [ ] Ability to export sequences with and without informative notes
- [ ] Additional Guideline 36 sequences
- [ ] Additional sequences beyond Guideline 36
- [ ] Points lists
- [ ] Control schematics
- [ ] Control logic in _CDL_ and _CXF_

# Known Issues

- Multiple MZAHUs with different options. The MZAHU sequences may not be edited correctly if there are multiple MZAHU configurations because of interactions between different portions of the sequences. To work around this, it may be best to run through the tool for each MZAHU one at a time and to manually recombine afterwards.
- The "edit" button in the upper left corner will clear out all selections and **should not be used**. Instead, use the “back” button in the lower left corner to navigate. 
- Clicking the “back” button all the way back to the start screen will initialize the project and clear out selections.

# Notes for how to use ctrl-flow

- Zone equipment configurations. Many projects will have multiple zones with varying configurations. For example some VAV reheat zones with CO2 sensors and some without. In that case, the software will only generate a single control sequence for VAV reheat zones with CO2 sensors – the output sequence will be based on the most inclusive configuration. As such, indicating all desired terminal control options in a single configuration is sufficient to generate the corresponding sequence; there generally is not a need to specify multiple configurations for each type of terminal unit for the current software release which only generates control sequences. 
- Adding configurations. In the current implementation, there is no need to click the “Add Config” button. The tool will only output a single control sequence for each terminal type (cooling only and reheat), and the tool should only be used to define a single MZAHU at a time, both as described above.
- Paragraph numbering. 
  - The software will delete sections from Guideline 36 that are not applicable based on user selections. The paragraph numbering and paragraph references within the document are dynamic – paragraph numbering will collapse when preceding paragraphs are deleted and references other remaining paragraphs will remain intact. However, the paragraph references in the output file will need to be manually updated to display the new paragraph numbers. In Microsoft Word, type ctrl-A to select all text, then type F9 to update.
  - Note that table and figure numbers and references are not dynamic and will not change. The numbering is fixed within the Guideline 36 source file itself. 
- Saving the project. There is currently no option to save a project. The tool can be used to generate a control sequence in a single session but revising the inputs at a later time may simply require starting over. Fortunately, it only takes minutes to enter the inputs. 

# Reporting Issues

While there has been extensive testing completed for this tool, it is still in what is considered “Beta” version – which means that you may encounter issues with the process or the tool. Your feedback is essential to the project team, and we are anxious to hear about any problems that you encounter as well as feature requests for future enhancements. If you encounter an issue, we would encourage you to report it to the project team.  

Please email the following information on any issues to ctrl-flow@lbl.gov:
- Operating system (PC, MAC, Other)
- Web Browser (Chrome, Firefox, Safari, etc.)
- Details on problem encountered (feel free to include multiple items in one report)
