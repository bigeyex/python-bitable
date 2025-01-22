from datetime import datetime

def to_date(date_text):
    d = datetime.strptime(date_text, "%Y-%m-%d")
    return int(d.timestamp() * 1000)

class WhereConditionException(Exception):
    pass

def wrap_and_filter(filter_object):
    return {
        "conjunction": "and",
        "conditions": [
            filter_object
        ]
    }

def make_filter(where, fields):
    # if where is dict with 2+ items, wrap with And
    # if where is dict with 1 item, wrap with Equal
    if isinstance(where, dict):
        if len(where) == 1:
            k, v = list(where.items())[0]
            return Equal(k, v).make_filter_object(fields)
        else:
            return And(*[Equal(k, v) for k, v in where.items()]).make_filter_object(fields)
    elif isinstance(where, Conjunction):
        # if where is Conjunction or Operator, make filter object
        return where.make_filter_object(fields)
    elif isinstance(where, Operator):
        return where.make_filter_object(fields)
    else:
        raise WhereConditionException('where condition is not supported')
    
class Conjunction:
    conjunction = None
    def __init__(self, *args):
        self.children = args

    def make_filter_object(self, fields):
        if self.conjunction is None:
            raise WhereConditionException('conjunction base class cannot be used')
        # if some of children are conjunction, use children expression, wrap single child with And
        if any(isinstance(child, Conjunction) for child in self.children):
            return {
                "conjunction": self.conjunction,
                "children": [child.make_filter_object(fields) if isinstance(child, Conjunction) else And(child).make_filter_object(fields)
                                for child in self.children]
            }
        else: 
            return {
                "conjunction": self.conjunction,
                "conditions": [child.make_filter_object(fields) for child in self.children]
            }


class Operator: 
    operator = None
    support_date = True
    def __init__(self, field_name, value=None):
        self.field_name = field_name
        self.value = value

    def make_filter_object(self, fields):
        if self.operator is None:
            raise WhereConditionException('operator base class cannot be used')
        if fields[self.field_name]['type'] == 'DateTime':
            if self.support_date:
                value = None
                if isinstance(self.value, SpecialDate):
                    value = [self.value.date_name]
                else: 
                    value = [to_date(self.value)]
                return {
                    "operator": self.operator,
                    "field_name": self.field_name,
                    "value": value
                }
            else: # date not supported
                raise WhereConditionException('date not supported in operator', self.__class__)
        if not isinstance(self.value, list):
            self.value = [self.value]
            return {
                "field_name": self.field_name,
                "operator": self.operator,
                "value": self.value
            }



class SpecialDate:
    date_name = None


# conjunctions
class And(Conjunction):
    conjunction = 'and'

class Or(Conjunction):
    conjunction = 'or'


# filters
class Equal(Operator):
    operator = 'is'

class Not(Operator):
    operator = 'isNot'
    support_date = False

class Contain(Operator):
    operator = 'contains'
    support_date = False

class NotContain(Operator):
    operator = 'doesNotContain'
    support_date = False

class Empty(Operator):
    operator = 'isEmpty'

class NotEmpty(Operator):
    operator = 'isNotEmpty'

class Greater(Operator):
    operator = 'isGreater'

class GreaterEqual(Operator):
    operator = 'isGreaterEqual'
    support_date = False

class Less(Operator):
    operator = 'isLess'

class LessEqual(Operator):
    operator = 'isLessEqual'
    support_date = False

# special dates
class Today(SpecialDate):
    date_name = "Today"

class Yesterday(SpecialDate):
    date_name = "Yesterday"

class Tomorrow(SpecialDate):
    date_name = "Tomorrow"

class CurrentWeek(SpecialDate):
    date_name = "CurrentWeek"

class LastWeek(SpecialDate):
    date_name = "LastWeek"

class CurrentMonth(SpecialDate):
    date_name = "CurrentMonth"

class LastMonth(SpecialDate):
    date_name = "LastMonth"

class Past7Days(SpecialDate):
    date_name = "TheLastWeek"

class Next7Days(SpecialDate):
    date_name = "TheNextWeek"

class Past30Days(SpecialDate):
    date_name = "TheLastMonth"

class Next30Days(SpecialDate):
    date_name = "TheNextMonth"

    

