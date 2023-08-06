import pytest
import copy
import math
from typing import Type, List
from ceed.function import FuncBase, FuncGroup, FunctionFactoryBase, \
    register_all_functions, FuncDoneException
from .common import add_prop_watch


def test_register_funcs():
    from ceed.function.plugin import ConstFunc, LinearFunc
    function_factory = FunctionFactoryBase()
    count = 0

    def count_changes(*largs):
        nonlocal count
        count += 1
    function_factory.fbind('on_changed', count_changes)

    assert not function_factory.funcs_cls
    assert not function_factory.funcs_user
    assert not function_factory.funcs_inst
    assert not function_factory.funcs_inst_default
    assert not function_factory.get_classes()
    assert not function_factory.get_names()

    function_factory.register(ConstFunc)
    assert count
    assert function_factory.funcs_cls['ConstFunc'] is ConstFunc
    assert isinstance(function_factory.funcs_inst['Const'], ConstFunc)
    assert isinstance(function_factory.funcs_inst_default['Const'], ConstFunc)
    assert ConstFunc in function_factory.get_classes()
    assert 'ConstFunc' in function_factory.get_names()

    f = LinearFunc(function_factory=function_factory)
    count = 0
    function_factory.register(LinearFunc, instance=f)
    assert count
    assert function_factory.funcs_cls['LinearFunc'] is LinearFunc
    assert function_factory.funcs_inst['Linear'] is f
    assert function_factory.funcs_inst_default['Linear'] is f
    assert LinearFunc in function_factory.get_classes()
    assert 'LinearFunc' in function_factory.get_names()
    assert not function_factory.funcs_user


def test_auto_register(function_factory: FunctionFactoryBase):
    from ceed.function.plugin import ConstFunc, LinearFunc, CosFunc, \
        ExponentialFunc
    assert not function_factory.funcs_user
    assert function_factory.get('ConstFunc') is ConstFunc
    assert function_factory.get('LinearFunc') is LinearFunc
    assert function_factory.get('CosFunc') is CosFunc
    assert function_factory.get('ExponentialFunc') is ExponentialFunc

    assert isinstance(function_factory.funcs_inst['Const'], ConstFunc)
    assert isinstance(function_factory.funcs_inst['Linear'], LinearFunc)
    assert isinstance(function_factory.funcs_inst['Cos'], CosFunc)
    assert isinstance(
        function_factory.funcs_inst['Exp'], ExponentialFunc)


def test_register_user_func(function_factory: FunctionFactoryBase):
    assert not function_factory.funcs_user

    const_cls = function_factory.get('ConstFunc')
    f = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    f2 = const_cls(
        function_factory=function_factory, duration=5, a=.9, name='f2')

    function_factory.test_changes_count = 0
    function_factory.add_func(f)
    assert function_factory.test_changes_count
    assert f in function_factory.funcs_user
    assert function_factory.funcs_inst['f'] is f

    function_factory.test_changes_count = 0
    function_factory.add_func(f2)
    assert function_factory.test_changes_count
    assert f2 in function_factory.funcs_user
    assert function_factory.funcs_inst['f2'] is f2


def test_factory_re_register(function_factory: FunctionFactoryBase):
    from ceed.function.plugin import ConstFunc, LinearFunc
    with pytest.raises(Exception):
        function_factory.register(ConstFunc)

    with pytest.raises(Exception):
        function_factory.register(LinearFunc)


def test_factory_func_unique_names(function_factory: FunctionFactoryBase):
    assert not function_factory.funcs_user
    function_factory.test_changes_count = 0

    const_cls = function_factory.get('ConstFunc')
    f = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    function_factory.add_func(f)
    f2 = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    function_factory.add_func(f2)

    def assert_not_f():
        assert function_factory.test_changes_count
        assert f in function_factory.funcs_user
        assert f2 in function_factory.funcs_user
        assert len(function_factory.funcs_user) == 2
        f2_name = f2.name
        assert f.name == 'f'
        assert f2_name != 'f'
        assert f2_name

        assert function_factory.funcs_inst['f'] is f
        assert function_factory.funcs_inst[f2_name] is f2
    assert_not_f()

    function_factory.test_changes_count = 0
    f2.name = 'f2'
    assert function_factory.test_changes_count
    assert f in function_factory.funcs_user
    assert f2 in function_factory.funcs_user
    assert len(function_factory.funcs_user) == 2
    assert f.name == 'f'
    assert f2.name == 'f2'

    assert function_factory.funcs_inst['f'] is f
    assert function_factory.funcs_inst['f2'] is f2

    function_factory.test_changes_count = 0
    f2.name = 'f'
    assert_not_f()


