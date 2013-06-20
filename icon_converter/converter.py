#from pgmagick import Image
from pgmagick import Image
from pgmagick import Geometry, Color, Blob
import adapter
import base64

def _create_image_adapter_by_blob( blob ):
    """
    Create a image adapter by blob.
    """

    image_adapter = adapter.Image( Image( blob ) )

    return image_adapter



def _set_arrow( image_adapter, border = dict() ):
    """
    Set a arrow.
    """

    image_adapter.arrow( border.get( "backgroundColor" ), border.get("color") )


def _setup_size_and_border( image_adapter, size, border ):
    """
    Set size and border for image_adapter.
    """

    image_adapter.resize( size )

    image_adapter.crop( {"width":size.get("width"),"height":size.get("height"),"x":0,"y":0} )

    image_adapter.border( border.get("size"), border.get("backgroundColor") )

    image_adapter.border( {"width":1,"height":1}, border.get("color") )


def convert_by_path( path, size, border, arrow = True ):
    """
    Create a icon by local or remote image.
    """

    image_adapter = _create_image_adapter_by_blob( path )

    _setup_size_and_border( image_adapter, size, border )

    if arrow:

        _set_arrow( image_adapter, border )

    return image_adapter.get_blob()


def convert( data, size, border, format_type = "", arrow = True ):
    """
    Create a icon by base64 or binary data.
    """

    if format_type == "base64":

        data = base64.b64decode( data )

    image_adapter = _create_image_adapter_by_blob( Blob( data ) )

    _setup_size_and_border( image_adapter, size, border )

    if arrow:

        _set_arrow( image_adapter, border )

    return image_adapter.get_blob()


"""border = {
    "size":{"width":4,"height":4},
    "color":"#BBBBBB",
    "backgroundColor":"#FFFFFF"
}

bb = convert_by_path( "http://lh3.ggpht.com/-Et2lmf3zvQ0/UY1VoJDBx0I/AAAAAAAAGy4/6BMfW7peasc/s130/300x300.jpg", {"width":40,"height":40}, border )

f = open( "123.png", "w" )
f.write( bb.data )
f.close()"""


