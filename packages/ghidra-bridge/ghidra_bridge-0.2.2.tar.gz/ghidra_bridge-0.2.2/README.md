Ghidra Bridge
=====================
Ghidra is great, and I like scripting as much of my RE as possible. But Ghidra's Python scripting is based on Jython, which isn't in a great state these days. Installing new packages is a hassle, if they can even run in a Jython environment, and it's only going to get worse as Python 2 slowly gets turned off.

So Ghidra Bridge is an effort to sidestep that problem - instead of being stuck in Jython, set up an RPC proxy for Python objects, so we can call into Ghidra/Jython-land to get the data we need, then bring it back to a more up-to-date Python with all the packages you need to do your work. 

The aim is to be as transparent as possible, so once you're set up, you shouldn't need to know if an object is local or from the remote Ghidra - the bridge should seamlessly handle getting/setting/calling against it.

How to use for Ghidra
======================

## Install the Ghidra Bridge package and server scripts
1. Install the ghidra_bridge package (packaged at https://pypi.org/project/ghidra-bridge/):
```
pip install ghidra_bridge
```

2. Install the server scripts to a directory on the Ghidra's script path (e.g., ~/ghidra_scripts, or you can add more directories in the Ghidra Script Manager by clicking the "3 line" button left of the big red "plus" at the top of the Script Manager).
```
python -m ghidra_bridge.install_server ~/ghidra_scripts
```
3. (optional) In the Ghidra Script Manager, select the Bridge folder and click the "In Tool" checkbox at the far left for the ghidra_bridge_server_background.py and ghidra_bridge_server_shutdown.py scripts. This will add these scripts as convenient menu items in Tools->Ghidra Bridge. 

## Start Server
### CodeBrowser Context

For a better interactive shell like IPython or if you need Python 3 libraries in your interactive environment you can start the bridge in the context of an interactive GUI session.

1. If you've done step 3 in the install instructions above, click Tools->Ghidra Bridge->Run in Background.

Otherwise:
1. Open the Ghidra Script Manager.
2. Select the Bridge folder.
3. Run the ghidra_bridge_server_background.py script for a clean, no-popups bridge. You can also use ghidra_bridge_server.py if for some reason you want a big script popup in your face the whole time.

### Headless Analysis Context

You can run Ghidra Bridge as a post analysis script for a headless analysis and then run some further analysis from the client. Use the ghidra_bridge_server.py (not \_background.py) for this one, so it doesn't exit until you shut the bridge down. 
```
$ghidraRoot/support/analyzeHeadless ghidra-project -import /bin/ls  -scriptPath <install directory for the server scripts> -postscript ghidra_bridge_server.py
```
### pythonRun Context

You can start the bridge in an environment without any program loaded, for example if you want to access some API like the DataTypeManager that doesn't require a program being analyzed

```
$ghidraRoot/support/pythonRun <install directory for the server scripts>/ghidra_bridge_server.py
```

## Setup Client
From the client python environment:
```python
import ghidra_bridge
with ghidra_bridge.GhidraBridge(namespace=globals()):
    print(getState().getCurrentAddress().getOffset())
    ghidra.program.model.data.DataUtilities.isUndefinedData(currentProgram, currentAddress)
```
or
```python
import ghidra_bridge
b = ghidra_bridge.GhidraBridge(namespace=globals()) # creates the bridge and loads the flat API into the global namespace
print(getState().getCurrentAddress().getOffset())
# ghidra module implicitly loaded at the same time as the flat API
ghidra.program.model.data.DataUtilities.isUndefinedData(currentProgram, currentAddress)
```

## Shutting Down the Server
Warning: if you're running in non-background mode, avoid clicking the "Cancel" button on the script popup, as this will leave the server socket in a bad state, and you'll have to completely close Ghidra to fix it.

To shutdown the server cleanly, if you've done step 3 in the install instructions above, click Tools->Ghidra Bridge->Shutdown. Otherwise, run the ghidra_bridge_server_shutdown.py script from the Bridge folder.

Alternatively, you can call remote_shutdown from any connected client.
```python
import ghidra_bridge
b = ghidra_bridge.GhidraBridge(namespace=globals())
b.bridge.remote_shutdown()
```

Security warning
=====================
Be aware that when running, a Ghidra Bridge server effectively provides code execution as a service. If an attacker is able to talk to the port Ghidra Bridge is running on, they can trivially gain execution with the privileges Ghidra is run with. 

Also be aware that the protocol used for sending and receiving Ghidra Bridge messages is unencrypted and unverified - a person-in-the-middle attack would allow complete control of the commands and responses, again providing trivial code execution on the server (and with a little more work, on the client). 

By default, the Ghidra Bridge server only listens on localhost to slightly reduce the attack surface. Only listen on external network addresses if you're confident you're on a network where it is safe to do so. Additionally, it is still possible for attackers to send messages to localhost (e.g., via malicious javascript in the browser, or by exploiting a different process and attacking Ghidra Bridge to elevate privileges). You can mitigate this risk by running Ghidra Bridge from a Ghidra server with reduced permissions (a non-admin user, or inside a container), by only running it when needed, or by running on non-network connected systems.

Remote eval
=====================
Ghidra Bridge is designed to be transparent, to allow easy porting of non-bridged scripts without too many changes. However, if you're happy to make changes, and you run into slowdowns caused by running lots of remote queries (e.g., something like `for function in currentProgram.getFunctionManager().getFunctions(): doSomething()` can be quite slow with a large number of functions as each function will result in a message across the bridge), you can make use of the bridge.remote_eval() function to ask for the result to be evaluated on the bridge server all at once, which will require only a single message roundtrip.

The following example demonstrates getting a list of all the names of all the functions in a binary:
```python
import ghidra_bridge 
b = ghidra_bridge.GhidraBridge(namespace=globals())
name_list = b.bridge.remote_eval("[ f.getName() for f in currentProgram.getFunctionManager().getFunctions(True)]")
```

If your evaluation is going to take some time, you might need to use the timeout_override argument to increase how long the bridge will wait before deciding things have gone wrong.

If you need to supply an argument for the remote evaluation, you can provide arbitrary keyword arguments to the remote_eval function which will be passed into the evaluation context as local variables. The following argument passes in a function:
```python
import ghidra_bridge 
b = ghidra_bridge.GhidraBridge(namespace=globals())
func = currentProgram.getFunctionManager().getFunctions(True).next()
mnemonics = b.bridge.remote_eval("[ i.getMnemonicString() for i in currentProgram.getListing().getInstructions(f.getBody(), True)]", f=func)
```
As a simplification, note also that the evaluation context has the same globals loaded into the \_\_main\_\_ of the script that started the server - in the case of the Ghidra Bridge server, these include the flat API and values such as the currentProgram.

Interactive mode
=====================
Normally, Ghidra scripts get an instance of the Ghidra state and current\* variables (currentProgram, currentAddress, etc) when first started, and it doesn't update while the script runs. However, if you run the Ghidra Python interpreter, that updates its state with every command, so that currentAddress always matches the GUI.

To reflect this, GhidraBridge will automatically attempt to determine if you're running the client in an interactive environment (e.g., the Python interpreter, iPython) or just from a script. If it's an interactive environment, it'll register an event listener with Ghidra and perform some dubious behind-the-scenes shenanigans to make sure that the state is updated with GUI changes to behave like the Ghidra Python interpreter.  It'll also replace `help()` with one that reaches out to use Ghidra's help across the bridge if you give it a bridged object.

You shouldn't have to care about this, but if for some reason the auto-detection doesn't give you the result you need, you can specify the boolean interactive_mode argument when creating your client GhidraBridge to force it on or off as required.

How it works
=====================
The actual bridge RPC code is implemented in [jfx-bridge](https://github.com/justfoxing/jfx_bridge/). Check it out there and file non-Ghidra specific issues related to the bridge there.

Design principles
=====================
* Needs to be run in Ghidra/Jython 2.7 and Python 3
* Needs to be easy to install in Ghidra - no pip install, just add a single directory 
(these two requirements ruled out some of the more mature Python RPC projects I looked into)

Tested
=====================
* Tested and working on Ghidra 9.1(Jython 2.7.1) <-> Python 3.7.3 on Windows
* Automatically tested on Ghidra 9.0(Jython 2.7.1) <-> Python 3.5.3 on Linux (bskaggs/ghidra docker image)

TODO
=====================
* Ghidra plugin for server control (cleaner start/stop, port selection, easy packaging/install)
* Examples
    * Jupyter notebook

Contributors
=====================
* Thx @fmagin for better iPython support, and much more useful reprs!
* Thanks also to @fmagin for remote_eval, allowing faster remote processing for batch queries!
