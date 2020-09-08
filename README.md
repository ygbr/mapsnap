# mapsnap - Apple Maps Web Snapshots on Python

**mapsnap** generates static maps using Apple's MapKit Web Snapshots API

```python
>>> from mapsnap import MapSnap, Annotation, ColorScheme, MarkerStyle
>>> map_snapshot = MapSnap(
...     _key=YOUR_PRIVATE_KEY_PATH,
...     teamId=YOUR_TEAM_ID,
...     keyId=YOUR_KEY_ID,
...     center=[-21.208392, -47.788517],
...     size="414x200",
...     colorScheme=ColorScheme.DARK,
... )
>>> print(map_snapshot.url)
https://snapshot.apple-mapkit.com/api/v1/snapshot?teamId=YOUR_TEAM_ID&keyId=YOUR_KEY_ID&center=-21.208392%2C-47.788517&size=414x200&scale=2&colorScheme=dark&lang=en-US&signature=A_DYNAMIC_SIGNATURE_GENERATED_AUTOMATICALLY_BY_THIS_MODULE
>>>
>>> print(map_snapshot.url)
https://snapshot.apple-mapkit.com/api/v1/snapshot?teamId=YOUR_TEAM_ID&keyId=YOUR_KEY_ID&center=-21.208392%2C-47.788517&size=414x200&scale=2&colorScheme=dark&lang=en-US&signature=A_DYNAMIC_SIGNATURE_GENERATED_AUTOMATICALLY_BY_THIS_MODULE
>>>
```

The **map_snapshot** variable will now have the **url** attribute containing the fully signed path to the static map image that can be accessed over https by any client. The string representation of the **map_snapshot** returned instance will always return the map URL as well.

If you want to dig deeper on the attributes and parameters of the returned instance you just need to take a look at its representation by either calling it directly on the Python REPL or by calling repr() over it like so:

```python
>>> map_snapshot
MapSnap(_key=None, teamId=None, keyId=None, center=[-21.208392, -47.788517], z=None, spn=None, size='414x200', scale=2, t=None, colorScheme=<ColorScheme.DARK: 'dark'>, poi=None, lang='en-US', annotations=None, overlays=None, referer=None, expires=None, imgs=None)
>>> repr(map_snapshot)
"MapSnap(_key=None, teamId=None, keyId=None, center=[-21.208392, -47.788517], z=None, spn=None, size='414x200', scale=2, t=None, colorScheme=<ColorScheme.DARK: 'dark'>, poi=None, lang='en-US', annotations=None, overlays=None, referer=None, expires=None, imgs=None)"
>>> print(repr(map_snapshot))
MapSnap(_key=None, teamId=None, keyId=None, center=[-21.208392, -47.788517], z=None, spn=None, size='414x200', scale=2, t=None, colorScheme=<ColorScheme.DARK: 'dark'>, poi=None, lang='en-US', annotations=None, overlays=None, referer=None, expires=None, imgs=None)
```

> Notice that the **\_key**, **teamId** and **keyId** attributed are always nullified by design before returning the instance for security purposes (try to prevent exposure of the key content and IDs).

You can also call the **.png()** method which returns a PNG file object.
The sample below shows how you can fetch the PNG image directly and write it to a file:

```python
>>> with open("test.png", "wb") as fp:
...     fp.write(map_snapshot.png().read())
...
86737
```

and alas, we have a map image:

![Sample1](/docs/img/sample1.png)

