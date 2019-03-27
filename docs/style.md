# Coding Style
Please conform to [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html)

## yapf
Please use [yapf](https://github.com/google/yapf/) to automatically format your code.

Usage:
```
pip install yapf
(if Python2: pip install futures)
(cd into the root directory containing README.md file)
yapf --in-place --recursive --parallel .
```

## pylint
All python code is required to pass [pylint](https://www.pylint.org/)

Usage:
```
pip install pylint
(cd into the root directory containing README.md file)
pylint src/app/
```
