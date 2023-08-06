CovsirPhy: COVID-19 data with SIR model
=======================================

| |PyPI version| |Downloads| |PyPI - Python Version|
| |GitHub license| |Maintainability|

CovsirPhy is a Python package for COVID-19 (Coronavirus disease 2019)
data analysis with SIR-derived models. Please refer to "Method" part of
`COVID-19 data with SIR
model <https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model>`__
notebook in Kaggle to understand the methods.

SIR-F is a customized SIR-derived ODE model. To evaluate the effect of
measures, parameter estimation of SIR-F will be applied to subsets of
time series data in each country. Parameter change points will be
determined by S-R trend analysis.

Functionalities
---------------

-  Downloading and cleaning data

   -  Epidemic data: the number of confirmed/fatal/recovered cases
   -  Population data: raw data must include country, (province), values
      of population

-  Data visualization with Matplotlib
-  S-R Trend analysis with Optuna and scipy.optimize.curve\_fit
-  Numerical simulation of ODE models with scipy.integrate.solve\_ivp
-  Description of ODE models

   -  Basic class of ODE models
   -  SIR, SIR-D, SIR-F, SIR-FV and SEWIR-F model

-  Parameter Estimation of ODE models with Optuna and numerical
   simulation
-  Simulate the number of cases with user-defined parameter values

Inspiration
-----------

-  Monitor the spread of COVID-19
-  Keep track parameter values/reproductive number in each
   country/province
-  Find the relationship of reproductive number and measures taken in
   each country/province

Trying now
----------

The author is trying to add the following functionalities. - Speed-up
S-R trend analysis and hyperparameter estimation of ODE models - Keep
track parameter values/reproductive number of all countries with a
simple code - Find relationship of reproductive number and measures
automatically

If you have ideas or need new functionalities, please join this project.
Any suggestions with `Github
Issues <https://github.com/lisphilar/covid19-sir/issues/new/choose>`__
are always welcomed.

Installation and dataset preparation
------------------------------------

We have the following options to start analysis with CovsirPhy. Datasets
are not included in this package, but we can prepare them with
``DataLoader`` class.

+--------------------------------+----------------+---------------------------------------+
|                                | Installation   | Dataset preparation                   |
+================================+================+=======================================+
| Standard users                 | pip/pipenv     | Automated with ``DataLoader`` class   |
+--------------------------------+----------------+---------------------------------------+
| Developers                     | git-cloning    | Automated with ``DataLoader`` class   |
+--------------------------------+----------------+---------------------------------------+
| Kagglers (local environment)   | git-cloning    | Kaggle API and Python script          |
+--------------------------------+----------------+---------------------------------------+
| Kagglers (Kaggle platform)     | pip            | Kaggle Datasets                       |
+--------------------------------+----------------+---------------------------------------+

We will use the following datasets.

+-------+-------+-------+
|       | Descr | URL   |
|       | iptio |       |
|       | n     |       |
+=======+=======+=======+
| The   | COVID | https |
| numbe | -19   | ://gi |
| r     | Data  | thub. |
| of    | Repos | com/C |
| cases | itory | SSEGI |
| (JHU) | by    | SandD |
|       | the   | ata/C |
|       | Cente | OVID- |
|       | r     | 19    |
|       | for   |       |
|       | Syste |       |
|       | ms    |       |
|       | Scien |       |
|       | ce    |       |
|       | and   |       |
|       | Engin |       |
|       | eerin |       |
|       | g     |       |
|       | (CSSE |       |
|       | )     |       |
|       | at    |       |
|       | Johns |       |
|       | Hopki |       |
|       | ns    |       |
|       | Unive |       |
|       | rsity |       |
|       | .     |       |
+-------+-------+-------+
| The   | Lisph | https |
| numbe | ilar  | ://gi |
| r     | (2020 | thub. |
| of    | ),    | com/l |
| cases | COVID | isphi |
| in    | -19   | lar/c |
| Japan | datas | ovid1 |
|       | et    | 9-sir |
|       | in    | /tree |
|       | Japan | /mast |
|       | .     | er/da |
|       |       | ta    |
+-------+-------+-------+
| Popul | The   | https |
| ation | World | ://da |
| in    | Bank  | ta.wo |
| each  | Group | rldba |
| count | (2020 | nk.or |
| ry    | ),    | g/ind |
|       | THE   | icato |
|       | WORLD | r/SP. |
|       | BANK, | POP.T |
|       | Popul | OTL   |
|       | ation |       |
|       | ,     |       |
|       | total |       |
|       | .     |       |
+-------+-------+-------+
| Gover | Thoma | https |
| nment | s     | ://gi |
| Respo | Hale, | thub. |
| nse   | Sam   | com/O |
| Track | Webst | xCGRT |
| er    | er,   | /covi |
| (OxCG | Anna  | d-pol |
| RT)   | Pethe | icy-t |
|       | rick, | racke |
|       | Toby  | r     |
|       | Phill |       |
|       | ips,  |       |
|       | and   |       |
|       | Beatr |       |
|       | iz    |       |
|       | Kira. |       |
|       | (2020 |       |
|       | ).    |       |
|       | Oxfor |       |
|       | d     |       |
|       | COVID |       |
|       | -19   |       |
|       | Gover |       |
|       | nment |       |
|       | Respo |       |
|       | nse   |       |
|       | Track |       |
|       | er.   |       |
|       | Blava |       |
|       | tnik  |       |
|       | Schoo |       |
|       | l     |       |
|       | of    |       |
|       | Gover |       |
|       | nment |       |
|       | .     |       |
+-------+-------+-------+

