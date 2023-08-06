# qrimg

Generate QRCode Image


## Install

```shell
    pip install qrimg
```

## Usage

**Help Information**

```shell
C:\Workspace\qrimg>qrimg --help
Usage: qrimg.py [OPTIONS] MESSAGE

Options:
  -o, --output TEXT               Output file name.  [required]
  -v, --version INTEGER           An integer from 1 to 40 that controls the
                                  size of the QR Code. The smallest, version
                                  1, is a 21x21 matrix. Default to None, means
                                  making the code to determine the size
                                  automatically.
  -c, --error-correction [7|15|25|30]
                                  controls the error correction used for the
                                  QR Code. Default to 30.
  -s, --box-size INTEGER          controls how many pixels each 'box' of the
                                  QR code is. Default to 10.
  -b, --border INTEGER            controls how many boxes thick the border
                                  should be (the default is 4, which is the
                                  minimum according to the specs).
  -f, --fill-color TEXT           Named color or #RGB color accepted. Default
                                  to named color 'black'.
  -b, --back-color TEXT           Named color or #RGB color accepted. Default
                                  to named color 'white'.
  --help                          Show this message and exit.
```

**Example 1**

Use qrimg command generate an image contain information "Hello world".

```shell
qrimg -o hello.png "Hello world"
```

**Example 2**

Use qrimg command generate an image contain a url.

```shell
qrimg -o site.png http://www.example.com
```

**Example 3**

Use qrimg command generate a blue colored image.

```shell
qrimg -o site.png -f blue http://www.example.com
```

**Example 3**

Use RGB color.

```shell
qrimg -o site.png -f #ff00cc http://www.example.com
```

## Bug report

Please report any issues at https://github.com/zencore-cn/zencore-issues.

## Releases


### v0.2.0 2020/06/29

- Add controller parameters in generating.

### v0.1.0 2019/05/25

- First release.