def test_factory_func_remove(function_factory: FunctionFactoryBase):
    assert not function_factory.funcs_user
    initial_funcs_n = len(function_factory.funcs_inst)

    const_cls = function_factory.get('ConstFunc')
    f = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    function_factory.add_func(f)
    f2 = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f2')
    function_factory.add_func(f2)

    assert len(function_factory.funcs_inst) == initial_funcs_n + 2

    function_factory.test_changes_count = 0
    assert function_factory.remove_func(f2)

    assert function_factory.test_changes_count
    assert f in function_factory.funcs_user
    assert f2 not in function_factory.funcs_user
    assert len(function_factory.funcs_user) == 1
    assert f.name == 'f'
    assert f2.name == 'f2'

    assert function_factory.funcs_inst['f'] is f
    assert 'f2' not in function_factory.funcs_inst
    assert len(function_factory.funcs_inst) == initial_funcs_n + 1

    function_factory.test_changes_count = 0
    f2.name = 'f'

    assert not function_factory.test_changes_count
    assert f.name == 'f'
    assert f2.name == 'f'

    function_factory.test_changes_count = 0
    assert function_factory.remove_func(f)

    assert function_factory.test_changes_count
    assert f not in function_factory.funcs_user
    assert f2 not in function_factory.funcs_user
    assert not function_factory.funcs_user
    assert f.name == 'f'
    assert f2.name == 'f'

    assert 'f' not in function_factory.funcs_inst
    assert 'f2' not in function_factory.funcs_inst

    assert len(function_factory.funcs_inst) == initial_funcs_n


def test_clear_funcs(function_factory: FunctionFactoryBase):
    assert not function_factory.funcs_user
    initial_funcs_n = len(function_factory.funcs_inst)

    const_cls = function_factory.get('ConstFunc')
    f = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    function_factory.add_func(f)
    f2 = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f2')
    function_factory.add_func(f2)

    assert len(function_factory.funcs_inst) == initial_funcs_n + 2

    function_factory.test_changes_count = 0
    function_factory.clear_added_funcs()
    assert len(function_factory.funcs_inst) == initial_funcs_n
    assert not function_factory.funcs_user


def test_recover_funcs(function_factory: FunctionFactoryBase):
    f1 = function_factory.get('ConstFunc')(
        function_factory=function_factory, a=.5, name='f1')
    f2 = function_factory.get('LinearFunc')(
        function_factory=function_factory, m=.5, b=.2, name='f2')
    f3 = function_factory.get('ExponentialFunc')(
        function_factory=function_factory, A=.5, B=.2, tau1=1.3, tau2=1.5,
        name='f3')
    f4 = function_factory.get('CosFunc')(
        function_factory=function_factory, f=.5, A=3.4, th0=7.5, b=12.2,
        name='f4')

    function_factory.add_func(f1)
    function_factory.add_func(f2)
    function_factory.add_func(f3)
    function_factory.add_func(f4)

    funcs = function_factory.save_functions()
    assert len(funcs) == 4

    recovered_funcs, name_mapping = function_factory.recover_funcs(funcs)
    assert len(recovered_funcs) == 4
    assert len(name_mapping) == 4

    for f_name in ('f1', 'f2', 'f3', 'f4'):
        assert f_name in name_mapping
        assert name_mapping[f_name] != f_name
        assert f_name in function_factory.funcs_inst
        assert name_mapping[f_name] in function_factory.funcs_inst

        for name in function_factory.funcs_inst[f_name].get_gui_props():
            original_f = function_factory.funcs_inst[f_name]
            new_f = function_factory.funcs_inst[name_mapping[f_name]]

            if name == 'name':
                assert original_f.name != new_f.name
                assert new_f.name.startswith(original_f.name)
                continue

            assert getattr(original_f, name) == getattr(new_f, name)


def test_make_function(function_factory: FunctionFactoryBase):
    f1 = function_factory.get('ConstFunc')(
        function_factory=function_factory, a=.5, name='f1')
    f2 = function_factory.get('LinearFunc')(
        function_factory=function_factory, m=.5, b=.2, name='f2')
    f3 = function_factory.get('ExponentialFunc')(
        function_factory=function_factory, A=.5, B=.2, tau1=1.3, tau2=1.5,
        name='f3')
    f4 = function_factory.get('CosFunc')(
        function_factory=function_factory, f=.5, A=3.4, th0=7.5, b=12.2,
        name='f4')

    funcs = f1, f2, f3, f4
    states = [f.get_state() for f in funcs]
    new_funcs = [function_factory.make_func(state) for state in states]
    assert len(new_funcs) == len(funcs)

    for new_func, f in zip(new_funcs, funcs):
        for name in f.get_gui_props():
            if name == 'name':
                assert f.name != new_func.name
                continue

            assert getattr(f, name) == getattr(new_func, name)

    # close should make them identical in all ways
    new_funcs = [
        function_factory.make_func(state, clone=True) for state in states]
    assert len(new_funcs) == len(funcs)

    for new_func, f in zip(new_funcs, funcs):
        for name in f.get_gui_props():
            assert getattr(f, name) == getattr(new_func, name)

    # provide instances
    new_funcs = [
        function_factory.make_func(
            state, instance=function_factory.get(state['cls'])(
                function_factory=function_factory), clone=True)
        for state in states]
    assert len(new_funcs) == len(funcs)

    for new_func, f in zip(new_funcs, funcs):
        for name in f.get_gui_props():
            assert getattr(f, name) == getattr(new_func, name)


