Intro
======
|pypi| |bld| |cvg| |black|

One of the most common ways to let users customize the way an app
works is to use config files. This means that many projects wind up
including an implementation to read in the config values, specify
defaults, control which values get looked up when, and enforce some
sort of schema.

settingscascade is designed to handle this scenario. While it can be
used in simple situations, it really shines when you need to pull in
values from a variety of sources, have a rich set of defaults, and
give users flexibility in configuring overrides at various levels.
The model it uses is CSS, mimicking the way that css uses selectors
to cascade settings from various levels of specificity. Your users
specify rule blocks the same as they would in CSS-

.. code-block:: yaml

	# Each rule block has a selector, using CSS semantics
	# this block is for a task element with the class "default"
	task.default:
	    command: "echo hello"
	    on_complete: "echo world"

	# You can specify top level settings as well for a final
	# level of fallback
	project_name: "my project"

Then your app can use the config

.. code-block:: python

	# Task represents an element (like a div or a in HTML).
	# you can specify what values are valid for this element type
	class Task(SettingsSchema):
		_name_ = task
		command: str
		on_complete: str

	config = SettingsManager(yaml.load("config.yml"), [Task])

	# In your code, you can pull an element from the settingsmanager
	# object and find the rules that apply. This is like an element
	# <task class="default"></task>
	task_config = config.task(class="default")
	run_task(
		command=task_config.command,
		on_complete=task_config.on_complete,
		name=config.project_name,
	)

Read the full documentation at https://settingscascade.readthedocs.io/en/latest/

Installation
==================

You can install settingscascade from pypi-

::

	pip install settingscascade

.. |cvg| image:: https://gitlab.com/pjbecotte/settingscascade/badges/master/coverage.svg
.. |bld| image:: https://gitlab.com/pjbecotte/settingscascade/badges/master/pipeline.svg
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
.. |pypi| image:: https://badge.fury.io/py/settingscascade.svg