If you want to use a new dataset for your analysis, please kindly inform
us via `GitHub
Issues <https://github.com/lisphilar/covid19-sir/issues/new/choose>`__
with "Request new method of DataLoader class" template.

1. Standard users
~~~~~~~~~~~~~~~~~

Covsirphy is available at `PyPI (The Python Package Index):
covsirphy <https://pypi.org/project/covsirphy/>`__ and supports Python
3.7 or newer versions.

::

    pip install covsirphy

Then, download the datasets with the following codes, when you want to
save the data in ``input`` directory.

.. code:: python

    import covsirphy as cs
    data_loader = cs.DataLoader("input")
    jhu_data = data_loader.jhu()
    japan_data = data_loader.japan()
    population_data = data_loader.population()
    oxcgrt_data = data_loader.oxcgrt()

If ``input`` directory has the datasets, ``DataLoader`` will load the
local files. If the datasets were updated in remote servers,
``DataLoader`` will update the local files automatically.

We can get descriptions of the datasets and raw/cleaned datasets easily.
As an example, JHU dataset will be used here.

.. code:: python

    # Description (string)
    jhu_data.citation
    # Raw data (pandas.DataFrame)
    jhu_data.raw
    # Cleaned data (pandas.DataFrame)
    jhu_data.cleaned()

2. Developers
~~~~~~~~~~~~~

Developers will clone this repository with ``git clone`` command and
install dependencies with pipenv.

::

    git clone https://github.com/lisphilar/covid19-sir.git
    cd covid19-sir
    pip install wheel; pip install --upgrade pip; pip install pipenv
    export PIPENV_VENV_IN_PROJECT=true
    export PIPENV_TIMEOUT=7200
    pipenv install --dev

Developers can perform tests with
``pipenv run pytest -v --durations=0 --profile-svg`` and call graph will
be saved as SVG file (prof/combined.svg).

-  Windows user need to install `Graphviz for
   Windows <https://graphviz.org/_pages/Download/Download_windows.html>`__
   in advance.
-  Debian/Ubuntu user need to install Graphviz with
   ``sudo apt install graphviz`` in advance.

If you can run ``make`` command,

+--------------------+----------------------------------------------------+
| ``make install``   | Install pipenv and the dependencies of CovsirPhy   |
+--------------------+----------------------------------------------------+
| ``make test``      | Run tests using Pytest                             |
+--------------------+----------------------------------------------------+
| ``make docs``      | Update sphinx document                             |
+--------------------+----------------------------------------------------+
| ``make example``   | Run example codes                                  |
+--------------------+----------------------------------------------------+
| ``make clean``     | Clean-up output files and pipenv environment       |
+--------------------+----------------------------------------------------+

We can prepare the dataset with the same codes as that was explained in
"1.Preferred" subsection.

3. Kagglers (local environment)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As explained in "2. Developers" subsection, we need to git-clone this
repository and install the dependencies when you want to uses this
package with Kaggle API in your local environment.