def test_group_recursive(function_factory: FunctionFactoryBase):
    factory = function_factory
    const_cls = factory.get('ConstFunc')

    g1 = FuncGroup(function_factory=factory)

    g2 = FuncGroup(function_factory=factory)
    g1.add_func(g2)
    f = const_cls(function_factory=factory, a=.9, duration=2)
    g2.add_func(f)
    f1 = const_cls(function_factory=factory, a=.1, duration=2)
    g2.add_func(f1)

    f2 = const_cls(function_factory=factory, a=.25, duration=2)
    g1.add_func(f2)
    f3 = const_cls(function_factory=factory, a=.75, duration=2)
    g1.add_func(f3)

    g3 = FuncGroup(function_factory=factory)
    g1.add_func(g3)
    f4 = const_cls(function_factory=factory, a=.8, duration=2)
    g3.add_func(f4)
    f5 = const_cls(function_factory=factory, a=.2, duration=2)
    g3.add_func(f5)

    def assert_times():
        assert list(g2.get_funcs()) == [g2, f, f1]
        assert g2.duration == 4
        assert g2.duration_min == 4
        assert g2.duration_min_total == 4

        assert list(g3.get_funcs()) == [g3, f4, f5]
        assert g3.duration == 4
        assert g3.duration_min == 4
        assert g3.duration_min_total == 4

        assert list(g1.get_funcs()) == [g1, g2, f, f1, f2, f3, g3, f4, f5]
        assert g1.duration == 12
        assert g1.duration_min == 12
        assert g1.duration_min_total == 12
    assert_times()

    g1.init_func(2)
    with pytest.raises(ValueError):
        g1(0)
    assert g1(2) == .9
    assert g1(4) == .1
    assert g1(6) == .25
    assert g1(8) == .75
    assert g1(10) == .8
    assert g1(12) == .2
    with pytest.raises(FuncDoneException):
        g1(14)

    assert_times()


def test_timebase_func(function_factory: FunctionFactoryBase):
    const_cls = function_factory.get('ConstFunc')
    f = const_cls(function_factory=function_factory)
    assert f.get_timebase() == 1

    f = const_cls(function_factory=function_factory, timebase_numerator=1,
                  timebase_denominator=2)
    assert f.get_timebase() == 0.5


def test_timebase_group(function_factory: FunctionFactoryBase):
    g = FuncGroup(function_factory=function_factory)
    assert g.get_timebase() == 1

    const_cls = function_factory.get('ConstFunc')
    f = const_cls(function_factory=function_factory)
    assert f.get_timebase() == 1

    g.add_func(f)
    assert f.get_timebase() == 1

    g.timebase_numerator = 1
    g.timebase_denominator = 4
    assert g.get_timebase() == 1 / 4
    assert f.get_timebase() == 1 / 4

    f.timebase_numerator = 1
    f.timebase_denominator = 8
    assert g.get_timebase() == 1 / 4
    assert f.get_timebase() == 1 / 8

    f.timebase_numerator = 0
    assert g.get_timebase() == 1 / 4
    assert f.get_timebase() == 1 / 4

    f.timebase_numerator = 1
    assert g.get_timebase() == 1 / 4
    assert f.get_timebase() == 1 / 8

    g.timebase_numerator = 0
    assert g.get_timebase() == 1
    assert f.get_timebase() == 1 / 8


def create_recursive_funcs(function_factory):
    factory = function_factory
    const_cls = factory.get('ConstFunc')

    g1 = FuncGroup(
        function_factory=factory, timebase_denominator=2, timebase_numerator=1)

    g2 = FuncGroup(
        function_factory=factory, timebase_denominator=4, timebase_numerator=1)
    g1.add_func(g2)
    f = const_cls(
        function_factory=factory, a=.9, duration=2, timebase_denominator=8,
        timebase_numerator=1)
    g2.add_func(f)
    f1 = const_cls(function_factory=factory, a=.1, duration=2)
    g2.add_func(f1)

    f2 = const_cls(function_factory=factory, a=.25, duration=2)
    g1.add_func(f2)
    f3 = const_cls(function_factory=factory, a=.75, duration=2)
    g1.add_func(f3)

    g3 = FuncGroup(function_factory=factory)
    g1.add_func(g3)
    f4 = const_cls(
        function_factory=factory, a=.8, duration=2, timebase_denominator=8,
        timebase_numerator=1)
    g3.add_func(f4)
    f5 = const_cls(function_factory=factory, a=.2, duration=2)
    g3.add_func(f5)

    return g1, g2, f, f1, f2, f3, g3, f4, f5


