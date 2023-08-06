AssetBuilder: Compile, Minify and Bundle CSS, JavaScript and other web assets
=============================================================================

AssetBuilder solves the problem of managing static assets — CSS files, JavaScript
bundles, images — in Python web projects.

- AssetBuilder lets you tag together asset files::

    assetbuilder.add_path('frontend-scripts', 'static/jquery.js')
    assetbuilder.add_path('frontend-scripts', 'static/intercooler.js')

    assetbuilder.add_path('styles', 'static/main.css')

    assetbuilder.add_path('admin-scripts', 'static/jquery.js')
    assetbuilder.add_path('admin-scripts', 'static/admin.js')

- AssetBuilder offers a WSGI endpoint for serving those files::

    MyApplication.route_wsgi('/assets', assetbuilder)

- AssetBuilder generates links to the served files::

    <link py:for="url in assetbuilder.urls('styles', environ)" rel="stylesheet" href="$url"/>

- AssetBuilder checks asset files are up to date before serving them and
  calls your build system as required (which could be `Gulp <https://gulpjs.com/>`_,
  `Webpack <https://webpack.js.org/>`_, `Make <http://man.openbsd.org/make>`_,
  …)

AssetBuilder **doesn't**: build, compile, minify, uglify or optimize JS, CSS or
images. You already have a build system for that. If you want to inline files,
It will concatenate – but only if you ask it to.

AssetBuilder **doesn't** wrap your build tools or require integration modules.
As long as you can call your build script from the CLI, so can AssetBuilder.

AssetBuilder works with **Flask**, **Fresco**, **Django**, **Pyramid** and any
other Python WSGI compatible web framework.

Links
-----

- `AssetBuilder documentation <https://ollycope.com/software/assetbuilder/>`_
- `Mercurial repo <https://hg.sr.ht/~olly/assetbuilder/>`_
