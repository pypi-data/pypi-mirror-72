----------------------------------
Package manager for libvis modules
----------------------------------

This is the ``npm + pip`` for libvis:
it allows you to download, install and develop custom libvis modules.



Install libvis module
---------------------

To download a module from libvis official repo https://github.com/libvis:

.. code-block:: bash

    libvis-mods download gh:/libvis/<module name>
    cd <module name>
    libvis-mods install

Start your own module
---------------------


Set up the project
~~~~~~~~~~~~~~~~~~

To try out a simple module, you can start with a simple template that uses two files:

.. code-block:: bash

    ⟩ libvis-mods init-file MyModule
    /home/dali/side-projects-hobby/pywebviz/mods/libvis_mods/project-templates/source-files {'name': 'MyModule'} .

    ⟩ cd MyModule/

    ~/MyModule ⟩ ls
    MyModule-front.coffee  MyModule_back.py  readme.md

Original template repo: https://github.com/libvis/module-template-files

For a more complex project, use the ``init-dir`` command:

.. code-block:: bash

    ⟩ libvis-mods init-dir MyModule
    /home/dali/side-projects-hobby/pywebviz/mods/libvis_mods/project-templates/source-dirs {'name': 'MyModule'} .

    ⟩ tree MyModule/
    MyModule/
    ├── Makefile
    ├── README.md
    ├── back
    │   ├── __init__.py
    │   ├── main.py
    │   └── utils.py
    ├── front
    │   ├── index.js
    │   ├── main.coffee
    │   └── style.css
    ├── js_requirements.txt
    ├── libvis-mod.conf
    └── py_requirements.txt

    2 directories, 11 files

Original template repo: https://github.com/libvis/module-template-dirs


Develop with Hot-reload
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cd MyModule
    libvis-mods develop

This will start the react development server and a hot-reload server for the python module.
The front and back will be reloaded on write. Use ``test`` variable on the web app to 
display the ``test_object`` from your module.


Commands
--------

.. code-block:: bash

    ⟩ libvis-mods
    Usage: libvis-mods [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      develop    Run the web server in development mode with hot reload
      download   Download source for the module into ./`module_name`
      init-dir
      init-file
      install    Install a module from directory
      list       list installed modules
      publish
      uninstall  Uninstall module
      where      Prints locations of where modules are installed


Requirements
------------

Just ``yarn`` or ``npm`` to build the webapp.

Feedback
--------

This project is under active development. Any feedback is welcome!

The mods repo is currently here https://github.com/DaniloZZZ/pywebviz.

