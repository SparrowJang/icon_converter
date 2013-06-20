
from pgmagick.api import Image as ApiImage
from pgmagick.api import Draw
from pgmagick import Image as OrginallyImage
from pgmagick import Geometry, Color, Blob

class Image( object ):
    """
    This is pgmagick.api.Image adapter.And add some util tools.
    """

    def __init__( self, filename = None, color = None, *args, **kargs ):
        """
        Init a adapter.

        :Args:
         - filename - This param is a file name or Image of pgmagick.
         - Color - This is color of pgmagick.api.
        """

        if isinstance( filename, OrginallyImage ):

            self.__apiImage = ApiImage()
            self.__apiImage.img = filename
        else:

            self.__apiImage = ApiImage( filename, color, args, kargs )

    def border( self, size, color_str = "white" ):
        """
        Set a border and color.

        :Args:
         - size - This is dict. (example: {"width":2,"height":2} )
         - color_str - The default value is white. ( example: "#ffeeff" )
        """

        img = self.get_pgmagick_image()

        img.borderColor( Color( color_str ) )

        img.border( Geometry( size.get("width"), size.get("height") ) );


    def crop( self, bounds ):
        """
        Crop this image.

        :Args:
         - bounds - This is bounds dict. ( example:{"width":40,"height":40,"x":0,"y":0} )
        """

        img = self.get_pgmagick_image()

        img.crop( Geometry( bounds.get("width"), bounds.get("height"), bounds.get("x"), bounds.get("y") ) )


    def resize( self, size, is_force = False ):
        """
        Reset a size.
        
        :Args:
         - size - This is dict. (example: {"width":2,"height":2} )
         - isForce - This is boolean.The image width or height will be possible less to set size,when isForce is true.
        """

        if is_force:

            self.__apiImage.scale( ( size.get("width"), size.get("height") ) )

        else:

            height = self.__apiImage.height

            width = self.__apiImage.width

            ratio_height = float( size.get("height") ) / float( height )

            ratio_width = float( size.get("width") ) / float( width )

            ratio = 1

            if ratio_height < ratio_width:

                ratio = ratio_width

            else:

                ratio = ratio_height

            self.__apiImage.scale( ( ratio * width, ratio * height ) )


    def get_blob( self ):
        """
        Get a blob object.
        """

        blob = Blob()

        img = self.get_pgmagick_image()
        img.write( blob, "png" )

        return blob


    def get_pgmagick_image( self ):
        """
        Get a pgmagick image.
        """

        return self.__apiImage.img


    def get_api_image( self ):
        """
        Get a pgmagick.api image.
        """

        return self.__apiImage


    def __create_arrow_bg( self, points, color ):
        """
        Create a draw of arrow background.
        """

        draw = Draw()
        draw.stroke_antialias( False )
        draw.polygon( points )
        draw.fill_color( color )

        return draw

    def __create_arrow_border( self, start_x, end_x , y, arrow_height, color ):
        """
        Create a draw of arrow border.
        """

        center_x = ( start_x + end_x ) /2
        center_y = arrow_height + y

        arrow_border_draw = Draw()
        arrow_border_draw.stroke_color( color )
        arrow_border_draw.stroke_antialias( False )
        arrow_border_draw.line( start_x, y, center_x, center_y )
        arrow_border_draw.line( center_x, center_y, end_x, y )
        arrow_border_draw.stroke_width( 2 )

        return arrow_border_draw


    def arrow( self, background_color = "#FFFFFF", border_color = "#BBBBBB" ):
        """
        Draw a arrow at icon bottom.
        """
        img = self.get_api_image()

        width = img.width
        height = img.height
        center_x = width / 2
        arrow_half_width = int( center_x / 3 )

        arrow_height = int( height / 7 )

        bg_img = ApiImage(( width, height + arrow_height + 1 ),'transparent')

        #
        arrow_start_x = center_x - arrow_half_width
        arrow_end_x = center_x + arrow_half_width
        center_y = height + arrow_height

        arrow_bg_start_point = ( arrow_start_x, height -1 )
        arrow_bg_end_point = ( arrow_end_x, height - 1 )
        arrow_bg_center_point = ( center_x, height + arrow_height )
        
        draw = Draw()
        draw.composite( 0, 0, width, height, img.img )

        bg_img.draw( draw )

        points = ( arrow_bg_start_point, arrow_bg_end_point, arrow_bg_center_point, arrow_bg_start_point )

        bg_img.draw( self.__create_arrow_bg( points, background_color ) )

        bg_img.draw( self.__create_arrow_border( arrow_start_x, arrow_end_x, height, arrow_height, border_color ) )

        self.__apiImage = bg_img

        

