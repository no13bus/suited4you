suited4you
===============

compare 2 coding tech by github, reddit, stackoverflow and so on

Error:
```
ResponseError: MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk. Commands that may modify the data set are disabled. Please check Redis logs for details about the error.
```
Resovle
运行　`redis-cli config set stop-writes-on-bgsave-error no`　命令

Test:

https://github.com/angular/angular
https://github.com/emberjs/ember.js