def test_recursive_timebase(function_factory: FunctionFactoryBase):
    g1, g2, f, f1, f2, f3, g3, f4, f5 = create_recursive_funcs(
        function_factory)

    def assert_times():
        assert list(g2.get_funcs()) == [g2, f, f1]
        assert g2.duration == (2 / 8 + 2 / 4) * 4
        assert g2.duration_min == (2 / 8 + 2 / 4) * 4
        assert g2.duration_min_total == (2 / 8 + 2 / 4) * 4

        assert list(g3.get_funcs()) == [g3, f4, f5]
        assert g3.duration == (2 / 8 + 2 / 2) * 2
        assert g3.duration_min == (2 / 8 + 2 / 2) * 2
        assert g3.duration_min_total == (2 / 8 + 2 / 2) * 2

        assert list(g1.get_funcs()) == [g1, g2, f, f1, f2, f3, g3, f4, f5]
        assert g1.duration == (4 / 8 + 2 / 4 + 6 / 2) * 2
        assert g1.duration_min == (4 / 8 + 2 / 4 + 6 / 2) * 2
        assert g1.duration_min_total == (4 / 8 + 2 / 4 + 6 / 2) * 2
    assert_times()

    g1.init_func(2)
    with pytest.raises(ValueError):
        g1(0)
    assert g1(2) == .9
    assert g1(2 + 2 / 8) == .1
    assert g1(2 + 2 / 8 + 2 / 4) == .25
    assert g1(2 + 2 / 8 + 2 / 4 + 2 / 2) == .75
    assert g1(2 + 2 / 8 + 2 / 4 + 4 / 2) == .8
    assert g1(2 + 4 / 8 + 2 / 4 + 4 / 2) == .2
    with pytest.raises(FuncDoneException):
        g1(2 + 4 / 8 + 2 / 4 + 6 / 2)

    assert_times()


def test_recursive_timebase_trigger(function_factory: FunctionFactoryBase):
    g1, g2, f, f1, f2, f3, g3, f4, f5 = create_recursive_funcs(
        function_factory)

    for func in g1.get_funcs():
        add_prop_watch(func, 'timebase', 'test_timebase_changes_count')

    g1.timebase_denominator = 16
    assert g1.test_timebase_changes_count
    assert not g2.test_timebase_changes_count
    assert not f.test_timebase_changes_count
    assert not f1.test_timebase_changes_count
    assert f2.test_timebase_changes_count
    assert f3.test_timebase_changes_count
    assert g3.test_timebase_changes_count
    assert not f4.test_timebase_changes_count
    assert f5.test_timebase_changes_count
    assert g1.duration == (4 / 8 + 2 / 4 + 6 / 16) * 16

    for func in g1.get_funcs():
        setattr(func, 'test_timebase_changes_count', 0)

    f2.timebase_numerator = 1
    assert not g1.test_timebase_changes_count
    assert not g2.test_timebase_changes_count
    assert not f.test_timebase_changes_count
    assert not f1.test_timebase_changes_count
    assert f2.test_timebase_changes_count
    assert not f3.test_timebase_changes_count
    assert not g3.test_timebase_changes_count
    assert not f4.test_timebase_changes_count
    assert not f5.test_timebase_changes_count
    assert g1.duration == (4 / 8 + 2 / 4 + 4 / 16 + 2) * 16


def test_recursive_parent_func(function_factory: FunctionFactoryBase):
    g1, g2, f, f1, f2, f3, g3, f4, f5 = create_recursive_funcs(
        function_factory)
    assert f5.parent_func is g3
    assert f4.parent_func is g3
    assert g3.parent_func is g1
    assert f3.parent_func is g1
    assert f2.parent_func is g1
    assert f1.parent_func is g2
    assert f.parent_func is g2
    assert g2.parent_func is g1


def test_can_other_func_be_added(function_factory: FunctionFactoryBase):
    g1, g2, f, f1, f2, f3, g3, f4, f5 = create_recursive_funcs(
        function_factory)

    assert g1.can_other_func_be_added(g2)
    assert g1.can_other_func_be_added(g3)
    assert not g1.can_other_func_be_added(g1)

    assert not g2.can_other_func_be_added(g1)
    assert g2.can_other_func_be_added(g3)
    assert not g2.can_other_func_be_added(g2)

    assert not g3.can_other_func_be_added(g1)
    assert g3.can_other_func_be_added(g2)
    assert not g3.can_other_func_be_added(g3)


def test_func_ref(function_factory: FunctionFactoryBase):
    const_cls = function_factory.get('ConstFunc')
    f = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    f2 = const_cls(
        function_factory=function_factory, duration=5, a=.9, name='f')

    function_factory.add_func(f)

    ref1 = function_factory.get_func_ref(name='f')
    ref2 = function_factory.get_func_ref(func=f2)

    assert ref1.func is f
    assert ref2.func is f2
    assert f.has_ref
    assert f2.has_ref
    assert f in function_factory._ref_funcs
    assert f2 in function_factory._ref_funcs

    function_factory.return_func_ref(ref1)
    assert ref2.func is f2
    assert not f.has_ref
    assert f2.has_ref
    assert f not in function_factory._ref_funcs
    assert f2 in function_factory._ref_funcs

    function_factory.return_func_ref(ref2)
    assert not f.has_ref
    assert not f2.has_ref
    assert f not in function_factory._ref_funcs
    assert f2 not in function_factory._ref_funcs


