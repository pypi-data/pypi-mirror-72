.. _install_bluefog:

Installing Bluefog
==================

Bluefog currently supports MacOS and Linux only. 


Installing Bluefog from Pip (CPU)
---------------------------------
Installing from pip should be sufficient for most Bluefog users.
However, our implementation highly independent on the MPI and other libraries. Please
make sure that ``python>=3.7`` and
``gcc>=4.0`` and supporting ``std=C++11`` in your development environment. 
We recommend using `conda`_ as python environment control. 
Most dependent python package should be automatically installed through the pip.
Lastly, we relied on the MPI implementation, please install 
`open-mpi>=4.0` `download link`_ and `instruction`_ for CPU usage.
After you think the environment is all set, just run following command to install Bluefog:

.. code-block:: bash

    pip install --no-cache-dir bluefog

.. Note::

    If ``--no-cache-dir`` is not present, you may receive the error information like
    ``Failed building wheel for bluefog``, which won't fail the installation though.
    The reason is Bluefog is a library with C-extention,
    which needs to be built on your system. Check this `stack overflow`_ answer if you are interested.


Installing Bluefog from Pip (GPU)
---------------------------------
All steps for GPU case are the same as CPU case except for the OpenMPI installation.
In order to get full support of GPU, you have to install `CUDA>=10.0` 
and install pytorch and/or tensorflow with the GPU support version. 
To maximize the efficiency of GPU and MPI, our implementation assumes the 
MPI installed is GPU-aware if GPU is available. It will avoid the extra cost 
that copy and moving the data from the GPU and host memory, i.e. the address of 
GPU location can be used directly. However, if MPI built is not GPU-aware, 
there will be a segmentation fault. To do that, you can configure the open install setting
after the download of OpenMPI:

.. code-block:: bash

    ./configure --prefix={YOUR_OWN_PREFIX} --with-cuda && \
    make -j $(nproc) all && \
    make install

If you have NCCL installed in your system, it is also recommend to use NCCL instead of OpenMPI as
communication implementation. To install Bluefog with NCCL implementation, you need to run

.. code-block:: bash

    BLUEFOG_WITH_NCCL=1 pip install --no-cache-dir bluefog


Installing Bluefog from Github Directly
---------------------------------------
First, please check your environment as mentioned in above subsections. Then,
clone or download the bluefog repository from `Github`_. Last, just run the
following command under the root folder of bluefog repository:

.. code-block:: bash

    pip install .

Use Bluefog through Docker
--------------------------
The docker image for Bluefog can be accessed through `Docker Hub <https://hub.docker.com/r/bluefoglib/bluefog>`_.
For more details, check :ref:`Docker Usage` page.

1. Download docker image with CUDA support:

.. code-block:: bash

    sudo docker pull bluefoglib/bluefog:gpu

2. Download docker image with only CPU support:

.. code-block:: bash

    sudo docker pull bluefoglib/bluefog:cpu

.. _conda: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
.. _download link: https://www.open-mpi.org/software/ompi/v4.0/
.. _instruction:  https://www.open-mpi.org/faq/?category=building#easy-build
.. _Github: https://github.com/ybc1991/bluefog
.. _stack overflow: https://stackoverflow.com/questions/53204916/what-is-the-meaning-of-failed-building-wheel-for-x-in-pip-install
