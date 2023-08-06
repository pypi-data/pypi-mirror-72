from PIL import Image, ExifTags
from math import sqrt
from pathlib import Path

def largest_ratio_box(ratio, img):
    """ Return a center rectangle box respecting the ratio inside the image.

    :param ratio:
    :param img: the img (from PIL.Image)
    :return: (left, upper, right, lower)
    """
    try:
        ratio[0]
    except TypeError:
        r = ratio
    else:
        r = ratio[0]/ratio[1]

    img_ratio  = img.size[0] / img.size[1]
    if img_ratio > r:
        return (int(img.size[0]/2-r*img.size[1]/2),
                0,
                int(img.size[0]/2+r*img.size[1]/2),
                img.size[1])
    else:
        return (0,
                int(img.size[1]/2-img.size[0]/(r*2)),
                img.size[0],
                int(img.size[1]/2+img.size[0]/(r*2)))

def auto_rotate_exif(img):
    """ Rotate the img corresponding to its exifdatas"""
    for orientation in ExifTags.TAGS.keys():
      if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(img._getexif().items())

    if exif[orientation] == 3:
        return img.rotate(180, expand=True)
    elif exif[orientation] == 6:
        return img.rotate(270, expand=True)
    elif exif[orientation] == 8:
        return img.rotate(90, expand=True)
    else:
        return img

def resize_to(img, megapixel=4):
    """ Resize the image to an image with total_pixel number of pixels
   
    :param img: the image
    :param megapixel: number of mega pixels
    """
    pixels = megapixel * 10**6
    org_ratio = img.size[0]/img.size[1]
    new_height = sqrt(pixels/org_ratio)
    new_width = org_ratio*new_height
    return img.resize((int(new_width), int(new_height)))

def fit_to(img, ratio, megapixel=4):
    """ auto_rotate then crop largest_ratio_box then resize_to
    if ration = 0, the image is not cropped
    """
    try:
        rot = auto_rotate_exif(img)
    except (AttributeError, KeyError):
        rot = img
    if ratio == 0:
        cropped = rot
    else:
        cropped = rot.crop(largest_ratio_box(ratio, rot))
    return resize_to(cropped, megapixel)

def cut_save(src, dest, ratio=0, megapixel=1):
    """
    if no ratio is given, the image is not cropped
    """
    img = Image.open(src)
    dest_filename = dest / rename(src, ratio)
    if not dest_filename.exists():
        print(f"Processing {dest_filename}")
        dest_filename.parent.mkdir(parents=True, exist_ok=True)
        out = fit_to(img, ratio, megapixel)
        out.save(dest_filename)
    else:
        print(f"{dest_filename} exists skipping")
    return dest_filename

def rename(src_filename, ratio):
    p_src = Path(src_filename)
    path = p_src.parent
    filename = p_src.stem
    ext = p_src.suffix
    return path / (filename + f"_{int(ratio[0])}by{int(ratio[1])}" + ext)


if __name__ == "__main__":
    img = Image.open("DSCN0119.JPG")
    filename = img.filename.split(".")[0]
    print(filename)
    print("img.size -> ", img.size)
    img = auto_rotate_exif(img)
    ratio = (1, 1)
    print(ratio)
    cropped = img.crop(largest_ratio_box(ratio, img))
    cropped.save(filename+f"_crop_{ratio[0]}by{ratio[1]}.jpg")
    crop_res = resize_to(cropped, 4)
    crop_res.save(filename+f"_resi_{ratio[0]}by{ratio[1]}.jpg")

    ratio = (2, 1)
    print(ratio)
    cropped = img.crop(largest_ratio_box(ratio, img))
    cropped.save(filename+f"_crop_{ratio[0]}by{ratio[1]}.jpg")
    crop_res = resize_to(cropped, 4)
    crop_res.save(filename+f"_resi_{ratio[0]}by{ratio[1]}.jpg")

    ratio = (1, 2)
    print(ratio)
    cropped = img.crop(largest_ratio_box(ratio, img))
    cropped.save(filename+f"_crop_{ratio[0]}by{ratio[1]}.jpg")
    crop_res = resize_to(cropped, 4)
    crop_res.save(filename+f"_resi_{ratio[0]}by{ratio[1]}.jpg")

    print("--------------")

    img = Image.open("IMG_2284.JPG")
    filename = img.filename.split(".")[0]
    print(filename)
    print("img.size -> ", img.size)
    img = auto_rotate_exif(img)
    ratio = (1, 1)
    print(ratio)
    cropped = img.crop(largest_ratio_box(ratio, img))
    cropped.save(filename+f"_crop_{ratio[0]}by{ratio[1]}.jpg")
    crop_res = resize_to(cropped, 4)
    crop_res.save(filename+f"_resi_{ratio[0]}by{ratio[1]}.jpg")

    ratio = (2, 1)
    print(ratio)
    cropped = img.crop(largest_ratio_box(ratio, img))
    cropped.save(filename+f"_crop_{ratio[0]}by{ratio[1]}.jpg")
    crop_res = resize_to(cropped, 4)
    crop_res.save(filename+f"_resi_{ratio[0]}by{ratio[1]}.jpg")

    ratio = (1, 2)
    print(ratio)
    cropped = img.crop(largest_ratio_box(ratio, img))
    cropped.save(filename+f"_crop_{ratio[0]}by{ratio[1]}.jpg")
    crop_res = resize_to(cropped, 4)
    crop_res.save(filename+f"_resi_{ratio[0]}by{ratio[1]}.jpg")
