.. _diffract:

diffract
--------

A local subclass of :class:`hkl.diffract.Diffractometer` for the desired
diffractometer geometry must be created to define the reciprocal-space
axes and customize the EPICS PVs used for the motor axes.  Other
capabilities are also customized in a local subclass.

Examples are provided after the source code documentation.

These are the diffractometer geometries provided by the **hkl-c++**
library [#hklcpp]_:

============================  ==========================
name                          description
============================  ==========================
:class:`~hkl.diffract.E4CH`   Eulerian 4-circle, vertical scattering plane
:class:`~hkl.diffract.E4CV`   Eulerian 4-circle, horizontal scattering plane
:class:`~hkl.diffract.E6C`    Eulerian 6-circle
:class:`~hkl.diffract.K4CV`   Kappa 4-circle, vertical scattering plane
:class:`~hkl.diffract.K6C`    Kappa 6-circle
:class:`~hkl.diffract.TwoC`   2-circle
:class:`~hkl.diffract.Zaxis`  Z-axis
============================  ==========================

These special-use geometries are also provided by the **hkl-c++**
library [#hklcpp]_:

* :class:`~hkl.diffract.Med2p3`
* :class:`~hkl.diffract.Petra3_p09_eh2`
* :class:`~hkl.diffract.SoleilMars`
* :class:`~hkl.diffract.SoleilSiriusKappa`
* :class:`~hkl.diffract.SoleilSiriusTurret`
* :class:`~hkl.diffract.SoleilSixs`
* :class:`~hkl.diffract.SoleilSixsMed1p2`
* :class:`~hkl.diffract.SoleilSixsMed2p2`

In all cases, see the **hkl-c++** documentation for further information
on these geometries.

.. [#hklcpp] **hkl-c++** documentation:
    https://people.debian.org/~picca/hkl/hkl.html

Energy
++++++

The monochromatic X-ray energy used by the diffractometer is defined as
an ophyd ``Signal``.  The ``.energy`` signal may be used as-provided, as
a constant or the Component may be replaced by an ``ophyd.EpicsSignal``
in a custom subclass of :class:`~hkl.diffract.Diffractometer`, to
connect with an EPICS PV from the instrument's control system.  There is
no corresponding ``.wavelength`` signal at the diffractometer level.
The ``.energy_offset`` signal is used to allow for a difference between
the reported energy of ``.energy`` and the energy used for
diffractometer operations ``.calc.energy``.  

These are the terms:

==================== =======================
term                 meaning
==================== =======================
``.energy``          nominal energy (such as value reported by control system)
``.energy_offset``   adjustment from nominal to calibrated energy for diffraction
``.energy_units``    engineering units to be used for ``.energy`` and ``.energy_offset``
``.calc.energy``     energy for diffraction (used to compute wavelength)
``.calc.wavelength`` used for diffraction calculations
==================== ======================= 

These are the relationships::

    .calc.energy = in_keV(.energy + .energy_offset)
    .calc.wavelength = A*keV / .calc.energy

For use with other types of radiation (such as neutrons or electrons),
the conversion between energy and wavelength must be changed by editing
the energy and wavelength methods in the :class:`hkl.calc.CalcRecip`
class.

When the Diffractometer ``.energy`` signal is written (via
``.energy.put(value)`` operation), the ``.energy_offset`` is added.
This result is converted to ``keV`` as required by the lower-level
:mod:`hkl.calc` module, and then written to ``.calc.energy`` which in
turn writes the ``.calc.wavelength`` value. Likewise, when
``.energy.get()`` reads the energy, it takes its value from
``.calc.energy``, converts into ``.energy_units``, and then applies
``.energy_offset``.

.. tip:: How to set energy, offset, and units

   To change energy, offset, & units, do it in this order:

   1. set units and offset first
   1. finally, set energy

   EXAMPLE::

    fourc.energy_units.put("eV")
    fourc.energy_offset.put(1.5)
    fourc.energy.put(8000)
    # now, fourc.calc.energy = 8.0015 keV


Engineering Units
+++++++++++++++++

The :mod:`~hkl.diffract` module is the main user interface, providing
the various diffractometer geometries provided by *libhkl* as *ophyd*
`PseudoPositioner` Devices [#]_.  In :mod:`~hkl.diffract`, a feature has
been added to allow the energy units to be set by the user.  Internally,
:mod:`~hkl.diffract` will apply any necessary units conversion when
interacting with the values from the :mod:`~hkl.calc` module.

In the :mod:`~hkl.calc` module (lower level than the
:mod:`~hkl.diffract` module), the units for *energy* and *wavelength*
are ``keV`` and ``angstrom``, respectively.  These engineering units are
not changeable by the user since the *libhkl* code requires a consistent
set of units (it does not anticipate the need to do a units conversion).

The Python *pint* package [#]_ is used to apply any unit conversion.

This table summarizes the units for the energy and wavelength terms in
the :mod:`~hkl.calc` and :mod:`~hkl.diffract` modules.

==========================  =================
diffractometer attribute    engineering units
==========================  =================
``.energy``                 set by value of ``.energy_units`` Signal
``.calc.energy``            ``keV``
``.wavelength``             does not exist in the :mod:`~hkl.diffract` module
``.calc.wavelength``        ``angstrom``
==========================  =================

.. [#] *ophyd* `PseudoPositioner` Device:
   https://blueskyproject.io/ophyd/positioners.html#pseudopositioner
.. [#] *pint* (for engineering units conversion):
   https://pint.readthedocs.io

----

Source code documentation
+++++++++++++++++++++++++

.. automodule:: hkl.diffract
    :members:

----

.. _diffract.examples:

Examples
++++++++

Demonstrate the setup of diffractometers using the *hkl* package.

* ``sim6c`` : simulated 6-circle
* ``k4cv`` : kappa 4-circle with EPICS PVs for motors
* ``k4cve`` : ``k4cv`` with energy from local control system

The :ref:`sample` :ref:`sample.examples` section describes how to setup
a crystal sample with an orientation matrix.

.. _diffract.sim6c:

``sim6c``: 6-circle with simulated motors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is useful, sometimes, to create a simulated diffractometer where the
motor axes are provided by software simulations, rather than using the
actual motors provided by the diffractometer.

The ``ophyd.SoftPositioner`` [#]_ is such a software simulation.

.. [#] ``ophyd.SoftPositioner``:
    https://blueskyproject.io/ophyd/positioners.html#ophyd.positioner.SoftPositioner

Create the custom 6-circle subclass:

.. code-block:: python
    :linenos:

    import gi
    gi.require_version('Hkl', '5.0')
    # MUST come before `import hkl`
    import hkl.diffract
    from ophyd import Component, PseudoSingle, SoftPositioner

    class SimulatedE6C(hkl.diffract.E6C):
        """E6C: Simulated (soft) 6-circle diffractometer"""

        h = Component(PseudoSingle, '')
        k = Component(PseudoSingle, '')
        l = Component(PseudoSingle, '')

        mu = Component(SoftPositioner)
        omega = Component(SoftPositioner)
        chi = Component(SoftPositioner)
        phi = Component(SoftPositioner)
        gamma = Component(SoftPositioner)
        delta = Component(SoftPositioner)

        def __init__(self, *args, **kwargs):
            """
            start the SoftPositioner objects with initial values
            """
            super().__init__(*args, **kwargs)
            for axis in self.real_positioners:
                axis.move(0)

Create an instance of this diffractometer with::

    sim6c = SimulatedE6C('', name='sim6c')

``k4cv`` : kappa 4-circle with EPICS motor PVs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To control a kappa diffractometer (in 4-circle geometry with vertical
scattering plane) where the motor axes are provided by EPICS PVs, use
`ophyd.EpicsMotor`. [#]_

In this example, we know from our local control system that
the kappa motors have these PVs:

==========  =========
kappa axis  EPICS PVs
==========  =========
komega      sky:m1
kappa       sky:m2
kphi        sky:m3
tth         sky:m4
==========  =========

.. [#] ``ophyd.EpicsMotor``:
    https://blueskyproject.io/ophyd/builtin-devices.html?highlight=epicsmotor#ophyd.epics_motor.EpicsMotor

Create the custom kappa 4-circle subclass:

.. code-block:: python
    :linenos:

    import gi
    gi.require_version('Hkl', '5.0')
    # MUST come before `import hkl`
    import hkl.diffract
    from ophyd import Component, PseudoSingle, EpicsMotor

    class KappaK4CV(hkl.diffract.K4CV):
        """K4CV: kappa diffractometer in 4-circle geometry"""

        h = Component(PseudoSingle, '')
        k = Component(PseudoSingle, '')
        l = Component(PseudoSingle, '')

        komega = Component(EpicsMotor, "sky:m1")
        kappa = Component(EpicsMotor, "sky:m2")
        kphi = Component(EpicsMotor, "sky:m3")
        tth = Component(EpicsMotor, "sky:m4")

Create an instance of this diffractometer with::

    k4cv = KappaK4CV('', name='k4cv')

``k4cve`` : ``k4cv`` with energy from local control system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extend the ``k4cv`` example above to use the energy as provided by the
local control system.  In this example, assume these are the PVs to be
used:

==============  ====================
signal          EPICS PV
==============  ====================
energy          optics:energy
energy units    optics:energy.EGU
energy locked?  optics:energy_locked
energy offset   no PV, same units as *energy* (above)
==============  ====================

The *energy locked?* signal is a flag controlled by the user that
controls whether (or not) the *energy* signal will update the wavelength
of the diffractometer's *calc* engine. We expect this to be either 1
(update the calc engine) or 0 (do NOT update the calc engine).

We'll also create a (non-EPICS) signal to provide for an energy offset
(in the same units as the control system energy). This offset will be
*added* to the control system energy (in
:meth:`~hkl.diffract.Diffractometer._update_calc_energy()`), before
conversion of the units to *keV* and then setting the diffractometer's
*calc* engine energy:

  calc engine *energy* (keV) = control system *energy* + *offset*

which then sets the wavelength:

  calc engine *wavelength* (angstrom) = :math:`h\nu` / calc engine *energy*

(:math:`h\nu=` 12.39842 angstrom :math:`\cdot` keV) and account for the
units of the control system *energy*.  To combine all this, we define a
new python class starting similar to `KappaK4CV` above, and adding the
energy signals.  Create the custom kappa 4-circle subclass with energy:

.. code-block:: python
    :linenos:

    import gi
    gi.require_version('Hkl', '5.0')
    # MUST come before `import hkl`
    import hkl.diffract
    from ophyd import Component
    from ophyd import PseudoSingle
    from ophyd import EpicsSignal, EpicsMotor, Signal
    import pint

    class KappaK4CV_Energy(hkl.diffract.K4CV):
        """
        K4CV: kappa diffractometer in 4-circle geometry with energy
        """

        h = Component(PseudoSingle, '')
        k = Component(PseudoSingle, '')
        l = Component(PseudoSingle, '')

        komega = Component(EpicsMotor, "sky:m1")
        kappa = Component(EpicsMotor, "sky:m2")
        kphi = Component(EpicsMotor, "sky:m3")
        tth = Component(EpicsMotor, "sky:m4")

        energy = Component(EpicsSignal, "optics:energy")
        energy_units = Component(EpicsSignal, "optics:energy.EGU")
        energy_offset = Component(Signal, value=0)
        energy_update_calc_flag = Component(
            EpicsSignal,
            "optics:energy_locked")

Create an instance of this diffractometer with::

    k4cve = KappaK4CV_Energy('', name='k4cve')

.. note::

    If you get a log message such as this on the console::

        W Fri-09:12:16 - k4cve not fully connected, k4cve.calc.energy not updated

    this informs you the update cannot happen until all EPICS
    PVs are connected.  The following code, will create the object, wait
    for all PVs to connect, then update the `calc` engine::

        k4cve = KappaK4CV_Energy('', name='k4cve')
        k4cve.wait_for_connection()
        k4cve._energy_changed(k4cve.energy.get())

To set the energy offset from the command line::

    %mov k4cve.energy_offset 50

which means the diffractometer (assuming the control system uses "eV"
units) will use an energy that is 50 eV *higher* than the control system
reports. The diffractometer's *calc* engine will **only** be updated
when the energy signal is next updated.  To force an update to the calc
engine, call ``_energy_changed()`` directly with the energy value as the
argument::

    k4cve._energy_changed()

But this only works when the ``optics:energy_locked`` PV is 1 (permitted
to update the calc engine energy). To update the diffractometer's *calc*
engine energy and bypass the ``k4cve.energy_update_calc_flag`` signal,
call this command::

    k4cve._update_calc_energy()

Finally, to set the energy of the diffractometer's *calc* engine, use
one of these two methods:

============================   ============================
``energy_update_calc_flag``    command
============================   ============================
obey signal                    ``k4cve._energy_changed()``
ignore signal                  ``k4cve._update_calc_energy()``
============================   ============================

Each of these two methods will accept an optional ``value`` argument
which, if provided, will be used in place of the ``energy`` signal from
the control system.
