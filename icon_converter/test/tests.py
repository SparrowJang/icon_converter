
import unittest
from icon_converter import adapter
from icon_converter import converter
from pgmagick import Blob
from pgmagick import Image
import base64

class TestImageAdapterFunctions(unittest.TestCase):

    def setUp(self):
        self.image_adapter = adapter.Image( "test_image.jpg" )

    def test_resize( self ):

        size = {"width":40,"height":40}
        image_adapter = self.image_adapter
        image_adapter.resize( size )
        api_image = image_adapter.get_api_image()

        self.assertEqual( api_image.width , 55 )
        self.assertEqual( api_image.height , 40 )

    def test_to_get_blob( self ):
 
        self.assertTrue( isinstance( self.image_adapter.get_blob() , Blob ) )


    def test_to_crop( self ):

        image_adapter = self.image_adapter
        bounds = {"width":40,"height":40,"x":0,"y":0}

        self.image_adapter.crop( bounds )
        api_image = image_adapter.get_api_image()

        self.assertEqual( api_image.width , 40 )
        self.assertEqual( api_image.height , 40 )

    def test_border( self ):

        image_adapter = self.image_adapter

        api_image = image_adapter.get_api_image()

        width = api_image.width

        height = api_image.height

        size = {"width":2,"height":2}

        image_adapter.border( size )

        self.assertEqual( api_image.width , width + 4 )
        self.assertEqual( api_image.height , height + 4 )
        


class TestConverterFunctions(unittest.TestCase):

    def setUp( self ):

       self.size = {"width":40,"height":40}
       self.border = {
           "size":{"width":2,"height":2},
           "color":"#BBBBBB",
           "backgroundColor":"#FFFFFF"
       }


    def test_convert_by_path( self ):

       local_blob = converter.convert_by_path( "test_image.jpg", self.size, self.border )

       url = "http://twitter.github.io/bootstrap/assets/img/bs-docs-masthead-pattern.png"

       https_url = "https://lh3.ggpht.com/-Et2lmf3zvQ0/UY1VoJDBx0I/AAAAAAAAGy4/6BMfW7peasc/s130/300x300.png"

       http_blob = converter.convert_by_path( url, self.size, self.border )

       https_blob = converter.convert_by_path( https_url, self.size, self.border )

       self.assertTrue( isinstance( https_blob, Blob ) )

       self.assertTrue( isinstance( local_blob, Blob ) )

       self.assertTrue( isinstance( http_blob, Blob ) )

    def test_convert( self ):

       f = open("test_image.jpg")

       img_data = f.read()

       f.close()

       blob = converter.convert( img_data, self.size, self.border, arrow = False )

       b64 =  base64.b64encode( img_data )

       blob_by_base64 = converter.convert( b64 , self.size, self.border, format_type = "base64" )

       self.assertTrue( isinstance( blob, Blob ) )

       self.assertTrue( isinstance( blob_by_base64, Blob ) )

       #arrow height > no arrow height
       self.assertTrue( Image( blob ).rows() < Image( blob_by_base64 ) )


if __name__ == '__main__':
    unittest.main()


