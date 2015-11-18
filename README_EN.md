chimera
=======

Chimera - learning process: AngularJS &amp; Python Tornado &amp; MongoDB

Dependency
----------

Python 3.5

* tornado 4.3 - web server + framework;
* motor 0.4 - MongoDB driver;
* motorengine 0.9 - MongoDB ORM;
* bcrypt - hashing passwords;
* transliterate 1.7 - for transliterate input text to eng slugs;

Example configs see in file install.md

Structure
---------

```
app - python app (backend)
│
├─ documents - MongoDB document-model
├─ handlers - Tornado handlers
├─ system - Chimera system files
│   ├─ components - System modules
│   ├─ services - Middle layer logic
│   ├─ utils - Helpers
└
```

