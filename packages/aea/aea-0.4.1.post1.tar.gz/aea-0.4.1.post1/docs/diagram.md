<div class="admonition note">
  <p class="admonition-title">Note</p>
  <p>Work in progress.</p>
</div>

The framework has two distinctive parts.

-   A **core** that is developed by the Fetch.ai team as well as external contributors.
-   **Extensions** (also known as **packages**) developed by any developer which promotes a modular and scalable framework.

Currently, the framework supports three types of packages which can be added to the core as modules:

-   Skills
-   Protocols
-   Connections

The following figure illustrates the framework's architecture:

<center>![The AEA Framework Architecture](assets/framework-architecture.png)</center>


In most cases, as a developer in the AEA framework, it is sufficient to focus on skills development, utilising existing protocols and connections.
The later doesn't try to discourage you though, from creating your own `connections` or `protocols` but you will need a better understanding of the framework than creating a skill.


<center>![Threads](assets/threads.png)</center>

The agent operation breaks down into three parts:

* Setup: calls the `setup()` method of all registered resources
* Operation:
    * Main loop (Thread 1 - Synchronous):
        * `react()`: this function grabs all Envelopes waiting in the `InBox` queue and calls the `handle()` function on the Handler(s) responsible for them.
        * `act()`: this function calls the `act()` function of all registered Behaviours.
        * `update()`: this function enqueues scheduled tasks for execution with the TaskManager.
    * Task loop (Thread 2- Synchronous): executes available tasks
    * Decision maker loop (Thread 3- Synchronous): processes internal messages
    * Multiplexer (Thread 4 - Asynchronous event loop): the multiplexer has an event loop which processes incoming and outgoing messages across several connections asynchronously.
* Teardown: calls the `teardown()` method of all registered resources


To prevent a developer from blocking the main loop with custom skill code, an execution time limit is  applied to every `Behaviour.act` and `Handler.handle` call.

By default, the execution limit is set to `0` seconds, which disables the feature. You can set the limit to `0.1` seconds to test your AEA for production readiness. If the `act` or `handle` time exceed this limit, the call will be terminated.

An appropriate message is added to the logs in the case of some code execution being terminated.


<br />