Then, please move to account page and download "kaggle.json" by
selecting "API > Create New API Token" button. Copy the json file to the
top directory of the local repository. Please refer to `How to Use
Kaggle: Public API <https://www.kaggle.com/docs/api>`__ and
`stackoverflow: documentation for Kaggle API *within*
python? <https://stackoverflow.com/questions/55934733/documentation-for-kaggle-api-within-python#:~:text=Here%20are%20the%20steps%20involved%20in%20using%20the%20Kaggle%20API%20from%20Python.&text=Go%20to%20your%20Kaggle%20account,json%20will%20be%20downloaded>`__

We can download datasets with ``pipenv run ./input.py`` command.
Modification of environment variables is un-necessary. Files will be
saved in ``input`` directory of your local repository.

| Note:
| Except for OxCGRT dataset, the datasets downloaded with ``input.py``
  scripts are different from that explained in the previous subsections.
  URLs are shown in the next table.

+-------+-------+-------+
|       | Descr | URL   |
|       | iptio |       |
|       | n     |       |
+=======+=======+=======+
| The   | Novel | https |
| numbe | Coron | ://ww |
| r     | a     | w.kag |
| of    | Virus | gle.c |
| cases | 2019  | om/su |
| (JHU) | Datas | dalai |
|       | et    | rajku |
|       | by    | mar/n |
|       | SRK   | ovel- |
|       |       | coron |
|       |       | a-vir |
|       |       | us-20 |
|       |       | 19-da |
|       |       | taset |
+-------+-------+-------+
| The   | COVID | https |
| numbe | -19   | ://ww |
| r     | datas | w.kag |
| of    | et    | gle.c |
| cases | in    | om/li |
| in    | Japan | sphil |
| Japan | by    | ar/co |
|       | Lisph | vid19 |
|       | ilar  | -data |
|       |       | set-i |
|       |       | n-jap |
|       |       | an    |
+-------+-------+-------+
| Popul | covid | https |
| ation | 19    | ://ww |
| in    | globa | w.kag |
| each  | l     | gle.c |
| count | forec | om/dg |
| ry    | astin | rechk |
|       | g:    | a/cov |
|       | locat | id19- |
|       | ions  | globa |
|       | popul | l-for |
|       | ation | ecast |
|       | by    | ing-l |
|       | Dmitr | ocati |
|       | y     | ons-p |
|       | A.    | opula |
|       | Grech | tion  |
|       | ka    |       |
+-------+-------+-------+
| Gover | Thoma | https |
| nment | s     | ://gi |
| Respo | Hale, | thub. |
| nse   | Sam   | com/O |
| Track | Webst | xCGRT |
| er    | er,   | /covi |
| (OxCG | Anna  | d-pol |
| RT)   | Pethe | icy-t |
|       | rick, | racke |
|       | Toby  | r     |
|       | Phill |       |
|       | ips,  |       |
|       | and   |       |
|       | Beatr |       |
|       | iz    |       |
|       | Kira. |       |
|       | (2020 |       |
|       | ).    |       |
|       | Oxfor |       |
|       | d     |       |
|       | COVID |       |
|       | -19   |       |
|       | Gover |       |
|       | nment |       |
|       | Respo |       |
|       | nse   |       |
|       | Track |       |
|       | er.   |       |
|       | Blava |       |
|       | tnik  |       |
|       | Schoo |       |
|       | l     |       |
|       | of    |       |
|       | Gover |       |
|       | nment |       |
|       | .     |       |
+-------+-------+-------+

Usage of ``DataLoader`` class is as follows. Please specify
``local_file`` argument in the methods.

.. code:: python

    import covsirphy as cs
    data_loader = cs.DataLoader("input")
    jhu_data = data_loader.jhu(local_file="covid_19_data.csv")
    japan_data = data_loader.japan(local_file="covid_jpn_total.csv")
    population_data = data_loader.population(local_file="locations_population.csv")
    oxcgrt_data = data_loader.oxcgrt(local_file="OxCGRT_latest.csv")

4. Kagglers (Kaggle platform)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you want to use this package in Kaggle notebook, please turn on
Internet option in notebook setting and download the datasets explained
in the previous section.

Then, install this package with pip command.

::

    !pip install covsirphy

Then, please load the datasets with the following codes, specifying the
filenames.

.. code:: python

    import covsirphy as cs
    # The number of cases (JHU)
    jhu_data = cs.JHUData("/kaggle/input/novel-corona-virus-2019-dataset/covid_19_data.csv")
    # (Optional) The number of cases in Japan
    jpn_data = cs.CountryData("/kaggle/input/covid19-dataset-in-japan/covid_jpn_total.csv", country="Japan")
    jpn_data.set_variables(
        date="Date", confirmed="Positive", fatal="Fatal", recovered="Discharged", province=None
    )
    # Population in each country
    pop_data = cs.Population(
        "/kaggle/input/covid19-global-forecasting-locations-population/locations_population.csv"
    )