def test_return_not_added_func_ref(function_factory: FunctionFactoryBase):
    from ceed.function import CeedFuncRef
    const_cls = function_factory.get('ConstFunc')
    f = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    ref = CeedFuncRef(function_factory=function_factory, func=f)

    with pytest.raises(ValueError):
        function_factory.return_func_ref(ref)


def test_remove_func_with_ref(function_factory: FunctionFactoryBase):
    const_cls = function_factory.get('ConstFunc')
    f = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    f2 = const_cls(
        function_factory=function_factory, duration=5, a=.9, name='f2')
    f3 = const_cls(
        function_factory=function_factory, duration=5, a=.9, name='f3')

    function_factory.add_func(f)
    function_factory.add_func(f2)
    function_factory.add_func(f3)

    assert function_factory.funcs_inst['f'] is f
    assert f in function_factory.funcs_user
    assert function_factory.funcs_inst['f2'] is f2
    assert f2 in function_factory.funcs_user
    assert function_factory.funcs_inst['f3'] is f3
    assert f3 in function_factory.funcs_user

    ref = function_factory.get_func_ref(name='f')
    ref3 = function_factory.get_func_ref(name='f3')
    assert not function_factory.remove_func(f)

    assert ref.func is f
    assert f.has_ref
    assert function_factory.funcs_inst['f'] is f
    assert f in function_factory.funcs_user
    assert function_factory.funcs_inst['f2'] is f2
    assert f2 in function_factory.funcs_user
    assert function_factory.funcs_inst['f3'] is f3
    assert f3 in function_factory.funcs_user

    assert function_factory.remove_func(f2)

    assert function_factory.funcs_inst['f'] is f
    assert f in function_factory.funcs_user
    assert 'f2' not in function_factory.funcs_inst
    assert f2 not in function_factory.funcs_user
    assert function_factory.funcs_inst['f3'] is f3
    assert f3 in function_factory.funcs_user

    assert not function_factory.remove_func(f3)

    assert ref3.func is f3
    assert f3.has_ref
    assert function_factory.funcs_inst['f'] is f
    assert f in function_factory.funcs_user
    assert function_factory.funcs_inst['f3'] is f3
    assert f3 in function_factory.funcs_user

    assert function_factory.remove_func(f3, force=True)

    assert ref3.func is f3
    assert f3.has_ref
    assert function_factory.funcs_inst['f'] is f
    assert f in function_factory.funcs_user
    assert 'f3' not in function_factory.funcs_inst
    assert f3 not in function_factory.funcs_user

    assert not function_factory.remove_func(f)

    assert ref.func is f
    assert f.has_ref
    assert function_factory.funcs_inst['f'] is f
    assert f in function_factory.funcs_user

    function_factory.return_func_ref(ref)
    assert not f.has_ref

    assert function_factory.remove_func(f)

    assert 'f' not in function_factory.funcs_inst
    assert f not in function_factory.funcs_user

    function_factory.return_func_ref(ref3)
    assert not f3.has_ref


def test_clear_funcs_with_ref(function_factory: FunctionFactoryBase):
    const_cls = function_factory.get('ConstFunc')
    f = const_cls(
        function_factory=function_factory, duration=4, a=.7, name='f')
    f2 = const_cls(
        function_factory=function_factory, duration=5, a=.9, name='f2')

    function_factory.add_func(f)
    function_factory.add_func(f2)

    assert function_factory.funcs_inst['f'] is f
    assert f in function_factory.funcs_user
    assert function_factory.funcs_inst['f2'] is f2
    assert f2 in function_factory.funcs_user

    ref = function_factory.get_func_ref(name='f')
    function_factory.clear_added_funcs()

    # f should not have been removed, but f2 was removed
    assert ref.func is f
    assert f.has_ref
    assert function_factory.funcs_inst['f'] is f
    assert f in function_factory.funcs_user
    assert 'f2' not in function_factory.funcs_inst
    assert f2 not in function_factory.funcs_user

    function_factory.clear_added_funcs(force=True)

    assert ref.func is f
    assert f.has_ref
    assert 'f' not in function_factory.funcs_inst
    assert f not in function_factory.funcs_user

    function_factory.return_func_ref(ref)
    assert not f.has_ref


