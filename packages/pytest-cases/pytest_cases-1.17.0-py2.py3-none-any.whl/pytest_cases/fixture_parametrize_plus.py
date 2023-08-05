from collections import Iterable, namedtuple
from distutils.version import LooseVersion
from functools import partial
from inspect import isgeneratorfunction
from warnings import warn

try:  # python 3.3+
    from inspect import signature, Parameter
except ImportError:
    from funcsigs import signature, Parameter  # noqa

try:
    from typing import Union, Callable, List, Any, Sequence, Optional  # noqa
except ImportError:
    pass

import pytest
from makefun import with_signature, remove_signature_parameters, add_signature_parameters, wraps

from .common_pytest import get_fixture_name, remove_duplicates, is_marked_parameter_value, mini_idvalset, \
    get_param_argnames_as_list, extract_parameterset_info, ParameterSet, has_pytest_param, get_pytest_marks_on_function, \
    transform_marks_into_decorators

from .fixture__creation import check_name_available, CHANGE, WARN, get_caller_module
from .fixture_core1_unions import InvalidParamsList, NOT_USED, UnionFixtureAlternative, _make_fixture_union, \
    _make_unpack_fixture
from .fixture_core2 import _create_param_fixture, fixture_plus


def _fixture_product(caller_module,
                     name,                # type: str
                     fixtures_or_values,
                     fixture_positions,
                     scope="function",    # type: str
                     ids=None,            # type: Union[Callable, List[str]]
                     unpack_into=None,    # type: Iterable[str]
                     autouse=False,       # type: bool
                     hook=None,           # type: Callable[[Callable], Callable]
                     caller=None,         # type: Callable
                     **kwargs):
    """
    Internal implementation for fixture products created by pytest parametrize plus.

    :param caller_module:
    :param name:
    :param fixtures_or_values:
    :param fixture_positions:
    :param idstyle:
    :param scope:
    :param ids:
    :param unpack_into:
    :param autouse:
    :param kwargs:
    :return:
    """
    # test the `fixtures` argument to avoid common mistakes
    if not isinstance(fixtures_or_values, (tuple, set, list)):
        raise TypeError("fixture_product: the `fixtures_or_values` argument should be a tuple, set or list")
    else:
        has_lazy_vals = any(isinstance(v, lazy_value) for v in fixtures_or_values)

    _tuple_size = len(fixtures_or_values)

    # first get all required fixture names
    f_names = [None] * _tuple_size
    for f_pos in fixture_positions:
        # possibly get the fixture name if the fixture symbol was provided
        f = fixtures_or_values[f_pos]
        if isinstance(f, fixture_ref):
            f = f.fixture
        # and remember the position in the tuple
        f_names[f_pos] = get_fixture_name(f)

    # remove duplicates by making it an ordered set
    all_names = remove_duplicates((n for n in f_names if n is not None))
    if len(all_names) < 1:
        raise ValueError("Empty fixture products are not permitted")

    def _tuple_generator(all_fixtures):
        for i in range(_tuple_size):
            fix_at_pos_i = f_names[i]
            if fix_at_pos_i is None:
                # fixed value
                # note: wouldnt it be almost as efficient but more readable to *always* call handle_lazy_args?
                yield handle_lazy_args(fixtures_or_values[i]) if has_lazy_vals else fixtures_or_values[i]
            else:
                # fixture value
                yield all_fixtures[fix_at_pos_i]

    # then generate the body of our product fixture. It will require all of its dependent fixtures
    @with_signature("(%s)" % ', '.join(all_names))
    def _new_fixture(**all_fixtures):
        return tuple(_tuple_generator(all_fixtures))

    _new_fixture.__name__ = name

    # finally create the fixture per se.
    # WARNING we do not use pytest.fixture but fixture_plus so that NOT_USED is discarded
    f_decorator = fixture_plus(scope=scope, autouse=autouse, ids=ids, hook=hook, **kwargs)
    fix = f_decorator(_new_fixture)

    # Dynamically add fixture to caller's module as explained in https://github.com/pytest-dev/pytest/issues/2424
    check_name_available(caller_module, name, if_name_exists=WARN, caller=caller)
    setattr(caller_module, name, fix)

    # if unpacking is requested, do it here
    if unpack_into is not None:
        _make_unpack_fixture(caller_module, argnames=unpack_into, fixture=name, hook=hook)

    return fix


_make_fixture_product = _fixture_product
"""A readable alias for callers not using the returned symbol"""


class fixture_ref(object):  # noqa
    """
    A reference to a fixture, to be used in `parametrize_plus`.
    You can create it from a fixture name or a fixture object (function).
    """
    __slots__ = 'fixture',

    def __init__(self, fixture):
        self.fixture = fixture


pytest53 = LooseVersion(pytest.__version__) >= LooseVersion("5.3.0")
if pytest53:
    # in the latest versions of pytest, the default _idmaker returns the value of __name__ if it is available,
    # even if an object is not a class nor a function. So we do not need to use any special trick.
    _LazyValueBase = object
