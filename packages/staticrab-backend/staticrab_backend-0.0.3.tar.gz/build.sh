#!/bin/bash

# install using pip from the whl file

if [ `uname` == Darwin ]; then
    if [ "$PY_VER" == "3.8" ]; then
        exit 1
    else
        exit 1
    fi
fi

if [ `uname` == Linux ]; then
    if [ "$PY_VER" == "3.8" ]; then
        pip install https://files.pythonhosted.org/packages/5a/b8/1678f7335768c5d45f9e9883c54b50915fa4b8cf6bfe2ede2e52d5a6a7b0/staticrab_backend-0.0.2-cp38-cp38-manylinux2014_x86_64.whl --no-dependencies
    elif [ "$PY_VER" == "3.7" ]; then
        pip install https://files.pythonhosted.org/packages/d8/0d/ad044b9f0d8de79f67daf165ef50c791790c82cf66b8c1c21a1d432ef1a3/staticrab_backend-0.0.2-cp37-cp37m-manylinux2014_x86_64.whl --no-dependencies
    else
        exit 1
    fi
fi