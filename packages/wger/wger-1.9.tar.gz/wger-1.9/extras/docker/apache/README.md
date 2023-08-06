Demo image for wger
===================
Thank you for downloading wger Workout Manager. wger (ˈvɛɡɐ) is a free, open
source web application that manages your exercises and personal workouts, weight
and diet plans. It can also be used as a simple gym management utility, providing
different administrative roles (trainer, manager, etc.). It offers a REST API
as well, for easy integration with other projects and tools.

It is written with python/django and uses jQuery and some D3js for charts.

Installation
------------

This docker image contains an instance of the application running as a WSGI
process under apache with a sqlite database. It is useful to just try it out and
play around. To start it:


```docker run -ti --name wger.apache --publish 8000:80 wger/apache```

Then just open <http://localhost:8000> and log in as: **admin**, password **admin**

To stop the container:

```sudo docker container stop wger.apache```

To start developing again:

```sudo docker container start --attach wger.apache```


Building
--------

If you build this yourself, keep in mind that you **must** build from the
project root!

```docker build -f extras/docker/apache/Dockerfile --tag wger/apache .```


Contact
-------

Feel free to contact us if you found this useful or if there was something that
didn't behave as you expected. We can't fix what we don't know about, so please
report liberally. If you're not sure if something is a bug or not, feel free to
file a bug anyway.

* gitter: <https://gitter.im/wger-project/wger>
* issue tracker: <https://github.com/wger-project/wger/issues>
* twitter: <https://twitter.com/wger_de>
* mailing list: <https://groups.google.com/group/wger> / wger@googlegroups.com, no registration needed

Sources
-------

All the code and the content is freely available:

* Main repository: <https://github.com/wger-project/wger>

Licence
-------

The application is licenced under the Affero GNU General Public License 3 or
later (AGPL 3+).

The initial exercise and ingredient data is licensed additionally under one of
the Creative Commons licenses, see the individual exercises for more details.

The documentation is released under a CC-BY-SA either version 4 of the License,
or (at your option) any later version.

Some images where taken from Wikipedia, see the SOURCES file in their respective
folders for more details.
