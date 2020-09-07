# mapsnap - Apple Maps Web Snapshots on Python

**mapsnap** generates static maps using Apple's MapKit Web Snapshots API

```python
>>> from mapsnap import MapSnap
>>> MapSnap(team_id=TEAM_ID,
>>>         key_id=KEY_ID,
>>>         key_path=PKEYPATH,
>>>         center=[-21.208392, -47.788517],
>>>         size="414x200",
>>>         colorScheme=MapSnap.ColorScheme.DARK)

```

### Installing

**mapsnap** is available on PyPI and can be installed with:

```shell
$ pip install mapsnap
```

-   First you need to convert your .p8 key to a EC PEM format that python-ecdsa can use.
    -   You can do that using: `$ openssl ec -in [PATH_TO_ORIGINAL_KEY.p8] -out [PATH_TO_OUTPUT_PEM_KEY.pem]`
    -   You need to set the path for this generated .pem on the _key_path_ parameter

### Requirements

**mapsnap** requires Python 3.7 os higher since it uses [dataclasses](https://docs.python.org/3/library/dataclasses.html).

-   Python 3.7 (or higher)
-   ecdsa[gmpy2] (`pip install ecdsa[gmpy2]`)
-   requests (`pip install requests`)

### References

-   Official Apple Docs: https://developer.apple.com/documentation/snapshots

### Authors

-   [Ygor Lemos <ygbr@mac.com>](@ygbr)

### Contributing

-   Follow the PEP8 specification
-   Write and Run Tests
-   Make sure to run pre-commit hooks

### LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
