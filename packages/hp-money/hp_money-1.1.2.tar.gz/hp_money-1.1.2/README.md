# hp_money

>
> version: 1.1.2
>
> author: [KuangQingxu](mailto:kuangqingxu@transfereasy.com?subject=[HipoPay - hp_money])
>
> date: 2020-04-26
>
> update: 2020-06-24

### Usage:
    - To be continue

### Packaging And Uploading:

- Update Verison:

    - `README.md`
    - `hp_money/__init__.py`
    - `setup.py`

- Packing:

    ```
    python setup.py sdist bdist_wheel
    ```

- Uploading:

    ```
    twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
    ```