else:
    fake_base = int

    class _LazyValueBase(int, object):
        """
        in this older version of pytest, the default _idmaker does *not* return the value of __name__ for
        objects that are not functions not classes. However it *does* return str(obj) for objects that are
        instances of bool, int or float. So that's why lazy_value inherits from int.
        """
        __slots__ = ()

        def __new__(cls,
                    valuegetter,  # type: Callable[[], Any]
                    id=None,      # type: str
                    marks=()      # type: Sequence
                    ):
            """ Inheriting from int is a bit hard in python: we have to override __new__ """
            obj = fake_base.__new__(cls, 111111)
            cls.__init__(obj, valuegetter=valuegetter, id=id, marks=marks)
            return obj

        def __getattribute__(self, item):
            """Map all default attribute and method access to the ones in object, not in int"""
            return object.__getattribute__(self, item)

        def __repr__(self):
            """Magic methods are not intercepted by __getattribute__ and need to be overridden manually.
            We do not need all of them by at least override this one for easier debugging"""
            return object.__repr__(self)


def _unwrap(obj):
    """A light copy of _pytest.compat.get_real_func. In our case
    we do not wish to unwrap the partial nor handle pytest fixture """
    start_obj = obj
    for i in range(100):
        # __pytest_wrapped__ is set by @pytest.fixture when wrapping the fixture function
        # to trigger a warning if it gets called directly instead of by pytest: we don't
        # want to unwrap further than this otherwise we lose useful wrappings like @mock.patch (#3774)
        # new_obj = getattr(obj, "__pytest_wrapped__", None)
        # if isinstance(new_obj, _PytestWrapper):
        #     obj = new_obj.obj
        #     break
        new_obj = getattr(obj, "__wrapped__", None)
        if new_obj is None:
            break
        obj = new_obj
    else:
        raise ValueError("could not find real function of {start}\nstopped at {current}".format(
                start=repr(start_obj), current=repr(obj)
            )
        )
    return obj


def partial_to_str(partialfun):
    """Return a string representation of a partial function, to use in lazy_value ids"""
    strwds = ", ".join("%s=%s" % (k, v) for k, v in partialfun.keywords.items())
    if len(partialfun.args) > 0:
        strargs = ', '.join(str(i) for i in partialfun.args)
        if len(partialfun.keywords) > 0:
            strargs = "%s, %s" % (strargs, strwds)
    else:
        strargs = strwds
    return "%s(%s)" % (partialfun.func.__name__, strargs)


# noinspection PyPep8Naming
class lazy_value(_LazyValueBase):
    """
    A reference to a value getter, to be used in `parametrize_plus`.

    A `lazy_value` is the same thing than a function-scoped fixture, except that the value getter function is not a
    fixture and therefore can neither be parametrized nor depend on fixtures. It should have no mandatory argument.
    """
    if pytest53:
        __slots__ = 'valuegetter', '_id', '_marks'
    else:
        # we can not define __slots__ since we extend int,
        # see https://docs.python.org/3/reference/datamodel.html?highlight=__slots__#notes-on-using-slots
        pass

    # noinspection PyMissingConstructor
    def __init__(self,
                 valuegetter,  # type: Callable[[], Any]
                 id=None,      # type: str
                 marks=()      # type: Sequence
                 ):
        """
        Creates a reference to a value getter, to be used in `parametrize_plus`.

        A `lazy_value` is the same thing than a function-scoped fixture, except that the value getter function is not a
        fixture and therefore can neither be parametrized nor depend on fixtures. It should have no mandatory argument.

        Note that a `lazy_value` can be included in a `pytest.param` without problem. In that case the id defined by
        `pytest.param` will take precedence over the one defined in `lazy_value` if any. The marks, however,
        will all be kept wherever they are defined.

        :param valuegetter: a callable without mandatory arguments
        :param id: an optional id. Otherwise `valuegetter.__name__` will be used by default
        :param marks: optional marks. `valuegetter` marks will also be preserved.
        """
        self.valuegetter = valuegetter
        self._id = id
        self._marks = marks

    def get_marks(self, as_decorators=False):
        """
        Overrides default implementation to return the marks that are on the case function

        :param as_decorators: when True, the marks will be transformed into MarkDecorators before being
            returned
        :return:
        """
        valuegetter_marks = get_pytest_marks_on_function(self.valuegetter, as_decorators=as_decorators)

        if self._marks:
            return transform_marks_into_decorators(self._marks) + valuegetter_marks
        else:
            return valuegetter_marks

    def get_id(self):
        """The id to use in pytest"""
        if self._id is not None:
            return self._id
        else:
            # default is the __name__ of the value getter
            _id = getattr(self.valuegetter, '__name__', None)
            if _id is not None:
                return _id

            # unwrap and handle partial functions
            vg = _unwrap(self.valuegetter)

            if isinstance(vg, partial):
                return partial_to_str(vg)
            else:
                return vg.__name__

    if not pytest53:
        def __str__(self):
            """in pytest<5.3 we inherit from int so that str(v) is called by pytest _idmaker to get the id"""
            return self.get_id()

    @property
    def __name__(self):
        """for pytest >= 5.3 we override this so that pytest uses it for id"""
        return self.get_id()


