import os
from PIL import Image
import io
# Generate size * size image overview

def make_image_thumb(upload_file, xsize=335, ysize=250):
    """
    Send in a path of the image, then generate a overview of that image, and 
    save it in the same directory with the postfix name of _200.jpg
    """
    #base, ext = os.path.splitext(path)
    #base = os.path.basename(path).split('.')[0]
    #filename = upload_file.filename
    try:
        im = Image.open(upload_file)
    except IOError:
        print("Error in IO")
        return 

    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            im.load()
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            # paste(color, box, mask
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size

    # 防止图片变形， 进行相关的裁剪
    if width > height:
        delta = (width-height) / 2
        box = (delta, 0, width-delta, height)
        region = im.crop(box)
    elif height > width:
        delta = (height-width) / 2
        box = (0, delta, width, height-delta)
        region = im.crop(box)
    else:
        region = im
    region = im
    #filename = '/tmp/bpm/'+ base + '_'+str(xsize)+ '_' + str(ysize) + '.jpg'
    thumb = region.resize((xsize, ysize), Image.ANTIALIAS)
    thumb_io = io.BytesIO()
    file_format = upload_file.content_type.split('/')[-1].upper()
    thumb.save(thumb_io, file_format)
    return thumb_io

#thumb.save(filename, quality=100)

