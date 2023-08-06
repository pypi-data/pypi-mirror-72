PACKAGING
=========

This guide is loosely following one of Hynek's fantastic blog posts:
https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/


Setup a venv
------------
    
    $ tox --devenv dev-env
    
    $ dev-env/bin/pip install -U pip pep517 twine

    $ rm -rf build dist
 
    $ python -m pep517.build .

    $ rm -rf venv-sdist

    $ venv-sdist/bin/pip install build/...

    -> import + test

    $ rm -rf venv-wheel

    $ virtualenv venv-wheel

    $ venv-wheel/bin/pip install dist/Flask_Reuploaded-0.3.dev0-py3-none-any.whl 

    -> import + test

