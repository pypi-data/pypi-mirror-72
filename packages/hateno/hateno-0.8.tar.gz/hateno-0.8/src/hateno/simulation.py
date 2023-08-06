#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import functools
import re

from .errors import *
from . import string

class Simulation():
	'''
	Represent a simulation, itself identified by its settings.

	Parameters
	----------
	folder : Folder
		Instance of `Folder` for the current simulation's folder.

	settings : dict
		Dictionary listing the user settings.
	'''

	def __init__(self, folder, settings):
		self._folder = folder
		self._user_settings = settings

		self._raw_globalsettings = None
		self._raw_settings = None
		self._raw_settings_dict = None

		self._settings_counters = {}

		self._setting_tag_regex_compiled = None
		self._eval_tag_regex_compiled = None
		self._parser_recursion_stack = []

	@classmethod
	def ensureType(cls, simulation, folder):
		'''
		Ensure a variable is a Simulation object.

		Parameters
		----------
		simulation : dict|Simulation
			The variable to check.

		folder : Folder
			The `Folder` instance to use in case we need to create a new object.

		Returns
		-------
		simulation : Simulation
			The simulation as a Simulation instance.
		'''

		if type(simulation) is cls:
			return simulation

		return cls(folder, simulation)

	def __getitem__(self, key):
		'''
		Access to a global setting.

		Parameters
		----------
		key : str
			The key of the setting to get.

		Raises
		------
		KeyError
			The key does not exist.

		Returns
		-------
		value : mixed
			The corresponding value.
		'''

		try:
			return self.reduced_globalsettings[key]

		except KeyError:
			raise KeyError('The key does not exist in the global settings')

	def __setitem__(self, key, value):
		'''
		Change a global setting.

		Parameters
		----------
		key : str
			The key of the setting to change.

		value : mixed
			The new value of the setting.

		Raises
		------
		KeyError
			The key does not exist.
		'''

		try:
			setting = [setting for setting in self._globalsettings if setting['name'] == key][0]

		except IndexError:
			raise KeyError('The key does not exist in the global settings')

		else:
			setting['value'] = value

	@property
	def _globalsettings(self):
		'''
		Return (and generate if needed) the complete list of global settings.

		Returns
		-------
		raw_globalsettings : list
			The global settings.
		'''

		if not(self._raw_globalsettings):
			self.generateGlobalSettings()

		return self._raw_globalsettings

	@property
	def _settings(self):
		'''
		Return (and generate if needed) the complete list of settings.

		Returns
		-------
		raw_settings : list
			The settings.
		'''

		if not(self._raw_settings):
			self.generateSettings()

		return self._raw_settings

	@property
	def _settings_dict(self):
		'''
		Return (and generate if needed) the complete list of settings as a dictionary.

		Returns
		-------
		raw_settings : dict
			The settings.
		'''

		if not(self._raw_settings_dict):
			self.generateSettings()

		return self._raw_settings_dict

	@property
	def settings(self):
		'''
		Return the complete list of sets of settings to use, as dictionaries.
		The settings with `exclude` to `True` are ignored.

		Returns
		-------
		settings : list
			List of sets of settings.
		'''

		return [
			{s.name: s.value for s in settings_set if not(s.exclude)}
			for settings_set in self._settings
		]

	@property
	def settings_dict(self):
		'''
		Return a dictionary with the complete list of sets of settings to use, as dictionaries.
		The settings with `exclude` to `True` are ignored.

		Returns
		-------
		settings : dict
			List of sets of settings.
		'''

		return {
			settings_set_name: [
				{s.name: s.value for s in settings_set if not(s.exclude)}
				for settings_set in settings_sets
			]
			for settings_set_name, settings_sets in self._settings_dict.items()
		}

	@property
	def settings_as_strings(self):
		'''
		Return the complete list of sets of settings to use, as strings.
		Take into account the `only_if` parameter.

		Returns
		-------
		settings : list
			Settings, generated according to their pattern.
		'''

		return [
			[str(s) for s in settings_set if s.shouldBeDisplayed()]
			for settings_set in self._settings
		]

	@property
	def reduced_globalsettings(self):
		'''
		Return the list of global settings, as a name: value dictionary.

		Returns
		-------
		settings : dict
			The global settings.
		'''

		return {setting['name']: setting['value'] for setting in self._globalsettings}

	@property
	def reduced_settings(self):
		'''
		Return the list of settings, as a name: value dictionary.
		Ignore multiple occurrences of the same setting.

		Returns
		-------
		settings : dict
			The settings.
		'''

		return functools.reduce(lambda a, b: {**a, **b}, self.settings)

	@property
	def settings_counters(self):
		'''
		Return the current settings global and local counters.

		Returns
		-------
		counters : dict
			The counters.
		'''

		return self._settings_counters

	@property
	def command_line(self):
		'''
		Return the command line to use to generate this simulation.

		Returns
		-------
		command_line : str
			The command line to execute.
		'''

		return ' '.join([self._folder.settings['exec']] + sum(self.settings_as_strings, []))

	@property
	def _setting_tag_regex(self):
		'''
		Regex to detect whether there is a setting or global setting tag in a string.

		Returns
		-------
		regex : re.Pattern
			The setting tag regex.
		'''

		if self._setting_tag_regex_compiled is None:
			self._setting_tag_regex_compiled = re.compile(r'\{(?P<category>(?:global)?setting):(?P<name>[^}]+)\}')

		return self._setting_tag_regex_compiled

	@property
	def _eval_tag_regex(self):
		'''
		Regex to detect whether we need to evaluate a part of a string.

		Returns
		-------
		regex : re.Pattern
			The eval tag regex.
		'''

		# The `\)*` part is needed so we don't have troubles with functions calls right before the end of a string.
		# Without this, such calls (e.g. in "((sqrt(16)))") end the string prematurely.

		if self._eval_tag_regex_compiled is None:
			self._eval_tag_regex_compiled = re.compile(r'\(\((.*?\)*)\)\)')

		return self._eval_tag_regex_compiled

	def _incrementSettingCounters(self, setting_name, set_name):
		'''
		Update the global counter of a setting.

		Parameters
		----------
		setting_name : str
			Name of the setting.

		set_name : str
			Name of the set the setting belongs to.
		'''

		for counters_dict in [self._settings_counters['global'], self._settings_counters['sets'][set_name]]:
			try:
				counters_dict[setting_name] += 1

			except KeyError:
				counters_dict[setting_name] = 0

	def generateGlobalSettings(self):
		'''
		Generate the full list of global settings.
		'''

		self._raw_globalsettings = []

		for setting in self._folder.settings['globalsettings']:
			self._raw_globalsettings.append({
				'name': setting['name'],
				'value': self._folder.applyFixers(self._user_settings[setting['name']]) if setting['name'] in self._user_settings else setting['default']
			})

		self.parseGlobalSettings()

	def generateSettings(self):
		'''
		Generate the full list of settings, taking into account the user settings and the default values in the folder.
		The "raw settings" are generated.
		Each set of settings is a list of all settings in this set.
		'''

		if type(self._user_settings['settings']) is list:
			user_settings = {
				setting_set_name: [s['settings'] for s in self._user_settings['settings'] if s['set'] == setting_set_name]
				for setting_set_name in set([s['set'] for s in self._user_settings['settings']])
			}

		else:
			user_settings = self._user_settings['settings']

		default_pattern = self._folder.settings['setting_pattern']

		self._raw_settings_dict = {}
		self._settings_counters = {'global': {}, 'sets': {}}

		for settings_set in self._folder.settings['settings']:
			self._settings_counters['sets'][settings_set['set']] = {}

			default_settings = [
				SimulationSetting(self._folder, settings_set['set'], s['name'], self)
				for s in settings_set['settings']
			]

			try:
				values_sets = user_settings[settings_set['set']]

			except KeyError:
				if settings_set['required']:
					for setting in default_settings:
						self._incrementSettingCounters(setting.name, settings_set['set'])
						setting.setIndexes()

					self._raw_settings_dict[settings_set['set']] = [default_settings]

			else:
				if not(type(values_sets) is list):
					values_sets = [values_sets]

				self._raw_settings_dict[settings_set['set']] = []

				for values_set in values_sets:
					set_to_add = copy.deepcopy(default_settings)

					for setting in set_to_add:
						self._incrementSettingCounters(setting.name, settings_set['set'])
						setting.setIndexes()

						try:
							setting.value = values_set[setting.name]

						except KeyError:
							pass

					self._raw_settings_dict[settings_set['set']].append(set_to_add)

		self._raw_settings = sum(self._raw_settings_dict.values(), [])
		self.parseSettings()

	def parseString(self, s):
		'''
		Parse a string to take into account possible settings.
		The tag `{setting:name}` is replaced by the value of the simulation's setting named `name`.
		The tag `{globalsetting:name}` is replaced by the value of the global setting named `name`.

		Tags are replaced recursively.

		Parameters
		----------
		s : str
			The string to parse.

		Returns
		-------
		parsed : mixed
			The parsed string, or a copy of the setting if the whole string is just one tag.
		'''

		# If the string is not a string, we don't have anything to do (seems reasonable!)
		# Then, we test if the string represents a number, so we can cast it

		if not(type(s) is str):
			return s

		try:
			return float(s)

		except ValueError:
			pass

		s = s.strip()

		# We search for settings tags in the string, and recursively replace them

		settings = {
			'setting': self.reduced_settings,
			'globalsetting': self.reduced_globalsettings
		}

		fullmatch = self._setting_tag_regex.fullmatch(s)

		if fullmatch:
			try:
				return copy.deepcopy(settings[fullmatch.group('category')][fullmatch.group('name')])

			except KeyError:
				return s

		def replaceSettingTag(match):
			'''
			Replace a setting tag by the value of the right setting.
			To be called by `re.sub()`.

			Parameters
			----------
			match : re.Match
				Match object corresponding to a setting tag.

			Returns
			-------
			setting_value : str
				The value of the setting.
			'''

			try:
				return str(settings[match.group('category')][match.group('name')])

			except KeyError:
				return match.group(0)

		parsed = self._setting_tag_regex.sub(replaceSettingTag, s)

		self._parser_recursion_stack.append(s)

		if not(parsed in self._parser_recursion_stack):
			return self.parseString(parsed)

		self._parser_recursion_stack.clear()

		# Final step: we try to evaluate the needed parts of the string to apply allowed operations, if any.
		# ValueError is raised if the string contains any unallowed operation, like the use of exec() or other evil functions.

		try:
			fullmatch = self._eval_tag_regex.fullmatch(parsed)

			if fullmatch:
				parsed = string.safeEval(fullmatch.group(1))

			else:
				parsed = self._eval_tag_regex.sub(lambda m: str(string.safeEval(m.group(1))), parsed)

		except (SyntaxError, ValueError):
			pass

		return parsed

	def parseGlobalSettings(self):
		'''
		Parse the global settings to take into account possible other settings' values.
		'''

		for setting in self._globalsettings:
			setting['value'] = self.parseString(setting['value'])

	def parseSettings(self):
		'''
		Parse the settings to take into account possible other settings' values.
		'''

		for settings_set in self._settings:
			for setting in settings_set:
				setting.value = self.parseString(setting.value)

