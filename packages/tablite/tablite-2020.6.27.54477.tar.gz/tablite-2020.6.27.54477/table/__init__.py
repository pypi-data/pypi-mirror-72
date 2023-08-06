# import zlib
import json
# import xlrd
# from time import process_time_ns
from itertools import count
from datetime import datetime, date, time
from functools import lru_cache
from collections import defaultdict
# from pathlib import Path


class DataTypes(object):
    # supported datatypes.
    int = int
    str = str
    float = float
    bool = bool
    date = date
    datetime = datetime
    time = time

    # reserved keyword for Nones:
    digits = '1234567890'
    decimals = set('1234567890-+eE.')
    integers = set('1234567890-+')
    nones = {'null', 'Null', 'NULL', '#N/A', '#n/a', "", 'None', None}

    date_formats = {  # Note: Only recognised ISO8601 formats are accepted.
        "NNNN-NN-NN": lambda x: date(*(int(i) for i in x.split("-"))),
        "NNNN-N-NN": lambda x: date(*(int(i) for i in x.split("-"))),
        "NNNN-NN-N": lambda x: date(*(int(i) for i in x.split("-"))),
        "NNNN-N-N": lambda x: date(*(int(i) for i in x.split("-"))),
        "NN-NN-NNNN": lambda x: date(*[int(i) for i in x.split("-")][::-1]),
        "N-NN-NNNN": lambda x: date(*[int(i) for i in x.split("-")][::-1]),
        "NN-N-NNNN": lambda x: date(*[int(i) for i in x.split("-")][::-1]),
        "N-N-NNNN": lambda x: date(*[int(i) for i in x.split("-")][::-1]),
        "NNNN.NN.NN": lambda x: date(*(int(i) for i in x.split("."))),
        "NNNN.N.NN": lambda x: date(*(int(i) for i in x.split("."))),
        "NNNN.NN.N": lambda x: date(*(int(i) for i in x.split("."))),
        "NNNN.N.N": lambda x: date(*(int(i) for i in x.split("."))),
        "NN.NN.NNNN": lambda x: date(*[int(i) for i in x.split(".")][::-1]),
        "N.NN.NNNN": lambda x: date(*[int(i) for i in x.split(".")][::-1]),
        "NN.N.NNNN": lambda x: date(*[int(i) for i in x.split(".")][::-1]),
        "N.N.NNNN": lambda x: date(*[int(i) for i in x.split(".")][::-1]),
        "NNNN/NN/NN": lambda x: date(*(int(i) for i in x.split("/"))),
        "NNNN/N/NN": lambda x: date(*(int(i) for i in x.split("/"))),
        "NNNN/NN/N": lambda x: date(*(int(i) for i in x.split("/"))),
        "NNNN/N/N": lambda x: date(*(int(i) for i in x.split("/"))),
        "NN/NN/NNNN": lambda x: date(*[int(i) for i in x.split("/")][::-1]),
        "N/NN/NNNN": lambda x: date(*[int(i) for i in x.split("/")][::-1]),
        "NN/N/NNNN": lambda x: date(*[int(i) for i in x.split("/")][::-1]),
        "N/N/NNNN": lambda x: date(*[int(i) for i in x.split("/")][::-1]),
        "NNNN NN NN": lambda x: date(*(int(i) for i in x.split(" "))),
        "NNNN N NN": lambda x: date(*(int(i) for i in x.split(" "))),
        "NNNN NN N": lambda x: date(*(int(i) for i in x.split(" "))),
        "NNNN N N": lambda x: date(*(int(i) for i in x.split(" "))),
        "NN NN NNNN": lambda x: date(*[int(i) for i in x.split(" ")][::-1]),
        "N N NNNN": lambda x: date(*[int(i) for i in x.split(" ")][::-1]),
        "NN N NNNN": lambda x: date(*[int(i) for i in x.split(" ")][::-1]),
        "N NN NNNN": lambda x: date(*[int(i) for i in x.split(" ")][::-1]),
        "NNNNNNNN": lambda x: date(*(int(x[:4]), int(x[4:6]), int(x[6:]))),
    }

    datetime_formats = {  # Note: Only recognised ISO8601 formats are accepted.

        # year first
        'NNNN-NN-NNTNN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x),  # -T
        'NNNN-NN-NNTNN:NN': lambda x: DataTypes.pattern_to_datetime(x),

        'NNNN-NN-NN NN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, T=" "),  # - space
        'NNNN-NN-NN NN:NN': lambda x: DataTypes.pattern_to_datetime(x, T=" "),

        'NNNN/NN/NNTNN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/'),  # / T
        'NNNN/NN/NNTNN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/'),

        'NNNN/NN/NN NN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', T=" "),  # / space
        'NNNN/NN/NN NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', T=" "),

        'NNNN NN NNTNN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd=' '),  # space T
        'NNNN NN NNTNN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd=' '),

        'NNNN NN NN NN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd=' ', T=" "),  # space
        'NNNN NN NN NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd=' ', T=" "),

        # day first
        'NN-NN-NNNNTNN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='-', T=' ', day_first=True),  # - T
        'NN-NN-NNNNTNN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='-', T=' ', day_first=True),

        'NN-NN-NNNN NN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='-', T=' ', day_first=True),  # - space
        'NN-NN-NNNN NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='-', T=' ', day_first=True),

        'NN/NN/NNNNTNN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', day_first=True),  # / T
        'NN/NN/NNNNTNN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', day_first=True),

        'NN/NN/NNNN NN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', T=' ', day_first=True),  # / space
        'NN/NN/NNNN NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', T=' ', day_first=True),

        'NN NN NNNNTNN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', day_first=True),  # space T
        'NN NN NNNNTNN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', day_first=True),

        'NN NN NNNN NN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', day_first=True),  # space
        'NN NN NNNN NN:NN': lambda x: DataTypes.pattern_to_datetime(x, ymd='/', day_first=True),

        # compact formats - type 1
        'NNNNNNNNTNNNNNN': lambda x: DataTypes.pattern_to_datetime(x, compact=1),
        'NNNNNNNNTNNNN': lambda x: DataTypes.pattern_to_datetime(x, compact=1),
        'NNNNNNNNTNN': lambda x: DataTypes.pattern_to_datetime(x, compact=1),
        # compact formats - type 2
        'NNNNNNNNNN': lambda x: DataTypes.pattern_to_datetime(x, compact=2),
        'NNNNNNNNNNNN': lambda x: DataTypes.pattern_to_datetime(x, compact=2),
        'NNNNNNNNNNNNNN': lambda x: DataTypes.pattern_to_datetime(x, compact=2),
        # compact formats - type 3
        'NNNNNNNNTNN:NN:NN': lambda x: DataTypes.pattern_to_datetime(x, compact=3),
    }

    @staticmethod
    def pattern_to_datetime(iso_string, ymd=None, T=None, compact=0, day_first=False):
        assert isinstance(iso_string, str)
        if compact:
            s = iso_string
            if compact == 1:  # has T
                slices = [(0, 4, "-"), (4, 6, "-"), (6, 8, "T"), (9, 11, ":"), (11, 13, ":"), (13, len(s), "")]
            elif compact == 2:  # has no T.
                slices = [(0, 4, "-"), (4, 6, "-"), (6, 8, "T"), (8, 10, ":"), (10, 12, ":"), (12, len(s), "")]
            elif compact == 3:  # has T and :
                slices = [(0, 4, "-"), (4, 6, "-"), (6, 8, "T"), (9, 11, ":"), (12, 14, ":"), (15, len(s), "")]
            else:
                raise TypeError
            iso_string = "".join([s[a:b] + c for a, b, c in slices if b <= len(s)])
            iso_string = iso_string.rstrip(":")

        if day_first:
            s = iso_string
            iso_string = "".join((s[6:10], "-", s[3:5], "-", s[0:2], s[10:]))

        if "," in iso_string:
            iso_string = iso_string.replace(",", ".")

        dot = iso_string[::-1].find('.')
        if 0 < dot < 10:
            ix = len(iso_string) - dot
            microsecond = int(float(f"0{iso_string[ix - 1:]}") * 10 ** 6)
            iso_string = iso_string[:len(iso_string) - dot] + str(microsecond).rjust(6, "0")
        if ymd:
            iso_string = iso_string.replace(ymd, '-', 2)
        if T:
            iso_string = iso_string.replace(T, "T")
        return datetime.fromisoformat(iso_string)

    @staticmethod
    def to_json(v):
        if v is None:
            return v
        if isinstance(v, int):
            return v
        elif isinstance(v, str):
            return v
        elif isinstance(v, float):
            return v
        elif isinstance(v, bool):
            return str(v)
        elif isinstance(v, date):
            return v.isoformat()
        elif isinstance(v, time):
            return v.isoformat()
        elif isinstance(v, datetime):
            return v.isoformat()
        else:
            raise TypeError(f"The datatype {type(v)} is not supported.")

    @staticmethod
    def from_json(v, dtype):

        if v in DataTypes.nones:
            if dtype is str and v == "":
                return ""
            else:
                return None
        if dtype is int:
            return int(v)
        elif dtype is str:
            return str(v)
        elif dtype is float:
            return float(v)
        elif dtype is bool:
            return bool(v)
        elif dtype is date:
            return date.fromisoformat(v)
        elif dtype is datetime:
            return datetime.fromisoformat(v)
        elif dtype is time:
            return time.fromisoformat(v)
        else:
            raise TypeError(f"The datatype {str(dtype)} is not supported.")

    @staticmethod
    @lru_cache(maxsize=256)
    def infer(v, dtype):
        if v is DataTypes.nones:
            return None
        if dtype is int:
            return DataTypes._infer_int(v)
        elif dtype is str:
            return DataTypes._infer_str(v)
        elif dtype is float:
            return DataTypes._infer_float(v)
        elif dtype is bool:
            return DataTypes._infer_bool(v)
        elif dtype is date:
            return DataTypes._infer_date(v)
        elif dtype is datetime:
            return DataTypes._infer_datetime(v)
        elif dtype is time:
            return DataTypes._infer_time(v)
        else:
            raise TypeError(f"The datatype {str(dtype)} is not supported.")

    @staticmethod
    def _infer_bool(value):
        if isinstance(value, bool):
            return value
        elif isinstance(value, int):
            raise ValueError("it's an integer.")
        elif isinstance(value, float):
            raise ValueError("it's a float.")
        elif isinstance(value, str):
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
            else:
                raise ValueError
        else:
            raise ValueError

    @staticmethod
    def _infer_int(value):
        if isinstance(value, bool):
            raise ValueError("it's a boolean")
        if isinstance(value, int):
            return value
        elif isinstance(value, float):
            if int(value) == value:
                return int(value)
            raise ValueError("it's a float")
        elif isinstance(value, str):
            value = value.replace('"', '').replace(" ", "")
            value_set = set(value)
            if value_set - DataTypes.integers:  # set comparison.
                raise ValueError
            return int(float(value))
        else:
            raise ValueError

    @staticmethod
    def _infer_float(value):
        if isinstance(value, int):
            raise ValueError("it's an integer")
        if isinstance(value, float):
            return value
        elif isinstance(value, str):
            value = value.replace('"', '')
            dot_index, comma_index = value.find('.'), value.find(',')
            if 0 < dot_index < comma_index:  # 1.234,567
                value = value.replace('.', '')  # --> 1234,567
                value = value.replace(',', '.')  # --> 1234.567
            elif dot_index > comma_index > 0:  # 1,234.678
                value = value.replace(',', '.')
            elif comma_index and dot_index == -1:
                value = value.replace(',', '.')
            else:
                pass

            value_set = set(value)

            if not value_set.issubset(DataTypes.decimals):
                raise TypeError

            # if it's a string, do also
            # check that reverse conversion is valid,
            # otherwise we have loss of precision. F.ex.:
            # int(0.532) --> 0

            float_value = float(value)
            if value_set.intersection('Ee'):  # it's scientific notation.
                v = value.lower()
                if v.count('e') != 1:
                    raise ValueError("only 1 e in scientific notation")

                e = v.find('e')
                v_float_part = float(v[:e])
                v_exponent = int(v[e + 1:])
                return float(f"{v_float_part}e{v_exponent}")

            elif "." in str(float_value) and not "." in value_set:
                # when traversing through Datatype.types,
                # integer is presumed to have failed for the column,
                # so we ignore this and turn it into a float...
                reconstructed_input = str(int(float_value))

            elif "." in value:
                precision = len(value) - value.index(".") - 1
                formatter = '{0:.' + str(precision) + 'f}'
                reconstructed_input = formatter.format(float_value)

            else:
                reconstructed_input = str(float_value)

            if value.lower() != reconstructed_input:
                raise ValueError

            return float_value
        else:
            raise ValueError

    @staticmethod
    def _infer_date(value):
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError:
                pattern = "".join(["N" if n in DataTypes.digits else n for n in value])
                f = DataTypes.date_formats.get(pattern, None)
                if f:
                    return f(value)
                else:
                    raise ValueError
        else:
            raise ValueError

    @staticmethod
    def _infer_datetime(value):
        if isinstance(value, datetime):
            return value
        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                if '.' in value:
                    dot = value.find('.')
                elif ',' in value:
                    dot = value.find(',')
                else:
                    dot = len(value)

                pattern = "".join(["N" if n in DataTypes.digits else n for n in value[:dot]])
                f = DataTypes.datetime_formats.get(pattern, None)
                if f:
                    return f(value)
                else:
                    raise ValueError
        else:
            raise ValueError

    @staticmethod
    def _infer_time(value):
        if isinstance(value, time):
            return value
        elif isinstance(value, str):
            return time.fromisoformat(value)
        else:
            raise ValueError

    @staticmethod
    def _infer_str(value):
        if isinstance(value, str):
            return value
        else:
            return str(value)

    # Order is very important!
    types = [datetime, date, time, int, bool, float, str]


