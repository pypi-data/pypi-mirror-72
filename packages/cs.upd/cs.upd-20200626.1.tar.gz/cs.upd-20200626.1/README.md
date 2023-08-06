Single and multiple line status updates with minimal update sequences.

*Latest release 20200626.1*:
Upd.__exit__: bugfix test of SystemExit exceptions.

This is available as an output mode in `cs.logutils`.

Single line example:

    from cs.upd import Upd, nl, print
    .....
    with Upd() as U:
        for filename in filenames:
            U.out(filename)
            ... process filename ...
            U.nl('an informational line to stderr')
            print('a line to stdout')

Multiline multithread example:

    from threading import Thread
    from cs.upd import Upd, print
    .....
    def runner(filename, proxy):
        # initial status message
        proxy.text = "process %r" % filename
        ... at various points:
            # update the status message with current progress
            proxy.text = '%r: progress status here' % filename
        # completed, remove the status message
        proxy.close()
        # print completion message to stdout
        print("completed", filename)
    .....
    with Upd() as U:
        U.out("process files: %r", filenames)
        Ts = []
        for filename in filenames:
            proxy = U.insert(1) # allocate an additional status line
            T = Thread(
                "process "+filename,
                target=runner,
                args=(filename, proxy))
            Ts.append(T)
            T.start()
        for T in Ts:
            T.join()

## A note about Upd and terminals

I routinely use an `Upd()` as a progress reporting tool for commands
running on a terminal. This attaches to `sys.stderr`.
However, it is usually not desirable to run an `Upd` display
if the backend is not a tty/terminal.
Therefore, an `Upd` has a "disabled" mode
which performs no output;
if the backend is not a tty (as tested by `backend.isatty()`)
this mode activates by default.

The constructor has an optional parameter `disabled` to override
this default behaviour.

The whole purpose of this "disabled" mode is to ease main programme
implementation.
Without the mode one has two basic idioms to support "noninteractive" use,
described below.

The former is to test `sys.stderr.isatty()` and define an `Upd` or not:

    upd = Upd() if sys.stderr.isatty() else None

and to scatter tests throughout the code:

    if upd:
        upd.out("new status here")

The latter is to work entirely through `UpdProxy` instances
(which is convenient anyway), like this 2 status line example:

    if sys.stderr.isatty():
        upd = Upd()
        status_proxy = upd.proxy(0)
        progress_proxy = upd.insert(1)
    else:
        status_proxy = UpdProxy(None, None)
        progress_proxy = UpdProxy(None, None)

and to use the proxies thereafter:

    status_proxy.text = "doing task A"
    ... during task A ...
    ... progress_proxy.text = progress.status() ...

This works because `UpdProxy` instances support a "detached" mode,
which is they state they move to when deleted
in the normal course of operations.

However, because an `Upd` defaults to being "disabled"
if its backend is not a tty
the usual main programme can just set one up and use it unconditionally;
on a nontty there will simply be no output.

## Function `cleanupAtExit()`

Cleanup function called at programme exit to clear the status line.

## Function `nl(msg, *a, **kw)`

Write `msg` to `file` (default `sys.stdout`),
without interfering with the `Upd` instance.
This is a thin shim for `Upd.print`.

## Function `out(msg, *a, **outkw)`

Update the status line of the default `Upd` instance.
Parameters are as for `Upd.out()`.

## Function `print(*a, **kw)`

Wrapper for the builtin print function
to call it inside `Upd.above()` and enforce a flush.

The function supports an addition parameter beyond the builtin print:
* `upd`: the `Upd` instance to use, default `Upd()`

Programmes integrating `cs.upd` with use of the builtin `print`
function should use this at import time:

    from cs.upd import print

## Class `Upd(cs.obj.SingletonMixin)`

A `SingletonMixin` subclass for maintaining a regularly updated status line.

The default backend is `sys.stderr`.

## Class `UpdProxy`

A proxy for a status line of a multiline `Upd`.

This provides a stable reference to a status line after it has been
instantiated by `Upd.insert`.

The status line can be accessed and set via the `.text` property.

An `UpdProxy` is also a context manager which self deletes on exit:

    U = Upd()
    ....
    with U.insert(1, 'hello!') as proxy:
        .... set proxy.text as needed ...
    # proxy now removed

# Release Log



*Release 20200626.1*:
Upd.__exit__: bugfix test of SystemExit exceptions.

*Release 20200626*:
* UpdProxy: call self.delete on __del__.
* If self._backend is None act as if disabled, occurs during shutdown.
* Upd.delete: ignore attempts to delete the last line, also occurs during shutdown.

*Release 20200621*:
New "disabled" mode, triggered by default if not backend.isatty().

*Release 20200613*:
* New UpdProxy.__call__ which sets the .text property in the manner of logging calls, with (msg,*a).
* New Upd.normalise static method exposing the text normalisation `unctrl(text.rstrip())`.
* New UpdProxy.prefix attribute with a fixed prefix for status updates; `prefix+text` is left cropped for display purposes when updated.
* New UpdProxy.width property computing the space available after the prefix, useful for sizing things like progress bars.
* Make UpdProxy a context manager which self deletes on exit.
* Upd: make default backend=sys.stderr, eases the common case.
* New Upd.above() context manager to support interleaving another stream with the output, as when stdout (for print) is using the same terminal as stderr (for Upd).
* New out() top level function for convenience use with the default Upd().
* New nl() top level function for writing a line to stderr.
* New print() top level function wrapping the builtin print; callers can use "from cs.upd import print" to easily interleave print() with cs.upd use.

*Release 20200517*:
* Multiline support!
* Multiline support!
* Multiline support!
* New UpdProxy class to track a status line of a multiline Upd in the face of further inserts and deletes.
* Upd(...) now returns a context manager to clean up the display on its exit.
* Upd(...) is now a SingletonMixin in order to use the same state if set up in multiple places.

*Release 20200229*:
* Upd: can now be used as a context manager, clearing the line on exit.
* Upd.without is now a context manager, returning the older state, and accepting an optional inner state (default "").
* Upd is now a singleton factory, obsoleting upd_for.
* Upd.nl: use "insert line above" mode if supported.

*Release 20181108*:
Documentation improvements.

*Release 20170903*:
* New function upd_for(stream) returning singleton Upds.
* Drop noStrip keyword argument/mode - always strip trailing whitespace.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* Add Upd.flush method.
* Upd.out: fix longstanding trailing text erasure bug.
* Upd.nl,out: accept optional positional parameters, use with %-formatting if supplied, just like logging.

*Release 20150118*:
metadata fix

*Release 20150116*:
Initial PyPI release.
