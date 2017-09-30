import platform


# Define saving place for the images.
if platform.system() == 'Darwin':
    WORKPATH = '/Users/EDISON/Pictures/AmazonBigPicture'
if platform.system() == 'Windows':
    WORKPATH = 'J:\AmazonBigPicture'