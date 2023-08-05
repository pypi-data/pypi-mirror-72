# staticrab-backend

This is just a very simple python wrapper for some of the rust functions implemented in [staticrab-rust](https://github.com/staticrab/staticrab-rust). For normal use with additional functionaly and checks, use the [staticrab](https://github.com/staticrab/staticrab) itself.


## For developers

maturin build --release -i C:\Users\V\.conda\envs\py38\python.exe
python -m twine upload target\wheels\* --skip-existing