> You can later convert the PNG file to other formats using an image module like [Pillow](https://pypi.org/project/Pillow/).

### Installing & Updating

**mapsnap** is available on **PyPI** and can be installed or updated with:

```shell
$ pip install -U mapsnap
```

If you're having installation problems due to ecdsa **gmpy2** dependency, try installing the **libgmp**, **libmpfr** and **libmpc**:

-   **(mac)** - `brew install gmp mpfr libmpc mpc`
-   **(linux)** - `sudo apt install -y libgmp-dev libmpfr-dev libmpc-dev`

### Setup

-   First you need to head to your [Apple Developer Account](https://developer.apple.com/account/)

    -   Then Go to [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/certificates/list)
    -   Click on [Keys](https://developer.apple.com/account/resources/authkeys/list) on the left menu
    -   Click the [+ Sign next to Keys](https://developer.apple.com/account/resources/authkeys/add)
    -   Choose a name for your new Apple MapKit JS Key
    -   Mark the **MapKit JS** checkbox and Configure it
    -   Click **Continue**
    -   Click on **Register** at the top right
    -   **Download** your key and store it **safely**!!! Take Note of your Key ID

-   After that you **MAY** need to convert your .p8 key to a EC PEM format that python-ecdsa can use.
    -   Sometimes the .p8 keys works out of the box. If you're having signing issues, than try the next steps. First try to use the .p8 key you have downloaded directly from apple as the **\_key** parameter.
    -   You can do that using either:
        -   `$ openssl ec -in __[PATH_TO_ORIGINAL_KEY.p8]__ -out __[PATH_TO_OUTPUT_PEM_KEY.pem]__`
        -   `$ openssl pkcs8 -nocrypt -in __[PATH_TO_ORIGINAL_KEY.p8]__ -out __[PATH_TO_OUTPUT_PEM_KEY.pem]__`
    -   You need to set the path for the generated .pem as the **\_key** parameter of the **MapSnap** class instance

### Usage

You just need to import the **MapSnap** class and instance it. you should also import utilities that you will need to use like Annotations, Colors and others.

Every time you create a new instance of this class, a signed URL is automatically generated and you can access it directly over the instance **.url** attribute or download the PNG from Apple for usage as a regular Python file object by calling the **.png()** method on the instance itself.

##### Customizing the Maps

```python

```

##### Adding Annotations (Markers)

```python

```

##### Default Parameters and Attributes

| Parameter  | Type         | Description                                                                                                                                                                                                                                                            |
| ---------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **\_key**  | str or bytes | The path for the .p8 or .pem file containing your MapKit JS Key downloaded from Apple Developer Portal. **(ex: /opt/myapplekeys/AuthKey_XXXXXXXXXX.p8)** <br> This can also be a **bytes** object containing the raw contents of the key file.                         |
| **teamId** | str          | Your Apple Developer Team ID (you can view it on https://developer.apple.com after logging in near your company/developer name or by accessing the **Membership** option on the menu)                                                                                  |
| **keyId**  | str          | This ID is shown to you when you create your key and is generally part of the key file name, for instance if the downloaded key file is AuthKey_XYZ712387.p8 your keyId is XYZ712387. (You can double check it by going to your details on the Apple Developer portal) |

The rest of the parameters are mapped directly from [Apple Maps Web Snapshots](https://developer.apple.com/documentation/snapshots) documentation and can be used as guided there.

I have tried to map as much as possible as dataclasses that can be imported from this module itself as shown in examples.

If you want to set a value for a parameter, you can check the mapped values currently implemented on [/mapsnap/utils.py](https://github.com/ygbr/mapsnap/blob/master/mapsnap/utils.py)

### Requirements

**mapsnap** requires Python 3.7 os higher since it uses [dataclasses](https://docs.python.org/3/library/dataclasses.html).

-   Python 3.7 (or higher)
-   ecdsa[gmpy2] (`pip install ecdsa[gmpy2]`)
-   requests (`pip install requests`)

### References

-   Official Apple Docs: https://developer.apple.com/documentation/snapshots

### Authors

-   [Ygor Lemos <ygbr@mac.com>](https://ygor.dev)

### Contributing

-   Follow the PEP8 specification
-   Write and Run Tests
-   Make sure to run pre-commit hooks

### LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### DISCLAIMERS AND TRADEMARKS

Apple, Apple Maps, MapKit and iOS are registered trademarks of [Apple Inc.](https://apple.com)

The Apple Maps Web Snapshots are currently considered **Beta Software** and subject to change.
