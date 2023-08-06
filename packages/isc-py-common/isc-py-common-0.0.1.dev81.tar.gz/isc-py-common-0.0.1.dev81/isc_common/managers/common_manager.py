from django.db import transaction
from django.db.models import Manager, QuerySet, Q
from django.forms import model_to_dict

from isc_common import getAttr, delAttr, setAttr
from isc_common.http.DSRequest import DSRequest


class CommonQuerySet(QuerySet):

    def get_field(self, field_name):
        fld = [x for x in self.model._meta.fields if x.name == field_name]
        if len(fld) > 0:
            return fld[0]
        return None

    def get_id_tuple(self, group):
        iter = [x for x in group]
        # print(iter)
        res = [x[1] for x in iter if x[0][1] == 'id']
        if len(res) > 0:
            return res[0]
        return None

    def getRecord(self, record):
        return record

    def getOperator(self, operator):
        if operator == "and":
            return Q.AND
        elif operator == "or":
            return Q.OR
        elif operator == "equals":
            return "exact"
        elif operator == "iEquals":
            return "iexact"
        elif operator == "notEqual":
            return "exact"
        elif operator == "iNotEqual":
            return "iexact"
        elif operator == "greaterThan":
            return "gt"
        elif operator == "lessThan":
            return "lt"
        elif operator == "greaterOrEqual":
            return "gte"
        elif operator == "lessOrEqual":
            return "lte"
        elif operator == "contains":
            return "contains"
        elif operator == "startsWith":
            return "startswith"
        elif operator == "endsWith":
            return "endswith"
        elif operator == "iContains":
            return "icontains"
        elif operator == "iStartsWith":
            return "istartswith"
        elif operator == "iEndsWith":
            return "iendswith"
        elif operator == "notContains":
            return "contains"
        elif operator == "notStartsWith":
            return "startswith"
        elif operator == "notEndsWith":
            return "endswith"
        elif operator == "iNotContains":
            return "icontains"
        elif operator == "iNotStartsWith":
            return "istartswith"
        elif operator == "iNotEndsWith":
            return "endswith"
        elif operator == "iBetween":
            return "range"
        elif operator == "iBetweenInclusive":
            return "range"
        elif operator == "matchesPattern":
            return "regex"
        elif operator == "iMatchesPattern":
            return "iregex"
        elif operator == "containsPattern":
            return "regex"
        elif operator == "startsWithPattern":
            return "regex"
        elif operator == "endsWithPattern":
            return "regex"
        elif operator == "iContainsPattern":
            return "iregex"
        elif operator == "iStartsWithPattern":
            return "iregex"
        elif operator == "iEndsWithPattern":
            return "iregex"
        elif operator == "regexp":
            return "regex"
        elif operator == "iregexp":
            return "iregex"
        elif operator == "isBlank":
            return "isblank"
        elif operator == "notBlank":
            return "notblank"
        elif operator == "isNull":
            return "isnull"
        elif operator == "notNull":
            return "notnull"
        elif operator == "inSet":
            return "in"
        elif operator == "notInSet":
            return "in"
        # elif operator == "equalsField":
        #     return ""
        # elif operator == "notEqualField":
        #     return ""
        # elif operator == "iEqualsField":
        #     return ""
        # elif operator == "iNotEqualField":
        #     return ""
        # elif operator == "greaterThanField":
        #     return ""
        # elif operator == "lessThanField":
        #     return ""
        # elif operator == "greaterOrEqualField":
        #     return ""
        # elif operator == "lessOrEqualField":
        #     return ""
        # elif operator == "containsField":
        #     return ""
        # elif operator == "startsWithField":
        #     return ""
        # elif operator == "endsWithField":
        #     return ""
        # elif operator == "iContainsField":
        #     return ""
        # elif operator == "iStartsWithField":
        #     return ""
        # elif operator == "iEndsWithField":
        #     return ""
        # elif operator == "notContainsField":
        #     return ""
        # elif operator == "notStartsWithField":
        #     return ""
        # elif operator == "notEndsWithField":
        #     return ""
        # elif operator == "iNotContainsField":
        #     return ""
        # elif operator == "iNotStartsWithField":
        #     return ""
        # elif operator == "iNotEndsWithField":
        #     return ""
        # elif operator == "not":
        #     return ""
        elif operator == "between":
            return "range"
        elif operator == "nbetweenInclusiveot":
            return "range"
        else:
            raise Exception(f'Неизветный operator: {operator}')

    def isNotOperator(self, operator):
        if operator == "notEqual":
            return True
        if operator == "iNotEqual":
            return True
        if operator == "notContains":
            return True
        if operator == "notStartsWith":
            return True
        if operator == "notEndsWith":
            return True
        if operator == "iNotContains":
            return True
        if operator == "iNotStartsWith":
            return True
        if operator == "iNotEndsWith":
            return True
        if operator == "notBlank":
            return True
        if operator == "notNull":
            return True
        if operator == "notInSet":
            return True
        if operator == "notEqualField":
            return True
        if operator == "iNotEqualField":
            return True
        if operator == "notContainsField":
            return True
        if operator == "notStartsWithField":
            return True
        if operator == "notEndsWithField":
            return True
        if operator == "iNotContainsField":
            return True
        if operator == "iNotStartsWithField":
            return True
        if operator == "iNotEndsWithField":
            return True
        if operator == "not":
            return True
        else:
            return False

    def textMatchStyleMapping(self, textMatchStyle):
        if textMatchStyle == 'exact':
            return 'iexact'
        elif textMatchStyle == 'exactCase':
            return 'exact'
        elif textMatchStyle == 'substring':
            return 'icontains'
        elif textMatchStyle == 'startsWith':
            return 'istartswith'
        else:
            raise Exception(f'Неизветный textMatchStyle: {textMatchStyle}')

    def getValue(self, criterion):
        value = getAttr(criterion, 'value')
        operator = getAttr(criterion, 'operator')
        if value == None:
            if operator == "isNull":
                return True
            elif operator == "notNull":
                return True
            elif operator == "isBlank":
                return "''"
            elif operator == "notBlank":
                return "''"
            else:
                return value

        if isinstance(value, str):
            return value
        elif isinstance(value, int):
            return value
        else:
            raise Exception(f'Неизветный value: {value}')

    def getCriteria(self, crireria, operator):
        res = Q()
        if isinstance(crireria, list):
            for criterion in crireria:
                _criteria = getAttr(criterion, "criteria")
                if _criteria:
                    if self.isNotOperator(operator):
                        res.add(~Q(self.getCriteria(_criteria, getAttr(criterion, "operator")), operator))
                    else:
                        res.add(Q(self.getCriteria(_criteria, getAttr(criterion, "operator")), operator))
                elif getAttr(criterion, 'fieldName') != 'ts':
                    _operator = self.getOperator(getAttr(criterion, 'operator'))
                    if _operator == "notnull":
                        _operator = "isnull"

                    if _operator == 'isblank' or _operator == 'notblank':
                        _operator = ''
                    else:
                        _operator = f'__{_operator}'

                    if self.isNotOperator(getAttr(criterion, 'operator')):
                        res.add(~Q(**{f"{getAttr(criterion, 'fieldName')}{_operator}": self.getValue(criterion)}), operator)
                    else:
                        res.add(Q(**{f"{getAttr(criterion, 'fieldName')}{_operator}": self.getValue(criterion)}), operator)

        return res

    def get_criteria(self, json=None):
        data = getAttr(json, 'data')
        delAttr(data, 'ts')

        # fields_name = [field.name for field in self.model._meta.fields]
        for key, value in data.items():
            if key.find('__id') == -1 and key.find('_id') != -1:
                delAttr(data, key)
                setAttr(data, key.replace('_id', '__id'), value)

        # todo Удалить несуществующие поля
        criteria = Q()
        operator = Q.AND

        if getAttr(data, '_constructor') == 'AdvancedCriteria':
            operator = self.getOperator(getAttr(data, "operator"))
            _criteria = getAttr(data, "criteria")
            if self.isNotOperator(getAttr(data, "operator")):
                criteria.add(~Q(self.getCriteria(_criteria, operator)), operator)
            else:
                criteria.add(Q(self.getCriteria(_criteria, operator)), operator)
        else:
            # "exact"	case-insensitive exact match ("foo" matches "foo" and "FoO", but not "FooBar")  iexact
            # "exactCase"	case-sensitive exact match ("foo" matches only "foo")                       exact
            # "substring"	case-insenstive substring match ("foo" matches "foobar" and "BarFoo")       icontains
            # "startsWith"	case-insensitive prefix match ("foo" matches "FooBar" but not "BarFoo")     istartswith
            textMatchStyle = self.textMatchStyleMapping(getAttr(json, 'textMatchStyle'))
            for key, value in data.items():
                if isinstance(value, list):
                    criteria.add(Q(**{f"{key}__in": value}), operator)
                else:
                    if textMatchStyle == "iexact" and isinstance(value, int):
                        textMatchStyle = "exact"

                    criteria.add(Q(**{f"{key}__{textMatchStyle}": value}), operator)
        return criteria

    def get_range_rows(self, start=None, end=None, function=None, json=None, *args, **kwargs):
        criteria = self.get_criteria(json=json)

        ob = getAttr(json, "sortBy", [])

        if start is not None and end is not None:
            queryResult = super().order_by(*ob).filter(*args, criteria).distinct()[start:end]
        elif start is not None and end is None:
            queryResult = super().order_by(*ob).filter(*args, criteria).distinct()[start:]
        elif end is not None and start is None:
            queryResult = super().order_by(*ob).filter(*args, criteria).distinct()[:end]
        else:
            queryResult = super().order_by(*ob).filter(*args, criteria).distinct()

        if function:
            res = [function(record) for record in queryResult]
            return res
        else:
            res = [model_to_dict(record) for record in queryResult]
            return res

    def get_range_rows1(self, request, function=None):
        request = DSRequest(request=request)
        return self.get_range_rows(start=request.startRow, end=request.endRow, function=function, json=request.json)

    def get_info(self, request, *args):
        request = DSRequest(request=request)
        criteria = self.get_criteria(json=request.json)
        queryResult = super().filter(*args, criteria)
        return dict(qty_rows=len(queryResult))


