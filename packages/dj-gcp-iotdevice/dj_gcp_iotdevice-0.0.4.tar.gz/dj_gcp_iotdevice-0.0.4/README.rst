=============================
Django GCP IoT Device Manager
=============================


.. image:: https://img.shields.io/pypi/v/dj_gcp_iotdevice.svg
        :target: https://pypi.python.org/pypi/dj_gcp_iotdevice

.. image:: https://img.shields.io/gitlab/pipeline/pennatus/dj_gcp_iotdevice/master
        :alt: Gitlab pipeline status

.. image:: https://readthedocs.org/projects/dj_gcp_iotdevice/badge/?version=latest
        :target: https://dj_gcp_iotdevice.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Provides a CRDL (Create, Retrieve, Destroy, List) interface to GCP IoT Core

* Free software: MIT license
* Documentation: https://dj_gcp_iotdevice.readthedocs.io.


Installation
------------

Install ``dj_gcp_iotdevice`` from pip ::

    $ pip install dj_gcp_iotdevice

Add to your top level ``apps.py`` ::

    from dj_gcp_iotdevice.apps import GCPIoTDeviceConfig

    class MyProjectDeviceConfig(GCPIoTDeviceConfig):
        registry = 'my-iot-registry'
        location = 'us-central1'
        project = 'my-project-id'

Add the new app config to your installed apps ::

    INSTALLED_APPS = [
        ...
        'apps.MyProjectDeviceConfig',
    ]

Add the provided urls to your list of urls ::

    urlpatterns = [
        ...
        path('', include('dj_gcp_iotdevice.urls')),
    ]
