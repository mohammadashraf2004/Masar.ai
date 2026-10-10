"""COURSE-014 Image Processing & Computer Vision Engineering: guided exercises.

OpenCV, Pillow, scikit-image and PyTorch are not installed in the practice
sandbox, so every exercise works on small synthetic images with NumPy and
SciPy (`ndimage`, `signal`), which implement the same operations; each brief
names the library call it mirrors.
"""
from . import Guided, check

NUMPY_NOTE = (
    "The image is a small synthetic array so the exercise runs in the sandbox; on a real photo the same NumPy/SciPy code applies, and the comments name the OpenCV, Pillow or scikit-image equivalent.",
    "الصورة مصفوفة اصطناعية صغيرة كي يعمل التمرين داخل بيئة التدريب؛ وعلى صورة حقيقية يُطبَّق كود NumPy/SciPy نفسه، وتذكر التعليقات المقابل في OpenCV أو Pillow أو scikit-image.",
)

EXERCISES = {
    "COURSE-014.M01.L01.EX01": Guided(
        goal=("Read an image as numbers: its shape order, dtype and range - then normalize it, mask it and do arithmetic safely.",
              "اقرأ الصورة بوصفها أرقامًا: ترتيب أبعادها ونوعها ونطاقها - ثم طبّعها وأنشئ قناعًا لها ونفّذ عليها عمليات حسابية بأمان."),
        steps=(
            ("Unpack NumPy's (height, width, channels) shape.", "فكّ أبعاد NumPy بالترتيب (height, width, channels)."),
            ("Convert to float in [0, 1].", "حوّل إلى أعداد عشرية في [0, 1]."),
            ("Make a grayscale image with the luma weights.", "أنشئ صورة رمادية بأوزان الإضاءة (luma)."),
            ("Build a Boolean mask of bright pixels.", "ابنِ قناعًا منطقيًا للبكسلات الساطعة."),
            ("Brighten by 10 without uint8 wrap-around.", "زِد السطوع بمقدار 10 دون التفاف قيم uint8."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)
# What np.asarray(Image.open(path)) gives for a 200 x 120 RGB photo
image = rng.integers(0, 256, size=(120, 200, 3), dtype=np.uint8)
pil_size = (200, 120)          # Pillow's img.size is (width, height); its mode would be "RGB"

# Step 1: NumPy order is (rows, columns, channels)
height, width, channels = ___
# Step 2: floats in [0, 1]
normalized = ___
# Step 3: grayscale = 0.299 R + 0.587 G + 0.114 B
gray = ___
# Step 4: True where a pixel is brighter than 0.5
mask = ___
# Step 5: uint8 wraps around (250 + 10 -> 4); add in a wider type, clip, convert back
brighter = ___

print(image.shape, image.dtype, image.min(), image.max(), "| Pillow size:", pil_size)
print(normalized.dtype, float(normalized.min()), float(normalized.max()), "| bright pixels:", int(mask.sum()))
''',
        answers=("image.shape", "image.astype(np.float32) / 255.0", "normalized @ np.array([0.299, 0.587, 0.114])", "gray > 0.5",
                 "np.clip(image.astype(np.int16) + 10, 0, 255).astype(np.uint8)"),
        checks=(
            check("[height, width, channels]", [120, 200, 3], "Blank 1: unpack `image.shape`.", "الفراغ 1: فكّ `image.shape`."),
            check("str(normalized.dtype).startswith('float') and float(normalized.max()) <= 1.0 and abs(float(normalized[0, 0, 0]) - image[0, 0, 0] / 255) < 1e-6", True,
                  "Blank 2: `image.astype(np.float32) / 255.0`.", "الفراغ 2: `image.astype(np.float32) / 255.0`."),
            check("list(gray.shape) == [120, 200] and bool(np.allclose(gray, normalized @ np.array([0.299, 0.587, 0.114])))", True,
                  "Blank 3: a weighted sum over the channel axis: `normalized @ np.array([0.299, 0.587, 0.114])`.",
                  "الفراغ 3: مجموع موزون على محور القنوات: `normalized @ np.array([0.299, 0.587, 0.114])`."),
            check("mask.dtype == bool and int(mask.sum()) == int((gray > 0.5).sum())", True, "Blank 4: `gray > 0.5`.", "الفراغ 4: `gray > 0.5`."),
            check("brighter.dtype == np.uint8 and int(brighter.max()) == 255 and bool(np.all(brighter >= image))", True,
                  "Blank 5: widen to int16, add 10, clip to 0-255, then back to uint8.", "الفراغ 5: وسّع إلى int16، وأضف 10، واقصص إلى 0-255، ثم أعد إلى uint8."),
        ),
        hints=(
            ("Pillow reports (width, height); NumPy reports (height, width, channels).", "يعرض Pillow (width, height)، ويعرض NumPy (height, width, channels)."),
            ("Divide by 255.0 after converting to float, never in uint8.", "اقسم على 255.0 بعد التحويل إلى عدد عشري، وليس داخل uint8."),
            ("`np.clip` keeps results inside 0-255 before converting back.", "يُبقي `np.clip` النتائج داخل 0-255 قبل التحويل مرة أخرى."),
        ),
        success=("Correct! The mask's True values mark pixels brighter than the threshold, and widening the dtype before adding prevents 250 + 10 from wrapping to 4.",
                 "صحيح! تشير قيم True في القناع إلى البكسلات الأسطع من العتبة، وتوسيع النوع قبل الجمع يمنع 250 + 10 من الالتفاف إلى 4."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-014.M01.L01.EX02": Guided(
        goal=("Build a small explainable pipeline: crop, change contrast safely, flip, blend and apply a sepia matrix.",
              "ابنِ خطًا صغيرًا قابلًا للشرح: القص، وتغيير التباين بأمان، والقلب، والمزج، وتطبيق مصفوفة سيبيا."),
        steps=(
            ("Crop rows 20-79 and columns 50-149.", "اقصص الصفوف 20-79 والأعمدة 50-149."),
            ("Increase contrast around mid-gray in float, then clip.", "زِد التباين حول الرمادي المتوسط بأعداد عشرية ثم اقصص."),
            ("Flip horizontally.", "اقلب أفقيًا."),
            ("Blend 70% original with 30% flipped.", "امزج 70% من الأصل مع 30% من المقلوب."),
            ("Apply the sepia color matrix.", "طبّق مصفوفة ألوان سيبيا."),
        ),
        starter='''import numpy as np

h, w = 120, 200
x = np.linspace(0, 1, w)
image = np.zeros((h, w, 3), dtype=np.uint8)
image[..., 0] = (x * 200 + 30).astype(np.uint8)          # red rises left to right
image[..., 1] = 90
image[..., 2] = ((1 - x) * 200 + 30).astype(np.uint8)    # blue falls left to right

# Step 1: a rectangular region by slicing (rows first, then columns)
crop = ___
# Step 2: contrast x1.3 around 128, computed in float32 and clipped before uint8
contrast = ___
# Step 3: mirror left-right
flipped = ___
# Step 4: 70% image + 30% flipped
blend = ___
SEPIA = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
# Step 5: every pixel's (R, G, B) multiplied by the sepia matrix
sepia = ___
print(crop.shape, contrast.dtype, int(flipped[0, 0, 0]), blend.dtype, sepia[0, 0])
''',
        answers=("image[20:80, 50:150]", "np.clip((image.astype(np.float32) - 128) * 1.3 + 128, 0, 255).astype(np.uint8)",
                 "image[:, ::-1]", "(0.7 * image + 0.3 * flipped).astype(np.uint8)",
                 "np.clip(image.astype(np.float32) @ SEPIA.T, 0, 255).astype(np.uint8)"),
        checks=(
            check("list(crop.shape) == [60, 100, 3] and bool(np.array_equal(crop[0, 0], image[20, 50]))", True,
                  "Blank 1: `image[20:80, 50:150]`.", "الفراغ 1: `image[20:80, 50:150]`."),
            check("contrast.dtype == np.uint8 and int(contrast[0, -1, 0]) == int(np.clip((float(image[0, -1, 0]) - 128) * 1.3 + 128, 0, 255))", True,
                  "Blank 2: subtract 128, multiply by 1.3, add 128, clip, then convert to uint8.", "الفراغ 2: اطرح 128، واضرب في 1.3، وأضف 128، واقصص، ثم حوّل إلى uint8."),
            check("bool(np.array_equal(flipped[:, 0], image[:, -1]))", True, "Blank 3: `image[:, ::-1]`.", "الفراغ 3: `image[:, ::-1]`."),
            check("blend.dtype == np.uint8 and int(blend[0, 0, 0]) == int(0.7 * int(image[0, 0, 0]) + 0.3 * int(image[0, -1, 0]))", True,
                  "Blank 4: `(0.7 * image + 0.3 * flipped).astype(np.uint8)`.", "الفراغ 4: `(0.7 * image + 0.3 * flipped).astype(np.uint8)`."),
            check("bool(np.array_equal(sepia, np.clip(image.astype(np.float32) @ SEPIA.T, 0, 255).astype(np.uint8)))", True,
                  "Blank 5: multiply each pixel vector by `SEPIA.T`, clip and convert.", "الفراغ 5: اضرب متجه كل بكسل في `SEPIA.T`، ثم اقصص وحوّل."),
        ),
        hints=(
            ("Image coordinates are [row, column] - y before x.", "إحداثيات الصورة [row, column] - أي y قبل x."),
            ("Do arithmetic in float32, clip to 0-255, then `.astype(np.uint8)`.", "نفّذ الحسابات بـ float32، واقصص إلى 0-255، ثم `.astype(np.uint8)`."),
            ("A color matrix applies to the last axis: `pixels @ M.T`.", "تُطبَّق مصفوفة الألوان على المحور الأخير: `pixels @ M.T`."),
        ),
        success=("Correct! Each step names its representation: slicing uses [row, column], arithmetic happens in float and is clipped, and color effects are matrix products on the channel axis.",
                 "صحيح! تسمّي كل خطوة تمثيلها: يستخدم القص [row, column]، وتجري الحسابات بأعداد عشرية مع القص، وتأثيرات الألوان ضرب مصفوفات على محور القنوات."),
        expected=NUMPY_NOTE,
        reflect=("Name one failure mode you avoided: dtype overflow, BGR/RGB channel order, value range or (x, y) versus (row, column).",
                 "اذكر نمط فشل واحدًا تجنّبته: فيض نوع البيانات، أو ترتيب القنوات BGR/RGB، أو نطاق القيم، أو (x, y) مقابل (row, column)."),
    ),
    "COURSE-014.M02.L01.EX01": Guided(
        goal=("Treat geometric transforms as coordinate mappings: translate, rotate about the centre, combine rotation and scale in a matrix, and invert it.",
              "تعامل مع التحويلات الهندسية بوصفها تحويلات للإحداثيات: الإزاحة، والتدوير حول المركز، ودمج التدوير والتحجيم في مصفوفة، ثم عكسها."),
        steps=(
            ("Shift the image down 10 and right 15 pixels.", "أزِح الصورة 10 بكسلات للأسفل و15 لليمين."),
            ("Rotate 30° about the centre.", "دوّر 30° حول المركز."),
            ("Write the similarity transform matrix.", "اكتب مصفوفة تحويل التشابه."),
            ("Invert it to map output pixels back to their source.", "اعكسها لتعيد بكسلات المخرج إلى مصدرها."),
            ("Count the distinct values after nearest-neighbour rotation.", "عُدّ القيم المميزة بعد التدوير بأقرب جار."),
        ),
        starter='''import numpy as np
from scipy import ndimage

image = np.zeros((100, 100))
image[20:30, 20:30] = 1.0                                     # a bright square

# Step 1: translation (skimage: AffineTransform(translation=...))
translated = ___
# Step 2: rotation about the centre, same canvas size, bilinear interpolation
rotated = ___

# Step 3: similarity = rotation + uniform scale + translation in one 3x3 matrix (x, y, 1)
theta, s, tx, ty = np.deg2rad(30), 1.2, 5.0, -3.0
M = ___
# Step 4: inverse mapping - for each OUTPUT pixel, where in the input does it come from?
M_inv = ___
source_of_centre = M_inv @ np.array([50.0, 50.0, 1.0])

# Step 5: nearest-neighbour keeps only the original values; bilinear creates in-between values
nearest = ndimage.rotate(image, 30, reshape=False, order=0)
distinct_nearest = ___
distinct_bilinear = len(np.unique(rotated.round(6)))
print(int(translated[30:40, 35:45].sum()), distinct_nearest, distinct_bilinear, source_of_centre.round(2))
''',
        answers=(
            "ndimage.shift(image, (10, 15), order=0)",
            "ndimage.rotate(image, 30, reshape=False, order=1)",
            "np.array([[s * np.cos(theta), -s * np.sin(theta), tx], [s * np.sin(theta), s * np.cos(theta), ty], [0.0, 0.0, 1.0]])",
            "np.linalg.inv(M)",
            "len(np.unique(nearest))",
        ),
        checks=(
            check("float(translated[30:40, 35:45].sum()) == 100.0 and float(translated[20:30, 20:30].sum()) == 0.0", True,
                  "Blank 1: `ndimage.shift(image, (10, 15), order=0)` - (rows, columns).", "الفراغ 1: `ndimage.shift(image, (10, 15), order=0)` - (الصفوف، الأعمدة)."),
            check("list(rotated.shape) == [100, 100] and bool(np.allclose(rotated, ndimage.rotate(image, 30, reshape=False, order=1)))", True,
                  "Blank 2: `ndimage.rotate(image, 30, reshape=False, order=1)`.", "الفراغ 2: `ndimage.rotate(image, 30, reshape=False, order=1)`."),
            check("bool(np.allclose(M @ np.array([1.0, 0.0, 1.0]), [1.2 * np.cos(np.deg2rad(30)) + 5, 1.2 * np.sin(np.deg2rad(30)) - 3, 1]))", True,
                  "Blank 3: the top-left 2x2 is s·rotation, the last column is (tx, ty, 1).", "الفراغ 3: الجزء 2x2 الأعلى يساري هو s·rotation، والعمود الأخير (tx, ty, 1)."),
            check("bool(np.allclose(M @ M_inv, np.eye(3)))", True, "Blank 4: `np.linalg.inv(M)`.", "الفراغ 4: `np.linalg.inv(M)`."),
            check("distinct_nearest == 2 and distinct_bilinear > 2", True, "Blank 5: `len(np.unique(nearest))`.", "الفراغ 5: `len(np.unique(nearest))`."),
        ),
        hints=(
            ("`ndimage.shift` takes (row shift, column shift).", "يأخذ `ndimage.shift` (إزاحة الصفوف، إزاحة الأعمدة)."),
            ("`reshape=False` keeps the canvas size, so corners can fall outside.", "يحافظ `reshape=False` على حجم اللوحة، فقد تخرج الزوايا منها."),
            ("Homogeneous coordinates let one 3x3 matrix rotate, scale and translate at once.", "تتيح الإحداثيات المتجانسة لمصفوفة 3x3 واحدة التدوير والتحجيم والإزاحة معًا."),
        ),
        success=("Correct! Every transform is a coordinate mapping; inverse mapping fills each output pixel from a source location, and the interpolation order decides whether new in-between values appear.",
                 "صحيح! كل تحويل تحويلٌ للإحداثيات؛ ويملأ الربط العكسي كل بكسل مخرج من موقع مصدري، ويحدد ترتيب الاستيفاء هل تظهر قيم وسيطة جديدة."),
        expected=NUMPY_NOTE,
        reflect=("Distinguish rigid, similarity, affine and projective transforms in two or three sentences.",
                 "ميّز بين التحويلات الصلبة والتشابهية والأفينية والإسقاطية في جملتين أو ثلاث."),
    ),
    "COURSE-014.M02.L01.EX02": Guided(
        goal=("Keep one colour while desaturating the rest, resize an overlay with its aspect ratio, and composite it with transparency.",
              "احتفظ بلون واحد مع إزالة تشبّع الباقي، وغيّر حجم طبقة علوية مع الحفاظ على نسبة أبعادها، وركّبها بالشفافية."),
        steps=(
            ("Mask the strongly red pixels.", "أنشئ قناعًا للبكسلات الحمراء بقوة."),
            ("Keep colour inside the mask and gray outside.", "احتفظ باللون داخل القناع والرمادي خارجه."),
            ("Compute the overlay height for a width of 50 px.", "احسب ارتفاع الطبقة العلوية لعرض 50 بكسلًا."),
            ("Alpha-blend the overlay at 60%.", "امزج الطبقة العلوية بشفافية 60%."),
            ("Blend with a left-to-right gradient mask.", "امزج بقناع متدرج من اليسار إلى اليمين."),
        ),
        starter='''import numpy as np
from scipy import ndimage

H, W = 100, 160
yy, xx = np.mgrid[0:H, 0:W]
image = np.zeros((H, W, 3), dtype=np.uint8)
image[...] = (40, 120, 160)                                  # blue-green background
image[(yy - 50) ** 2 + (xx - 80) ** 2 < 25 ** 2] = (220, 30, 40)   # a red disc
gray = image.mean(axis=2, keepdims=True).astype(np.uint8).repeat(3, axis=2)

# Step 1: red clearly dominates
mask = ___
# Step 2: colour where the mask is True, gray elsewhere
selective = ___

logo = np.full((40, 80, 3), 255, dtype=np.uint8)              # a 80 x 40 white overlay
# Step 3: new (height, width) for width 50, keeping the aspect ratio
new_size = ___
overlay = ndimage.zoom(logo, (new_size[0] / logo.shape[0], new_size[1] / logo.shape[1], 1), order=1)

composite = image.copy()
region = composite[5:5 + overlay.shape[0], 5:5 + overlay.shape[1]]
# Step 4: 60% overlay over the image underneath
composite[5:5 + overlay.shape[0], 5:5 + overlay.shape[1]] = ___
# Step 5: colour on the right, gray on the left, smoothly in between
ramp = np.linspace(0, 1, W)[None, :, None]
gradient_blend = ___
print(int(mask.sum()), new_size, composite[10, 10], gradient_blend[0, 0], gradient_blend[0, -1])
''',
        answers=(
            "(image[:, :, 0] > 150) & (image[:, :, 1] < 100)",
            "np.where(mask[:, :, None], image, gray)",
            "(round(logo.shape[0] * 50 / logo.shape[1]), 50)",
            "(0.6 * overlay + 0.4 * region).astype(np.uint8)",
            "(ramp * image + (1 - ramp) * gray).astype(np.uint8)",
        ),
        checks=(
            check("int(mask.sum()) == int(((yy - 50) ** 2 + (xx - 80) ** 2 < 625).sum())", True,
                  "Blank 1: red channel high AND green channel low.", "الفراغ 1: القناة الحمراء مرتفعة والقناة الخضراء منخفضة."),
            check("bool(np.array_equal(selective[50, 80], image[50, 80])) and bool(np.array_equal(selective[0, 0], gray[0, 0]))", True,
                  "Blank 2: `np.where(mask[:, :, None], image, gray)`.", "الفراغ 2: `np.where(mask[:, :, None], image, gray)`."),
            check("list(new_size)", [25, 50], "Blank 3: height = 40 × 50 / 80 = 25.", "الفراغ 3: الارتفاع = 40 × 50 / 80 = 25."),
            check("composite[10, 10].tolist() == (0.6 * 255 + 0.4 * np.array([40, 120, 160])).astype(np.uint8).tolist()", True,
                  "Blank 4: `(0.6 * overlay + 0.4 * region).astype(np.uint8)`.", "الفراغ 4: `(0.6 * overlay + 0.4 * region).astype(np.uint8)`."),
            check("gradient_blend[0, 0].tolist() == gray[0, 0].tolist() and gradient_blend[0, -1].tolist() == image[0, -1].tolist()", True,
                  "Blank 5: weight the colour image by `ramp` and the gray image by `1 - ramp`.", "الفراغ 5: زِن الصورة الملوّنة بـ `ramp` والرمادية بـ `1 - ramp`."),
        ),
        hints=(
            ("Combine channel conditions with `&`.", "اجمع شروط القنوات بـ `&`."),
            ("`mask[:, :, None]` broadcasts one mask over three channels.", "يبث `mask[:, :, None]` قناعًا واحدًا على ثلاث قنوات."),
            ("Alpha compositing: alpha · top + (1 − alpha) · bottom.", "التركيب بالشفافية: alpha · العلوي + (1 − alpha) · السفلي."),
        ),
        success=("Correct! The mask isolates the red disc, the overlay keeps its 2:1 shape, and both blends work because the images share the same height, width, channel count and dtype.",
                 "صحيح! يعزل القناع القرص الأحمر، وتحافظ الطبقة العلوية على شكلها 2:1، ويعمل المزجان لأن الصور تتشارك الارتفاع والعرض وعدد القنوات ونوع البيانات."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-014.M03.L01.EX01": Guided(
        goal=("Enhance a photo with a gamma lookup table, a warm colour grade and a radial vignette mask.",
              "حسّن صورة بجدول بحث لجاما (gamma)، وتدرج لوني دافئ، وقناع تعتيم شعاعي (vignette)."),
        steps=(
            ("Build a 256-entry gamma lookup table.", "ابنِ جدول بحث لجاما من 256 مدخلًا."),
            ("Warm the colours: more red, less blue.", "دفّئ الألوان: أحمر أكثر وأزرق أقل."),
            ("Build a radial mask: 1 at the centre, darker towards the corners.", "ابنِ قناعًا شعاعيًا: 1 في المركز ويغمق نحو الزوايا."),
            ("Apply the mask to darken the edges.", "طبّق القناع لتعتيم الحواف."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)
h, w = 90, 140
image = rng.integers(40, 200, size=(h, w, 3), dtype=np.uint8)

# Step 1: lookup table - out = 255 * (in / 255) ** gamma for every possible input value
gamma = 0.6
lut = ___
corrected = lut[image]                                      # Pillow: image.point(lut)
# Step 2: colour temperature - red x1.08, green x1.0, blue x0.9
warm = ___
# Step 3: 1 at the centre, falling to 0.4 in the corners
yy, xx = np.mgrid[0:h, 0:w]
r = np.sqrt((yy - h / 2) ** 2 + (xx - w / 2) ** 2) / np.sqrt((h / 2) ** 2 + (w / 2) ** 2)
vignette_mask = ___
# Step 4: the mask scales every channel of every pixel
final = ___
print(lut[[0, 64, 128, 255]], warm[0, 0], round(float(vignette_mask.min()), 2), round(float(vignette_mask.max()), 2))
''',
        answers=(
            "np.clip(255 * (np.arange(256) / 255) ** gamma, 0, 255).astype(np.uint8)",
            "np.clip(corrected.astype(np.float32) * np.array([1.08, 1.0, 0.9]), 0, 255).astype(np.uint8)",
            "1 - 0.6 * r ** 2",
            "(warm * vignette_mask[:, :, None]).astype(np.uint8)",
        ),
        checks=(
            check("len(lut) == 256 and int(lut[0]) == 0 and int(lut[255]) == 255 and int(lut[64]) > 64", True,
                  "Blank 1: `255 * (np.arange(256) / 255) ** gamma`, clipped and converted to uint8 - gamma < 1 brightens the mid-tones.",
                  "الفراغ 1: `255 * (np.arange(256) / 255) ** gamma` مع القص والتحويل إلى uint8 - وجاما أقل من 1 تفتّح الدرجات المتوسطة."),
            check("warm.dtype == np.uint8 and int(warm[0, 0, 2]) == int(np.clip(float(corrected[0, 0, 2]) * 0.9, 0, 255))", True,
                  "Blank 2: multiply the channels by `[1.08, 1.0, 0.9]` in float, then clip.", "الفراغ 2: اضرب القنوات في `[1.08, 1.0, 0.9]` بأعداد عشرية، ثم اقصص."),
            check("[round(float(vignette_mask.max()), 2), round(float(vignette_mask.min()), 2)]", [1.0, 0.4],
                  "Blank 3: `1 - 0.6 * r ** 2`.", "الفراغ 3: `1 - 0.6 * r ** 2`."),
            check("bool(np.array_equal(final[h // 2, w // 2], warm[h // 2, w // 2])) and int(final[0, 0].sum()) < int(warm[0, 0].sum())", True,
                  "Blank 4: multiply by `vignette_mask[:, :, None]` and convert to uint8.", "الفراغ 4: اضرب في `vignette_mask[:, :, None]` وحوّل إلى uint8."),
        ),
        hints=(
            ("A LUT precomputes the output for all 256 input values; indexing applies it.", "يحسب جدول البحث مسبقًا المخرج لكل القيم الـ256، والفهرسة تطبّقه."),
            ("Per-channel gains are a 3-element array that broadcasts over the image.", "معاملات الكسب لكل قناة مصفوفة من 3 عناصر تُبثّ على الصورة."),
            ("`[:, :, None]` lets a 2-D mask scale all three channels.", "يتيح `[:, :, None]` لقناع ثنائي الأبعاد تحجيم القنوات الثلاث."),
        ),
        success=("Correct! The LUT and the colour grade change pixel values everywhere; the vignette changes them through a spatial mask. JPEG quality, by contrast, would only change how the image is stored.",
                 "صحيح! يغيّر جدول البحث والتدرج اللوني قيم البكسلات في كل مكان، بينما يغيّرها التعتيم عبر قناع مكاني. أما جودة JPEG فلا تغيّر إلا طريقة تخزين الصورة."),
        expected=NUMPY_NOTE,
        reflect=("Why could an extreme version of this effect hurt a model if used as training augmentation?",
                 "لماذا قد تضرّ نسخة متطرفة من هذا التأثير بالنموذج إذا استُخدمت تعزيزًا للتدريب؟"),
    ),
    "COURSE-014.M03.L01.EX02": Guided(
        goal=("Rectify a tilted planar object by solving a homography from four corner correspondences, and see what swapped corners do.",
              "قوّم جسمًا مستويًا مائلًا بحل homography من أربع زوايا متقابلة، ولاحظ ما تفعله الزوايا المتبادلة."),
        steps=(
            ("Solve the 8×8 system for the homography entries.", "حلّ نظام 8×8 لإيجاد عناصر homography."),
            ("Append h33 = 1 and reshape to 3×3.", "أضف h33 = 1 وأعد التشكيل إلى 3×3."),
            ("Divide by w after applying H.", "اقسم على w بعد تطبيق H."),
            ("Compute the homography with two destination corners swapped.", "احسب homography مع تبديل زاويتين من زوايا الوجهة."),
            ("Zoom an image with cubic interpolation.", "كبّر صورة باستيفاء تكعيبي."),
        ),
        starter='''import numpy as np
from scipy import ndimage

# Corners of a tilted poster in the photo (x, y), clockwise from top-left, and the upright target
src = np.array([[10, 20], [180, 5], [190, 110], [5, 100]], dtype=float)
dst = np.array([[0, 0], [199, 0], [199, 99], [0, 99]], dtype=float)

def homography(src, dst):
    """What cv2.getPerspectiveTransform(src, dst) computes."""
    rows = []
    for (x, y), (u, v) in zip(src, dst):
        rows.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        rows.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A, b = np.array(rows), dst.reshape(-1)
    # Step 1: eight equations, eight unknowns
    h = ___
    # Step 2: h33 is fixed to 1
    return ___

def apply(H, point):
    x, y, w = H @ np.array([point[0], point[1], 1.0])
    # Step 3: back from homogeneous coordinates
    return ___

H = homography(src, dst)
# Step 4: the same corners with the first two destination points swapped
H_swapped = ___

small = np.arange(16, dtype=float).reshape(4, 4)
zoom_nearest = ndimage.zoom(small, 2, order=0)
# Step 5: smooth (cubic) interpolation
zoom_cubic = ___
print([tuple(np.round(apply(H, p), 2)) for p in src])
print(tuple(np.round(apply(H_swapped, src[0]), 2)), zoom_cubic.shape)
''',
        answers=("np.linalg.solve(A, b)", "np.append(h, 1.0).reshape(3, 3)", "(x / w, y / w)",
                 "homography(src, dst[[1, 0, 2, 3]])", "ndimage.zoom(small, 2, order=3)"),
        checks=(
            check("all(bool(np.allclose(apply(H, s), d, atol=1e-6)) for s, d in zip(src, dst))", True,
                  "Blanks 1-3: solve `A h = b`, append 1, reshape to 3x3, and divide x and y by w.",
                  "الفراغات 1-3: حلّ `A h = b`، وأضف 1، وأعد التشكيل إلى 3x3، واقسم x وy على w."),
            check("bool(np.allclose(apply(H_swapped, src[0]), [199, 0], atol=1e-6))", True,
                  "Blank 4: swap destination rows 0 and 1 with `dst[[1, 0, 2, 3]]`.", "الفراغ 4: بدّل صفي الوجهة 0 و1 بـ `dst[[1, 0, 2, 3]]`."),
            check("list(zoom_cubic.shape) == [8, 8] and len(np.unique(zoom_cubic.round(6))) > len(np.unique(zoom_nearest))", True,
                  "Blank 5: `ndimage.zoom(small, 2, order=3)`.", "الفراغ 5: `ndimage.zoom(small, 2, order=3)`."),
        ),
        hints=(
            ("`np.linalg.solve` finds x in A x = b; here x is the 8 unknowns h11..h32.", "تجد `np.linalg.solve` قيمة x في A x = b، وx هنا هي المجاهيل الثمانية h11..h32."),
            ("A projective point (x, y, w) corresponds to (x/w, y/w).", "النقطة الإسقاطية (x, y, w) تقابل (x/w, y/w)."),
            ("Fancy indexing `dst[[1, 0, 2, 3]]` reorders rows.", "تعيد الفهرسة `dst[[1, 0, 2, 3]]` ترتيب الصفوف."),
        ),
        success=("Correct! Four correspondences in a consistent order define the rectifying homography; swapping two corners silently produces a different, twisted mapping - correspondence order matters.",
                 "صحيح! تحدد أربع تقابلات بترتيب متسق homography التقويم؛ وتبديل زاويتين ينتج بصمت تحويلًا مختلفًا ملتويًا - فترتيب التقابل مهم."),
        expected=NUMPY_NOTE,
        reflect=("How do rectification and warping both reduce to coordinate mapping plus resampling?",
                 "كيف يختزل التقويم والتشويه كلاهما إلى تحويل إحداثيات مع إعادة أخذ العينات؟"),
    ),
    "COURSE-014.M04.L01.EX01": Guided(
        goal=("See aliasing appear when fine stripes are sampled too sparsely, prevent it by blurring first, and measure quantization error.",
              "شاهد ظهور التعرّج (aliasing) عند أخذ عينات متباعدة جدًا من خطوط دقيقة، وامنعه بالتمويه أولًا، وقِس خطأ التكميم."),
        steps=(
            ("Downsample by keeping every 3rd column.", "صغّر بأخذ عمود من كل 3 أعمدة."),
            ("Blur first, then downsample.", "موّه أولًا ثم صغّر."),
            ("Quantize to a given number of levels.", "كمّم إلى عدد معيّن من المستويات."),
            ("Compute the MSE for 16, 8 and 4 levels.", "احسب MSE لـ 16 و8 و4 مستويات."),
        ),
        starter='''import numpy as np
from scipy import ndimage

columns = np.arange(240)
stripes = np.tile((np.sin(2 * np.pi * columns / 4) + 1) / 2, (32, 1))   # fine stripes: period 4 px

# Step 1: direct slicing - no low-pass filter
naive = ___
# Step 2: anti-aliasing - remove frequencies that cannot survive, THEN sample
blurred = ndimage.gaussian_filter(stripes, sigma=1.5)
anti_aliased = ___

def dominant_period(row):
    spectrum = np.abs(np.fft.rfft(row - row.mean()))
    return len(row) / int(np.argmax(spectrum))

gradient = np.tile(np.linspace(0, 1, 256), (16, 1))
# Step 3: snap values in [0, 1] to `levels` evenly spaced levels
def quantize(img, levels):
    return ___

# Step 4: mean squared error against the original gradient
mse = {levels: ___ for levels in (16, 8, 4)}
print("naive period:", round(dominant_period(naive[0]), 1), "| anti-aliased std:", round(float(anti_aliased.std()), 3))
print(mse)
''',
        answers=("stripes[:, ::3]", "blurred[:, ::3]", "np.round(img * (levels - 1)) / (levels - 1)",
                 "round(float(np.mean((gradient - quantize(gradient, levels)) ** 2)), 6)"),
        checks=(
            check("list(naive.shape) == [32, 80] and round(dominant_period(naive[0])) == 4", True,
                  "Blank 1: `stripes[:, ::3]` - the true 12-pixel stripes now look like a false 4-sample pattern.",
                  "الفراغ 1: `stripes[:, ::3]` - تبدو الخطوط الحقيقية الآن نمطًا زائفًا كل 4 عينات."),
            check("list(anti_aliased.shape) == [32, 80] and float(anti_aliased.std()) < 0.05", True,
                  "Blank 2: sample the blurred image: `blurred[:, ::3]`.", "الفراغ 2: خذ العينات من الصورة المموّهة: `blurred[:, ::3]`."),
            check("[sorted(set(np.round(quantize(gradient, 4), 6).ravel().tolist())), float(quantize(np.array([0.49]), 2)[0])]", [[0.0, 0.333333, 0.666667, 1.0], 0.0],
                  "Blank 3: `np.round(img * (levels - 1)) / (levels - 1)`.", "الفراغ 3: `np.round(img * (levels - 1)) / (levels - 1)`."),
            check("mse[16] < mse[8] < mse[4] and mse[4] > 0", True, "Blank 4: the mean of the squared differences.", "الفراغ 4: متوسط مربعات الفروق."),
        ),
        hints=(
            ("Step slicing `[:, ::3]` keeps every third column.", "يحتفظ التقطيع بخطوة `[:, ::3]` بعمود من كل ثلاثة."),
            ("A low-pass blur removes detail that the coarser grid cannot represent.", "يزيل التمويه منخفض التمرير التفاصيل التي لا تستطيع الشبكة الأخشن تمثيلها."),
            ("Scale to 0..levels-1, round, then scale back.", "حجّم إلى 0..levels-1، ثم قرّب، ثم أعد التحجيم."),
        ),
        success=("Correct! Sampling too sparsely turned real detail into a false pattern (aliasing); blurring first removed it instead. Quantization loses information differently - fewer levels, larger error.",
                 "صحيح! حوّل أخذ العينات المتباعد جدًا التفاصيل الحقيقية إلى نمط زائف (تعرّج)، بينما أزالها التمويه أولًا. ويفقد التكميم المعلومات بطريقة مختلفة - مستويات أقل تعني خطأ أكبر."),
        expected=NUMPY_NOTE,
        reflect=("Enlarge a small crop with nearest, bilinear and bicubic interpolation (`ndimage.zoom` orders 0, 1, 3). What does each do to edges?",
                 "كبّر قصاصة صغيرة باستيفاء أقرب جار وثنائي الخطية وتكعيبي (رتب `ndimage.zoom` 0 و1 و3). ماذا يفعل كلٌّ منها بالحواف؟"),
    ),
    "COURSE-014.M04.L01.EX02": Guided(
        goal=("Read an image through its Fourier transform: reconstruct it, see what translation does to the spectrum, check Parseval, and window the edges.",
              "اقرأ الصورة عبر تحويل فورييه: أعد بناءها، ولاحظ أثر الإزاحة في الطيف، وتحقّق من مبرهنة بارسفال، وطبّق نافذة على الحواف."),
        steps=(
            ("Compute the 2-D FFT.", "احسب FFT ثنائي الأبعاد."),
            ("Reconstruct the image with the inverse FFT.", "أعد بناء الصورة بـ FFT العكسي."),
            ("Check that a circular shift keeps the magnitude.", "تحقّق من أن الإزاحة الدائرية تحافظ على المقدار."),
            ("Check Parseval's energy identity.", "تحقّق من هوية الطاقة لبارسفال."),
            ("Apply a 2-D Hann window.", "طبّق نافذة Hann ثنائية الأبعاد."),
        ),
        starter='''import numpy as np

h, w = 64, 64
yy, xx = np.mgrid[0:h, 0:w]
img = 0.5 + 0.3 * np.sin(2 * np.pi * xx / 8)          # vertical stripes
img[20:40, 20:40] += 0.2                               # a square with sharp edges

# Step 1: the 2-D spectrum (complex numbers)
F = ___
log_magnitude = np.log1p(np.abs(np.fft.fftshift(F)))   # centred, for display
phase = np.angle(F)
# Step 2: back to the image
reconstructed = ___

# Step 3: a circular translation changes only the phase
shifted = np.roll(img, (5, 9), axis=(0, 1))
same_magnitude = ___

# Step 4: Parseval with NumPy's unnormalized FFT: sum |img|^2 == sum |F|^2 / N
parseval_ok = ___

# Step 5: taper the borders to zero to reduce edge leakage
window = np.outer(np.hanning(h), np.hanning(w))
windowed = ___
print(bool(np.allclose(reconstructed, img)), same_magnitude, parseval_ok, round(float(windowed[0, 0]), 3))
''',
        answers=("np.fft.fft2(img)", "np.real(np.fft.ifft2(F))", "bool(np.allclose(np.abs(np.fft.fft2(shifted)), np.abs(F)))",
                 "bool(np.isclose(np.sum(img ** 2), np.sum(np.abs(F) ** 2) / img.size))", "img * window"),
        checks=(
            check("bool(np.allclose(F, np.fft.fft2(img)))", True, "Blank 1: `np.fft.fft2(img)`.", "الفراغ 1: `np.fft.fft2(img)`."),
            check("bool(np.allclose(reconstructed, img)) and not np.iscomplexobj(reconstructed)", True,
                  "Blank 2: `np.real(np.fft.ifft2(F))`.", "الفراغ 2: `np.real(np.fft.ifft2(F))`."),
            check("same_magnitude is True and not bool(np.allclose(np.angle(np.fft.fft2(shifted)), phase))", True,
                  "Blank 3: compare `np.abs` of both spectra with `np.allclose`.", "الفراغ 3: قارن `np.abs` للطيفين باستخدام `np.allclose`."),
            check("parseval_ok is True", True, "Blank 4: compare the two energies with `np.isclose`, dividing the spectral energy by `img.size`.",
                  "الفراغ 4: قارن الطاقتين بـ `np.isclose` مع قسمة الطاقة الطيفية على `img.size`."),
            check("bool(np.allclose(windowed, img * window)) and float(windowed[0, 0]) == 0.0", True, "Blank 5: `img * window`.", "الفراغ 5: `img * window`."),
        ),
        hints=(
            ("`np.fft.fft2` and `np.fft.ifft2` are inverses; take the real part at the end.", "`np.fft.fft2` و`np.fft.ifft2` متعاكستان؛ خذ الجزء الحقيقي في النهاية."),
            ("Shifting multiplies the spectrum by a phase factor, so |F| does not change.", "تضرب الإزاحة الطيف في معامل طور، لذا لا يتغير |F|."),
            ("NumPy's FFT is unnormalized, hence the division by N in Parseval.", "تحويل NumPy غير مُطبَّع، ولهذا نقسم على N في بارسفال."),
        ),
        success=("Correct! The FFT is lossless, translation lives entirely in the phase, energy is conserved, and a window removes the artificial edges that a periodic FFT assumes.",
                 "صحيح! تحويل FFT بلا فقد، والإزاحة تعيش كليًا في الطور، والطاقة محفوظة، وتزيل النافذة الحواف الاصطناعية التي يفترضها FFT الدوري."),
        expected=NUMPY_NOTE,
        reflect=("Rotate the image by 90° and compare the spectrum's dominant directions. Which observations did you predict, and which surprised you?",
                 "دوّر الصورة 90° وقارن الاتجاهات السائدة في الطيف. أي الملاحظات توقعتها، وأيها فاجأتك؟"),
    ),
    "COURSE-014.M05.L01.EX01": Guided(
        goal=("Filter with convolution, compare border modes, and find a template with raw and normalized cross-correlation.",
              "رشّح بالالتفاف، وقارن أنماط الحدود، وجد قالبًا بالارتباط المتقاطع الخام والمُطبَّع."),
        steps=(
            ("Build a normalized 3×3 box kernel.", "ابنِ نواة صندوقية 3×3 مُطبَّعة."),
            ("Sharpen with the Laplacian-style kernel.", "اشحذ بالنواة المشابهة للابلاسيان."),
            ("Locate the raw cross-correlation peak.", "حدّد قمة الارتباط المتقاطع الخام."),
            ("Compute normalized cross-correlation for one window.", "احسب الارتباط المتقاطع المُطبَّع لنافذة واحدة."),
        ),
        starter='''import numpy as np
from scipy.signal import convolve2d, correlate2d, fftconvolve

h, w = 60, 80
img = np.tile(np.linspace(0.0, 0.6, w), (h, 1))          # brighter to the right
img[30:35, 20:25] += 0.4                                    # a small distinctive cross ...
img[25:40, 22:23] += 0.4
template = img[25:40, 15:30].copy()                         # ... cut out as the template (top-left at row 25, col 15)

# Step 1: averaging kernel whose weights sum to 1
box = ___
zero_border = convolve2d(img, box, mode="same", boundary="fill")
mirrored_border = convolve2d(img, box, mode="same", boundary="symm")
sharpened = convolve2d(img, np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]), mode="same", boundary="symm")

# Step 2: raw correlation rewards bright regions, not just matching shapes
raw = correlate2d(img, template, mode="valid")
raw_peak = ___

def ncc_at(image, template, i, j):
    patch = image[i:i + template.shape[0], j:j + template.shape[1]]
    p, t = patch - patch.mean(), template - template.mean()
    # Step 3: correlation of the zero-mean patch and template, divided by both norms
    return ___

ncc = np.array([[ncc_at(img, template, i, j) for j in range(w - 15 + 1)] for i in range(h - 15 + 1)])
# Step 4: where NCC is highest
ncc_peak = ___
print("border mean (zero vs mirrored):", round(float(zero_border[0].mean()), 3), round(float(mirrored_border[0].mean()), 3))
print("raw peak:", raw_peak, "| NCC peak:", ncc_peak)
''',
        answers=("np.ones((3, 3)) / 9", "tuple(int(v) for v in np.unravel_index(np.argmax(raw), raw.shape))",
                 "float((p * t).sum() / (np.sqrt((p ** 2).sum() * (t ** 2).sum()) + 1e-12))",
                 "tuple(int(v) for v in np.unravel_index(np.argmax(ncc), ncc.shape))"),
        checks=(
            check("abs(float(box.sum()) - 1.0) < 1e-12 and list(box.shape) == [3, 3] and float(zero_border[0].mean()) < float(mirrored_border[0].mean())", True,
                  "Blank 1: `np.ones((3, 3)) / 9` - zero-filled borders darken the edges, mirrored ones do not.",
                  "الفراغ 1: `np.ones((3, 3)) / 9` - تعتّم الحدود المملوءة بالأصفار الحواف، ولا تفعل الحدود المعكوسة ذلك."),
            check("list(raw_peak) == [int(v) for v in np.unravel_index(np.argmax(raw), raw.shape)] and list(raw_peak) != [25, 15]", True,
                  "Blank 2: `np.unravel_index(np.argmax(raw), raw.shape)` - it lands on the bright side, not the cross.",
                  "الفراغ 2: `np.unravel_index(np.argmax(raw), raw.shape)` - تقع القمة في الجهة الساطعة لا على الصليب."),
            check("abs(ncc_at(img, template, 25, 15) - 1.0) < 1e-9 and abs(ncc_at(img + 0.3, template, 25, 15) - 1.0) < 1e-9", True,
                  "Blank 3: divide the sum of p·t by sqrt(sum p² · sum t²) - brightness offsets cancel out.",
                  "الفراغ 3: اقسم مجموع p·t على sqrt(sum p² · sum t²) - فتُلغى إزاحات السطوع."),
            check("list(ncc_peak)", [25, 15], "Blank 4: the argmax of `ncc` as (row, column).", "الفراغ 4: موضع أكبر قيمة في `ncc` بصيغة (row, column)."),
        ),
        hints=(
            ("A normalized kernel's weights sum to 1, so flat regions keep their value.", "مجموع أوزان النواة المُطبَّعة 1، فتحتفظ المناطق المستوية بقيمتها."),
            ("`np.unravel_index(np.argmax(a), a.shape)` turns a flat index into (row, column).", "يحوّل `np.unravel_index(np.argmax(a), a.shape)` الفهرس المسطّح إلى (row, column)."),
            ("Subtracting means and dividing by norms makes NCC immune to brightness and contrast changes.", "طرح المتوسطات والقسمة على المعايير يجعل NCC محصنًا ضد تغيّرات السطوع والتباين."),
        ),
        success=("Correct! Raw correlation was fooled by the bright side of the image; NCC found the cross exactly, even after a brightness change. Correlation (not convolution) compares the template without flipping it.",
                 "صحيح! خُدع الارتباط الخام بالجهة الساطعة من الصورة، بينما وجد NCC الصليب بدقة حتى بعد تغيير السطوع. والارتباط (لا الالتفاف) يقارن القالب دون قلبه."),
        expected=NUMPY_NOTE,
    ),
    "COURSE-014.M05.L01.EX02": Guided(
        goal=("Show that spatial and FFT convolution agree, and work through what a Conv2d layer does with three input channels and upsampling.",
              "بيّن أن الالتفاف المكاني والالتفاف عبر FFT متطابقان، وتتبّع ما تفعله طبقة Conv2d بثلاث قنوات إدخال وبالتكبير."),
        steps=(
            ("Blur with direct spatial convolution.", "موّه بالالتفاف المكاني المباشر."),
            ("Blur with FFT convolution.", "موّه بالالتفاف عبر FFT."),
            ("Measure the largest difference.", "قِس أكبر فرق."),
            ("Sum the per-channel correlations like one Conv2d output channel.", "اجمع الارتباطات لكل قناة كما تفعل قناة إخراج واحدة في Conv2d."),
            ("Upsample 2× by repeating pixels.", "كبّر مرتين بتكرار البكسلات."),
        ),
        starter='''import numpy as np
from scipy.signal import convolve2d, correlate2d, fftconvolve

rng = np.random.default_rng(0)
img = rng.random((64, 64))
ax = np.arange(-3, 4)
gauss_1d = np.exp(-ax ** 2 / (2 * 1.5 ** 2))
kernel = np.outer(gauss_1d, gauss_1d) / np.outer(gauss_1d, gauss_1d).sum()   # 7x7 Gaussian

# Step 1: direct convolution (zero padding, same size)
direct = ___
# Step 2: the same via the FFT (faster for large kernels)
via_fft = ___
# Step 3: how far apart are they?
max_difference = ___

# A Conv2d with 3 input channels has one 3x3 slice per input channel for EACH output channel
rgb = rng.random((3, 32, 32))                                  # C, H, W
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
weights = np.stack([sobel_x, sobel_x, sobel_x])                # (in_channels, k, k)
# Step 4: PyTorch's Conv2d correlates each channel with its slice and SUMS them
out_channel = ___

# Step 5: fixed 2x nearest-neighbour upsampling (nn.Upsample(scale_factor=2))
upsampled = ___
print(round(max_difference, 12), out_channel.shape, upsampled.shape)
''',
        answers=(
            'convolve2d(img, kernel, mode="same", boundary="fill")',
            'fftconvolve(img, kernel, mode="same")',
            "float(np.max(np.abs(direct - via_fft)))",
            'sum(correlate2d(rgb[c], weights[c], mode="valid") for c in range(3))',
            "np.repeat(np.repeat(img, 2, axis=0), 2, axis=1)",
        ),
        checks=(
            check("list(direct.shape) == [64, 64] and bool(np.allclose(direct, convolve2d(img, kernel, mode='same')))", True,
                  "Blank 1: `convolve2d(img, kernel, mode=\"same\", boundary=\"fill\")`.", "الفراغ 1: `convolve2d(img, kernel, mode=\"same\", boundary=\"fill\")`."),
            check("list(via_fft.shape) == [64, 64]", True, "Blank 2: `fftconvolve(img, kernel, mode=\"same\")`.", "الفراغ 2: `fftconvolve(img, kernel, mode=\"same\")`."),
            check("max_difference < 1e-10 and max_difference == float(np.max(np.abs(direct - via_fft)))", True,
                  "Blank 3: the maximum absolute difference between the two outputs.", "الفراغ 3: أكبر فرق مطلق بين المخرجين."),
            check("list(out_channel.shape) == [30, 30] and bool(np.allclose(out_channel, sum(correlate2d(rgb[c], sobel_x, mode='valid') for c in range(3))))", True,
                  "Blank 4: sum `correlate2d(rgb[c], weights[c], mode=\"valid\")` over the three channels.",
                  "الفراغ 4: اجمع `correlate2d(rgb[c], weights[c], mode=\"valid\")` على القنوات الثلاث."),
            check("list(upsampled.shape) == [128, 128] and bool(np.array_equal(upsampled[::2, ::2], img))", True,
                  "Blank 5: repeat every row and every column twice.", "الفراغ 5: كرّر كل صف وكل عمود مرتين."),
        ),
        hints=(
            ("Same `mode=\"same\"` and zero padding make both methods comparable.", "يجعل `mode=\"same\"` والحشو بالأصفار الطريقتين قابلتين للمقارنة."),
            ("Deep-learning 'convolution' is mathematically correlation.", "«الالتفاف» في التعلّم العميق هو رياضيًا ارتباط."),
            ("`np.repeat(x, 2, axis=...)` duplicates entries along one axis.", "يضاعف `np.repeat(x, 2, axis=...)` العناصر على محور واحد."),
        ),
        success=("Correct! Spatial and FFT convolution match to floating-point precision; a Conv2d output channel is the sum of per-channel correlations, which is why RGB input needs no special handling.",
                 "صحيح! يتطابق الالتفاف المكاني والالتفاف عبر FFT بدقة الأعداد العشرية؛ وقناة إخراج Conv2d هي مجموع الارتباطات لكل قناة، ولهذا لا يحتاج مدخل RGB إلى معالجة خاصة."),
        expected=NUMPY_NOTE,
        reflect=("Time both convolutions locally with a 31×31 kernel. Which wins, and why does kernel size matter?",
                 "احسب زمن الالتفافين محليًا بنواة 31×31. أيهما يفوز؟ ولماذا يهم حجم النواة؟"),
    ),
    "COURSE-014.M06.L01.EX01": Guided(
        goal=("Design Gaussian low- and high-pass filters in the frequency domain, then remove periodic noise with a symmetric notch.",
              "صمّم مرشحات غاوسية منخفضة ومرتفعة التمرير في مجال التردد، ثم أزل الضجيج الدوري بمرشح نوتش متماثل."),
        steps=(
            ("Write the Gaussian low-pass transfer function.", "اكتب دالة النقل للمرشح الغاوسي منخفض التمرير."),
            ("Apply a mask in the centred spectrum and transform back.", "طبّق قناعًا في الطيف المتمركز وأعد التحويل."),
            ("Build a notch mask at ±16 cycles, symmetric about the centre.", "ابنِ قناع نوتش عند ±16 دورة، متماثلًا حول المركز."),
            ("Measure the error before and after notch filtering.", "قِس الخطأ قبل الترشيح وبعده."),
        ),
        starter='''import numpy as np

h, w = 128, 128
yy, xx = np.mgrid[0:h, 0:w]
img = 0.5 + 0.3 * ((xx // 16 + yy // 16) % 2)                 # a checkerboard
cy, cx = h // 2, w // 2
D = np.hypot(yy - cy, xx - cx)                                  # distance from the spectrum centre

# Step 1: H(u, v) = exp(-D^2 / (2 * cutoff^2))
def gaussian_lpf(cutoff):
    return ___

# Step 2: multiply the CENTRED spectrum by the mask, un-centre, invert, keep the real part
def apply(F_centred, mask):
    return ___

F = np.fft.fftshift(np.fft.fft2(img))
low = apply(F, gaussian_lpf(10))
high = apply(F, 1 - gaussian_lpf(10))

noisy = img + 0.4 * np.sin(2 * np.pi * 16 * xx / w)            # periodic stripe noise
F_noisy = np.fft.fftshift(np.fft.fft2(noisy))
# Step 3: zero two small discs at (cy, cx + 16) and (cy, cx - 16) - real images have symmetric spectra
notch = ___
restored = apply(F_noisy, notch)
# Step 4: mean squared error against the clean image
mse_noisy, mse_restored = ___
print(round(mse_noisy, 4), round(mse_restored, 4))
''',
        answers=(
            "np.exp(-(D ** 2) / (2 * cutoff ** 2))",
            "np.real(np.fft.ifft2(np.fft.ifftshift(F_centred * mask)))",
            "(np.hypot(yy - cy, xx - (cx + 16)) > 3) & (np.hypot(yy - cy, xx - (cx - 16)) > 3)",
            "float(np.mean((noisy - img) ** 2)), float(np.mean((restored - img) ** 2))",
        ),
        checks=(
            check("abs(float(gaussian_lpf(10)[cy, cx]) - 1.0) < 1e-12 and float(gaussian_lpf(10)[cy, cx + 30]) < 0.02", True,
                  "Blank 1: `np.exp(-(D ** 2) / (2 * cutoff ** 2))`.", "الفراغ 1: `np.exp(-(D ** 2) / (2 * cutoff ** 2))`."),
            check("bool(np.allclose(apply(F, np.ones((h, w))), img)) and float(low.std()) < float(img.std())", True,
                  "Blank 2: `np.real(np.fft.ifft2(np.fft.ifftshift(F_centred * mask)))`.", "الفراغ 2: `np.real(np.fft.ifft2(np.fft.ifftshift(F_centred * mask)))`."),
            check("bool(notch[cy, cx]) and not bool(notch[cy, cx + 16]) and not bool(notch[cy, cx - 16])", True,
                  "Blank 3: keep everything except two small discs at ±16 on the horizontal axis.", "الفراغ 3: احتفظ بكل شيء عدا قرصين صغيرين عند ±16 على المحور الأفقي."),
            check("mse_restored < mse_noisy / 10", True, "Blank 4: compare both images with `img` using the mean squared difference.",
                  "الفراغ 4: قارن الصورتين بـ `img` بمتوسط مربع الفرق."),
        ),
        hints=(
            ("D is already the distance from the centre.", "D هي المسافة من المركز بالفعل."),
            ("Undo `fftshift` with `ifftshift` before `ifft2`.", "ألغِ `fftshift` بـ `ifftshift` قبل `ifft2`."),
            ("A real-valued image's spectrum is symmetric, so interference appears as a mirrored pair.", "طيف الصورة ذات القيم الحقيقية متماثل، فيظهر التداخل زوجًا متناظرًا."),
        ),
        success=("Correct! The low-pass keeps smooth content, the high-pass keeps edges, and two tiny symmetric notches remove the stripe noise while leaving the rest of the spectrum intact.",
                 "صحيح! يحتفظ المرشح منخفض التمرير بالمحتوى الناعم، ويحتفظ المرشح مرتفع التمرير بالحواف، ويزيل نوتشان صغيران متماثلان ضجيج الخطوط مع ترك باقي الطيف سليمًا."),
        expected=NUMPY_NOTE,
        reflect=("Compare an abrupt ideal mask with the Gaussian one at the same cutoff. Where do ringing artifacts come from?",
                 "قارن قناعًا مثاليًا حادًا بالقناع الغاوسي عند العتبة نفسها. من أين تأتي آثار التموّج (ringing)؟"),
    ),
    "COURSE-014.M06.L01.EX02": Guided(
        goal=("Compare raw coordinates with Fourier-feature mappings for fitting a signal with fine detail, and find the frequency scale that generalises best.",
              "قارن الإحداثيات الخام بتحويلات خصائص فورييه في ملاءمة إشارة ذات تفاصيل دقيقة، وجد مقياس التردد الذي يعمّم أفضل."),
        steps=(
            ("Map coordinates to sin/cos Fourier features.", "حوّل الإحداثيات إلى خصائص فورييه sin/cos."),
            ("Write PSNR for signals in [-1.5, 1.5].", "اكتب PSNR لإشارات في [-1.5, 1.5]."),
            ("Fit the same model to every representation.", "درّب النموذج نفسه على كل تمثيل."),
            ("Pick the scale with the best test PSNR.", "اختر المقياس ذا أفضل PSNR في الاختبار."),
        ),
        starter='''import numpy as np
from sklearn.linear_model import Ridge

x = np.linspace(0, 1, 512)
y = np.sin(2 * np.pi * 3 * x) + 0.5 * np.sin(2 * np.pi * 40 * x)     # smooth trend + fine detail
train, test = np.arange(512) % 2 == 0, np.arange(512) % 2 == 1

# Step 1: [sin(2 pi x B), cos(2 pi x B)] for a vector of frequencies B
def fourier_features(x, B):
    return ___

# Step 2: peak-to-peak range is 3, so PSNR = 10 log10(3^2 / MSE)
def psnr(a, b):
    return ___

def evaluate(features):
    # Step 3: the same linear model for every representation
    model = ___
    return round(psnr(model.predict(features[train]), y[train]), 1), round(psnr(model.predict(features[test]), y[test]), 1)

results = {"raw": evaluate(x.reshape(-1, 1))}
rng = np.random.default_rng(0)
for scale in (1, 10, 30, 1000):
    results[scale] = evaluate(fourier_features(x, rng.normal(0, scale, 128)))
# Step 4: the representation with the highest TEST PSNR
best = ___
print(results, "->", best)
''',
        answers=(
            "np.concatenate([np.sin(2 * np.pi * np.outer(x, B)), np.cos(2 * np.pi * np.outer(x, B))], axis=1)",
            "float(10 * np.log10(9 / np.mean((a - b) ** 2)))",
            "Ridge(alpha=1e-3).fit(features[train], y[train])",
            "max(results, key=lambda name: results[name][1])",
        ),
        checks=(
            check("list(fourier_features(np.array([0.0, 0.25]), np.array([1.0])).round(6).tolist())", [[0.0, 1.0], [1.0, 0.0]],
                  "Blank 1: sin and cos of `2 * np.pi * np.outer(x, B)`, side by side.", "الفراغ 1: sin وcos لـ `2 * np.pi * np.outer(x, B)` جنبًا إلى جنب."),
            check("round(psnr(np.zeros(4), np.full(4, 0.3)), 4)", 20.0, "Blank 2: `10 * np.log10(9 / mse)`.", "الفراغ 2: `10 * np.log10(9 / mse)`."),
            check("results['raw'][1] < 15 and results[30][1] > 40 and results[1000][1] < results[1000][0]", True,
                  "Blank 3: fit `Ridge(alpha=1e-3)` on the training features and targets only.", "الفراغ 3: درّب `Ridge(alpha=1e-3)` على خصائص التدريب وأهدافه فقط."),
            check("best", 30,
                  "Blank 4: compare the second number (test PSNR) of each result.", "الفراغ 4: قارن الرقم الثاني (PSNR الاختبار) في كل نتيجة."),
        ),
        hints=(
            ("`np.outer(x, B)` gives one row per coordinate and one column per frequency.", "يعطي `np.outer(x, B)` صفًا لكل إحداثي وعمودًا لكل تردد."),
            ("PSNR grows as the error shrinks.", "يزداد PSNR كلما صغر الخطأ."),
            ("Fit on `features[train]` and `y[train]`; evaluate on both splits.", "درّب على `features[train]` و`y[train]`، وقيّم على القسمين."),
        ),
        success=("Correct! Raw coordinates cannot express the fine detail at all; a moderate Fourier scale captures it, while very high scales fit training points but generalise worse - the same overfitting pattern as a coordinate MLP.",
                 "صحيح! لا تستطيع الإحداثيات الخام التعبير عن التفاصيل الدقيقة إطلاقًا؛ ويلتقطها مقياس فورييه متوسط، بينما تلائم المقاييس العالية جدًا نقاط التدريب لكنها تعمّم أسوأ - وهو نمط فرط الملاءمة نفسه في MLP الإحداثي."),
        expected=(
            "A linear model on the features keeps the experiment fast in the sandbox; the lesson's coordinate MLP shows the same effect on 2-D images.",
            "يُبقي نموذج خطي على الخصائص التجربة سريعة داخل بيئة التدريب؛ ويُظهر MLP الإحداثي في الدرس الأثر نفسه على الصور ثنائية الأبعاد.",
        ),
        reflect=("Why is this experiment different from applying an FFT filter to the image?", "لماذا تختلف هذه التجربة عن تطبيق مرشح FFT على الصورة؟"),
    ),
    "COURSE-014.M07.L01.EX01": Guided(
        goal=("Brighten a dark image, equalize its histogram, and choose the right denoiser for Gaussian versus salt-and-pepper noise using PSNR.",
              "فتّح صورة داكنة، وسوِّ مدرجها التكراري، واختر مزيل الضجيج المناسب للضجيج الغاوسي مقابل ضجيج الملح والفلفل باستخدام PSNR."),
        steps=(
            ("Apply gamma 0.5 to brighten the dark image.", "طبّق جاما 0.5 لتفتيح الصورة الداكنة."),
            ("Equalize the histogram with its cumulative distribution.", "سوِّ المدرج التكراري باستخدام توزيعه التراكمي."),
            ("Median-filter the salt-and-pepper image.", "طبّق مرشح الوسيط على صورة الملح والفلفل."),
            ("Write PSNR for images in [0, 1].", "اكتب PSNR لصور في [0, 1]."),
        ),
        starter='''import numpy as np
from scipy import ndimage

rng = np.random.default_rng(0)
yy, xx = np.mgrid[0:96, 0:96]
clean = 0.15 + 0.2 * (((xx // 12) + (yy // 12)) % 2) + 0.1 * xx / 96     # a dark, low-contrast pattern

# Step 1: gamma < 1 lifts dark tones
gamma_img = ___
# Step 2: map each value through the cumulative histogram
hist, edges = np.histogram(clean, bins=256, range=(0, 1))
cdf = hist.cumsum() / hist.sum()
equalized = ___

gaussian_noisy = np.clip(clean + rng.normal(0, 0.05, clean.shape), 0, 1)
sp_noisy = clean.copy()
noise = rng.random(clean.shape)
sp_noisy[noise < 0.05], sp_noisy[noise > 0.95] = 0.0, 1.0

# Step 3: a median ignores isolated extreme pixels
median_on_sp = ___
gauss_on_sp = ndimage.gaussian_filter(sp_noisy, 1)
gauss_on_gaussian = ndimage.gaussian_filter(gaussian_noisy, 1)
median_on_gaussian = ndimage.median_filter(gaussian_noisy, size=3)

# Step 4: PSNR = 10 log10(1 / MSE) for values in [0, 1]
def psnr(reference, test):
    return ___

results = {name: round(psnr(clean, img), 1) for name, img in (
    ("noisy s&p", sp_noisy), ("gaussian filter on s&p", gauss_on_sp), ("median on s&p", median_on_sp),
    ("noisy gaussian", gaussian_noisy), ("gaussian filter on gaussian", gauss_on_gaussian), ("median on gaussian", median_on_gaussian))}
print(round(float(clean.mean()), 3), round(float(gamma_img.mean()), 3), round(float(equalized.std()), 3))
print(results)
''',
        answers=("clean ** 0.5", "np.interp(clean.ravel(), edges[:-1], cdf).reshape(clean.shape)",
                 "ndimage.median_filter(sp_noisy, size=3)", "float(10 * np.log10(1.0 / np.mean((reference - test) ** 2)))"),
        checks=(
            check("bool(np.allclose(gamma_img, clean ** 0.5)) and float(gamma_img.mean()) > float(clean.mean())", True,
                  "Blank 1: `clean ** 0.5`.", "الفراغ 1: `clean ** 0.5`."),
            check("list(equalized.shape) == [96, 96] and float(equalized.std()) > 2 * float(clean.std())", True,
                  "Blank 2: `np.interp(clean.ravel(), edges[:-1], cdf).reshape(clean.shape)` spreads the values over [0, 1].",
                  "الفراغ 2: ينشر `np.interp(clean.ravel(), edges[:-1], cdf).reshape(clean.shape)` القيم على [0, 1]."),
            check("bool(np.allclose(median_on_sp, ndimage.median_filter(sp_noisy, size=3)))", True,
                  "Blank 3: `ndimage.median_filter(sp_noisy, size=3)`.", "الفراغ 3: `ndimage.median_filter(sp_noisy, size=3)`."),
            check("round(psnr(np.zeros(4), np.full(4, 0.1)), 4) == 20.0 and results['median on s&p'] > results['gaussian filter on s&p'] > results['noisy s&p']", True,
                  "Blank 4: `10 * np.log10(1.0 / mse)`.", "الفراغ 4: `10 * np.log10(1.0 / mse)`."),
        ),
        hints=(
            ("Values in [0, 1] raised to a power below 1 get larger.", "القيم في [0, 1] المرفوعة إلى قوة أقل من 1 تكبر."),
            ("Histogram equalization replaces each value by its cumulative frequency.", "تستبدل تسوية المدرج كل قيمة بتكرارها التراكمي."),
            ("A higher PSNR means closer to the clean reference.", "يعني PSNR الأعلى قربًا أكبر من المرجع النظيف."),
        ),
        success=("Correct! The median filter wins clearly on salt-and-pepper noise because it discards isolated extremes, while Gaussian smoothing suits Gaussian noise - and stronger filtering always risks erasing real detail.",
                 "صحيح! يفوز مرشح الوسيط بوضوح على ضجيج الملح والفلفل لأنه يتجاهل القيم المتطرفة المعزولة، بينما يناسب التنعيم الغاوسي الضجيج الغاوسي - والترشيح الأقوى يخاطر دائمًا بمحو تفاصيل حقيقية."),
        expected=NUMPY_NOTE,
        reflect=("Locally, compare adaptive histogram equalization (CLAHE) with global equalization. When does the adaptive version help?",
                 "محليًا، قارن التسوية التكيفية للمدرج (CLAHE) بالتسوية العامة. متى تساعد النسخة التكيفية؟"),
    ),
    "COURSE-014.M07.L01.EX02": Guided(
        goal=("Write the processing module behind an enhancement demo - gamma, gray-world white balance, median denoising and detail fusion - separate from any UI.",
              "اكتب وحدة المعالجة خلف عرض تحسين الصور - جاما، وموازنة اللون الأبيض بطريقة العالم الرمادي، وإزالة الضجيج بالوسيط، ودمج التفاصيل - بمعزل عن أي واجهة."),
        steps=(
            ("Implement gamma adjustment.", "نفّذ ضبط جاما."),
            ("Implement gray-world white balance.", "نفّذ موازنة اللون الأبيض بطريقة العالم الرمادي."),
            ("Median-filter each colour channel separately.", "طبّق مرشح الوسيط على كل قناة لونية بشكل منفصل."),
            ("Fuse two images by keeping the stronger detail at each pixel.", "ادمج صورتين بالاحتفاظ بالتفصيل الأقوى في كل بكسل."),
        ),
        starter='''import numpy as np
from scipy import ndimage

# ---- processing.py: no UI code here; a Streamlit app only calls enhance(...) ----
def adjust_gamma(img, gamma=0.7):
    # Step 1
    return ___

def gray_world(img):
    means = img.reshape(-1, 3).mean(axis=0)
    # Step 2: scale each channel so all three averages become the overall average
    return ___

def median_denoise(img, size=3):
    # Step 3: filter within each channel, never across channels
    return ___

METHODS = {"gamma": adjust_gamma, "white balance": gray_world, "median": median_denoise}

def enhance(img, method, **params):
    return METHODS[method](img, **params)

def fuse_detail(a, b):
    detail_a, detail_b = a - ndimage.gaussian_filter(a, 2), b - ndimage.gaussian_filter(b, 2)
    # Step 4: per pixel, keep the image whose detail is stronger (max-abs fusion)
    return ___

rng = np.random.default_rng(1)
photo = np.clip(rng.random((40, 60, 3)) * [0.9, 0.7, 0.5], 0, 1)      # a warm colour cast
balanced = enhance(photo, "white balance")
print(photo.reshape(-1, 3).mean(axis=0).round(3), balanced.reshape(-1, 3).mean(axis=0).round(3))
''',
        answers=(
            "np.clip(img, 0, 1) ** gamma",
            "np.clip(img * (means.mean() / means), 0, 1)",
            "ndimage.median_filter(img, size=(size, size, 1))",
            "np.where(np.abs(detail_a) >= np.abs(detail_b), a, b)",
        ),
        checks=(
            check("bool(np.allclose(enhance(np.full((2, 2, 3), 0.25), 'gamma', gamma=0.5), 0.5))", True,
                  "Blank 1: `np.clip(img, 0, 1) ** gamma`.", "الفراغ 1: `np.clip(img, 0, 1) ** gamma`."),
            check("float(np.ptp(balanced.reshape(-1, 3).mean(axis=0))) < 0.03 < float(np.ptp(photo.reshape(-1, 3).mean(axis=0)))", True,
                  "Blank 2: multiply by `means.mean() / means` so the channel averages match.", "الفراغ 2: اضرب في `means.mean() / means` كي تتطابق متوسطات القنوات."),
            check("bool(np.allclose(median_denoise(photo), ndimage.median_filter(photo, size=(3, 3, 1))))", True,
                  "Blank 3: `ndimage.median_filter(img, size=(size, size, 1))` - size 1 on the channel axis.",
                  "الفراغ 3: `ndimage.median_filter(img, size=(size, size, 1))` - الحجم 1 على محور القنوات."),
            check("(lambda a, b: bool(np.allclose(fuse_detail(a, b)[:, :20], a[:, :20])) and bool(np.allclose(fuse_detail(a, b)[:, -20:], b[:, -20:])))(np.hstack([rng.random((30, 30)), np.full((30, 30), 0.5)]), np.hstack([np.full((30, 30), 0.5), rng.random((30, 30))]))", True,
                  "Blank 4: `np.where(np.abs(detail_a) >= np.abs(detail_b), a, b)`.", "الفراغ 4: `np.where(np.abs(detail_a) >= np.abs(detail_b), a, b)`."),
        ),
        hints=(
            ("Clip before raising to a power so values stay valid.", "اقصص قبل الرفع إلى قوة كي تبقى القيم صالحة."),
            ("Gray world assumes the scene averages to neutral gray.", "يفترض العالم الرمادي أن متوسط المشهد رمادي محايد."),
            ("A `size` tuple sets the window per axis.", "يحدد الصفّ `size` النافذة لكل محور."),
        ),
        success=("Correct! Each method is a pure function the UI can call, so the Streamlit layer only handles upload, a selector, a slider and side-by-side display.",
                 "صحيح! كل طريقة دالة نقية تستطيع الواجهة استدعاءها، فلا تتعامل طبقة Streamlit إلا مع الرفع والمحدِّد وشريط التمرير والعرض جنبًا إلى جنب."),
        expected=NUMPY_NOTE,
        reflect=("Sketch the Streamlit UI that calls `enhance`, and document how you would run one advanced method (Zero-DCE, MAXIM, Dark Channel Prior or EDSR).",
                 "ارسم واجهة Streamlit التي تستدعي `enhance`، ووثّق كيف ستشغّل طريقة متقدمة واحدة (Zero-DCE أو MAXIM أو Dark Channel Prior أو EDSR)."),
    ),
    "COURSE-014.M08.L01.EX01": Guided(
        goal=("Compare first- and second-derivative edge detectors on clean and noisy images, and use Laplacian variance as a sharpness score.",
              "قارن كاشفات الحواف بالمشتقة الأولى والثانية على صور نظيفة ومشوّشة، واستخدم تباين اللابلاسيان مقياسًا للحدة."),
        steps=(
            ("Combine the Sobel derivatives into a gradient magnitude.", "اجمع مشتقات Sobel في مقدار التدرّج."),
            ("Compare how much noise inflates each detector's response.", "قارن مقدار تضخيم الضجيج لاستجابة كل كاشف."),
            ("Smooth before the Laplacian (LoG).", "نعّم قبل اللابلاسيان (LoG)."),
            ("Score sharpness with the Laplacian's variance.", "قيّم الحدة بتباين اللابلاسيان."),
        ),
        starter='''import numpy as np
from scipy import ndimage

rng = np.random.default_rng(0)
clean = np.zeros((80, 80))
clean[20:60, 20:60] = 1.0                                 # a square with strong edges
noisy = clean + rng.normal(0, 0.1, clean.shape)

def gradient_magnitude(img):
    gx, gy = ndimage.sobel(img, axis=1), ndimage.sobel(img, axis=0)     # cv2.Sobel
    # Step 1
    return ___

# Step 2: how much stronger is the average response on the noisy image? (first vs second derivative)
sobel_noise_ratio = gradient_magnitude(noisy).mean() / gradient_magnitude(clean).mean()
laplacian_noise_ratio = ___
# Step 3: Laplacian of Gaussian - smooth with sigma 2 first
log_noisy = ___

# Step 4: a sharper image has a wider spread of Laplacian values
def sharpness(img):
    return ___

scores = [round(sharpness(clean), 4), round(sharpness(ndimage.gaussian_filter(clean, 1)), 4), round(sharpness(ndimage.gaussian_filter(clean, 3)), 4)]
print(round(float(sobel_noise_ratio), 2), round(float(laplacian_noise_ratio), 2), scores)
''',
        answers=("np.hypot(gx, gy)", "np.abs(ndimage.laplace(noisy)).mean() / np.abs(ndimage.laplace(clean)).mean()",
                 "ndimage.gaussian_laplace(noisy, sigma=2)", "float(ndimage.laplace(img).var())"),
        checks=(
            check("bool(np.allclose(gradient_magnitude(clean), np.sqrt(ndimage.sobel(clean, axis=1) ** 2 + ndimage.sobel(clean, axis=0) ** 2)))", True,
                  "Blank 1: `np.hypot(gx, gy)`.", "الفراغ 1: `np.hypot(gx, gy)`."),
            check("float(laplacian_noise_ratio) > float(sobel_noise_ratio) > 1", True,
                  "Blank 2: the mean absolute Laplacian on `noisy` divided by the one on `clean`.", "الفراغ 2: متوسط القيمة المطلقة للابلاسيان على `noisy` مقسومًا على مثيله على `clean`."),
            check("bool(np.allclose(log_noisy, ndimage.gaussian_laplace(noisy, sigma=2))) and float(np.abs(log_noisy).mean()) < float(np.abs(ndimage.laplace(noisy)).mean())", True,
                  "Blank 3: `ndimage.gaussian_laplace(noisy, sigma=2)`.", "الفراغ 3: `ndimage.gaussian_laplace(noisy, sigma=2)`."),
            check("scores[0] > scores[1] > scores[2]", True, "Blank 4: `float(ndimage.laplace(img).var())`.", "الفراغ 4: `float(ndimage.laplace(img).var())`."),
        ),
        hints=(
            ("Gradient magnitude is sqrt(gx² + gy²).", "مقدار التدرّج هو sqrt(gx² + gy²)."),
            ("Second derivatives amplify noise more than first derivatives.", "تضخّم المشتقات الثانية الضجيج أكثر من المشتقات الأولى."),
            ("Blur lowers the Laplacian's variance, which is why it measures focus.", "يخفض التمويه تباين اللابلاسيان، ولهذا يقيس التركيز."),
        ),
        success=("Correct! The Laplacian reacts to noise far more than Sobel, smoothing first (LoG) tames it, and the Laplacian variance falls as blur increases - a simple focus measure.",
                 "صحيح! يتفاعل اللابلاسيان مع الضجيج أكثر بكثير من Sobel، ويروّضه التنعيم المسبق (LoG)، وينخفض تباين اللابلاسيان مع ازدياد التمويه - وهو مقياس بسيط للتركيز."),
        expected=NUMPY_NOTE,
        reflect=("Locally, run Canny with two threshold pairs. How do the thresholds change edge thickness, missing edges and false edges?",
                 "محليًا، شغّل Canny بزوجين من العتبات. كيف تغيّر العتبات سماكة الحواف والحواف المفقودة والحواف الزائفة؟"),
    ),
    "COURSE-014.M08.L01.EX02": Guided(
        goal=("Analyse an image across scales: find which LoG scale suits each blob, then build and invert a Laplacian pyramid.",
              "حلّل صورة عبر المقاييس: جد مقياس LoG الأنسب لكل نقطة (blob)، ثم ابنِ هرم لابلاسيان واعكسه."),
        steps=(
            ("Compute scale-normalized LoG responses.", "احسب استجابات LoG المُطبَّعة بالمقياس."),
            ("Downsample: blur, then keep every second pixel.", "صغّر: موّه ثم احتفظ ببكسل من كل اثنين."),
            ("Build each Laplacian level as a difference.", "ابنِ كل مستوى لابلاسيان بوصفه فرقًا."),
            ("Reconstruct the image from the pyramid.", "أعد بناء الصورة من الهرم."),
        ),
        starter='''import numpy as np
from scipy import ndimage

yy, xx = np.mgrid[0:128, 0:128]
img = np.zeros((128, 128))
img[(yy - 32) ** 2 + (xx - 32) ** 2 < 4 ** 2] = 1.0     # small blob
img[(yy - 80) ** 2 + (xx - 80) ** 2 < 16 ** 2] = 1.0    # large blob

# Step 1: -sigma^2 * LoG makes responses comparable across scales
responses = {sigma: ___ for sigma in (2, 4, 8, 12)}
best_small = max(responses, key=lambda s: responses[s][32, 32])
best_large = max(responses, key=lambda s: responses[s][80, 80])

# Step 2: one Gaussian pyramid step
def downsample(x):
    return ___

def upsample(x, shape):
    return ndimage.zoom(x, 2, order=1)[:shape[0], :shape[1]]

gaussian_pyramid = [img]
for _ in range(3):
    gaussian_pyramid.append(downsample(gaussian_pyramid[-1]))
# Step 3: detail lost between consecutive levels, plus the coarsest level at the end
laplacian_pyramid = [___ for fine, coarse in zip(gaussian_pyramid[:-1], gaussian_pyramid[1:])] + [gaussian_pyramid[-1]]

reconstructed = laplacian_pyramid[-1]
for detail in reversed(laplacian_pyramid[:-1]):
    # Step 4: upsample the coarse image and add back the detail
    reconstructed = ___
print(best_small, best_large, [level.shape for level in gaussian_pyramid], bool(np.allclose(reconstructed, img)))
''',
        answers=("-sigma ** 2 * ndimage.gaussian_laplace(img, sigma)", "ndimage.gaussian_filter(x, 1)[::2, ::2]",
                 "fine - upsample(coarse, fine.shape)", "detail + upsample(reconstructed, detail.shape)"),
        checks=(
            check("best_small < best_large and best_small in (2, 4) and best_large in (8, 12)", True,
                  "Blank 1: `-sigma ** 2 * ndimage.gaussian_laplace(img, sigma)` - small blobs peak at small sigma.",
                  "الفراغ 1: `-sigma ** 2 * ndimage.gaussian_laplace(img, sigma)` - تبلغ النقاط الصغيرة ذروتها عند sigma صغيرة."),
            check("[list(g.shape) for g in gaussian_pyramid]", [[128, 128], [64, 64], [32, 32], [16, 16]],
                  "Blank 2: blur with `ndimage.gaussian_filter(x, 1)` and slice `[::2, ::2]`.", "الفراغ 2: موّه بـ `ndimage.gaussian_filter(x, 1)` واقطع `[::2, ::2]`."),
            check("len(laplacian_pyramid) == 4 and bool(np.allclose(laplacian_pyramid[0], gaussian_pyramid[0] - upsample(gaussian_pyramid[1], (128, 128))))", True,
                  "Blank 3: `fine - upsample(coarse, fine.shape)`.", "الفراغ 3: `fine - upsample(coarse, fine.shape)`."),
            check("bool(np.allclose(reconstructed, img))", True, "Blank 4: `detail + upsample(reconstructed, detail.shape)` - exact reconstruction.",
                  "الفراغ 4: `detail + upsample(reconstructed, detail.shape)` - إعادة بناء دقيقة."),
        ),
        hints=(
            ("A blob of radius r responds most at sigma ≈ r/√2.", "تستجيب نقطة نصف قطرها r أقصى استجابة عند sigma ≈ r/√2."),
            ("Each Laplacian level stores what upsampling the coarser level cannot recover.", "يخزّن كل مستوى لابلاسيان ما لا يستطيع تكبير المستوى الأخشن استعادته."),
            ("Reconstruction runs the construction in reverse.", "تعمل إعادة البناء بعكس خطوات البناء."),
        ),
        success=("Correct! Each blob is detected at its own scale, and the Laplacian pyramid splits the image into detail bands that add back up exactly - boost one band to sharpen just that scale.",
                 "صحيح! تُكتشف كل نقطة عند مقياسها الخاص، ويقسم هرم لابلاسيان الصورة إلى نطاقات تفاصيل تُجمع مرة أخرى بدقة - عزّز نطاقًا واحدًا لتشحذ ذلك المقياس وحده."),
        expected=NUMPY_NOTE,
        reflect=("Make a decision table: which detector would you choose for noisy edges, thin ridges, blobs of unknown size and semantic object outlines?",
                 "أنشئ جدول قرار: أي كاشف ستختار للحواف المشوّشة، والخطوط الرفيعة، والنقاط مجهولة الحجم، وحدود الأجسام الدلالية؟"),
    ),
    "COURSE-014.M09.L01.EX01": Guided(
        goal=("Restore a blurred image with inverse, Wiener and Tikhonov filters, and see why the inverse filter collapses once noise is added.",
              "استعد صورة مموّهة بمرشحات العكس وWiener وTikhonov، وافهم لماذا ينهار مرشح العكس بمجرد إضافة الضجيج."),
        steps=(
            ("Apply the inverse filter in the frequency domain.", "طبّق مرشح العكس في مجال التردد."),
            ("Apply the Wiener filter with a noise-to-signal constant K.", "طبّق مرشح Wiener مع ثابت نسبة الضجيج إلى الإشارة K."),
            ("Apply Tikhonov regularization with a Laplacian penalty.", "طبّق تنظيم Tikhonov مع عقوبة لابلاسيان."),
            ("Pick the best lambda by MSE.", "اختر أفضل lambda حسب MSE."),
        ),
        starter='''import numpy as np

rng = np.random.default_rng(0)
yy, xx = np.mgrid[0:64, 0:64]
clean = 0.5 + 0.4 * np.sin(xx / 4) * np.cos(yy / 6)

ax = np.arange(64) - 32
psf_1d = np.exp(-ax ** 2 / (2 * 1.2 ** 2))
psf = np.fft.ifftshift(np.outer(psf_1d, psf_1d) / np.outer(psf_1d, psf_1d).sum())   # centred at (0, 0)
H = np.fft.fft2(psf)
blurred = np.real(np.fft.ifft2(np.fft.fft2(clean) * H))
noisy = blurred + rng.normal(0, 0.01, clean.shape)

def restore(observed, filter_):
    return np.real(np.fft.ifft2(np.fft.fft2(observed) * filter_))

# Step 1: divide by the blur's transfer function
inverse_filter = ___
# Step 2: Wiener: conj(H) / (|H|^2 + K)
def wiener(K):
    return ___

laplacian = np.zeros((64, 64))
laplacian[0, 0], laplacian[0, 1], laplacian[1, 0], laplacian[0, -1], laplacian[-1, 0] = 4, -1, -1, -1, -1
L = np.fft.fft2(laplacian)
# Step 3: Tikhonov: conj(H) / (|H|^2 + lambda |L|^2)
def tikhonov(lam):
    return ___

def mse(img):
    return float(np.mean((img - clean) ** 2))

errors = {"inverse, no noise": mse(restore(blurred, inverse_filter)), "inverse, noisy": mse(restore(noisy, inverse_filter)),
          "wiener": mse(restore(noisy, wiener(1e-3)))}
tikhonov_errors = {lam: mse(restore(noisy, tikhonov(lam))) for lam in (1e-5, 1e-3, 1e-1)}
# Step 4: the lambda with the lowest error
best_lambda = ___
print({k: f"{v:.2e}" for k, v in errors.items()}, {k: f"{v:.2e}" for k, v in tikhonov_errors.items()}, best_lambda)
''',
        answers=("1 / H", "np.conj(H) / (np.abs(H) ** 2 + K)", "np.conj(H) / (np.abs(H) ** 2 + lam * np.abs(L) ** 2)",
                 "min(tikhonov_errors, key=tikhonov_errors.get)"),
        checks=(
            check("errors['inverse, no noise'] < 1e-8 and errors['inverse, noisy'] > 1.0", True,
                  "Blank 1: `1 / H` - exact without noise, explosive with it.", "الفراغ 1: `1 / H` - دقيق دون ضجيج، ومتفجر معه."),
            check("errors['wiener'] < 0.01 and bool(np.allclose(wiener(0.0) * H, 1))", True,
                  "Blank 2: `np.conj(H) / (np.abs(H) ** 2 + K)`.", "الفراغ 2: `np.conj(H) / (np.abs(H) ** 2 + K)`."),
            check("bool(np.allclose(tikhonov(0.0) * H, 1)) and tikhonov_errors[1e-3] < tikhonov_errors[1e-5]", True,
                  "Blank 3: `np.conj(H) / (np.abs(H) ** 2 + lam * np.abs(L) ** 2)`.", "الفراغ 3: `np.conj(H) / (np.abs(H) ** 2 + lam * np.abs(L) ** 2)`."),
            check("best_lambda == min(tikhonov_errors, key=tikhonov_errors.get) and best_lambda != 1e-5", True,
                  "Blank 4: `min(tikhonov_errors, key=tikhonov_errors.get)`.", "الفراغ 4: `min(tikhonov_errors, key=tikhonov_errors.get)`."),
        ),
        hints=(
            ("Blurring multiplies the spectrum by H, so undoing it divides by H.", "يضرب التمويه الطيف في H، لذا يقسم الإلغاء على H."),
            ("Where H is tiny, 1/H is huge - and so is any noise at those frequencies.", "حيث تكون H صغيرة جدًا تكون 1/H ضخمة - وكذلك أي ضجيج عند تلك الترددات."),
            ("K and lambda keep the denominator away from zero.", "يُبعد K وlambda المقام عن الصفر."),
        ),
        success=("Correct! The inverse filter is perfect on noise-free data but amplifies tiny noise enormously; Wiener and Tikhonov trade a little sharpness for stability, and lambda tunes that trade-off.",
                 "صحيح! مرشح العكس مثالي على البيانات الخالية من الضجيج لكنه يضخّم الضجيج الضئيل تضخيمًا هائلًا؛ ويقايض Wiener وTikhonov قليلًا من الحدة بالاستقرار، وتضبط lambda هذه المقايضة."),
        expected=NUMPY_NOTE,
        reflect=("Does your preferred method rely on a statistical estimate of the noise or on a smoothness prior?",
                 "هل تعتمد طريقتك المفضّلة على تقدير إحصائي للضجيج أم على افتراض مسبق بالنعومة؟"),
    ),
    "COURSE-014.M10.L01.EX01": Guided(
        goal=("Turn an image into counted objects: Otsu threshold, hole filling, small-region removal, distance transform and peak markers.",
              "حوّل صورة إلى أجسام معدودة: عتبة Otsu، وملء الثقوب، وإزالة المناطق الصغيرة، وتحويل المسافة، وعلامات القمم."),
        steps=(
            ("Complete Otsu's between-class variance.", "أكمل التباين بين الفئات في طريقة Otsu."),
            ("Fill holes inside the objects.", "املأ الثقوب داخل الأجسام."),
            ("Remove regions smaller than 30 pixels.", "احذف المناطق الأصغر من 30 بكسلًا."),
            ("Compute the Euclidean distance transform.", "احسب تحويل المسافة الإقليدية."),
        ),
        starter='''import numpy as np
from scipy import ndimage

rng = np.random.default_rng(0)
yy, xx = np.mgrid[0:100, 0:120]
img = np.full((100, 120), 0.2)
for cy, cx, r in ((30, 30, 14), (30, 55, 14), (70, 85, 16)):        # two touching discs + one separate
    img[(yy - cy) ** 2 + (xx - cx) ** 2 < r ** 2] = 0.8
img[68:73, 83:88] = 0.2                                              # a hole inside the large disc
img[85:88, 10:13] = 0.8                                              # a small speck of noise
img = img + rng.normal(0, 0.03, img.shape)

def otsu(values):
    best_t, best_var = 0.0, -1.0
    for t in np.linspace(values.min(), values.max(), 128)[1:-1]:
        below, above = values[values <= t], values[values > t]
        w0, w1 = below.size / values.size, above.size / values.size
        mu0, mu1 = below.mean(), above.mean()
        # Step 1: between-class variance
        between = ___
        if between > best_var:
            best_t, best_var = t, between
    return best_t

mask = img > otsu(img)
# Step 2
mask = ___
labels, n = ndimage.label(mask)
sizes = ndimage.sum(mask, labels, range(1, n + 1))
# Step 3: keep only labels whose size is at least 30 pixels (labels start at 1)
mask = ___
# Step 4: distance from each foreground pixel to the background
distance = ___
peaks = (distance == ndimage.maximum_filter(distance, size=9)) & (distance > 6)
markers, n_objects = ndimage.label(peaks)                            # seeds for watershed
print("regions before cleaning:", n, "| objects:", n_objects)
''',
        answers=("w0 * w1 * (mu0 - mu1) ** 2", "ndimage.binary_fill_holes(mask)", "np.isin(labels, np.flatnonzero(sizes >= 30) + 1)",
                 "ndimage.distance_transform_edt(mask)"),
        checks=(
            check("0.3 < float(otsu(img)) < 0.7", True, "Blank 1: `w0 * w1 * (mu0 - mu1) ** 2`.", "الفراغ 1: `w0 * w1 * (mu0 - mu1) ** 2`."),
            check("bool(mask[70, 85])", True, "Blank 2: `ndimage.binary_fill_holes(mask)` fills the hole in the large disc.",
                  "الفراغ 2: يملأ `ndimage.binary_fill_holes(mask)` الثقب في القرص الكبير."),
            check("not bool(mask[86, 11]) and int(ndimage.label(mask)[1]) == 2", True,
                  "Blank 3: keep labels with `sizes >= 30` - the speck disappears; the touching discs are still one region.",
                  "الفراغ 3: احتفظ بالتسميات التي `sizes >= 30` - تختفي البقعة الصغيرة، ويبقى القرصان المتلامسان منطقة واحدة."),
            check("n_objects == 3 and float(distance.max()) > 12", True,
                  "Blank 4: `ndimage.distance_transform_edt(mask)` - its peaks separate the touching discs into 3 objects.",
                  "الفراغ 4: `ndimage.distance_transform_edt(mask)` - تفصل قممه القرصين المتلامسين فتصبح الأجسام 3."),
        ),
        hints=(
            ("Otsu maximizes w0·w1·(μ0 − μ1)².", "يعظّم Otsu القيمة w0·w1·(μ0 − μ1)²."),
            ("`ndimage.label` numbers regions from 1, so add 1 to the 0-based indices.", "يرقّم `ndimage.label` المناطق بدءًا من 1، لذا أضف 1 إلى الفهارس التي تبدأ من 0."),
            ("The distance transform peaks at each object's centre.", "يبلغ تحويل المسافة ذروته في مركز كل جسم."),
        ),
        success=("Correct! Thresholding saw two regions, but the distance-transform peaks found three objects - exactly the markers watershed needs to split touching objects.",
                 "صحيح! رأى التحديد بالعتبة منطقتين، لكن قمم تحويل المسافة وجدت ثلاثة أجسام - وهي بالضبط العلامات التي يحتاجها watershed لفصل الأجسام المتلامسة."),
        expected=NUMPY_NOTE,
        reflect=("Locally, run `skimage.segmentation.watershed(-distance, markers, mask=mask)` and `regionprops`. What geometric rule would reject non-target regions?",
                 "محليًا، شغّل `skimage.segmentation.watershed(-distance, markers, mask=mask)` و`regionprops`. ما القاعدة الهندسية التي سترفض المناطق غير المستهدفة؟"),
    ),
    "COURSE-014.M11.L01.EX01": Guided(
        goal=("Turn a text-prompted probability map into masks at several thresholds, overlay one, and select an object with a point prompt.",
              "حوّل خريطة احتمالات ناتجة عن موجّه نصي إلى أقنعة عند عدة عتبات، واعرض أحدها فوق الصورة، واختر جسمًا بنقرة نقطية."),
        steps=(
            ("Threshold the probability map at 0.3, 0.5 and 0.7.", "طبّق العتبات 0.3 و0.5 و0.7 على خريطة الاحتمالات."),
            ("Tint the masked pixels red at 50%.", "لوّن البكسلات المقنّعة بالأحمر بنسبة 50%."),
            ("Keep the connected region under the clicked point.", "احتفظ بالمنطقة المتصلة تحت النقطة المنقورة."),
            ("Compute the bounding box of that region.", "احسب الصندوق المحيط بتلك المنطقة."),
        ),
        starter='''import numpy as np
from scipy import ndimage

yy, xx = np.mgrid[0:80, 0:120]
image = np.full((80, 120, 3), 200, dtype=np.uint8)
# Stand-in for CLIPSeg's sigmoid output for the prompt "a mug": two mug-like blobs
prob = 0.85 * np.exp(-((yy - 30) ** 2 + (xx - 35) ** 2) / (2 * 9 ** 2)) \\
     + 0.75 * np.exp(-((yy - 50) ** 2 + (xx - 90) ** 2) / (2 * 7 ** 2)) + 0.05

# Step 1: one mask per threshold - keep the raw probabilities for later
masks = {t: ___ for t in (0.3, 0.5, 0.7)}
areas = {t: int(m.sum()) for t, m in masks.items()}

overlay = image.copy()
# Step 2: blend the masked pixels halfway towards pure red
overlay[masks[0.5]] = ___

# Step 3: a SAM-style point prompt - keep only the region containing the click
labels, _ = ndimage.label(masks[0.5])
click = (30, 35)
selected = ___
# Step 4: (top, left, bottom, right) of the selected region, e.g. to crop it for a VLM
rows, cols = np.nonzero(selected)
box = ___
print(areas, int(selected.sum()), box)
''',
        answers=("prob >= t", "(0.5 * image[masks[0.5]] + 0.5 * np.array([255, 0, 0])).astype(np.uint8)",
                 "labels == labels[click]", "(int(rows.min()), int(cols.min()), int(rows.max()), int(cols.max()))"),
        checks=(
            check("areas[0.3] > areas[0.5] > areas[0.7] > 0", True, "Blank 1: `prob >= t` - higher thresholds keep less.",
                  "الفراغ 1: `prob >= t` - تحتفظ العتبات الأعلى بأقل."),
            check("overlay[30, 35].tolist() == [227, 100, 100] and overlay[0, 0].tolist() == [200, 200, 200]", True,
                  "Blank 2: `(0.5 * image[masks[0.5]] + 0.5 * np.array([255, 0, 0])).astype(np.uint8)`.",
                  "الفراغ 2: `(0.5 * image[masks[0.5]] + 0.5 * np.array([255, 0, 0])).astype(np.uint8)`."),
            check("bool(selected[30, 35]) and not bool(selected[50, 90]) and int(ndimage.label(selected)[1]) == 1", True,
                  "Blank 3: `labels == labels[click]` keeps only the clicked component.", "الفراغ 3: يحتفظ `labels == labels[click]` بالمكوّن المنقور فقط."),
            check("box[0] < 30 < box[2] and box[1] < 35 < box[3] and box[3] < 60", True,
                  "Blank 4: the min and max of `rows` and `cols`.", "الفراغ 4: أصغر وأكبر قيم `rows` و`cols`."),
        ),
        hints=(
            ("Comparing an array with a number gives a Boolean mask.", "مقارنة مصفوفة برقم تعطي قناعًا منطقيًا."),
            ("Boolean indexing selects the masked pixels as an (N, 3) array.", "تختار الفهرسة المنطقية البكسلات المقنّعة بوصفها مصفوفة (N, 3)."),
            ("Every connected region gets its own label number.", "تحصل كل منطقة متصلة على رقم تسمية خاص بها."),
        ),
        success=("Correct! The text prompt produced a soft map whose foreground grows or shrinks with the threshold; the point prompt then picked one object geometrically.",
                 "صحيح! أنتج الموجّه النصي خريطة ناعمة يكبر قسمها الأمامي أو يصغر مع العتبة، ثم اختار الموجّه النقطي جسمًا واحدًا هندسيًا."),
        expected=NUMPY_NOTE,
        reflect=("Explain the difference between geometric prompting (point/box) and semantic prompting (text), with one failure case of each.",
                 "اشرح الفرق بين التوجيه الهندسي (نقطة/صندوق) والتوجيه الدلالي (نص)، مع حالة فشل لكلٍّ منهما."),
    ),
    "COURSE-014.M11.L01.EX02": Guided(
        goal=("Implement the metrics and loss of a segmentation pipeline: IoU, Dice, pixel accuracy, a class-weighted loss and sliding-window tiling.",
              "نفّذ مقاييس خط التقسيم ودالة خسارته: IoU وDice ودقة البكسل وخسارة موزونة بالفئات وتقسيم النوافذ المنزلقة."),
        steps=(
            ("Compute IoU.", "احسب IoU."),
            ("Compute Dice.", "احسب Dice."),
            ("Compute pixel accuracy.", "احسب دقة البكسل."),
            ("Weight the positive class in binary cross-entropy.", "زِن الفئة الإيجابية في binary cross-entropy."),
            ("List the tile start positions that cover the image.", "اذكر مواضع بداية البلاطات التي تغطي الصورة."),
        ),
        starter='''import numpy as np

target = np.zeros((100, 100), dtype=bool)
target[40:60, 40:60] = True                     # a small lesion: 4% of the pixels
pred = np.zeros((100, 100), dtype=bool)
pred[45:65, 45:65] = True

# Step 1: overlap / union
def iou(pred, target):
    return ___

# Step 2: 2 * overlap / (|pred| + |target|)
def dice(pred, target):
    return ___

# Step 3: share of pixels labelled correctly - misleading under class imbalance
pixel_accuracy = ___

# Step 4: positives count pos_weight times more than negatives
def weighted_bce(prob, target, pos_weight):
    prob = np.clip(prob, 1e-7, 1 - 1e-7)
    return ___

# Step 5: tile starts so `tile`-sized windows with step `stride` cover the whole length
def tile_starts(size, tile, stride):
    starts = list(range(0, size - tile + 1, stride))
    if starts[-1] + tile < size:
        starts.append(___)
    return starts

all_background = np.zeros_like(target)
print(round(float(iou(pred, target)), 3), round(float(dice(pred, target)), 3), pixel_accuracy,
      "| all-background accuracy:", float((all_background == target).mean()), tile_starts(300, 128, 64))
''',
        answers=(
            "(pred & target).sum() / (pred | target).sum()",
            "2 * (pred & target).sum() / (pred.sum() + target.sum())",
            "float((pred == target).mean())",
            "float(-np.mean(pos_weight * target * np.log(prob) + (1 - target) * np.log(1 - prob)))",
            "size - tile",
        ),
        checks=(
            check("round(float(iou(pred, target)), 4)", 0.3913, "Blank 1: 225 / 575.", "الفراغ 1: 225 / 575."),
            check("round(float(dice(pred, target)), 4)", 0.5625, "Blank 2: 2 × 225 / 800.", "الفراغ 2: 2 × 225 / 800."),
            check("pixel_accuracy", 0.965, "Blank 3: `float((pred == target).mean())`.", "الفراغ 3: `float((pred == target).mean())`."),
            check("[round(weighted_bce(np.array([0.5, 0.5]), np.array([1, 0]), 1), 4), round(weighted_bce(np.array([0.5, 0.5]), np.array([1, 0]), 3), 4)]", [0.6931, 1.3863],
                  "Blank 4: `-np.mean(pos_weight * target * log(prob) + (1 - target) * log(1 - prob))`.", "الفراغ 4: `-np.mean(pos_weight * target * log(prob) + (1 - target) * log(1 - prob))`."),
            check("tile_starts(300, 128, 64)", [0, 64, 128, 172], "Blank 5: the last tile starts at `size - tile`.", "الفراغ 5: تبدأ البلاطة الأخيرة عند `size - tile`."),
        ),
        hints=(
            ("For Boolean masks, `&` is the overlap and `|` the union.", "في الأقنعة المنطقية `&` هو التداخل و`|` الاتحاد."),
            ("Dice and IoU always rank predictions the same way, but Dice is larger.", "يرتّب Dice وIoU التنبؤات دائمًا بالطريقة نفسها، لكن Dice أكبر."),
            ("The last window must end exactly at the image border.", "يجب أن تنتهي النافذة الأخيرة عند حافة الصورة بالضبط."),
        ),
        success=("Correct! Pixel accuracy says 96.5% - and predicting no lesion at all scores 96% - while IoU and Dice reveal the real overlap. That imbalance is why weighted or Dice-based losses exist.",
                 "صحيح! تقول دقة البكسل 96.5% - ويحقق التنبؤ بعدم وجود أي آفة 96% - بينما يكشف IoU وDice التداخل الحقيقي. وهذا الاختلال هو سبب وجود الخسائر الموزونة أو المعتمدة على Dice."),
        reflect=("Choose a domain and an architecture (U-Net, Swin-UNETR, MAnet). How must masks be resized differently from images, and why?",
                 "اختر مجالًا ومعمارية (U-Net أو Swin-UNETR أو MAnet). كيف يجب تغيير حجم الأقنعة بطريقة مختلفة عن الصور؟ ولماذا؟"),
    ),
    "COURSE-014.M12.L01.EX01": Guided(
        goal=("Classify images by cosine similarity to few-shot class prototypes, and keep only confident pseudo-labels for unlabeled data.",
              "صنّف الصور بتشابه جيب التمام مع نماذج أولية للفئات من أمثلة قليلة، واحتفظ فقط بالتسميات الزائفة الواثقة للبيانات غير المسمّاة."),
        steps=(
            ("Build one normalized prototype per class from its support embeddings.", "ابنِ نموذجًا أوليًا مُطبَّعًا لكل فئة من تضمينات أمثلتها الداعمة."),
            ("Classify a query by its most similar prototype.", "صنّف الاستعلام بأكثر نموذج أولي تشابهًا معه."),
            ("Keep predictions with confidence ≥ 0.9.", "احتفظ بالتنبؤات التي ثقتها ≥ 0.9."),
        ),
        starter='''import numpy as np

def normalize(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)

rng = np.random.default_rng(0)
centres = {"cat": np.array([1.0, 0.1, 0.0, 0.2]), "car": np.array([0.0, 1.0, 0.2, 0.1]), "tree": np.array([0.1, 0.0, 1.0, 0.3])}
# Stand-in for DINOv2 embeddings: 3 support images per class
support = {name: c + rng.normal(0, 0.1, (3, 4)) for name, c in centres.items()}

# Step 1: mean support embedding, normalized
prototypes = {name: ___ for name, vectors in support.items()}

def classify(embedding):
    sims = {name: float(normalize(embedding) @ p) for name, p in prototypes.items()}
    # Step 2: the most similar prototype
    return ___

queries = [centres["car"] + rng.normal(0, 0.1, 4), centres["tree"] + rng.normal(0, 0.1, 4)]

# Softmax outputs of a small classifier on 6 unlabeled images
probs = np.array([[0.95, 0.03, 0.02], [0.40, 0.35, 0.25], [0.05, 0.92, 0.03],
                  [0.30, 0.30, 0.40], [0.02, 0.01, 0.97], [0.60, 0.20, 0.20]])
# Step 3: only confident predictions become pseudo-labels
confident = ___
pseudo_labels = probs.argmax(axis=1)[confident]
print([classify(q) for q in queries], confident.tolist(), pseudo_labels.tolist())
''',
        answers=("normalize(vectors.mean(axis=0))", "max(sims, key=sims.get)", "probs.max(axis=1) >= 0.9"),
        checks=(
            check("all(abs(float(np.linalg.norm(p)) - 1.0) < 1e-9 for p in prototypes.values()) and bool(np.allclose(prototypes['cat'], normalize(support['cat'].mean(axis=0))))", True,
                  "Blank 1: `normalize(vectors.mean(axis=0))`.", "الفراغ 1: `normalize(vectors.mean(axis=0))`."),
            check("[classify(q) for q in queries] + [classify(centres['cat'])]", ["car", "tree", "cat"],
                  "Blank 2: `max(sims, key=sims.get)`.", "الفراغ 2: `max(sims, key=sims.get)`."),
            check("[confident.tolist(), pseudo_labels.tolist()]", [[True, False, True, False, True, False], [0, 1, 2]],
                  "Blank 3: `probs.max(axis=1) >= 0.9`.", "الفراغ 3: `probs.max(axis=1) >= 0.9`."),
        ),
        hints=(
            ("A prototype is the average of a class's examples.", "النموذج الأولي هو متوسط أمثلة الفئة."),
            ("With unit vectors, the dot product is the cosine similarity.", "مع المتجهات ذات الطول الواحد يكون الضرب النقطي هو تشابه جيب التمام."),
            ("Low-confidence pseudo-labels would teach the model its own mistakes.", "التسميات الزائفة منخفضة الثقة ستعلّم النموذج أخطاءه الخاصة."),
        ),
        success=("Correct! Three support images per class were enough to classify new queries, and only half of the unlabeled predictions were confident enough to reuse as training labels.",
                 "صحيح! كفت ثلاث صور داعمة لكل فئة لتصنيف استعلامات جديدة، ولم يكن واثقًا بما يكفي لإعادة استخدامه تسمياتٍ للتدريب إلا نصف التنبؤات غير المسمّاة."),
        expected=(
            "The embeddings are stand-ins with the shape and geometry of a pretrained encoder's output, so prototype classification runs in the sandbox.",
            "التضمينات بدائل لها أبعاد مخرجات مُرمِّز مدرَّب مسبقًا وهندستها، لذلك يعمل التصنيف بالنماذج الأولية داخل بيئة التدريب.",
        ),
        reflect=("Locally, compare t-SNE of raw pixels with t-SNE of deep features, and try a CLIP zero-shot prompt. Which representation separates the classes best?",
                 "محليًا، قارن t-SNE للبكسلات الخام بـ t-SNE للخصائص العميقة، وجرّب موجّهًا بأسلوب CLIP دون أمثلة. أي تمثيل يفصل الفئات أفضل؟"),
    ),
    "COURSE-014.M12.L01.EX02": Guided(
        goal=("Post-process detector output in a multi-stage pipeline: confidence threshold, box IoU, duplicate removal and an ROI crop.",
              "عالج مخرجات الكاشف في خط متعدد المراحل: عتبة الثقة، وIoU للصناديق، وإزالة التكرار، وقص منطقة الاهتمام."),
        steps=(
            ("Drop detections below the confidence threshold.", "احذف الاكتشافات الأقل من عتبة الثقة."),
            ("Compute the intersection area of two boxes.", "احسب مساحة تقاطع صندوقين."),
            ("Keep a box only if it does not overlap a kept box of the same label by IoU > 0.5.", "احتفظ بالصندوق فقط إن لم يتداخل مع صندوق محفوظ من التسمية نفسها بـ IoU > 0.5."),
            ("Crop the plate region for OCR.", "اقصص منطقة اللوحة لتمريرها إلى OCR."),
        ),
        starter='''import numpy as np

image = np.arange(120 * 160, dtype=np.uint32).reshape(120, 160)       # stand-in frame
# (x1, y1, x2, y2) boxes, as a detector such as YOLO returns them
detections = [
    {"label": "car", "score": 0.92, "box": (10, 20, 110, 80)},
    {"label": "car", "score": 0.88, "box": (12, 22, 108, 82)},        # duplicate of the first car
    {"label": "plate", "score": 0.81, "box": (40, 60, 80, 75)},
    {"label": "car", "score": 0.35, "box": (120, 10, 150, 40)},        # too uncertain
]
THRESHOLD = 0.5

# Step 1
confident = ___

def box_iou(a, b):
    ix1, iy1, ix2, iy2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    # Step 2: zero when the boxes do not overlap
    intersection = ___
    area = lambda r: (r[2] - r[0]) * (r[3] - r[1])
    return intersection / (area(a) + area(b) - intersection)

kept = []
for det in sorted(confident, key=lambda d: d["score"], reverse=True):
    # Step 3: non-maximum suppression within each label
    if ___:
        kept.append(det)

plate = next(d for d in kept if d["label"] == "plate")
x1, y1, x2, y2 = plate["box"]
# Step 4: images are indexed [rows (y), columns (x)]
plate_roi = ___
print([(d["label"], d["score"]) for d in kept], plate_roi.shape)
''',
        answers=(
            '[d for d in detections if d["score"] >= THRESHOLD]',
            "max(0, ix2 - ix1) * max(0, iy2 - iy1)",
            'all(box_iou(det["box"], k["box"]) <= 0.5 for k in kept if k["label"] == det["label"])',
            "image[y1:y2, x1:x2]",
        ),
        checks=(
            check("[d['score'] for d in confident]", [0.92, 0.88, 0.81], "Blank 1: keep detections with `score >= THRESHOLD`.",
                  "الفراغ 1: احتفظ بالاكتشافات التي `score >= THRESHOLD`."),
            check("[round(box_iou((0, 0, 10, 10), (5, 5, 15, 15)), 4), box_iou((0, 0, 10, 10), (20, 20, 30, 30))]", [0.1429, 0.0],
                  "Blank 2: `max(0, ix2 - ix1) * max(0, iy2 - iy1)`.", "الفراغ 2: `max(0, ix2 - ix1) * max(0, iy2 - iy1)`."),
            check("[(d['label'], d['score']) for d in kept]", [["car", 0.92], ["plate", 0.81]],
                  "Blank 3: keep a box only if every kept box with the same label overlaps it by IoU ≤ 0.5.",
                  "الفراغ 3: احتفظ بالصندوق فقط إن كان تداخل كل صندوق محفوظ من التسمية نفسها معه IoU ≤ 0.5."),
            check("list(plate_roi.shape) == [15, 40] and int(plate_roi[0, 0]) == 60 * 160 + 40", True,
                  "Blank 4: `image[y1:y2, x1:x2]` - rows first.", "الفراغ 4: `image[y1:y2, x1:x2]` - الصفوف أولًا."),
        ),
        hints=(
            ("A list comprehension with a condition filters detections.", "يرشّح list comprehension مع شرط الاكتشافات."),
            ("Negative widths mean no overlap - clamp them at 0.", "العروض السالبة تعني عدم التداخل - احصرها عند 0."),
            ("Boxes are (x, y) but arrays are [row, column].", "الصناديق بصيغة (x, y) لكن المصفوفات بصيغة [row, column]."),
        ),
        success=("Correct! The uncertain car is dropped, the duplicate box is suppressed, and the plate crop is ready for OCR - each stage feeds the next a cleaner input.",
                 "صحيح! حُذفت السيارة غير المؤكدة، وأُخمد الصندوق المكرر، وأصبح قص اللوحة جاهزًا لـ OCR - فكل مرحلة تغذّي التالية بمدخل أنظف."),
        reflect=("For your chosen application, which stages need classification, detection, segmentation, OCR or landmarks, and what threshold would you document?",
                 "في التطبيق الذي اخترته، أي المراحل تحتاج إلى تصنيف أو اكتشاف أو تقسيم أو OCR أو معالم؟ وما العتبة التي ستوثّقها؟"),
    ),
    "COURSE-014.M13.L01.EX01": Guided(
        goal=("Compute the core quantities of conditional and latent generative models: the CVAE KL term, latent interpolation, a class-conditioned input and a forward diffusion step.",
              "احسب الكميات الأساسية في النماذج التوليدية الشرطية والكامنة: حد KL في CVAE، والاستيفاء الكامن، ومدخلًا مشروطًا بالفئة، وخطوة انتشار أمامية."),
        steps=(
            ("Write the KL divergence of a diagonal Gaussian from N(0, I).", "اكتب تباعد KL لتوزيع غاوسي قطري عن N(0, I)."),
            ("Interpolate linearly between two latent codes.", "استوفِ خطيًا بين رمزين كامنين."),
            ("Concatenate the one-hot class to the noise (cGAN generator input).", "اربط الفئة بترميز One-hot مع الضجيج (مدخل مولّد cGAN)."),
            ("Sample x_t in closed form.", "اسحب x_t بالصيغة المغلقة."),
            ("Compute latent diffusion's compression factor.", "احسب معامل الضغط في الانتشار الكامن."),
        ),
        starter='''import numpy as np

# Step 1: KL(N(mu, sigma^2) || N(0, 1)) = -0.5 * sum(1 + log_var - mu^2 - exp(log_var))
def kl_divergence(mu, log_var):
    return ___

# Step 2: `steps` codes evenly spaced from z0 to z1
def interpolate(z0, z1, steps):
    return ___

# Step 3: where the class condition enters a cGAN generator
def generator_input(noise, label, n_classes=10):
    return ___

betas = np.linspace(1e-4, 0.02, 1000)
alpha_bar = np.cumprod(1 - betas)
rng = np.random.default_rng(0)
x0, noise = rng.random(16), rng.normal(size=16)
t = 600
# Step 4: closed-form forward diffusion
x_t = ___

# Step 5: pixel space 512x512x3 versus Stable Diffusion's latent 64x64x4
compression = ___
print(kl_divergence(np.zeros(4), np.zeros(4)), len(interpolate(np.zeros(2), np.ones(2), 5)), generator_input(np.zeros(3), 2).shape, compression)
''',
        answers=(
            "float(-0.5 * np.sum(1 + log_var - mu ** 2 - np.exp(log_var)))",
            "[z0 + t * (z1 - z0) for t in np.linspace(0, 1, steps)]",
            "np.concatenate([noise, np.eye(n_classes)[label]])",
            "np.sqrt(alpha_bar[t]) * x0 + np.sqrt(1 - alpha_bar[t]) * noise",
            "(512 * 512 * 3) / (64 * 64 * 4)",
        ),
        checks=(
            check("[kl_divergence(np.zeros(3), np.zeros(3)), round(kl_divergence(np.ones(2), np.zeros(2)), 4)]", [0.0, 1.0],
                  "Blank 1: `-0.5 * np.sum(1 + log_var - mu ** 2 - np.exp(log_var))`.", "الفراغ 1: `-0.5 * np.sum(1 + log_var - mu ** 2 - np.exp(log_var))`."),
            check("[np.asarray(z).tolist() for z in interpolate(np.zeros(2), np.array([2.0, 4.0]), 3)]", [[0.0, 0.0], [1.0, 2.0], [2.0, 4.0]],
                  "Blank 2: `z0 + t * (z1 - z0)` for t in `np.linspace(0, 1, steps)`.", "الفراغ 2: `z0 + t * (z1 - z0)` لقيم t في `np.linspace(0, 1, steps)`."),
            check("generator_input(np.zeros(3), 2).tolist()", [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                  "Blank 3: append `np.eye(n_classes)[label]` to the noise.", "الفراغ 3: أضف `np.eye(n_classes)[label]` إلى الضجيج."),
            check("bool(np.allclose(x_t, np.sqrt(alpha_bar[600]) * x0 + np.sqrt(1 - alpha_bar[600]) * noise))", True,
                  "Blank 4: `np.sqrt(alpha_bar[t]) * x0 + np.sqrt(1 - alpha_bar[t]) * noise`.", "الفراغ 4: `np.sqrt(alpha_bar[t]) * x0 + np.sqrt(1 - alpha_bar[t]) * noise`."),
            check("compression", 48.0, "Blank 5: 786,432 values versus 16,384 - a factor of 48.", "الفراغ 5: 786,432 قيمة مقابل 16,384 - أي بمعامل 48."),
        ),
        hints=(
            ("The KL term is zero when mu = 0 and log_var = 0.", "يكون حد KL صفرًا عندما mu = 0 وlog_var = 0."),
            ("`np.eye(n)[k]` is the one-hot vector for class k.", "`np.eye(n)[k]` هو متجه One-hot للفئة k."),
            ("Diffusion keeps sqrt(alpha_bar) of the signal and adds sqrt(1 − alpha_bar) of noise.", "يحتفظ الانتشار بـ sqrt(alpha_bar) من الإشارة ويضيف sqrt(1 − alpha_bar) من الضجيج."),
        ),
        success=("Correct! The KL term pulls latents towards a standard normal so interpolation stays smooth, the condition enters as an extra input, and latent diffusion denoises 48× fewer values than pixel-space diffusion.",
                 "صحيح! يسحب حد KL الرموز الكامنة نحو التوزيع الطبيعي القياسي فيبقى الاستيفاء ناعمًا، ويدخل الشرط بوصفه مدخلًا إضافيًا، ويزيل الانتشار الكامن الضجيج من قيم أقل بـ 48 مرة من الانتشار في فضاء البكسلات."),
        reflect=("Compare paired (Pix2Pix) and unpaired (CycleGAN) translation: what training data does each need?",
                 "قارن الترجمة المقترنة (Pix2Pix) وغير المقترنة (CycleGAN): ما بيانات التدريب التي يحتاجها كلٌّ منهما؟"),
    ),
}
