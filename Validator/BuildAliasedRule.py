import Validator

class BuildAliasedRule(object):
    def __init__(self, source, alias):
        if not isinstance(alias, dict):
            raise Exception('Wrong alias format. Dict required')
        if not 'name' in alias:
            raise Exception('Alias name required')
        if not 'rules' in alias:
            raise Exception('Alias rules required')
        if 'error' in alias:
            self._error = alias['error']
        else:
            self._error = None

        self._livr = {'value': alias['rules']}
        source[alias['name']] = self

    def __call__(self, *args):
        self.__rule_builders = args[0]
        self.__validator = Validator.Validator(self._livr)

        self.__validator.register_rules(self.__rule_builders)
        self.__validator.prepare()

        return self._validate

    def _validate(self, value, output):
        result = self.__validator.validate({'value': value})

        if result:
            output.append(result['value'])
        else:
            if self._error:
                return self._error
            return self.__validator.get_errors()