class Column(list):
    def __init__(self, header, datatype, allow_empty, data=None):
        super().__init__()
        assert isinstance(header, str)
        self.header = header
        assert isinstance(datatype, type)
        assert hasattr(DataTypes, datatype.__name__)
        self.datatype = datatype
        assert isinstance(allow_empty, bool)
        self.allow_empty = allow_empty

        if data:
            for v in data:
                self.append(v)  # append does the type check.

    def __eq__(self, other):
        if not isinstance(other, Column):
            a, b = self.__class__.__name__, other.__class__.__name__
            raise TypeError(f"cannot compare {a} with {b}")

        return all([
            self.header == other.header,
            self.datatype == other.datatype,
            self.allow_empty == other.allow_empty,
            len(self) == len(other),
            all(a == b for a, b in zip(self, other))
        ])

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Column({self.header},{self.datatype},{self.allow_empty}) # ({len(self)} rows)"

    def __copy__(self):
        return self.copy()

    def copy(self):
        return Column(self.header, self.datatype, self.allow_empty, data=self[:])

    def to_json(self):
        return json.dumps({
            'header': self.header,
            'datatype': self.datatype.__name__,
            'allow_empty': self.allow_empty,
            'data': json.dumps([DataTypes.to_json(v) for v in self])
        })

    @classmethod
    def from_json(cls, json_):
        j = json.loads(json_)
        j['datatype'] = dtype = getattr(DataTypes, j['datatype'])
        j['data'] = [DataTypes.from_json(v, dtype) for v in json.loads(j['data'])]
        return Column(**j)

    def type_check(self, value):
        """ helper that does nothing unless it raises an exception. """
        if value is None:
            if not self.allow_empty:
                raise ValueError("None is not permitted.")
            return
        if not isinstance(value, self.datatype):
            raise TypeError(f"{value} is not of type {self.datatype}")

    def append(self, __object) -> None:
        self.type_check(__object)
        super().append(__object)

    def replace(self, values) -> None:
        assert isinstance(values, list)
        if len(values) != len(self):
            raise ValueError("input is not of same length as column.")
        for v in values:
            self.type_check(v)
        self.clear()
        self.extend(values)

    def __setitem__(self, key, value):
        self.type_check(value)
        super().__setitem__(key, value)


