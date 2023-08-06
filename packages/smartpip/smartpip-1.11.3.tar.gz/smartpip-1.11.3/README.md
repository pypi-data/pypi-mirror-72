<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# SmartPip base on Airflow


[![License](http://img.shields.io/:license-Apache%202-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.txt)


Airflow is a platform to programmatically author, schedule, and monitor
workflows.

When workflows are defined as code, they become more maintainable,
versionable, testable, and collaborative.

Use Airflow to author workflows as directed acyclic graphs (DAGs) of tasks.
The Airflow scheduler executes your tasks on an array of workers while
following the specified dependencies. Rich command line utilities make
performing complex surgeries on DAGs a snap. The rich user interface
makes it easy to visualize pipelines running in production,
monitor progress, and troubleshoot issues when needed.

But actually, most cases we don't need so much functions, the factory only use some of them,
but what they want is, deploy easy, develop easy, system integration. but airflow use every
function as operator, no benefit to do code automatic, and what we found we mostly use is
python operator, we can use it to do almost every thing, and it is easy to customize.
SmartPip is born for this as we choose another way

we keep all functions of airflow(1.10.1), so you can use it as airflow

## What is New on SmartPip
- DAG setup code automatic
- user control enhancement
- Token auth with data portal
- New UI to fit with new DAG setup

## Getting started
Please visit the Airflow Platform documentation (latest **stable** release) for help with [installing Airflow](https://airflow.incubator.apache.org/installation.html), getting a [quick start](https://airflow.incubator.apache.org/start.html), or a more complete [tutorial](https://airflow.incubator.apache.org/tutorial.html).

Documentation of GitHub master (latest development branch): [ReadTheDocs Documentation](https://airflow.readthedocs.io/en/latest/)

For further information, please visit the [Airflow Wiki](https://cwiki.apache.org/confluence/display/AIRFLOW/Airflow+Home).

## Beyond the Horizon

Airflow **is not** a data streaming solution. Tasks do not move data from
one to the other (though tasks can exchange metadata!). Airflow is not
in the [Spark Streaming](http://spark.apache.org/streaming/)
or [Storm](https://storm.apache.org/) space, it is more comparable to
[Oozie](http://oozie.apache.org/) or
[Azkaban](https://azkaban.github.io/).

Workflows are expected to be mostly static or slowly changing. You can think
of the structure of the tasks in your workflow as slightly more dynamic
than a database structure would be. Airflow workflows are expected to look
similar from a run to the next, this allows for clarity around
unit of work and continuity.

## Principles

- **Dynamic**:  Airflow pipelines are configuration as code (Python), allowing for dynamic pipeline generation. This allows for writing code that instantiates pipelines dynamically.
- **Extensible**:  Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.
- **Elegant**:  Airflow pipelines are lean and explicit. Parameterizing your scripts is built into the core of Airflow using the powerful **Jinja** templating engine.
- **Scalable**:  Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers. Airflow is ready to scale to infinity.

## User Interface

- **DAGs**: Overview of all DAGs in your environment.
![](/docs/img/dags.png)

- **Tree View**: Tree representation of a DAG that spans across time.
![](/docs/img/tree.png)

- **Graph View**: Visualization of a DAG's dependencies and their current status for a specific run.
![](/docs/img/graph.png)

- **Task Duration**: Total time spent on different tasks over time.
![](/docs/img/duration.png)

- **Gantt View**: Duration and overlap of a DAG.
![](/docs/img/gantt.png)

- **Code View**:  Quick way to view source code of a DAG.
![](/docs/img/code.png)