def test_recover_ref_funcs(function_factory: FunctionFactoryBase):
    from ceed.function import FuncGroup, CeedFuncRef
    f1 = function_factory.get('ConstFunc')(
        function_factory=function_factory, a=.5, name='f1', duration=1.2)
    f2 = function_factory.get('LinearFunc')(
        function_factory=function_factory, m=.5, b=.2, name='f2', duration=1.2)
    f3 = function_factory.get('ExponentialFunc')(
        function_factory=function_factory, A=.5, B=.2, tau1=1.3, tau2=1.5,
        name='f3', duration=1.2)
    f4 = function_factory.get('CosFunc')(
        function_factory=function_factory, f=.5, A=3.4, th0=7.5, b=12.2,
        name='f4', duration=1.2)
    g = FuncGroup(function_factory=function_factory, name='g')

    function_factory.add_func(f1)
    function_factory.add_func(f2)
    function_factory.add_func(f3)
    function_factory.add_func(f4)
    function_factory.add_func(g)

    g.add_func(function_factory.get_func_ref(name='f1'))
    g.add_func(function_factory.get_func_ref(name='f2'))
    g.add_func(function_factory.get_func_ref(name='f3'))
    g.add_func(function_factory.get_func_ref(name='f4'))

    funcs = function_factory.save_functions()
    assert len(funcs) == 5

    recovered_funcs, name_mapping = function_factory.recover_funcs(funcs)
    assert len(recovered_funcs) == 5
    assert len(name_mapping) == 5

    for f_name in ('f1', 'f2', 'f3', 'f4', 'g'):
        assert f_name in name_mapping
        assert name_mapping[f_name] != f_name
        assert f_name in function_factory.funcs_inst
        assert name_mapping[f_name] in function_factory.funcs_inst

        for name in function_factory.funcs_inst[f_name].get_gui_props():
            original_f = function_factory.funcs_inst[f_name]
            new_f = function_factory.funcs_inst[name_mapping[f_name]]

            if name == 'name':
                assert original_f.name != new_f.name
                assert new_f.name.startswith(original_f.name)
                continue

            assert getattr(original_f, name) == getattr(new_f, name)

    new_g: FuncGroup = function_factory.funcs_inst[name_mapping['g']]
    assert len(new_g.funcs) == 4

    func: CeedFuncRef
    for func, name in zip(new_g.funcs, ('f1', 'f2', 'f3', 'f4')):
        assert isinstance(func, CeedFuncRef)
        assert func.func is function_factory.funcs_inst[name_mapping[name]]


def test_get_funcs_ref(function_factory: FunctionFactoryBase):
    factory = function_factory
    const_cls = factory.get('ConstFunc')

    g1 = FuncGroup(function_factory=factory)

    g2 = FuncGroup(function_factory=factory)
    ref_g2 = function_factory.get_func_ref(func=g2)
    g1.add_func(ref_g2)

    f = const_cls(function_factory=factory, a=.9, duration=2)
    g2.add_func(f)

    f2 = const_cls(function_factory=factory, a=.25, duration=2)
    g1.add_func(f2)

    assert list(g1.get_funcs()) == [g1, g2, f, f2]
    assert list(g1.get_funcs(step_into_ref=False)) == [g1, ref_g2, f2]
    assert g1.duration == 4
    assert g1.duration_min == 4
    assert g1.duration_min_total == 4


def test_call_funcs_ref(function_factory: FunctionFactoryBase):
    factory = function_factory
    const_cls = factory.get('ConstFunc')

    g1 = FuncGroup(function_factory=factory)

    g2 = FuncGroup(function_factory=factory)
    ref_g2 = function_factory.get_func_ref(func=g2)
    g1.add_func(ref_g2)

    f = const_cls(function_factory=factory, a=.9, duration=2)
    g2.add_func(f)

    f2 = const_cls(function_factory=factory, a=.25, duration=2)
    g1.add_func(f2)

    with pytest.raises(TypeError):
        g1.init_func(0)

    with pytest.raises(TypeError):
        ref_g2.init_func(0)

    with pytest.raises(TypeError):
        ref_g2(0)

    with pytest.raises(TypeError):
        g1(0)


def test_can_other_func_be_added_ref(function_factory: FunctionFactoryBase):
    factory = function_factory
    const_cls = factory.get('ConstFunc')

    g1 = FuncGroup(function_factory=factory)

    g2 = FuncGroup(function_factory=factory)
    ref_g2 = function_factory.get_func_ref(func=g2)
    g1.add_func(ref_g2)

    f = const_cls(function_factory=factory, a=.9, duration=2)
    g2.add_func(f)

    f2 = const_cls(function_factory=factory, a=.25, duration=2)
    g1.add_func(f2)

    g3 = FuncGroup(function_factory=factory)
    g1.add_func(g3)
    f4 = const_cls(function_factory=factory, a=.8, duration=2)
    g3.add_func(f4)

    assert g1.can_other_func_be_added(g2)
    assert g1.can_other_func_be_added(ref_g2)
    assert g1.can_other_func_be_added(g3)
    assert not g1.can_other_func_be_added(g1)

    assert not g2.can_other_func_be_added(g1)
    assert g2.can_other_func_be_added(g3)
    assert not g2.can_other_func_be_added(g2)
    assert not g2.can_other_func_be_added(ref_g2)

    assert not g3.can_other_func_be_added(g1)
    assert g3.can_other_func_be_added(g2)
    assert g3.can_other_func_be_added(ref_g2)
    assert not g3.can_other_func_be_added(g3)


