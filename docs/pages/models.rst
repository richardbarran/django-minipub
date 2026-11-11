#################
The Minipub model
#################

.. automodule:: minipub.models

Publication dates
-----------------
Publication follows the calendar date in Django's configured ``TIME_ZONE``
when ``USE_TZ=True``. Activating another time zone for a visitor does not change
which articles are live. With ``USE_TZ=False``, publication uses the local date
returned by Django's clock.

'staff_preview' property
------------------------
.. automethod:: minipub.models.MinipubModel.staff_preview()

