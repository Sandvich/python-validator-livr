import sys
import os
ROOT_PATH = '/'.join(str(os.path.abspath(__file__)).split('/')[:-3])
sys.path.insert(0,ROOT_PATH)

import Validator

class NestedObject(object):
    def __init__(self, *args):
            self._livr = args[1]
            self._rule_builders = args[0]
            self._validator = Validator.Validator(self._livr)

            self._validator.register_rules(self._rule_builders)
            self._validator.prepare()

    def __call__(self, nested_obj, unuse, output):
        if not nested_obj or nested_obj == 0:
            return
        if not isinstance(nested_obj, dict):
            return 'FORMAT_ERROR'

        result = self._validator.validate(nested_obj)

        if not result:  
            return self._validator.get_errors()

        output.append(result) 

class ListOf(object):
    def __init__(self, *args):
        self._livr = args[1]
        self._rule_builders = args[0]
        self._validator = Validator.Validator({'field':self._livr})

        self._validator.register_rules(self._rule_builders)
        self._validator.prepare()

    def __call__(self, values, unuse, output):   
        if not values or values == 0:
            return
        if not isinstance(values, dict) and not isinstance(values, list):
            return 'FORMAT_ERROR'
        return self._check_validation(values, output)

    def _check_validation(self, values, output):
        results = []
        errors = []
        error_flag = False

        for val in values:
            result = self._validator.validate({'field': val})
            
            if result:
                results.append(result['field'])
                errors.append(None)
            else:
                error_flag = True
                errors.append(self._validator.get_errors()['field'])

        if error_flag:
            return errors

        output.append(results)

class ListOfObjects(object):
    def __init__(self, *args):
        self._livr = args[1]
        self._rule_builders = args[0]
        self._validator = Validator.Validator(self._livr)

        self._validator.register_rules(self._rule_builders)
        self._validator.prepare()

    def __call__(self, objects, unuse, output):
        if objects == None or objects == '':
            return
        if not isinstance(objects, dict) and not isinstance(objects, list):
            return 'FORMAT_ERROR'   

        return self._check_validation(objects, output)

    def _check_validation(self, objects, output):
        results = []
        errors = []
        error_flag = False

        for obj in objects:
            if not isinstance(obj, dict):
                errors.append('FORMAT_ERROR')
                continue

            result = self._validator.validate(obj)
            
            if result:
                results.append(result)
                errors.append(None)
            else:
                error_flag = True
                errors.append(self._validator.get_errors())

        if error_flag:
            return errors

        output.append(results)

class ListOfDiferentObjects(object):
    def __init__(self, *args):
        self._selector_fields = args[1]
        self._livrs = args[2]
        self._rule_builders = args[0]
        self._validators = {}


        for selector, livr in self._livrs.iteritems():
            validator = Validator.Validator(livr)
            
            validator.register_rules(self._rule_builders)
            validator.prepare()
            self._validators[selector] = validator

    def __call__(self, objects, unuse, output):
        results = []
        errors = []
        error_flag = False

        if not objects or objects == 0:
            return
        if not isinstance(objects, list):
            return 'FORMAT_ERROR'

        for obj in objects:
            if not isinstance(obj, dict) and not self._selector_fields in obj:
                errors.append("FORMAT_ERROR")
                continue
            if not obj[self._selector_fields] in self._validators:
                errors.append("FORMAT_ERROR")
                continue

            validator = self._validators[obj[self._selector_fields]]
            result = validator.validate(obj)

            if result:
                results.append(result)
                errors.append(None)
            else:
                error_flag = True
                errors.append(validator.get_errors())
        
        if error_flag:
            return errors

        output.append(results)