def test_expand_ref_funcs(function_factory: FunctionFactoryBase):
    from ceed.function import FuncGroup, CeedFuncRef
    factory = function_factory
    const_cls = factory.get('ConstFunc')

    g1 = FuncGroup(function_factory=factory)

    g2 = FuncGroup(function_factory=factory)
    ref_g2 = function_factory.get_func_ref(func=g2)
    g1.add_func(ref_g2)

    f = const_cls(function_factory=factory, a=.9, duration=2)
    g2.add_func(f)
    f1 = const_cls(function_factory=factory, a=.1, duration=2)
    g2.add_func(f1)

    f2 = const_cls(function_factory=factory, a=.25, duration=2)
    g1.add_func(f2)
    f3 = const_cls(function_factory=factory, a=.75, duration=2)
    ref_f3 = function_factory.get_func_ref(func=f3)
    g1.add_func(ref_f3)

    g3 = FuncGroup(function_factory=factory)
    g1.add_func(g3)
    f4 = const_cls(function_factory=factory, a=.8, duration=2)
    ref_f4 = function_factory.get_func_ref(func=f4)
    g3.add_func(ref_f4)
    f5 = const_cls(function_factory=factory, a=.2, duration=2)
    g3.add_func(f5)

    assert list(g1.get_funcs(step_into_ref=False)) == \
        [g1, ref_g2, f2, ref_f3, g3, ref_f4, f5]
    assert list(g1.get_funcs(step_into_ref=True)) == \
        [g1, g2, f, f1, f2, f3, g3, f4, f5]

    g1_copy = g1.copy_expand_ref()
    # the copy shouldn't have any refs
    assert len(list(g1_copy.get_funcs(step_into_ref=False))) == \
        len(list(g1.get_funcs(step_into_ref=True)))

    for original_f, new_f in zip(
            g1.get_funcs(step_into_ref=True),
            g1_copy.get_funcs(step_into_ref=False)):
        for name in original_f.get_gui_props():
            if name == 'name':
                continue

            assert getattr(original_f, name) == getattr(new_f, name)


def test_t_offset(function_factory: FunctionFactoryBase):
    f1 = function_factory.get('ConstFunc')(
        function_factory=function_factory, a=.5, name='f1', t_offset=3.5,
        duration=1.2)
    f2 = function_factory.get('LinearFunc')(
        function_factory=function_factory, m=.5, b=.2, name='f2', t_offset=3.5,
        duration=1.2)
    f3 = function_factory.get('ExponentialFunc')(
        function_factory=function_factory, A=.5, B=.2, tau1=1.3, tau2=1.5,
        name='f3', t_offset=3.5, duration=1.2)
    f4 = function_factory.get('CosFunc')(
        function_factory=function_factory, f=.5, A=3.4, th0=7.5, b=12.2,
        name='f4', t_offset=3.5, duration=1.2)

    for f in (f1, f2, f3, f4):
        f.init_func(2.3)

    t = 1 + 3.5
    assert math.isclose(f1(3.3), .5)
    assert math.isclose(f2(3.3), t * .5 + .2)
    assert math.isclose(
        f3(3.3), .5 * math.exp(-t / 1.3) + .2 * math.exp(-t / 1.5)
    )
    assert math.isclose(
        f4(3.3),
        3.4 * math.cos(2 * math.pi * .5 * t + 7.5 * math.pi / 180.) + 12.2
    )


def test_copy_funcs(function_factory: FunctionFactoryBase):
    from ceed.function import FuncGroup, CeedFuncRef
    f1 = function_factory.get('ConstFunc')(
        function_factory=function_factory, a=.5, name='f1', duration=1.2)
    f2 = function_factory.get('LinearFunc')(
        function_factory=function_factory, m=.5, b=.2, name='f2', duration=1.2)
    f3 = function_factory.get('ExponentialFunc')(
        function_factory=function_factory, A=.5, B=.2, tau1=1.3, tau2=1.5,
        name='f3', duration=1.2)
    f4 = function_factory.get('CosFunc')(
        function_factory=function_factory, f=.5, A=3.4, th0=7.5, b=12.2,
        name='f4', duration=1.2)
    g = FuncGroup(function_factory=function_factory, name='g')

    function_factory.add_func(f1)
    function_factory.add_func(f2)
    function_factory.add_func(f3)
    function_factory.add_func(f4)

    g.add_func(function_factory.get_func_ref(func=f1))
    g.add_func(function_factory.get_func_ref(func=f2))
    g.add_func(function_factory.get_func_ref(func=f3))
    g.add_func(function_factory.get_func_ref(func=f4))

    for func in (f1, f2, f3, f4):
        func_copy = copy.deepcopy(func)
        assert func is not func_copy
        assert isinstance(func_copy, func.__class__)

        for name in func.get_gui_props():
            if name == 'name':
                continue

            assert getattr(func, name) == getattr(func_copy, name)

    func_copy = copy.deepcopy(g)
    assert len(func_copy.funcs) == 4
    for new_f, original_f in zip(func_copy.funcs, g.funcs):
        assert new_f is not original_f
        assert isinstance(new_f, CeedFuncRef)
        assert isinstance(original_f, CeedFuncRef)
        assert new_f.func is original_f.func