class CommonManager(Manager):
    def get_field(self, field_name):
        fld = [x for x in self.model._meta.fields if x.name == field_name]
        if len(fld) > 0:
            return fld[0]
        return None

    def get_queryset(self):
        return CommonQuerySet(self.model, using=self._db)

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        delAttr(_data, 'dataSource')
        delAttr(_data, 'operationType')
        delAttr(_data, 'textMatchStyle')
        delAttr(_data, 'form')

        res = super().create(**_data)
        data.update(model_to_dict(res))
        return data

    def updateFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        super().filter(id=request.get_id()).update(**data)
        return data

    def lookupFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()

        _data = dict()
        _key = None

        for key, value in data.items():
            if value == 'null':
                setAttr(_data, key[key.find('__') + 2:], None)
            else:
                setAttr(_data, key[key.find('__') + 2:], value)
            _key = key[: key.find('__')]
            break

        field = self.get_field(_key)
        if field.null and value == 'null':
            setAttr(_data, 'id', None)
            res = _data
        else:
            res = field.related_model.objects.get(**_data)
            res = model_to_dict(res)

        _res = {}
        for key, value in res.items():
            if not isinstance(value, list) and not isinstance(value, dict):
                setAttr(_res, key, value)
        return _res

    def deleteFromRequest(self, request):
        request = DSRequest(request=request)
        return super().filter(id=request.get_id()).delete()

    def get_ex(self, *args, **kwargs):
        """
        Perform the query and return a single object matching the given
        keyword arguments.
        """
        clone = super().get_queryset().filter(*args, **kwargs)
        num = len(clone)
        if num >= 1:
            return clone._result_cache
        if not num:
            return None
        return None
