


## I want to get up and running as quickly as possible, accessing my tcl stuff from python.

Great!

Tohil gives you a few options for how to run tcl code and access tcl data
from python.


The easiest way is to load up your tcl
code and then use tohil.import_tcl() to create corresponding
python functions, and start using them.

```
import tohil
tohil.package_require("Tclx")
tcl = tohil.import_tcl()
>>> intersect_list = tcl.intersect(["A", "B", "C", "D", "E", "F"], ["D", "E", "F", "G", "H", "I"], to=list)
>>> intersect_list
['D', 'E', 'F']
```

Bam.  That's it.  This really is enough to get going.

But let's go ahead and dig a little deeper.

Note the use of `to=list`, indicating we want the result as a python list.
All the python functions tohil makes and most or all tohil functions that
return data from tcl support a "to" named parameter, allowing the caller
to specify what python data type
they want to get the result back as.  You can get stuff back as str (the
default), int, bool, float, list, set, dict, tuple, or as one of a
couple of data types that tohil itself provides, tohil.tclobj and
tohil.tcldict.  More on this later.

You probably noticed `tohil.package_require()` above.  Yeah, that's
a convenience function tohil provides, along with `tohil.source()`
for sourcing in tcl code, and a few others.

Once you've used import_tcl() to import all of tcl into python, you
can as easily do `tcl.package("require", "yajl")` or
`tcl.source("myfile.tcl)`.

There's nothing special about calling the thing resulting from
import_tcl() "tcl", by the way.  It's a TclNamespace object, you're
invoking your tcl procs and C commands by invoking methods on it.

All the Tcl namespaces are recursively imported, and chaining works,
so you can chain through namespaces to get to a function









"tcl", above, is a TclNamespace object, and all the procs and C commands
found are methods.



After building and installing tohil, from python you should be able
to `import tohil` from the python command line.




You can pick and choose what you need, and how far you want to go.


### tohil.eval

The simplest way to do something with tcl from python, is to
use `tohil.eval`.

```
import tohil
tohil.eval("package require Tclx")
```

You can call tohil.eval as much as you want, and feed it any tcl
code, and tcl will evaluate it, and return the result.
If a tcl error occurs and it isn't caught by "try" or "catch",
tohil will raise a python TclError exception that contains all
the stuff tcl knows about the error.

Pretty cool.  Very handy.  You'll probably use it some, and for some
people it may be all that they need.

But if we get to the point where we're trying to embed data into the
stuff we're passing to "eval", like say with f-strings or something...

```
tohil.eval(f"""set users({user}) [list name "{name}" address "{address}" phone "{phone}"]""")
```

^ don't do this!

...we are asking for trouble.  Dollar signs, double quotes, curly brackets,
square brackets in the data, the tcl interpreter will try to interpret it.

You can do some heavy lifting to try to make sure that the data if properly
quoted, but that's pretty hard and kind of error prone and if you miss
running your data through your conditioner anywhere, you've got the risk
of the problem again.

```
>>> tohil.package_require("clock::rfc2822")
'0.1'
>>> clock = tohil.eval('::clock::rfc2822::parse_date "Wed, 14 Apr 2021 12:04:48 -0500"')
>>> clock
'1618419888'
```

### tohil.call

tohil.call is a way to call tcl with each argument specified explicitly.

This way, even if the arguments contain metacharacters we can ensure they
are not evaluated by tcl because when invoked this way, tcl will not
evaluate tohil.call's arguments.

```
>>> user = "leon"
>>> name = "Leon Kowalski"
>>> address = "1187 Unterwasser"
>>> phone = "+1-415-555-2822"
>>> tohil.call("set", f"users({user})", tohil.call("list", "name", name, "address", address, "phone", phone))
'name {Leon Kowalski} address {1187 Unterwasser} phone +1-415-555-2822'
```


```
>>> clock = tohil.call('::clock::rfc2822::parse_date', "Wed, 14 Apr 2021 12:04:48 -0500")
>>> clock
'1618419888'
```

There are tcl-side equivalents to these things for calling python from
tcl, by the way.

So that's handy.

But since you have to explicitly invoke this "call" function when
you want to call, that can get old pretty quick.

"Fluent" would be where the tcl commands look and act like python commands
to a very high degree.

"Fluent" also would mean that when exceptions and errors are handled
gracefully across the boundary between the two languages.  That is,
for example, if a python exception is thrown and no python code in the
call stack traps it, ergo it makes its way all the way back to tcl,
that it is translated into a tcl error that represents the python error
in a way that is thorough and accurate, such that tcl code can figure
out the error and see the important error information such as the
traceback, error object type, etc, using tcl's facilities for doing that.
Tohil supports that.

Likewise from the python side, an uncaught tcl error from tcl code
invoked from python should throw a python exception by creating an
exception object that robustly contains the tcl error information,
and tohil does that with its TclError class, which can be poked and
prodded to find out the tcl result, error code, traceback, etc.

Recognize that it's going to need to go both ways.  Once you begin to create
your libraries of python code, it'll be inevitable that you'll need to
call python from tcl as well.  Currently from tcl you need to use
tohil::eval, tohil::exec, and tohil::call to call python, although
Gerald Lester's pyman extension points to a way to introspect python to
generate tcl-side code structures to make python functions and classes
look to tcl like tcl ones.  We are likely to add such support in a
future version of tohil.



WHEN we import namespaces should we also import variables and arrays!?!?

could it see the non-array namespace variables as a dict of variables associated with the namespace