# Fix for https://github.com/smarie/python-pytest-cases/issues/71
# In order for pytest to allow users to import this symbol in conftest.py
# they should be declared as optional plugin hooks.
# A workaround otherwise would be to remove the 'pytest_' name prefix
# See https://github.com/pytest-dev/pytest/issues/6475
@pytest.hookimpl(optionalhook=True)
def pytest_parametrize_plus(*args,
                            **kwargs):
    warn("`pytest_parametrize_plus` is deprecated. Please use the new alias `parametrize_plus`. "
         "See https://github.com/pytest-dev/pytest/issues/6475")
    return _parametrize_plus(*args, **kwargs)


class ParamAlternative(UnionFixtureAlternative):
    """Defines an "alternative", used to parametrize a fixture union in the context of parametrize_plus"""
    __slots__ = ('argnames', )

    def __init__(self,
                 union_name,
                 alternative_name,
                 argnames,
                 ):
        super(ParamAlternative, self).__init__(union_name=union_name, alternative_name=alternative_name)
        self.argnames = argnames

    @property
    def argnames_str(self):
        return '_'.join(self.argnames)


class SingleParamAlternative(ParamAlternative):
    """alternative class for single parameter value"""
    __slots__ = 'argvalues_index', 'argvalues'

    def __init__(self,
                 union_name,
                 alternative_name,
                 argnames,
                 argvalues_index,
                 argvalues
                 ):
        super(SingleParamAlternative, self).__init__(union_name=union_name, alternative_name=alternative_name,
                                                     argnames=argnames)
        self.argvalues_index = argvalues_index
        self.argvalues = argvalues

    def get_id(self):
        # return "-".join(self.argvalues)
        return mini_idvalset(self.argnames, self.argvalues, idx=self.argvalues_index)


class MultiParamAlternative(ParamAlternative):
    """alternative class for multiple parameter values"""
    __slots__ = 'argvalues_index_from', 'argvalues_index_to'

    def __init__(self,
                 union_name,
                 alternative_name,
                 argnames,
                 argvalues_index_from,
                 argvalues_index_to
                 ):
        super(MultiParamAlternative, self).__init__(union_name=union_name, alternative_name=alternative_name,
                                                    argnames=argnames)
        self.argvalues_index_from = argvalues_index_from
        self.argvalues_index_to = argvalues_index_to


class FixtureParamAlternative(ParamAlternative):
    """alternative class for a single parameter containing a fixture ref"""
    __slots__ = 'argvalues_index',

    def __init__(self,
                 union_name,
                 alternative_name,
                 argnames,
                 argvalues_index,
                 ):
        super(FixtureParamAlternative, self).__init__(union_name=union_name, alternative_name=alternative_name,
                                                      argnames=argnames)
        self.argvalues_index = argvalues_index


class ProductParamAlternative(ParamAlternative):
    """alternative class for a single product parameter containing fixture refs"""
    __slots__ = 'argvalues_index'

    def __init__(self,
                 union_name,
                 alternative_name,
                 argnames,
                 argvalues_index,
                 ):
        super(ProductParamAlternative, self).__init__(union_name=union_name, alternative_name=alternative_name,
                                                      argnames=argnames)
        self.argvalues_index = argvalues_index


class ParamIdMakers(object):
    """ 'Enum' of id styles for param ids """

    # @staticmethod
    # def nostyle(param):
    #     return param.alternative_name

    @staticmethod
    def explicit(param  # type: ParamAlternative
                 ):
        if isinstance(param, SingleParamAlternative):
            # return "%s_is_P%s" % (param.param_name, param.argvalues_index)
            return "%s_is_%s" % (param.argnames_str, param.get_id())
        elif isinstance(param, MultiParamAlternative):
            return "%s_is_P%stoP%s" % (param.argnames_str, param.argvalues_index_from, param.argvalues_index_to - 1)
        elif isinstance(param, FixtureParamAlternative):
            return "%s_is_%s" % (param.argnames_str, param.alternative_name)
        elif isinstance(param, ProductParamAlternative):
            return "%s_is_P%s" % (param.argnames_str, param.argvalues_index)
        else:
            raise TypeError("Unsupported alternative: %r" % param)

    # @staticmethod
    # def compact(param):
    #     return "U%s" % param.alternative_name

    @classmethod
    def get(cls, style  # type: str
            ):
        # type: (...) -> Callable[[Any], str]
        """
        Returns a function that one can use as the `ids` argument in parametrize, applying the given id style.
        See https://github.com/smarie/python-pytest-cases/issues/41

        :param style:
        :return:
        """
        style = style or 'nostyle'
        try:
            return getattr(cls, style)
        except AttributeError:
            raise ValueError("Unknown style: %r" % style)


