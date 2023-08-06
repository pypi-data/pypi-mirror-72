Session
==================


Sessions manage a group of related processes.

Main Features:

- The session data is stored in a *working directory*.
- Is possible to *attach* a process to a session.
- A session can *supervise* process and *relaunch* when it dies.
- Is possible to get a *fingerprint* of a process to get its internal *state*.
- Is possible to set process *inter-dependences*.
  

Setting up an environment
--------------------------


.. code-block:: bash

	$ mkdir workspace
	$ cd working
	$ # it will initialize working directory
	$ <app> session init   # <app> is a cement based cmd line application


It will copy some folders from source library structure to the working directory:

.. code-block:: bash

   $ ls -ls
   total 20
   drwxr-sr-x 2 agp agp 4096 Nov 29 13:21 bin
   drwxr-sr-x 2 agp agp 4096 Nov 29 13:17 db
   drwxr-sr-x 2 agp agp 4096 Nov 29 13:21 err
   drwxr-sr-x 2 agp agp 4096 Nov 29 13:17 etc
   drwxr-sr-x 2 agp agp 4096 Nov 29 13:21 out


Directory Layout
--------------------------

The working directory follows a particular *layout* to locate the required information:

.. code-block:: bash
   :emphasize-lines: 7

   ./etc/<name>.yaml         # configuration file for <name> process
   ./fp/<name>.yaml          # memory fingerprint for <name> process
   ./fp/<name>.<state>.yaml  # memory fingerprint for <name> process in the <state> state
   ./pid/<name>.pid          # active pid for <name> process
   ./out/<name>.out          # sdtout for <name> process
   ./err/<name>.out          # stderr for <name> process
   ./db/<name>.db            # the default sqlite3 database for <name> process
   ./bin/                    # directory containing session helpers scripts (bash completion, ...)


Process are usually launched defining an *uri*. Based on the `uri`, session will select a human readable name by *hashing* the `uri`, giving `questionable-dish` or `yellow-panda` for example.



Launch a process by URI
------------------------

A session can launch an arbitrary process by URI, if the <app> can handle this URI.


.. code-block:: bash

   $ <app> session start --uri "ib://localhost:9090/master-trader?account=0&tws=master.tws" --alias master.trader  

This will launch the process/service related to ``ib`` scheme.

Executing external programs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   $ <app> session start --uri "exec://<host>/<executable_path>?param1=value1&param2=value2" --alias <alias> --restart 1 --shutdown 1




An Example Session with Atlas application
-------------------------------------------

This example covers:

#. Initialize an empty workspace.
#. Launch an external process tagged as *master.tws* that will be launched and stopped when session starts or ends.
#. wait until master.tws process has some sockets in LISTEN mode.
#. Tag the internal state of the process as `operative` when user knows that can be used for trading.
#. Start service named master.trader service by uri.
#. Set a dependence that will launch the *master.trader* process when *master.tws* is in *operative* state.

.. code-block:: bash
   :emphasize-lines: 6,7

   $ cd ~/workspace/atlas
   $ atlas session init
   $ atlas session start --uri "exec://localhost/home/agp/Jts/tws?username=myuser&password=mypassword" --alias master.tws --restart 1 --shutdown 1
   $ atlas session wait --alias master.tws --condition "len(fp['listen'])>0" --timeout 60
   $ atlas session attach --alias master.tws --state operative 
   $ atlas session start --uri "ib://localhost/sync?uid=master&account=0&tws=master.tws" --alias master.trader --restart 1 --shutdown 1
   $ atlas session dependence add --parent master.tws:operative --child master.trader


.. todo:: 

   remove this *remainder* line

   atlas session start --uri "exec://localhost/home/agp/Jts/tws?username=dmztt7321&password=monday123" --alias master.tws --restart 1 --shutdown 1



Let's assume that reset the computer or simply all these processes are down.
Then we can activate/deactivate the whole session by:


.. code-block:: bash

   $ atlas session activate 
   $ atlas session deactivate 


Attaching running processes to a session
----------------------------------------

To add a running process to the session we can use sentences like:

.. code-block:: bash

   $ <app> session attach --pid 12814
   $ <app> session attach --pid 12814 --alias master.tws
   $ <app> session attach --pid 12814 --alias master.tws --restart 1
   $ <app> session attach --pid 12814 --alias master.tws --restart 1 --state operative

- ``alias``: set an alias to the process, so it will be preserved and easily referenced later on.
- ``restart``: determine if process must be relaunched if died.
- ``state``: tag the current process state for the fingerprint.


Adding dependences between process
----------------------------------

Sometimes a process need another process to be ready, or even in a certain state, prior being launched.

.. code-block:: bash

   $ <app> session dependence add --parent master.tws:operative --child master.trader
   
This makes ``master.trader`` process dependent on ``master.tws:operative`` process.

A process may have multiple *parent* dependences.

.. graphviz::

   digraph Process_Dependences {
      edge [style="dashed"];

      master_tws [label="master.tws:operative"];
      master_trader [label="master.trader"]

      slave_tws [label="slave.tws:operative"];
      slave_trader [label="slave.trader"]

      master_tws -> master_trader;
      slave_tws -> slave_trader;

      master_trader -> slave_trader;

   }

To remove a dependences just:

.. code-block:: bash

   $ <app> session dependence remove --parent master.tws --child master.trader:operative


Showing session processes
-------------------------

.. code-block:: bash

   $ <app> session show
   ....
   ....
   ....
   $ 






.. todo:: 

   - supervise *fp* states and update DB.
   - check prerequisites when a process is down. Try to launch the process.
   - uri may determine whenever is a service or process.
   - every service is a child of current process
   - every attached is a child as well, but launched with Popen()   

.. todo:: 

   - Set a criteria for using alias, states, names, _get_preferred_fp(), etc.
   - Simplify them all.

Session Code
-------------------------

.. autoclass:: gutools.session.USession
   :members:



Session Data
-------------------------

Currently (pending to simplify) the information is stored in:

- db/session.db
- fp/<name>.fp
- pid/<name>.pid
- etc/<alias>.yaml
  


- pid/<name>.pid : must contain only the "alive" pids. A garbage collection is needed.
- fp<name>.<state>.fp : contains saved fingerprints that would reflect the state of a running processes.
- etc/<alias>.yaml: contain information about process that user may change like command line to use, and any `**kw` calling arguments passed to launcher, behavior, etc.
- fingerprints that has not equivalent on etc/<alias>.yaml must considered obsolete and may be deleted.
- pid that has not equivalent on fp/<name>.fp must be deleted as well (they are duplicated)
  

DB basically is used for:

.. code-block:: bash

   self.workspace.find(**kw)
   self.workspace.update(process)

- All the right info is located in DB, and is *extended* in several files in DB.
- Information that user may modify should be located in files instead DB.

   + restart, shutdown
   + command line for launching

- Information that is *unique* must be placed in DB

   + name <----> alias association.
   + state
   + pid
     

Steps for recoding:

- [x] remove restart and shutdown from DB and queries. 
- [x] move shutdown and restart to etc files.
- [x] name and alias should be *unique* in DB.
- [ ] check running processes 1st when supervisor starts.
- [ ] delete layout files that are obsoleted.
- [ ] read etc, fp files to complete information.
- [ ] stamp pid file (is redundant with DB status, remove this feature?)

