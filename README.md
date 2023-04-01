# Pandora Toolbox App

## About

Pandora Toolbox is a swiss-knife application framework that enable fast and reliable development of small or big automation routines by providing security and different types of integration between systems and software products.

### Motivation

In a lot of time, software developers, researchers and enthusiasts spent a lot of time in boring and annoying monkey tasks that can and should be automated. But, even some languages providing a lot of tools, it is hard to maintain different code repositories, snippets and routines, plus, it is hard to organize and control the security of them. Because of that, the Pandora Toolbox Project started: to enable people to do things in a fast and reliable way.

## Getting Started

### Technical Background

Pandora Toolbox Framework relies on a custom Software Development Toolkit (SDK) and in a Pandora Toolbox Application ("Pandora App", "Pandora Toolbox App", "Pandora CLI"), that provide proper interfaces, integrations and tools to enable further development.

As the Core Functionality of the Pandora Toolbox Application, a Micro-Kernel Architecture Pattern is implemented to enable Extensibility, Feature Separation and Isolation and Code Organization.

[Mark Richards, in Chapter 3 of 'Software Architecture Patterns' book](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch03.html), describes the Micro-Kernel Architecture as a pattern, sometimes referred as Plug-In Architecture Pattern, that provides extensibility and feature separation and isolation by allowing an integration between the core application and new features as plug-ins.

To achieve the Extensibility (1) and Feature Separation and Isolation (2), the core application should have a Plugin Management Layer (PML) that provides:

* **Plugin Interface** to enable the existence of Plugins;
* **Plugin Recursion** by making the core application a Plugin that loads another Plugins;
* **Plugin Collections** to be a repository to a) organize; b) store; c) share; d) develop and e) secure Plugins;
* **Runtime Plugin Discovery** to identify Plugin Collections and available plugins to be executed;
* **Runtime Plugin Container** to enable Plugin Execution;
* **Runtime Security Layer** to allow or deny any operation from all the runtimes;
* **Plugin Management Container (PMC)** to enable Basic Data Operations (BDO, a.k.a CRUD), Security Operations (SO) and Management Operations (MO) and be the main interface of Plugin Management Layer (PML). Below, the operations that should be enabled:
  * **Basic Data Operations (BDO, a.k.a CRUD)**\:
    * Creation (C);
    * Recovery (R);
    * Update (U);
    * Deletion (D).
  * **Security Operations (SO):**
    * **Data Signing** via Asymmetric Keys;
    * **Data Fingerprint Management** via complex hashing operations;
  * **Management Operations (MO)**:
    * Plugin Discovery;
    * Plugin Execution;
    * Plugin Collection Management;
    * Plugin Setup;
* **Core Plugins**, that extends the functionality of core application by enabling:
  * **External Plugin Management** via Plugin Management Container (PMC)
  * **Self Plugin Management** via Plugin Management Container (PMC) to enable Self Management and Core Plugin Management;

To enable improvements on security and performance, all the internal operations of Plugin Management Layer (PML) **are executed at runtime by default** to lower the Storage I/O and increase performance by not depend on a *daemon,* e.g. Podman vs Docker, even though the existence of a daemon is not restricted. In that way, if a Plugin wants **to be** or **to have** a *daemon*, should can :)

That Micro-Kernel Architecture is followed by a 
* Dependency Inversion and Dependency Injection; and
* Logging Management Layer;


## External Resources

* [Project Page @ Artemis Developer Portal](https://artemisia.youtrack.cloud/projects/d66bc65d-2820-4a09-a019-9216745426db)
* [Project Kanban @ Artemis Developer Portal](https://artemisia.youtrack.cloud/agiles/141-2/current)