class SimulationSetting():
	'''
	Represent a simulation setting.

	Parameters
	----------
	folder : Folder
		The simulations folder this setting is part of.

	set_name : str
		Name of the set this setting is part of.

	setting_name : str
		Name of this setting.

	simulation : Simulation
		Simulation that uses this setting.

	Raises
	------
	SettingsSetNotFoundError
		The settings set has not been found.

	SettingNotFoundError
		The setting has not been found in the set.
	'''

	def __init__(self, folder, set_name, setting_name, simulation = None):
		self._folder = folder
		self._simulation = simulation

		try:
			self._settings_set_dict = [
				settings_set
				for settings_set in self._folder.settings['settings']
				if settings_set['set'] == set_name
			][0]

		except IndexError:
			raise SettingsSetNotFoundError(set_name)

		try:
			self._setting_dict = [
				setting
				for setting in self._settings_set_dict['settings']
				if setting['name'] == setting_name
			][0]

		except IndexError:
			raise SettingNotFoundError(set_name, setting_name)

		self._set_name = set_name
		self._name = self._setting_dict['name']
		self._value = self._setting_dict['default']
		self._exclude_for_db = 'exclude' in self._setting_dict and self._setting_dict['exclude']
		self._pattern = self._setting_dict['pattern'] if 'pattern' in self._setting_dict else self._folder.settings['setting_pattern']

		self._use_only_if = 'only_if' in self._setting_dict
		if self._use_only_if:
			self._only_if_value = self._setting_dict['only_if']

		self._fixers_dict = None
		self._namers_dict = None

	def __deepcopy__(self, memo):
		'''
		Override the default behavior of `deepcopy()` to keep the references to the Folder and the Simulation.
		'''

		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result

		for k, v in self.__dict__.items():
			if k in ['_folder', '_simulation']:
				setattr(result, k, v)

			else:
				setattr(result, k, copy.deepcopy(v, memo))

		return result

	def __str__(self):
		'''
		Return a string representing the setting and its value, according to the pattern.

		Returns
		-------
		setting : str
			The representation of the setting.
		'''

		return self._pattern.format(name = self.display_name, value = self.value)

	def setIndexes(self):
		'''
		Define the global and local indexes of this setting.
		'''

		self._global_index = self._simulation.settings_counters['global'][self._name]
		self._local_index = self._simulation.settings_counters['sets'][self._set_name][self._name]

	def _setModifier(self, modifier):
		'''
		Set a "modifier" property (fixers or namers).

		Parameters
		----------
		modifier : str
			Modifier to define.

		Returns
		-------
		modifier_functions : dict
			The functions to call, in the right order.
		'''

		modifier_functions = {'before': [], 'after': []}

		keys_to_search = {
			'before': [
				(self._setting_dict, ''),
				(self._settings_set_dict, ''),
				(self._setting_dict, '_between')
			],
			'after': [
				(self._setting_dict, '_between'),
				(self._settings_set_dict, ''),
				(self._setting_dict, '')
			]
		}

		for when, keys_path in keys_to_search.items():
			for dict_to_search, key_to_search in keys_path:
				try:
					modifier_functions[when] += dict_to_search[f'{modifier}{key_to_search}_{when}']

				except KeyError:
					pass

		return modifier_functions

	@property
	def _fixers(self):
		'''
		Get the fixers to apply to the value.

		Returns
		-------
		fixers : dict
			The list of fixers, in the right order.
		'''

		if self._fixers_dict is None:
			self._fixers_dict = self._setModifier('fixers')

		return self._fixers_dict

	@property
	def _namers(self):
		'''
		Get the namers to apply to the name.

		Returns
		-------
		namers : dict
			The list of namers, in the right order.
		'''

		if self._namers_dict is None:
			self._namers_dict = self._setModifier('namers')

		return self._namers_dict

	@property
	def name(self):
		'''
		Getter for the setting name.

		Returns
		-------
		name : str
			Name of the setting.
		'''

		return self._name

	@property
	def display_name(self):
		'''
		Get the name of the setting to use inside the simulation.

		Returns
		-------
		name : str
			Name to use.
		'''

		local_total = self._simulation.settings_counters['sets'][self._set_name][self._name] + 1
		global_total = self._simulation.settings_counters['global'][self._name] + 1

		return self._folder.applyNamers(self._name, self._local_index, local_total, self._global_index, global_total, **self._namers)

	@property
	def value(self):
		'''
		Getter for the setting value.

		Returns
		-------
		value : mixed
			Value of the setting.
		'''

		return self._value

	@value.setter
	def value(self, new_value):
		'''
		Setter for the setting value.

		Parameters
		----------
		new_value : mixed
			New value of the setting
		'''

		self._value = self._folder.applyFixers(new_value, **self._fixers)

	@property
	def exclude(self):
		'''
		Return `True` if the setting should be excluded to define a simulation.

		Returns
		-------
		exclude : bool
			Exclusion parameter.
		'''

		return self._exclude_for_db

	def shouldBeDisplayed(self):
		'''
		Return `True` if the setting can be displayed/used for the execution.
		This check is based on the `only_if` parameter. There are several cases for the test string.

		1. It is a full test (e.g. `a < b`): we execute it as it is.
		2. It begins by a conditional operator (<, <=, >, >=, ==, !=, in): we test against the setting value.
		3. It does not contain any conditional operator: we test the equality against the setting value.

		Returns
		-------
		should_be_displayed : bool
			The result of the check.
		'''

		if not(self._use_only_if):
			return True

		if type(self._only_if_value) is str:
			first_operator_match = re.search(r'([<>]=?|[!=]=|in)', self._only_if_value.strip())

			if first_operator_match:
				if first_operator_match.start() > 0:
					return self._simulation.parseString(f'(({self._only_if_value}))')

				return self._simulation.parseString(f'(({self.value} {self._only_if_value}))')

			return self.value == self._simulation.parseString(self._only_if_value)

		return self.value == self._only_if_value
