Manual
======

You can install NOIA using pip. If you don’t have pip installed, you can
download it from here.

Pip is the package installer for Python. You can use pip to install
packages from the Python Package Index and other indexes.
https://pypi.org/project/pip/

1. Install NOIA agent
^^^^^^^^^^^^^^^^^^^^^

``pip install platform-agent``

2. Edit a /etc/noia-agent/config.ini file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``api_key = z99CuiZnMhe2qtz4LLX43Gbho5Zu9G8oAoWRY68WdMTVB9GzuMY2HNn667A752EA``

List of Networks to join
^^^^^^^^^^^^^^^^^^^^^^^^

If ``network_ids = 0`` or not present the Agent will not join any
network when deployed

``network_ids = Lpy3zq2ehdVZehZvoRFur4tV,U7FrPST7bV6NQGyBdhHyiebg``

Metadata (Optional)
^^^^^^^^^^^^^^^^^^^

.. code:: ini
a
    [INFO]
    NOIA_NETWORK_API = docker
    name = Azure EU gateway 
    country = Germany 
    city = Frankfurt 

    #Select one of the categories from the list or default will be assigned 
    # 'zIoT', 'Server','none' 
    category = IoT 

    #Select one of providers from the list or default will be assigned 
    #'AWS', 'DigtialOcean', 'Microsoft Azure', 'Rackspace', 'Alibaba Cloud', 
    #'Google Cloud Platform', 'Oracle Cloud', 'VMware', 'IBM Cloud', 'Vultr'. 

    provider = Microsoft Azure 
    lat = 40.14 
    lon = -74.21

Tags (Optional)
^^^^^^^^^^^^^^^

categorize your end-points. #You can use more than one tag.  e.g.
eu-group,fr-group

.. code:: ini

    tags = Tag1,Tag2

Start a NOIA Agent
^^^^^^^^^^^^^^^^^^

``/usr/local/bin/noia_agent run`` or ``noia_agent run``

You can install NOIA using pip. If you don’t have pip installed, you can
download it from here.