def test_replace_ref_func_with_source_funcs(
        function_factory: FunctionFactoryBase):
    from ceed.function import FuncGroup, CeedFuncRef
    factory = function_factory
    const_cls = factory.get('ConstFunc')

    g1 = FuncGroup(function_factory=factory, name='g1')

    g2 = FuncGroup(function_factory=factory, name='g2')
    ref_g2 = function_factory.get_func_ref(func=g2)
    g1.add_func(ref_g2)

    f = const_cls(function_factory=factory, a=.9, duration=2)
    g2.add_func(f)

    f1 = const_cls(function_factory=factory, a=.1, duration=2, name='f1')
    function_factory.add_func(f1)
    ref_f1 = function_factory.get_func_ref(func=f1)
    g2.add_func(ref_f1)

    f2 = const_cls(function_factory=factory, a=.25, duration=2)
    g1.add_func(f2)

    f3 = const_cls(function_factory=factory, a=.75, duration=2, name='f3')
    function_factory.add_func(f3)
    ref_f3 = function_factory.get_func_ref(func=f3)
    g1.add_func(ref_f3)

    with pytest.raises(ValueError):
        g1.replace_ref_func_with_source(f2)

    with pytest.raises(ValueError):
        g1.replace_ref_func_with_source(ref_f1)

    f3_new, i = g1.replace_ref_func_with_source(ref_f3)

    assert i == 2
    assert ref_f3 not in g1.funcs
    assert f3 not in g1.funcs
    assert not isinstance(f3_new, CeedFuncRef)
    assert isinstance(f3_new, f3.__class__)
    assert g1.funcs[i] is f3_new

    for name in f3.get_gui_props():
        if name == 'name':
            continue
        assert getattr(f3, name) == getattr(f3_new, name)

    g2_new: FuncGroup
    g2_new, i = g1.replace_ref_func_with_source(ref_g2)

    assert i == 0
    assert ref_g2 not in g1.funcs
    assert g2 not in g1.funcs
    assert not isinstance(g2_new, CeedFuncRef)
    assert isinstance(g2_new, FuncGroup)
    assert g1.funcs[i] is g2_new

    assert len(g2_new.funcs) == 2
    assert g2_new.funcs[0] is not g2.funcs[0]
    assert g2_new.funcs[1] is not g2.funcs[1]
    assert isinstance(g2_new.funcs[0], f.__class__)
    assert isinstance(g2_new.funcs[1], ref_f1.__class__)
    assert isinstance(g2_new.funcs[1], CeedFuncRef)

    for name in f.get_gui_props():
        if name == 'name':
            continue
        assert getattr(f, name) == getattr(g2_new.funcs[0], name)
    assert g2_new.funcs[1].func is f1


def test_group_remove_func(function_factory: FunctionFactoryBase):
    factory = function_factory
    const_cls = factory.get('ConstFunc')

    g1 = FuncGroup(function_factory=factory)

    g2 = FuncGroup(function_factory=factory)
    ref_g2 = function_factory.get_func_ref(func=g2)
    g1.add_func(ref_g2)
    f = const_cls(function_factory=factory, a=.9, duration=2)
    g2.add_func(f)
    f1 = const_cls(function_factory=factory, a=.9, duration=2)
    g2.add_func(f1)

    f2 = const_cls(function_factory=factory, a=.25, duration=2)
    g1.add_func(f2)

    assert list(g1.get_funcs(step_into_ref=False)) == [g1, ref_g2, f2]
    assert g1.duration == 6
    assert g1.duration_min == 6
    assert g1.duration_min_total == 6

    g1.remove_func(f2)
    assert list(g1.get_funcs(step_into_ref=False)) == [g1, ref_g2]
    assert g1.duration == 4
    assert g1.duration_min == 4
    assert g1.duration_min_total == 4

    g2.remove_func(f)
    assert list(g1.get_funcs(step_into_ref=False)) == [g1, ref_g2]
    assert g1.duration == 2
    assert g1.duration_min == 2
    assert g1.duration_min_total == 2

    g1.remove_func(ref_g2)
    assert list(g1.get_funcs(step_into_ref=False)) == [g1, ]
    assert g1.duration == 0
    assert g1.duration_min == 0
    assert g1.duration_min_total == 0
