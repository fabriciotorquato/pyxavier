find . -name '*.pyc' -delete
find . -name '*.dat' -delete
find . -name '*.sav' -delete
find . -name '*.pkl' -delete
isort -rc ./xavier/