def parametrize_plus(argnames,
                     argvalues,
                     indirect=False,      # type: bool
                     ids=None,            # type: Union[Callable, List[str]]
                     idstyle='explicit',  # type: str
                     scope=None,          # type: str
                     hook=None,           # type: Callable[[Callable], Callable]
                     debug=False,         # type: bool
                     **kwargs):
    """
    Equivalent to `@pytest.mark.parametrize` but also supports new possibilities in argvalues:

     - one can include references to fixtures with `fixture_ref(<fixture>)` where <fixture> can be the fixture name or
       fixture function. When such a fixture reference is detected in the argvalues, a new function-scope "union" fixture
       will be created with a unique name, and the test function will be wrapped so as to be injected with the correct
       parameters from this fixture. Special test ids will be created to illustrate the switching between the various
       normal parameters and fixtures. You can see debug print messages about all fixtures created using `debug=True`

     - one can include lazy argvalues with `lazy_value(<valuegetter>, [id=..., marks=...])`. A `lazy_value` is the same
       thing than a function-scoped fixture, except that the value getter function is not a fixture and therefore can
       neither be parametrized nor depend on fixtures. It should have no mandatory argument.

    Both `fixture_ref` and `lazy_value` can be used to represent a single argvalue, or a whole tuple of argvalues when
    there are several argnames. Several of them can be used in a tuple.

    Finally, `pytest.param` is supported even when there are `fixture_ref` and `lazy_value`.

    An optional `hook` can be passed, to apply on each fixture function that is created during this call. The hook
    function will be called everytime a fixture is about to be created. It will receive a  single argument (the
    function implementing the fixture) and should return the function to use. For example you can use `saved_fixture`
    from `pytest-harvest` as a hook in order to save all such created fixtures in the fixture store.

    :param argnames: same as in pytest.mark.parametrize
    :param argvalues: same as in pytest.mark.parametrize except that `fixture_ref` and `lazy_value` are supported
    :param indirect: same as in pytest.mark.parametrize
    :param ids: same as in pytest.mark.parametrize
    :param idstyle: style of ids to be used in generated "union" fixtures. See `fixture_union` for details.
    :param scope: same as in pytest.mark.parametrize
    :param hook: an optional hook to apply to each fixture function that is created during this call. The hook function
        will be called everytime a fixture is about to be created. It will receive a single argument (the function
        implementing the fixture) and should return the function to use. For example you can use `saved_fixture` from
        `pytest-harvest` as a hook in order to save all such created fixtures in the fixture store.
    :param debug: print debug messages on stdout to analyze fixture creation (use pytest -s to see them)
    :param kwargs: additional arguments for pytest.mark.parametrize
    :return:
    """
    return _parametrize_plus(argnames, argvalues, indirect=indirect, ids=ids, idstyle=idstyle, scope=scope, hook=hook,
                             debug=debug, **kwargs)


def handle_lazy_args(argval):
    """ Possibly calls the lazy values contained in argval if needed, before returning it"""

    # First handle the general case
    try:
        if not isinstance(argval, (lazy_value, LazyTuple, LazyTuple.LazyItem)):
            return argval
    except:  # noqa
        return argval

    # Now the lazy ones
    if isinstance(argval, lazy_value):
        return argval.valuegetter()
    elif isinstance(argval, LazyTuple):
        return argval.get()
    elif isinstance(argval, LazyTuple.LazyItem):
        return argval.get()
    else:
        return argval


class LazyTuple(object):
    """
    A wrapper representing a lazy_value used as a tuple = for several argvalues at once.

     -
       while not calling the lazy value
     -
    """
    __slots__ = ('value', 'theoretical_size', 'retrieved')

    def __init__(self,
                 valueref,        # type: Union[lazy_value, Sequence]
                 theoretical_size  # type: int
                 ):
        self.value = valueref
        self.theoretical_size = theoretical_size
        self.retrieved = False

    def __len__(self):
        return self.theoretical_size

    def get_id(self):
        """return the id to use by pytest"""
        return self.value.get_id()

    class LazyItem(namedtuple('LazyItem', ('host', 'item'))):
        def get(self):
            return self.host.force_getitem(self.item)

    def __getitem__(self, item):
        """
        Getting an item in the tuple with self[i] does *not* retrieve the value automatically, but returns
        a facade (a LazyItem), so that pytest can store this item independently wherever needed, without
        yet calling the value getter.
        """
        if self.retrieved:
            # this is never called by pytest, but keep it for debugging
            return self.value[item]
        else:
            # do not retrieve yet: return a facade
            return LazyTuple.LazyItem(self, item)

    def force_getitem(self, item):
        """ Call the underlying value getter, then return self[i]. """
        return self.get()[item]

    def get(self):
        """ Call the underlying value getter, then return the tuple (not self) """
        if not self.retrieved:
            # retrieve
            self.value = self.value.valuegetter()
            self.retrieved = True
        return self.value


