================
lcmap-app-deploy
================

Backup or deploy Marathon application job definitions.

What does it do?
----------------
* Gets job definitions from a Marathon endpoint and saves them to a json file.
* Loads job definitions from a json file and puts them to a Marathon endpoint.
* Project and job name filters can be used to limit which jobs are backed up/deployed.
* A test mode will show what would have been backed up/deployed.


Use
----

.. code:: bash

   # Show app's help/all arguments.
   app-deploy --help

   # Test a backup from a dev Marathon endpoint to a file.
   # Use job filters "/myproject" and then all for all jobs.
   app-deploy --backup --test --env dev --project myproject --job all --file mytest.json

   # Run a backup from a dev Marathon endpoint to a file.
   # Use job filters "/myproject" and then further filter jobs with "myjob" in the name.
   app-deploy --backup --env dev --project myproject --job myjob --file mytest.json

   # Test a deploy from a file to a dev Marathon endpoint.
   # Use job filters "/myproject and then all for all jobs.
   app-deploy --deploy --test --env dev --project myproject --job all --file mytest.json


Install and Run
---------------

.. code:: bash

   pip install lcmap-app-deploy

   export marathon_username=myuser
   export marathon_password=mypw
   export marathon_site_dev=https://hostdev:port/v2/apps
   export marathon_site_prod=https://hostprod:port/v2/apps

   app-deploy --help


Versioning
----------
lcmap-app-deploy follows semantic versioning: http://semver.org/