| Note:
| Currently, OxCGRT dataset is not supported.

Quick usage for analysis
------------------------

Example Python codes are in ``example`` directory. With Pipenv
environment, we can run the Python codes with Bash code ``example.sh``
in the top directory of this repository.

Preparation
~~~~~~~~~~~

.. code:: python

    import covsirphy as cs
    cs.__version__

Please load the datasets as explained in the previous section.

(Optional) We can replace a part of JHU data with country-specific
datasets. As an example, we will the records in Japan, because values of
JHU dataset sometimes differ from government-announced values as shown
in `COVID-19: Government/JHU data in
Japan <https://www.kaggle.com/lisphilar/covid-19-government-jhu-data-in-japan>`__.

.. code:: python

    jhu_data.replace(japan_data)
    ncov_df = jhu_data.cleaned()

Scenario analysis
~~~~~~~~~~~~~~~~~

As an example, use dataset in Italy. #### Check records

.. code:: python

    ita_scenario = cs.Scenario(jhu_data, population_data, country="Italy", province=None)

See the records as a figure.

.. code:: python

    ita_record_df = ita_scenario.records()

S-R trend analysis
^^^^^^^^^^^^^^^^^^

Show S-R trend to determine the number of change points.

.. code:: python

    ita_scenario.trend()

As an example, set the number of change points as 4.

.. code:: python

    ita_scenario.trend(n_points=4, set_phases=True)

Start/end date of the four phase were automatically determined. Let's
see.

.. code:: python

    print(ita_scenario.summary())

Hyperparameter estimation of ODE models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As an example, use SIR-F model.

.. code:: python

    ita_scenario.estimate(cs.SIRF)
    print(ita_scenario.summary())

We can check the accuracy of estimation with a figure.

.. code:: python

    # Table
    ita_scenario.estimate_accuracy(phase="1st")
    # Get a value
    ita_scenario.get("Rt", phase="4th")
    # Show parameter history as a figure
    ita_scenario.param_history(targets=["Rt"], divide_by_first=False, box_plot=False)
    ita_scenario.param_history(targets=["rho", "sigma"])

Prediction of the number of cases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

we can add some future phases.

.. code:: python

    # if needed, clear the registered future phases
    ita_scenario.clear(name="Main")
    # Add future phase to main scenario
    ita_scenario.add_phase(name="Main", end_date="01Aug2020")
    # Get parameter value
    sigma_4th = ita_scenario.get("sigma", name="Main", phase="4th")
    # Add future phase with changed parameter value to new scenario
    sigma_6th = sigma_4th * 2
    ita_scenario.add_phase(end_date="31Dec2020", name="Medicine", sigma=sigma_6th)
    ita_scenario.add_phase(days=30, name="Medicine")
    print(ita_scenario.summary())

Then, we can predict the number of cases and get a figure.

.. code:: python

    # Prediction and show figure
    sim_df = ita_scenario.simulate(name="Main")
    # Describe representative values
    print(ita_scenario.describe())

Apache License 2.0
------------------

Please refer to
`LICENSE <https://github.com/lisphilar/covid19-sir/blob/master/LICENSE>`__
file.

Citation
--------

Lisphilar, 2020, Kaggle notebook, COVID-19 data with SIR model,
https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model

CovsirPhy development team, 2020, GitHub repository, CovsirPhy, Python
package for COVID-19 data with SIR model,
https://github.com/lisphilar/covid19-sir

.. |PyPI version| image:: https://badge.fury.io/py/covsirphy.svg
   :target: https://badge.fury.io/py/covsirphy
.. |Downloads| image:: https://pepy.tech/badge/covsirphy
   :target: https://pepy.tech/project/covsirphy
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/covsirphy
   :target: https://badge.fury.io/py/covsirphy
.. |GitHub license| image:: https://img.shields.io/github/license/lisphilar/covid19-sir
   :target: https://github.com/lisphilar/covid19-sir/blob/master/LICENSE
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/eb97eaf9804f436062b9/maintainability
   :target: https://codeclimate.com/github/lisphilar/covid19-sir/maintainability
