chimera
=======

Chimera - learning process: AngularJS &amp; Python Tornado &amp; MongoDB

Dependency
----------

* tornado - web server + framework;
* motor - MongoDB driver;
* motorengine - MongoDB ORM;
* bcrypt - hashing passwords;
* transliterate - for transliterate input text to eng slugs;

Structure
---------

```
│ ─ └ ├

app - python app (backend)
│
├─ documents - MongoDB document-model
├─ handlers - Tornado handlers
├─ system - Chimera system files
│   ├─ components System modules
│   ├─ services Middle layer logic
│   ├─ utils Helpers

```
