from PIL import Image, ExifTags
from ffmpy import FFmpeg
import os

DEBUG = True
if DEBUG is False:
    print = lambda *a, **k: None


def MakeVideoThumbnail(videoPath, thumbnailWidth=300):
    try:
        saveToPath = '{}_thumb.png'.format(*videoPath.split('.')[0])
        print('saveToPath=', saveToPath)
        ff = FFmpeg(
            inputs={videoPath: None},
            outputs={saveToPath: None},
        )
        ff.run()
        return saveToPath

    except Exception as e:
        print('17 MakeVideoThumbnail Exception:', e)
        return None


def OptimizeToSize(imagePath, maxWidth=1920, maxHeight=1080):
    '''
    This function should scale the image to a new resolution not exceeting the maxWidth/maxHeight but preserving the aspect ratio

    :param imagePath:
    :param maxWidth:
    :param maxHeight:
    :return: path to new resized image
    '''
    print('MakeThumbnail(', imagePath, maxWidth, maxHeight)

    if imagePath.lower().endswith('.gif'):
        return ResizeGif(imagePath, maxWidth, maxHeight)

    try:
        saveToPath = '{}_{}x{}.{}'.format(
            imagePath.split('.')[0],
            maxWidth,
            maxHeight,
            imagePath.split('.')[1],
        )

        img = Image.open(imagePath)

        print('img.size=', img.size)
        width, height = img.size

        wDelta = width - maxWidth
        hDelta = height - maxHeight

        print('46 wDelta=', wDelta)
        print('47 hDelta=', hDelta)

        newHeight = None
        newWidth = None

        if wDelta > 0:
            # the image is too wide (need to scale down)
            if hDelta > 0:
                # the image is also too tall
                if wDelta < hDelta:
                    newHeight = maxHeight
                else:
                    newWidth = maxWidth
            else:
                newWidth = maxWidth
        else:
            if hDelta > 0:
                newHeight = maxHeight
            else:
                # the image is within the max height/width
                # scale it up to fit the max height/width

                if wDelta < 0:
                    # the image has short width
                    if hDelta < 0:
                        # the image has short height
                        if wDelta < hDelta:
                            newHeight = maxHeight
                        else:
                            newWidth = maxWidth
                    else:
                        newWidth = maxWidth
                else:
                    print('this should not happen')

        print('74 newWidth=', newWidth)
        print('75 newHeight=', newHeight)

        if newWidth is not None:
            newWidthPercent = (newWidth / float(img.size[0]))
            newHeight = int((float(img.size[1]) * float(newWidthPercent)))

        elif newHeight is not None:
            newHeightPercent = (newHeight / float(img.size[1]))
            newWidth = int((float(img.size[0]) * float(newHeightPercent)))

        print('85 newWidth=', newWidth)
        print('86 newHeight=', newHeight)

        img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
        img.save(saveToPath)
        return saveToPath

    except Exception as e:
        print('19 MakeThumbnail Excpetion:', e)
        return imagePath


def ResizeGif(oldPath, maxWidth, maxHeight):
    '''
    Taken from
    https://gist.github.com/BigglesZX/4016539
    and
    https://stackoverflow.com/questions/41718892/pillow-resizing-a-gif

    :return:
    '''

    def analyseImage(path):
        '''
        Pre-process pass over the image to determine the mode (full or additive).
        Necessary as assessing single frames isn't reliable. Need to know the mode
        before processing all frames.
        '''
        im = Image.open(path)
        results = {
            'size': im.size,
            'mode': 'full',
        }
        try:
            while True:
                if im.tile:
                    tile = im.tile[0]
                    update_region = tile[1]
                    update_region_dimensions = update_region[2:]
                    if update_region_dimensions != im.size:
                        results['mode'] = 'partial'
                        break
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        return results

    def processImage(path, maxWidth=1920, maxHeight=1080):
        '''
        Iterate the GIF, extracting each frame.
        '''
        resize_to = (maxWidth, maxHeight)

        mode = analyseImage(path)['mode']

        im = Image.open(path)

        i = 0
        p = im.getpalette()
        last_frame = im.convert('RGBA')

        all_frames = []
        try:
            while True:
                print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))

                '''
                If the GIF uses local colour tables, each frame will have its own palette.
                If not, we need to apply the global palette to the new frame.
                '''
                if not im.getpalette():
                    im.putpalette(p)

                new_frame = Image.new('RGBA', im.size)

                '''
                Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
                If so, we need to construct the new frame by pasting it on top of the preceding frames.
                '''
                if mode == 'partial':
                    new_frame.paste(last_frame)

                new_frame.paste(im, (0, 0), im.convert('RGBA'))
                new_frame.thumbnail(resize_to, Image.ANTIALIAS)
                all_frames.append(new_frame)
                # new_frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')

                i += 1
                last_frame = new_frame
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        return all_frames

    name, ext = oldPath.split('.')
    save_as = '{}_{}x{}.{}'.format(name, maxWidth, maxHeight, ext)
    all_frames = processImage(oldPath, maxWidth, maxHeight)
    all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)
    return save_as


def MakeThumbnail(imagePath, thumbnailWidth=300):
    print('MakeThumbnail(', imagePath, thumbnailWidth)
    try:
        saveToPath = '{}_thumb.{}'.format(*imagePath.split('.'))

        img = Image.open(imagePath)

        try:

            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation': break
            exif = dict(img._getexif().items())

            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)

        except Exception as e:
            print('133', e)

        wpercent = (thumbnailWidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))

        img = img.resize((thumbnailWidth, hsize), Image.ANTIALIAS)

        img.save(saveToPath)
        return saveToPath

    except Exception as e:
        print('19 MakeThumbnail Excpetion:', e)
        return imagePath


if __name__ == '__main__':
    # ret = MakeThumbnail(
    #     imagePath='static/user_content/1d0f4cff6bd5ee3418092ef3fca3bb597ebb1e25d08336e2e8875efcef124acf44a27c0acb4822074846e357f7dee693afd7bdccfee77c3932a66e6d284ea768.png',
    # )
    # print('37 ret=', ret)
    #
    # ret = MakeVideoThumbnail(
    #     videoPath='static/user_content/2018-10-11-1158-02.flv',
    # )
    # print('42 ret=', ret)
    # OptimizeToSize('static/user_content/update.jpg') # 4032x3024
    # OptimizeToSize('static/user_content/AR mmmkay copy.png')# 1198x1299
    # OptimizeToSize('static/user_content/potato.PNG') #431x458
    # OptimizeToSize('static/user_content/3024x4028.jpg') #3024x4032
    pass