class Table(object):
    def __init__(self, **kwargs):
        self.columns = {}
        self.metadata = {**kwargs}

    def __eq__(self, other):
        if not isinstance(other, Table):
            a, b = self.__class__.__name__, other.__class__.__name__
            raise TypeError(f"cannot compare {a} with {b}")
        if self.metadata != other.metadata:
            return False
        if any(a != b for a, b in zip(self.columns.values(), other.columns.values())):
            return False
        return True

    def __len__(self):
        """ returns length of longest column."""
        return max(len(c) for c in self.columns.values())

    def __bool__(self):
        return any(self.columns)

    def __copy__(self):
        t = Table()
        for col in self.columns.values():
            t.add_column(col.header, col.datatype, col.allow_empty, data=col[:])
        t.metadata = self.metadata.copy()
        return t

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        variation = ""
        lengths = {k: len(v) for k, v in self.columns.items()}
        if len(set(lengths.values())) != 1:
            longest_col = max(lengths.values())
            variation = f"(except {', '.join([f'{k}({v})' for k, v in lengths.items() if v < longest_col])})"
        return f"{self.__class__.__name__}() # {len(self.columns)} columns x {len(self)} rows {variation}"

    def show(self, *items):
        """ shows the table.
        param: items: column names, slice.
        :returns None. Output is printed to stdout.
        """
        if any(not isinstance(i, (str, slice)) for i in items):
            raise SyntaxError(f"unexpected input: {[not isinstance(i, (str, slice)) for i in items]}")

        slices = [i for i in items if isinstance(i, slice)]
        if len(slices) > 2: raise SyntaxError("1 > slices")
        if not slices:
            slc = slice(0, len(self), None)
        else:
            slc = slices[0]
        assert isinstance(slc, slice)

        headers = [i for i in items if isinstance(i, str)]
        if any(h not in self.columns for h in headers):
            raise ValueError(f"column not found: {[h for h in headers if h not in self.columns]}")
        if not headers:
            headers = list(self.columns)

        # starting to produce output
        c_lens = {}
        for h in headers:
            col = self.columns[h]
            assert isinstance(col, Column)
            c_lens[h] = max(
                [len(col.header), len(str(col.datatype.__name__)), len(str(False))] + [len(str(v)) for v in col[slc]])

        print("+", "+".join(["=" * c_lens[h] for h in headers]), "+", sep="")
        print("|", "|".join([h.center(c_lens[h], " ") for h in headers]), "|", sep="")
        print("|", "|".join([self.columns[h].datatype.__name__.center(c_lens[h], " ") for h in headers]), "|", sep="")
        print("|", "|".join([str(self.columns[h].allow_empty).center(c_lens[h], " ") for h in headers]), "|", sep="")
        print("+", "+".join(["-" * c_lens[h] for h in headers]), "+", sep="")
        for row in self.filter(*tuple(headers) + (slc,)):
            print("|", "|".join([str(v).rjust(c_lens[h]) for v, h in zip(row, headers)]), "|", sep="")
        print("+", "+".join(["=" * c_lens[h] for h in headers]), "+", sep="")

    def copy(self):
        return self.__copy__()

    def to_json(self):
        return json.dumps({
            'metadata': self.metadata,
            'columns': [c.to_json() for c in self.columns.values()]
        })

    @classmethod
    def from_json(cls, json_):
        t = Table()
        data = json.loads(json_)
        t.metadata = data['metadata']
        for c in data['columns']:
            col = Column.from_json(c)
            col.header = t.check_for_duplicate_header(col.header)
            t.columns[col.header] = col
        return t

    def check_for_duplicate_header(self, header):
        assert isinstance(header, str)
        if not header:
            header = 'None'
        new_header = header
        counter = count(start=1)
        while new_header in self.columns:
            new_header = f"{header}_{next(counter)}"  # valid attr names must be ascii.
        return new_header

    def add_column(self, header, datatype, allow_empty=False, data=None):
        assert isinstance(header, str)
        header = self.check_for_duplicate_header(header)
        self.columns[header] = Column(header, datatype, allow_empty, data=data)

    def add_row(self, values):
        if not isinstance(values, tuple):
            raise TypeError(f"expected tuple, got {type(values)}")
        if len(values) != len(self.columns):
            raise ValueError(f"expected {len(self.columns)} values not {len(values)}: {values}")
        for value, col in zip(values, self.columns.values()):
            col.append(value)

    def __contains__(self, item):
        return item in self.columns

    def __iter__(self):
        raise AttributeError("use Table.rows or Table.columns")

    def _slice(self, item=None):
        """ transforms a slice into start,stop,step"""
        if not item:
            item = slice(None, len(self), None)
        else:
            assert isinstance(item, slice)

        if item.stop < 0:
            start = len(self) + item.stop
            stop = len(self)
            step = 1 if item.step is None else item.step
        else:
            start = 0 if item.start is None else item.start
            stop = item.stop
            step = 1 if item.step is None else item.step
        return start, stop, step

    def __getitem__(self, item):
        """ returns rows as a tuple """
        if isinstance(item, int):
            item = slice(item, item + 1, 1)
        if isinstance(item, slice):
            start, stop, step = self._slice(item)

            t = Table()
            for col in self.columns.values():
                t.add_column(col.header, col.datatype, col.allow_empty, col[start:stop:step])
            return t
        else:
            return self.columns[item]

    def __setitem__(self, key, value):
        if key in self.columns and isinstance(value, list):
            c = self.columns[key]
            c.clear()
            for v in value:
                c.append(v)
        else:
            raise TypeError(f"Use add_column to add_column: {key}")

    def __delitem__(self, key):
        """ delete column as key """
        if key in self.columns:
            del self.columns[key]
        else:
            raise KeyError(f"key not found")

    def __setattr__(self, name, value):
        if isinstance(name, str) and hasattr(self, name):
            if name in self.columns and isinstance(value, list):
                col = self.columns[name]
                col.replace(value)
                return
        super().__setattr__(name, value)

    def compare(self, other):
        """ compares the metadata of two tables."""
        if not isinstance(other, Table):
            a, b = self.__class__.__name__, other.__class__.__name__
            raise TypeError(f"cannot compare type {b} with {a}")

        if self.metadata != other.metadata:
            raise ValueError("tables have different metadata.")
        for a, b in [[self, other], [other, self]]:  # check both dictionaries.
            for name, col in a.columns.items():
                if name not in b.columns:
                    raise ValueError(f"Column {name} not in other")
                col2 = b.columns[name]
                if col.datatype != col2.datatype:
                    raise ValueError(f"Column {name}.datatype different: {col.datatype}, {col2.datatype}")
                if col.allow_empty != col2.allow_empty:
                    raise ValueError(f"Column {name}.allow_empty is different")
        return True

    def __iadd__(self, other):
        """ enables Table_1 += Table_2 """
        self.compare(other)
        for h, col in self.columns.items():
            c2 = other.columns[h]
            col.extend(c2[:])
        return self

    def __add__(self, other):
        """ enables Table_3 = Table_1 + Table_2 """
        self.compare(other)
        cp = self.copy()
        for h, col in cp.columns.items():
            c2 = other.columns[h]
            col.extend(c2[:])
        return cp

    @property
    def rows(self):
        """ enables iteration

        for row in table.rows:
            print(row)

        """
        for ix in range(len(self)):
            item = tuple(c[ix] if ix < len(c) else None for c in self.columns.values())
            yield item

    def index(self, *args):
        """ Creates index on *args columns as d[(key tuple, ) = {index1, index2, ...} """
        idx = defaultdict(set)
        for ix, key in enumerate(self.filter(*args)):
            idx[key].add(ix)
        return idx

    def _sort_index(self, **kwargs):
        if not isinstance(kwargs, dict):
            raise ValueError("Expected keyword arguments")
        if not kwargs:
            kwargs = {c: False for c in self.columns}

        for k, v in kwargs.items():
            if k not in self.columns:
                raise ValueError(f"no column {k}")
            if not isinstance(v, bool):
                raise ValueError(f"{k} was mapped to {v} - a non-boolean")
        none_substitute = float('-inf')

        rank = {i: tuple() for i in range(len(self))}
        for key in kwargs:
            unique_values = {v: 0 for v in self.columns[key] if v is not None}
            for r, v in enumerate(sorted(unique_values, reverse=kwargs[key])):
                unique_values[v] = r
            for ix, v in enumerate(self.columns[key]):
                rank[ix] += (unique_values.get(v, none_substitute),)

        new_order = [(r, i) for i, r in rank.items()]  # tuples are listed and sort...
        new_order.sort()
        sorted_index = [i for r, i in new_order]  # new index is extracted.

        rank.clear()  # free memory.
        new_order.clear()

        return sorted_index

    def sort(self, **kwargs):
        """ Perform multi-pass sorting with precedence given order of column names.
        :param kwargs: keys: columns, values: 'reverse' as boolean.
        """
        sorted_index = self._sort_index(**kwargs)
        for col_name, col in self.columns.items():
            assert isinstance(col, Column)
            col.replace(values=[col[ix] for ix in sorted_index])

    def is_sorted(self, **kwargs):
        sorted_index = self._sort_index(**kwargs)
        if any(ix != i for ix, i in enumerate(sorted_index)):
            return False
        return True

    def filter(self, *items):
        """ enables iteration on a limited number of headers:

        >>> table.columns
        'a','b','c','d','e'

        for row in table.filter('b', 'a', 'a', 'c'):
            b,a,a,c = row ...

        returns values in same order as headers. """
        if any(not isinstance(i, (str, slice)) for i in items):
            raise SyntaxError(f"unexpected input: {[not isinstance(i, (str, slice)) for i in items]}")

        slices = [i for i in items if isinstance(i, slice)]
        if len(slices) > 2: raise SyntaxError("1 > slices")
        if not slices:
            slc = slice(None, len(self), None)
        else:
            slc = slices[0]
        assert isinstance(slc, slice)

        headers = [i for i in items if isinstance(i, str)]
        if any(h not in self.columns for h in headers):
            raise ValueError(f"column not found: {[h for h in headers if h not in self.columns]}")

        L = [self.columns[h] for h in headers]
        for ix in range(*self._slice(slc)):
            item = tuple(c[ix] if ix < len(c) else None for c in L)
            yield item

    def all(self, **kwargs):
        """
        returns Table for rows where ALL kwargs match
        :param kwargs: dictionary with headers and values / boolean callable
        """
        if not isinstance(kwargs, dict):
            raise TypeError("did you remember to add the ** in front of your dict?")
        if not all(k in self.columns for k in kwargs):
            raise ValueError(f"Unknown column(s): {[k for k in kwargs if k not in self.columns]}")

        ixs = None
        for k, v in kwargs.items():
            col = self.columns[k]
            if ixs is None:  # first header.
                if callable(v):
                    ix2 = {ix for ix, i in enumerate(col) if v(i)}
                else:
                    ix2 = {ix for ix, i in enumerate(col) if v == i}

            else:  # remaining headers.
                if callable(v):
                    ix2 = {ix for ix in ixs if v(col[ix])}
                else:
                    ix2 = {ix for ix in ixs if v == col[ix]}

            if not isinstance(ixs, set):
                ixs = ix2
            else:
                ixs = ixs.intersection(ix2)

            if not ixs:  # There are no matches.
                break

        t = Table()
        for col in self.columns.values():
            t.add_column(col.header, col.datatype, col.allow_empty, data=[col[ix] for ix in ixs])
        return t

    def any(self, **kwargs):
        """
        returns Table for rows where ANY kwargs match
        :param kwargs: dictionary with headers and values / boolean callable
        """
        if not isinstance(kwargs, dict):
            raise TypeError("did you remember to add the ** in front of your dict?")

        ixs = set()
        for k, v in kwargs.items():
            col = self.columns[k]
            if callable(v):
                ix2 = {ix for ix, r in enumerate(col) if v(r)}
            else:
                ix2 = {ix for ix, r in enumerate(col) if v == r}
            ixs.update(ix2)

        t = Table()
        for col in self.columns.values():
            t.add_column(col.header, col.datatype, col.allow_empty, data=[col[ix] for ix in ixs])
        return t

    def _join_type_check(self, other, keys, columns):
        if not isinstance(other, Table):
            raise TypeError(f"other expected other to be type Table, not {type(other)}")
        if not isinstance(keys, list) and all(isinstance(k, str) for k in keys):
            raise TypeError(f"Expected keys as list of strings, not {type(keys)}")
        union = list(self.columns) + list(other.columns)
        if not all(k in self.columns and k in other.columns for k in keys):
            raise ValueError(f"key(s) not found: {[k for k in keys if k not in union]}")
        if not all(k in union for k in columns):
            raise ValueError(f"column(s) not found: {[k for k in keys if k not in union]}")

    def left_join(self, other, keys, columns):
        """
        :param other: self, other = (left, right)
        :param keys: list of keys for the join
        :param columns: list of columns to retain
        :return: new table

        Example:
        SQL:   SELECT number, letter FROM left LEFT JOIN right on left.colour == right.colour
        Table: left_join = left_table.left_join(right_table, keys=['colour'], columns=['number', 'letter'])
        """
        self._join_type_check(other, keys, columns)  # raises if error

        left_join = Table()
        for col_name in columns:
            if col_name in self.columns:
                col = self.columns[col_name]
            elif col_name in other.columns:
                col = other.columns[col_name]
            else:
                raise ValueError(f"column name '{col_name}' not in any table.")
            left_join.add_column(col_name, col.datatype, allow_empty=True)

        left_ixs = range(len(self))
        right_idx = other.index(*keys)

        for left_ix in left_ixs:
            key = tuple(self[h][left_ix] for h in keys)
            right_ixs = right_idx.get(key, (None,))
            for right_ix in right_ixs:
                for col_name, column in left_join.columns.items():
                    if col_name in self:
                        column.append(self[col_name][left_ix])
                    elif col_name in other:
                        if right_ix is not None:
                            column.append(other[col_name][right_ix])
                        else:
                            column.append(None)
                    else:
                        raise Exception('bad logic')
        return left_join

    def inner_join(self, other, keys, columns):
        """
        :param other: table
        :param keys: list of keys
        :param columns: list of columns to retain
        :return: new Table

        Example:
        SQL:   SELECT number, letter FROM left INNER JOIN right ON left.colour == right.colour
        Table: inner_join = left_table.inner_join_with(right_table, keys=['colour'],  columns=['number','letter'])
        """
        self._join_type_check(other, keys, columns)  # raises if error

        inner_join = Table()
        for col_name in columns:
            if col_name in self.columns:
                col = self.columns[col_name]
            elif col_name in other.columns:
                col = other.columns[col_name]
            else:
                raise ValueError(f"column name '{col_name}' not in any table.")
            inner_join.add_column(col_name, col.datatype, allow_empty=True)

        key_union = set(self.filter(*keys)).intersection(set(other.filter(*keys)))

        left_ixs = self.index(*keys)
        right_ixs = other.index(*keys)

        for key in key_union:
            for left_ix in left_ixs.get(key, set()):
                for right_ix in right_ixs.get(key, set()):
                    for col_name, column in inner_join.columns.items():
                        if col_name in self:
                            column.append(self[col_name][left_ix])
                        elif col_name in other:
                            column.append(other[col_name][right_ix])
                        else:
                            raise Exception("bad logic.")
        return inner_join

    def outer_join(self, other, keys, columns):
        """
        :param other: table
        :param keys: list of keys
        :param columns: list of columns to retain
        :return: new Table

        Example:
        SQL:   SELECT number, letter FROM left OUTER JOIN right ON left.colour == right.colour
        Table: outer_join = left_table.outer_join(right_table, keys=['colour'], columns=['number','letter'])
        """
        self._join_type_check(other, keys, columns)  # raises if error

        outer_join = Table()
        for col_name in columns:
            if col_name in self.columns:
                col = self.columns[col_name]
            elif col_name in other.columns:
                col = other.columns[col_name]
            else:
                raise ValueError(f"column name '{col_name}' not in any table.")
            outer_join.add_column(col_name, col.datatype, allow_empty=True)

        left_ixs = range(len(self))
        right_idx = other.index(*keys)
        right_keyset = set(right_idx)

        for left_ix in left_ixs:
            key = tuple(self[h][left_ix] for h in keys)
            right_ixs = right_idx.get(key, (None,))
            right_keyset.discard(key)
            for right_ix in right_ixs:
                for col_name, column in outer_join.columns.items():
                    if col_name in self:
                        column.append(self[col_name][left_ix])
                    elif col_name in other:
                        if right_ix is not None:
                            column.append(other[col_name][right_ix])
                        else:
                            column.append(None)
                    else:
                        raise Exception('bad logic')

        for right_key in right_keyset:
            for right_ix in right_idx[right_key]:
                for col_name, column in outer_join.columns.items():
                    if col_name in self:
                        column.append(None)
                    elif col_name in other:
                        column.append(other[col_name][right_ix])
                    else:
                        raise Exception('bad logic')
        return outer_join

