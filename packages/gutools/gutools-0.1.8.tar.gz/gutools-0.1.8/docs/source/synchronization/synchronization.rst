TWS Synchronization
-------------------


The purpose of this feature is to drive several slaves accounts coping
the actions from a master one.

.. graphviz::

   digraph Master_Slave_Sync {
      edge [style="dashed"];
      # a [label="sphinx", href="http://sphinx-doc.org", target="_top"];
      # b [label="other"];
      # a -> b;

      master -> slave1 [label="trades"];
      master -> slave2 [label="trades"];
      master -> slave3 [label="trades"];
   }

Main Features:

-  The master account could be a *demo* or *real* account.
-  Is possible to set different risks levels for each slave account, so
   not all trades should be taken by slaves.
-  Each slave account get a copy of each actions from the master
   account.
-  Each slave will reflect the trades taken.
-  The bracket range determines whenever a slave account may or may not
   take the trade.
-  The number of contracts set on the master account is not relevant for
   taking the trade, just the prices levels.

.. todo::

   diagram with master and slace trades databases.




Setting up an evironment
~~~~~~~~~~~~~~~~~~~~~~~~

We need to setup an environment for the *master* node and oner per *slave* nodes.

Master Environment
^^^^^^^^^^^^^^^^^^

First of all, we will create the **master** trader environment

.. code:: bash

   $ mkdir master
   $ cd master
   $ # it will initialize working directory
   $ atlas session init
   $ # launch a master TWS and attach the process to the session
   $ tws username=user1 password=passwd1 & 
   $ atlas session attach --pid 1234 --alias master.tws --restart 1
   $ # launch a ib-tws service as master node
   $ atlas session start --uri "ib://tws:9090/master-trader?account=0&tws=master.tws" --alias master.trader

Note the ``account=0`` parameter that specifiy the acoount (the 1st in
this example) in case of multiaccount. We assume a multiaccount in the
rest of the example. Using 2 independent account will require the
launching of 2 tws instances using different accounts.

.. todo::

   using 2 different TWS in 2 different computers.

It will create these files:

.. code:: bash

   $ ls etc/*
   session.yaml
   master.tws.yaml
   master.trader.yaml

The files contains:

-  ``session.yaml`` : the active configuration for the session.
-  ``master.tws.yaml`` : default settings for the attached application.
   User can edit an tune the behavior for next restart.
-  ``master.trader.yaml`` : default settings for the master node
   application. User can edit an tune the behavior for next restart.

Slave Environment
^^^^^^^^^^^^^^^^^

Now we can create a **slave** environment in a similar way.

.. code:: bash

   $ mkdir slave
   $ cd slave
   $ # it will initialize working directory
   $ atlas session init
   $ # launch a master TWS and attach the process to the session
   $ tws username=user2 password=passwd2 & 
   $ atlas session attach --pid 1234 --alias slave.tws --restart 1
   $ atlas session start --uri "ib://tws:9090/slave-trader?account=1&tws=slave.tws" --alias slave.trader

Note that we are reusing the same TWS running instance in this example,
attaching with different aliases.

In this case, we are using the 2nd account as slave from the
multiaccount in the URL: ``?account=1&...``

It will create these files as well:

.. code:: bash

   $ ls etc/*
   session.yaml
   slave.tws.yaml
   slave.trader.yaml

Encryption and certificates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To handle certificates and encryption keys:

.. code:: bash

   $ atlas cert add --public-key public_file.rsa --private-key private_file.rsa


Running slaves in remote computers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add nodes or network links

.. code:: bash

   $ atlas network add --uri node://example.com:53200
   $ atlas network add --uri dht://bootstrap.jami.net:4222?network_id
   $ atlas network add --uri broadcast://192.168.1.255:53200

- add a direct node.
- add a dht network identity using a bootstrap node and port.
- add a broadcast address with port.