def _parametrize_plus(argnames,
                      argvalues,
                      indirect=False,      # type: bool
                      ids=None,            # type: Union[Callable, List[str]]
                      idstyle='explicit',  # type: str
                      scope=None,          # type: str
                      hook=None,           # type: Callable[[Callable], Callable]
                      _frame_offset=2,
                      debug=False,         # type: bool
                      **kwargs):
    # make sure that we do not destroy the argvalues if it is provided as an iterator
    try:
        argvalues = list(argvalues)
    except TypeError:
        raise InvalidParamsList(argvalues)

    # get the param names
    initial_argnames = argnames
    argnames = get_param_argnames_as_list(argnames)
    nb_params = len(argnames)

    # extract all marks and custom ids.
    # Do not check consistency of sizes argname/argvalue as a fixture_ref can stand for several argvalues.
    marked_argvalues = argvalues
    custom_pids, p_marks, argvalues = extract_parameterset_info(argnames, argvalues, check_nb=False)

    # find if there are fixture references in the values provided
    fixture_indices = []
    if nb_params == 1:
        for i, v in enumerate(argvalues):
            if isinstance(v, lazy_value):
                # Note: no need to modify the id, it will be ok thanks to the lazy_value class design
                # handle marks
                _mks = v.get_marks(as_decorators=True)
                if len(_mks) > 0:
                    # merge with the mark decorators possibly already present with pytest.param
                    if p_marks[i] is None:
                        p_marks[i] = []
                    p_marks[i] = list(p_marks[i]) + _mks

                    # update the marked_argvalues
                    marked_argvalues[i] = ParameterSet(values=(argvalues[i],), id=custom_pids[i], marks=p_marks[i])
                del _mks

            if isinstance(v, fixture_ref):
                fixture_indices.append((i, None))
    elif nb_params > 1:
        for i, v in enumerate(argvalues):
            if isinstance(v, lazy_value):
                # a lazy value is used for several parameters at the same time, and is NOT between pytest.param()
                argvalues[i] = LazyTuple(v, nb_params)

                # TUPLE usage: we HAVE to set an id to prevent too early access to the value by _idmaker
                # note that on pytest 2 we cannot set an id here, so the lazy value wont be too lazy
                assert custom_pids[i] is None
                _id = v.get_id()
                if not has_pytest_param:
                    warn("The custom id %r in `lazy_value` will be ignored as this version of pytest is too old to"
                         " support `pytest.param`." % _id)
                    _id = None

                # handle marks
                _mks = v.get_marks(as_decorators=True)
                if len(_mks) > 0:
                    # merge with the mark decorators possibly already present with pytest.param
                    assert p_marks[i] is None
                    p_marks[i] = _mks

                # note that here argvalues[i] IS a tuple-like so we do not create a tuple around it
                marked_argvalues[i] = ParameterSet(values=argvalues[i], id=_id, marks=_mks)
                custom_pids[i] = _id
                del _id, _mks

            elif isinstance(v, fixture_ref):
                # a fixture ref is used for several parameters at the same time
                fixture_indices.append((i, None))

            elif len(v) == 1 and isinstance(v[0], lazy_value):
                # same than above but it was in a pytest.mark
                # valueref_indices.append((i, None))
                argvalues[i] = LazyTuple(v[0], nb_params)  # unpack it
                if custom_pids[i] is None:
                    # force-use the id from the lazy value (do not have pytest request for it, that would unpack it)
                    custom_pids[i] = v[0].get_id()
                # handle marks
                _mks = v[0].get_marks(as_decorators=True)
                if len(_mks) > 0:
                    # merge with the mark decorators possibly already present with pytest.param
                    if p_marks[i] is None:
                        p_marks[i] = []
                    p_marks[i] = list(p_marks[i]) + _mks
                del _mks
                marked_argvalues[i] = ParameterSet(values=argvalues[i], id=custom_pids[i], marks=p_marks[i])

            elif len(v) == 1 and isinstance(v[0], fixture_ref):
                # same than above but it was in a pytest.mark
                fixture_indices.append((i, None))
                argvalues[i] = v[0]  # unpack it
            else:
                # check for consistency
                if len(v) != len(argnames):
                    raise ValueError("Inconsistent number of values in pytest parametrize: %s items found while the "
                                     "number of parameters is %s: %s." % (len(v), len(argnames), v))

                # let's dig into the tuple
                fix_pos_list = [j for j, _pval in enumerate(v) if isinstance(_pval, fixture_ref)]
                if len(fix_pos_list) > 0:
                    # there is at least one fixture ref inside the tuple
                    fixture_indices.append((i, fix_pos_list))

                # let's dig into the tuple
                # has_val_ref = any(isinstance(_pval, lazy_value) for _pval in v)
                # val_pos_list = [j for j, _pval in enumerate(v) if isinstance(_pval, lazy_value)]
                # if len(val_pos_list) > 0:
                #     # there is at least one value ref inside the tuple
                #     argvalues[i] = tuple_with_value_refs(v, theoreticalsize=nb_params, positions=val_pos_list)
    del i

    if len(fixture_indices) == 0:
        if debug:
            print("No fixture reference found. Calling @pytest.mark.parametrize...")
        # no fixture reference: shortcut, do as usual (note that the hook wont be called since no fixture is created)
        return pytest.mark.parametrize(initial_argnames, marked_argvalues, indirect=indirect,
                                       ids=ids, scope=scope, **kwargs)
    else:
        if len(kwargs) > 0:
            warn("Unsupported kwargs for `parametrize_plus`: %r" % kwargs)

        if debug:
            print("Fixture references found. Creating fixtures...")
        # there are fixture references: we have to create a specific decorator
        caller_module = get_caller_module(frame_offset=_frame_offset)
        param_names_str = '_'.join(argnames).replace(' ', '')

        def _make_idfun_for_params(argnames,  # noqa
                                   nb_positions):
            """
            Creates an id creating function that will use 'argnames' as the argnames
            instead of the one(s) received by pytest. We use this in the case of param fixture
            creation because on one side we need a unique fixture name so it is big and horrible,
            but on the other side we want the id to rather reflect the simple argnames, no that fixture name.

            :param argnames:
            :param nb_positions:
            :return:
            """
            # create a new make id function with its own local counter of parameter
            def _tmp_make_id(argvals):
                _tmp_make_id.i += 1
                if _tmp_make_id.i >= nb_positions:
                    raise ValueError("Internal error, please report")
                if len(argnames) <= 1:
                    argvals = (argvals,)
                elif isinstance(argvals, LazyTuple):
                    return argvals.get_id()
                return mini_idvalset(argnames, argvals, idx=_tmp_make_id.i)

            # init its positions counter
            _tmp_make_id.i = -1
            return _tmp_make_id

        def _create_params_alt(test_func_name, union_name, from_i, to_i, hook):  # noqa
            """ Routine that will be used to create a parameter fixture for argvalues between prev_i and i"""

            # check if this is about a single value or several values
            single_param_val = (to_i == from_i + 1)

            if single_param_val:
                i = from_i  # noqa

                # Create a unique fixture name
                p_fix_name = "%s_%s_P%s" % (test_func_name, param_names_str, i)
                p_fix_name = check_name_available(caller_module, p_fix_name, if_name_exists=CHANGE,
                                                  caller=parametrize_plus)

                if debug:
                    print("Creating fixture %r to handle parameter %s" % (p_fix_name, i))

                # Create the fixture that will return the unique parameter value ("auto-simplify" flag)
                # IMPORTANT that fixture is NOT parametrized so has no id nor marks: use argvalues not marked_argvalues
                _create_param_fixture(caller_module, argname=p_fix_name, argvalues=argvalues[i:i+1], hook=hook,
                                      auto_simplify=True)

                # Create the alternative
                argvals = (argvalues[i],) if nb_params == 1 else argvalues[i]
                p_fix_alt = SingleParamAlternative(union_name=union_name, alternative_name=p_fix_name,
                                                   argnames=argnames, argvalues_index=i, argvalues=argvals)
                # Finally copy the custom id/marks on the ParamAlternative if any
                if is_marked_parameter_value(marked_argvalues[i]):
                    p_fix_alt = pytest.param(p_fix_alt, id=marked_argvalues[i].id, marks=marked_argvalues[i].marks)

            else:
                # Create a unique fixture name
                p_fix_name = "%s_%s_is_P%stoP%s" % (test_func_name, param_names_str, from_i, to_i - 1)
                p_fix_name = check_name_available(caller_module, p_fix_name, if_name_exists=CHANGE,
                                                  caller=parametrize_plus)

                if debug:
                    print("Creating fixture %r to handle parameters %s to %s" % (p_fix_name, from_i, to_i - 1))

                # If an explicit list of ids was provided, slice it. Otherwise use the provided callable
                try:
                    p_ids = ids[from_i:to_i]
                except TypeError:
                    # callable ? otherwise default to a customized id maker that replaces the fixture name
                    # that we use (p_fix_name) with a simpler name in the ids (just the argnames)
                    p_ids = ids or _make_idfun_for_params(argnames=argnames, nb_positions=(to_i - from_i))

                # Create the fixture that will take ALL these parameter values (in a single parameter)
                # That fixture WILL be parametrized, this is why we propagate the p_ids and use the marked values
                if nb_params == 1:
                    _argvals = marked_argvalues[from_i:to_i]
                else:
                    # we have to create a tuple around the vals because we have a SINGLE parameter that is a tuple
                    _argvals = tuple(ParameterSet((vals, ), id=id, marks=marks or ())
                                     for vals, id, marks in zip(argvalues[from_i:to_i],
                                                                custom_pids[from_i:to_i], p_marks[from_i:to_i]))
                _create_param_fixture(caller_module, argname=p_fix_name, argvalues=_argvals, ids=p_ids, hook=hook)

                # todo put back debug=debug above

                # Create the corresponding alternative
                p_fix_alt = MultiParamAlternative(union_name=union_name, alternative_name=p_fix_name, argnames=argnames,
                                                  argvalues_index_from=from_i, argvalues_index_to=to_i)
                # no need to copy the custom id/marks to the ParamAlternative: they were passed above already

            return p_fix_name, p_fix_alt

        def _create_fixture_ref_alt(union_name, i):  # noqa
            # Get the referenced fixture name
            f_fix_name = get_fixture_name(argvalues[i].fixture)

            if debug:
                print("Creating reference to fixture %r" % (f_fix_name,))

            # Create the alternative
            f_fix_alt = FixtureParamAlternative(union_name=union_name, alternative_name=f_fix_name,
                                                argnames=argnames, argvalues_index=i)
            # Finally copy the custom id/marks on the ParamAlternative if any
            if is_marked_parameter_value(marked_argvalues[i]):
                f_fix_alt = pytest.param(f_fix_alt, id=marked_argvalues[i].id, marks=marked_argvalues[i].marks)

            return f_fix_name, f_fix_alt

        def _create_fixture_ref_product(union_name, i, fixture_ref_positions, test_func_name, hook):  # noqa

            # If an explicit list of ids was provided, slice it. Otherwise use the provided callable
            try:
                p_ids = ids[i]
            except TypeError:
                p_ids = ids  # callable

            # values to use:
            p_values = argvalues[i]

            # Create a unique fixture name
            p_fix_name = "%s_%s_P%s" % (test_func_name, param_names_str, i)
            p_fix_name = check_name_available(caller_module, p_fix_name, if_name_exists=CHANGE, caller=parametrize_plus)

            if debug:
                print("Creating fixture %r to handle parameter %s that is a cross-product" % (p_fix_name, i))

            # Create the fixture
            _make_fixture_product(caller_module, name=p_fix_name, hook=hook, ids=p_ids, fixtures_or_values=p_values,
                                  fixture_positions=fixture_ref_positions, caller=parametrize_plus)

            # Create the corresponding alternative
            p_fix_alt = ProductParamAlternative(union_name=union_name, alternative_name=p_fix_name,
                                                argnames=argnames, argvalues_index=i)
            # copy the custom id/marks to the ParamAlternative if any
            if is_marked_parameter_value(marked_argvalues[i]):
                p_fix_alt = pytest.param(p_fix_alt, id=marked_argvalues[i].id, marks=marked_argvalues[i].marks)

            return p_fix_name, p_fix_alt

        # then create the decorator
        def parametrize_plus_decorate(test_func):
            """
            A decorator that wraps the test function so that instead of receiving the parameter names, it receives the
            new fixture. All other decorations are unchanged.

            :param test_func:
            :return:
            """
            test_func_name = test_func.__name__

            # Are there explicit ids provided ?
            try:
                if len(ids) != len(argvalues):
                    raise ValueError("Explicit list of `ids` provided has a different length (%s) than the number of "
                                     "parameter sets (%s)" % (len(ids), len(argvalues)))
                explicit_ids_to_use = []
            except TypeError:
                explicit_ids_to_use = None

            # first check if the test function has the parameters as arguments
            old_sig = signature(test_func)
            for p in argnames:
                if p not in old_sig.parameters:
                    raise ValueError("parameter '%s' not found in test function signature '%s%s'"
                                     "" % (p, test_func_name, old_sig))

            # The name for the final "union" fixture
            # style_template = "%s_param__%s"
            main_fixture_style_template = "%s_%s"
            fixture_union_name = main_fixture_style_template % (test_func_name, param_names_str)
            fixture_union_name = check_name_available(caller_module, fixture_union_name, if_name_exists=CHANGE,
                                                      caller=parametrize_plus)

            # Retrieve (if ref) or create (for normal argvalues) the fixtures that we will union
            fixture_alternatives = []
            prev_i = -1
            for i, j_list in fixture_indices:  # noqa
                # A/ Is there any non-empty group of 'normal' parameters before the fixture_ref at <i> ? If so, handle.
                if i > prev_i + 1:
                    # create a new "param" fixture parametrized with all of that consecutive group.
                    # Important note: we could either wish to create one fixture for parameter value or to create
                    #  one for each consecutive group as shown below. This should not lead to different results but perf
                    #  might differ. Maybe add a parameter in the signature so that users can test it ?
                    #  this would make the ids more readable by removing the "P2toP3"-like ids
                    p_fix_name, p_fix_alt = _create_params_alt(test_func_name=test_func_name, hook=hook,
                                                               union_name=fixture_union_name, from_i=prev_i + 1, to_i=i)
                    fixture_alternatives.append((p_fix_name, p_fix_alt))
                    if explicit_ids_to_use is not None:
                        if isinstance(p_fix_alt, SingleParamAlternative):
                            explicit_ids_to_use.append(ids[prev_i + 1])
                        else:
                            # the ids provided by the user are propagated to the params of this fix, so we need an id
                            explicit_ids_to_use.append(ParamIdMakers.explicit(p_fix_alt))

                # B/ Now handle the fixture ref at position <i>
                if j_list is None:
                    # argvalues[i] contains a single argvalue that is a fixture_ref : add the referenced fixture
                    f_fix_name, f_fix_alt = _create_fixture_ref_alt(union_name=fixture_union_name, i=i)
                    fixture_alternatives.append((f_fix_name, f_fix_alt))
                    if explicit_ids_to_use is not None:
                        explicit_ids_to_use.append(ids[i])

                else:
                    # argvalues[i] is a tuple, some of them being fixture_ref. create a fixture refering to all of them
                    prod_fix_name, prod_fix_alt = _create_fixture_ref_product(union_name=fixture_union_name, i=i,
                                                                              fixture_ref_positions=j_list,
                                                                              test_func_name=test_func_name, hook=hook)
                    fixture_alternatives.append((prod_fix_name, prod_fix_alt))
                    if explicit_ids_to_use is not None:
                        explicit_ids_to_use.append(ids[i])

                prev_i = i

            # C/ handle last consecutive group of normal parameters, if any
            i = len(argvalues)  # noqa
            if i > prev_i + 1:
                p_fix_name, p_fix_alt = _create_params_alt(test_func_name=test_func_name, union_name=fixture_union_name,
                                                           from_i=prev_i + 1, to_i=i, hook=hook)
                fixture_alternatives.append((p_fix_name, p_fix_alt))
                if explicit_ids_to_use is not None:
                    if isinstance(p_fix_alt, SingleParamAlternative):
                        explicit_ids_to_use.append(ids[prev_i + 1])
                    else:
                        # the ids provided by the user are propagated to the params of this fix, so we need an id
                        explicit_ids_to_use.append(ParamIdMakers.explicit(p_fix_alt))

            # TO DO if fixtures_to_union has length 1, simplify ? >> No, we leave such "optimization" to the end user

            # consolidate the list of alternatives
            fix_alternatives = tuple(a[1] for a in fixture_alternatives)

            # and the list of their names. Duplicates should be removed here
            fix_alt_names = []
            for a, alt in fixture_alternatives:
                if a not in fix_alt_names:
                    fix_alt_names.append(a)
                else:
                    # this should only happen when the alternative is directly a fixture reference
                    assert isinstance(alt, FixtureParamAlternative), \
                        "Created fixture names are not unique, please report"

            # Finally create a "main" fixture with a unique name for this test function
            if debug:
                print("Creating final union fixture %r with alternatives %r" % (fixture_union_name, fix_alternatives))

            # note: the function automatically registers it in the module
            _make_fixture_union(caller_module, name=fixture_union_name, hook=hook, caller=parametrize_plus,
                                fix_alternatives=fix_alternatives, unique_fix_alt_names=fix_alt_names,
                                ids=explicit_ids_to_use or ids or ParamIdMakers.get(idstyle))

            # --create the new test function's signature that we want to expose to pytest
            # it is the same than existing, except that we want to replace all parameters with the new fixture
            # first check where we should insert the new parameters (where is the first param we remove)
            _first_idx = -1
            for _first_idx, _n in enumerate(old_sig.parameters):
                if _n in argnames:
                    break
            # then remove all parameters that will be replaced by the new fixture
            new_sig = remove_signature_parameters(old_sig, *argnames)
            # finally insert the new fixture in that position. Indeed we can not insert first or last, because
            # 'self' arg (case of test class methods) should stay first and exec order should be preserved when possible
            new_sig = add_signature_parameters(new_sig, custom_idx=_first_idx,
                                               custom=Parameter(fixture_union_name,
                                                                kind=Parameter.POSITIONAL_OR_KEYWORD))

            if debug:
                print("Creating final test function wrapper with signature %s%s" % (test_func_name, new_sig))

            # --Finally create the fixture function, a wrapper of user-provided fixture with the new signature
            def replace_paramfixture_with_values(kwargs):  # noqa
                # remove the created fixture value
                encompassing_fixture = kwargs.pop(fixture_union_name)
                # and add instead the parameter values
                if nb_params > 1:
                    for i, p in enumerate(argnames):  # noqa
                        kwargs[p] = encompassing_fixture[i]
                else:
                    kwargs[argnames[0]] = encompassing_fixture
                # return
                return kwargs

            if not isgeneratorfunction(test_func):
                # normal test function with return statement
                @wraps(test_func, new_sig=new_sig)
                def wrapped_test_func(*args, **kwargs):  # noqa
                    if kwargs.get(fixture_union_name, None) is NOT_USED:
                        # TODO why this ? it is probably useless: this fixture
                        #  is private and will never end up in another union
                        return NOT_USED
                    else:
                        replace_paramfixture_with_values(kwargs)
                        return test_func(*args, **kwargs)

            else:
                # generator test function (with one or several yield statements)
                @wraps(test_func, new_sig=new_sig)
                def wrapped_test_func(*args, **kwargs):  # noqa
                    if kwargs.get(fixture_union_name, None) is NOT_USED:
                        # TODO why this ? it is probably useless: this fixture
                        #  is private and will never end up in another union
                        yield NOT_USED
                    else:
                        replace_paramfixture_with_values(kwargs)
                        for res in test_func(*args, **kwargs):
                            yield res

            # move all pytest marks from the test function to the wrapper
            # not needed because the __dict__ is automatically copied when we use @wraps
            #   move_all_pytest_marks(test_func, wrapped_test_func)

            # With this hack we will be ordered correctly by pytest https://github.com/pytest-dev/pytest/issues/4429
            wrapped_test_func.place_as = test_func

            # return the new test function
            return wrapped_test_func

        return parametrize_plus_decorate
