# Icon Converter

## Introduction

This is a icon converter.It is able to transform image to icon.


## Dependency

If you want to run it your device, please make sure you have installed this.

* pgmagick > 0.5.0


## Installation

``` bash
git clone https://github.com/SparrowJang/icon_converter

cd icon_converter

sudo python setup.py install
```

# Usage

## Basic example

### Use http or local file to convert

``` python

from icon_converter import converter

#target image ( http or local )
path = "http://example.com/test.png"

#resize and crop image
size = {"width":40,"height":40}

border = {
    "size":{"width":2,"height":2},
    "color":"#BBBBBB",
    "backgroundColor":"#FFFFFF"
}

blob = converter.convert_by_path( path, size, border )

```

### User binary or base64 to convert

``` python

f = open( "test.png" )

data = f.read()

base64data = base64.b64encode( data )

#binary data
converter.convert( data, size, border )

#base64
converter.convert( base64, size, border, format_type = "base64" )

```

If you don't need arrow, the "arrow" parameter set to False.

``` python

converter.convert( data, size, border, arrow = False )

# or

converter.convert_by_path( path, size, border, arrow = False )
```

Get a base64.

``` python

blob = converter.convert( data, size, border )

blob.base64()
```

Save a file.

``` python

f = open( "arrow.png", "w" )

f.write( blob.data )

f.close()
```

