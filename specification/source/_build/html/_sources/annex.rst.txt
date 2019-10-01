.. _sec_annex:

Annex
=====

.. _par_valid_bus:

Validation of Bus Connections
-----------------------------

The use of expandable connectors (control bus) is validated in case of a complex controller (``Buildings.Controls.OBC.ASHRAE.G36_PR1.AHUs.MultiZone.VAV.Controller``).

The validation is performed:

* with Dymola (Version 2020, 64-bit, 2019-04-10) and JModelica (revision numbers from svn: JModelica 12903, Assimulo 873);
* first with a single instance of the controller and then with multiple instances corresponding to different parameters set up (see validation cases of the original controller ``Validation.Controller`` and ``Validation.ControllerConfigurationTest``),
* with nested expandable connectors: a top-level control bus composed of a first sub-level control bus for control output variables and another for control input variables.

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

    Providing an explicit indices range e.g. ``[1:numZon]`` like in the previous code snippet only causes a translation warning: Dymola seems to allocate a default dimension of **20** to the connector, the unused
    indices (from 3 to 20 in the example hereunder) are then removed from the simulation problem since they are not used in the model.

    .. code:: modelica

        Warning: The bus-input conAHU.ahuSubBusI.VDis_flow[3] matches multiple top-level connectors in the connection sets.

        Bus-signal: ahuI.VDis_flow[3]

        Connected bus variables:
        ahuSubBusI.VDis_flow[3] (connect) "Connector of Real output signal"
        conAHU.ahuBus.ahuI.VDis_flow[3] (connect) "Primary airflow rate to the ventilation zone from the air handler, including outdoor air and recirculated air"
        ahuBus.ahuI.VDis_flow[3] (connect)
        conAHU.ahuSubBusI.VDis_flow[3] (connect)

    This is a strange behavior in Dymola. On the other hand JModelica 1) allows the unspecified ``[:]`` syntax and 2) does not generate any translation warning when explicitly specifying the indices range.
    JModelica's behavior seems more aligned with :cite:`Modelica2017` *§9.1.3 Expandable Connectors* that states: "A non-parameter array element may be declared with array dimensions “:” indicating that the size is unknown."
    The logic of JModelica for expandable connectors should be the requirement for LinkageJS.

    `Issue: how to make clear to the user which variable of the bus needs to be connected i.e. which variable is actually connected to an input connector of a component`.

Simulation succeeds for the two tests cases with the two simulation tools.
The results comparison to the original test case (without control bus) is presented in :numref:`annex_valid_bus` for Dymola.

.. figure:: img/annex_valid_bus.svg
      :name: annex_valid_bus

      G36 AHU controller model: comparison of simulation results (Dymola) between implementation without (``origin``) and with (``new_bus``) expandable connectors
