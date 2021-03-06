User Manual
===========

This part of the documentation is intended to describe the features of pyFDA that are relevant to a user (i.e. non-developer).

Once you have started up pyFDA, you'll see a screen similar to the following figure:

.. figure:: ../img/pyfda_specs_Hf.png
   :alt: pyfda screenshot

   Screenshot of pyfda

*	*Input widgets:* On the left-hand side you see tabs for different input widgets, i.e. where you can enter and modify parameters for the filter to be designed

*	*Plotting widgets* can be selected on the right hand side of the application.

*	The two parts can be resized using the handles (red dots).

Specifications
--------------

The figure above features the **Specs** widget where you can select:
- *response type* (low pass, band pass, ...)
- *filter type* (IIR for a recursive filter with infinite impulse response or FIR for a transversal filter with finite impulse response)
- *filter class* (elliptic, ...) allowing you to select 

Features
--------

-  **Filter design**



Customization
~~~~~~~~~~~~~

- Layout and some parameters can be customized with the file
  ``pyfda/pyfda_rc.py`` (within the install directory right now). 
- Select which widgets and filters will be included, define a user
  directory for integration of your own widgets in ``<USER_HOME>/.pyfda/pyfda.conf``
- Control logging behaviour with ``<USER_HOME>/.pyfda/pyfda_log.conf``
