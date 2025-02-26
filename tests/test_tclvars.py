
import tohil

import hypothesis
from hypothesis import given, strategies as st
import unittest

tohil.eval("""namespace forget ::tohil_test; namespace eval ::tohil_test {}""")

class TclVarTests(unittest.TestCase):
    @given(st.integers(-1000000000, 1000000000), st.integers(-1000000000, 1000000000))
    def test_tclvar1(self, x, y):
        """test 'tclvar' tcolbj var sync into tcl and see it from python and vice versa"""
        ns_name = "::tohil_test"
        xname = ns_name + "::varsync_x"
        yname = ns_name + "::varsync_y"

        tohil.unset(xname, yname)

        tx = tohil.tclvar(xname, default=x)
        ty = tohil.tclvar(yname, default=y)

        # compare the tclvar to tcl via a few different approaches
        assert tx == x
        assert tx == tohil.getvar(xname, to=int)
        assert tx == tohil.eval(f"set {xname}", to=int)
        assert tx == tohil.eval(f"return ${xname}", to=int)
        assert tx == tohil.expr(f"${xname}", to=int)

        # mutate tx tclvar and make sure the variable is changing
        # on the tcl side
        tx += ty
        assert tx == tohil.getvar(xname, to=int)
        assert tx == x + y
        assert tx == tohil.getvar(xname, to=int)
        assert tx == x + tohil.getvar(yname, to=int)
        tx -= ty
        assert tx == x
        assert tx == tohil.getvar(xname, to=int)

    @given(st.integers(-1000000000, 1000000000), st.integers(-1000000000, 1000000000))
    def test_tclvar2(self, x, y):
        """test tclvar tcobj shove stuff into tcl and see it from python and vice versa"""
        ns_name = "::tohil_test"
        xname = ns_name + "::varsync_x"
        yname = ns_name + "::varsync_y"

        tx = tohil.tclvar(xname)
        ty = tohil.tclvar(yname)

        tohil.eval(f"set {xname} {x}")
        tohil.eval(f"set {yname} {y}")

        assert tx == tx
        assert tx == x
        assert ty == ty

        tohil.incr(xname)
        assert tx == x + 1
        assert tx == tohil.expr(f"${xname}")
        tohil.eval(f"incr {xname} -1")
        assert tx == x

    @given(st.lists(st.integers(-1000000000, 1000000000)))
    def test_tclvar3(self, x):
        """interoperate python lists back and forth with tcl lists"""
        ns_name = "::tohil_test"
        list_name = ns_name + "::varsync_list"

        tohil.unset(list_name)
        tl = tohil.tclvar(list_name, default=x)
        assert(str(tl) == tohil.getvar(list_name))

        assert(tl.as_list() == tohil.getvar(list_name, to=list))
        assert(list(tl) == tohil.getvar(list_name, to=list))


if __name__ == "__main__":
    unittest.main()
