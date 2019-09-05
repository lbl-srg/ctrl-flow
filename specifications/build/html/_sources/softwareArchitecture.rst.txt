.. _sec_soft_arch:

Software Architecture
---------------------

This section describes the software architecture
of the LinkageJS tool and the functional verification tool.
In the text below, we mean by *plant* the HVAC and building system,
and by *control* the controls other than product integrated controllers
(PIC).
Thus, the HVAC or building system model may, and likely will,
contain product integrated controllers, which will be out
of scope for CDL apart from reading measured values from PICs and
sending setpoints to PICs.
