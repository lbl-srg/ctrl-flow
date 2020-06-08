.. raw:: latex

   \pagestyle{plain}


Preamble and Conventions
========================

This documentation specifies the requirements for LinkageJS software: *a graphical user interface for editing Modelica models of HVAC and control systems*.

* Everything that relates to the software functionalities and the data formats to be consumed and returned must be considered as minimum requirements and implemented in the final deliverables.

* However, the specification also provides some implementation strategies when it comes to devising the "assisted modeling" mode, enabling to build complex thermo-fluid models and control sequences based on a simple HTML input form. Here the proposed design should only be considered as a possible path. Alternative approaches are welcome but they must at least provide the same level of functionalities as the proposed approach and meet the minimum requirements that are expressed.

.. warning::

   To clearly distinguish what constitutes requirements from what constitutes a design proposition open to some alternative approaches, we will use this warning format throughout the specification.

   Furthermore we use the following **convention**.

   - The words *must, must not, required, shall, shall not, should, should not, recommended, may, optional* in this document must be interpreted as described in `RFC2119 <https://tools.ietf.org/html/rfc2119>`_.
