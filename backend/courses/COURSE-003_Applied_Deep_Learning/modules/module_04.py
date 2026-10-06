"""M04.L01 — Representing Real-World Data with Tensors.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 4.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"
MODULE_ORDER = 4
MODULE_TITLE = "Representing Real-World Data"
MODULE_DESCRIPTION = (
    "Learn how to turn images, volumetric scans, tabular records, time series, "
    "and text into tensor representations that preserve the structure a neural "
    "network needs."
)

SOURCE_CHAPTER = 4
SOURCE_PAGES = "Chapter 4 (page range not provided in source excerpt)"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Representing Real-World Data with Tensors",
    "slug": "applied-deep-learning-m04-l01",
    "description": (
        "A practical guide to converting common real-world data types into "
        "well-shaped numerical tensors for neural-network input."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 3.25,
    "skill_tags": [
        "pytorch",
        "data-representation",
        "images",
        "volumetric-data",
        "tabular-data",
        "categorical-data",
        "one-hot-encoding",
        "normalization",
        "time-series",
        "text",
        "embeddings",
        "module-04",
    ],
    "prerequisite_ids": ["M03.L01"],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Representing Real-World Data with Tensors",
        "content": (
            "# Representing Real-World Data with Tensors\n"
            "\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M04.L01  \n"
            "> **Module:** Representing Real-World Data  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, "
            "Chapter 4. This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why real-world data must be converted into numerical tensor representations.\n"
            "- Load image data and convert `H × W × C` arrays into PyTorch's `C × H × W` layout.\n"
            "- Build batches of images using the `N × C × H × W` convention.\n"
            "- Normalize image values appropriately for neural-network input.\n"
            "- Represent volumetric data using depth in addition to channels, height, and width.\n"
            "- Convert tabular data into feature and target tensors.\n"
            "- Distinguish continuous, ordinal, and categorical variables.\n"
            "- Use integer labels and one-hot encoding appropriately.\n"
            "- Normalize quantitative columns and filter rows with Boolean indexing.\n"
            "- Reshape flat time-series tables into sequence-oriented tensors.\n"
            "- Explain why tensor axis order should match how a model will consume the data.\n"
            "- Convert characters and words into numerical encodings.\n"
            "- Explain why embeddings are often preferable to huge one-hot vectors.\n"
            "- Recognize the common data-preparation pattern shared across different modalities.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. The central problem: turn meaning into numbers without losing structure\n"
            "\n"
            "Neural networks consume tensors and produce tensors. Their parameters, intermediate "
            "representations, inputs, and outputs are all numerical. Therefore, before training can "
            "begin, real-world data has to be encoded in a numerical form that preserves the aspects "
            "of the data that matter for the task.\n"
            "\n"
            "This leads to two questions for every dataset:\n"
            "\n"
            "1. **How should the raw values be converted into numbers?**\n"
            "2. **How should those numbers be arranged across tensor dimensions?**\n"
            "\n"
            "Those questions are just as important as loading the file itself.\n"
            "\n"
            "For example:\n"
            "\n"
            "| Data type | Typical structure |\n"
            "|---|---|\n"
            "| Image | channels × height × width |\n"
            "| Image batch | batch × channels × height × width |\n"
            "| 3D volume | channels × depth × height × width |\n"
            "| Table | samples × features |\n"
            "| Time series | samples × variables × sequence length |\n"
            "| Text | sequence positions × character/word representation |\n"
            "\n"
            "The exact layout is not universal. It depends on what each axis means and how the model "
            "will process it.\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Representing images\n"
            "\n"
            "A digital image is fundamentally a grid of numerical pixel values.\n"
            "\n"
            "A grayscale image may store one number per pixel. An RGB image stores three values per "
            "pixel: the intensity of red, green, and blue.\n"
            "\n"
            '{{image:rgb-image-channels}}'
            '\n'
            "\n"
            "Consumer images commonly use 8-bit integer values, while scientific or medical images "
            "may use higher numerical precision.\n"
            "\n"
            "### Loading an image\n"
            "\n"
            "The source chapter uses `imageio` to load a JPEG:\n"
            "\n"
            "```python\n"
            "import imageio.v2 as imageio\n"
            "\n"
            "img_arr = imageio.imread('../data/image.jpg')\n"
            "print(img_arr.shape)\n"
            "```\n"
            "\n"
            "A typical result may look like:\n"
            "\n"
            "```text\n"
            "(720, 1280, 3)\n"
            "```\n"
            "\n"
            "That means:\n"
            "\n"
            "```text\n"
            "height × width × channels\n"
            "```\n"
            "\n"
            "But many PyTorch vision modules expect:\n"
            "\n"
            "```text\n"
            "channels × height × width\n"
            "```\n"
            "\n"
            "### Reordering dimensions with `permute`\n"
            "\n"
            "```python\n"
            "import torch\n"
            "\n"
            "img = torch.from_numpy(img_arr)\n"
            "img = img.permute(2, 0, 1)\n"
            "\n"
            "print(img.shape)\n"
            "```\n"
            "\n"
            "Now the shape becomes:\n"
            "\n"
            "```text\n"
            "(3, 720, 1280)\n"
            "```\n"
            "\n"
            "This operation is conceptually cheap because `permute` can change the tensor's view by "
            "adjusting dimension metadata such as shape and stride rather than copying every pixel.\n"
            "\n"
            "[[IMAGE_NEEDED: Image layout conversion | "
            "A diagram showing an image tensor changing from H×W×C to C×H×W, with the same underlying "
            "pixel data but reordered logical axes | Learner should notice that the meaning/order of "
            "dimensions changes even though the image content does not]]\n"
            "\n"
            "### Building a batch\n"
            "\n"
            "A single image uses `C × H × W`. Multiple images are commonly stacked as:\n"
            "\n"
            "```text\n"
            "N × C × H × W\n"
            "```\n"
            "\n"
            "where `N` is the number of images.\n"
            "\n"
            "```python\n"
            "batch = torch.zeros(\n"
            "    len(image_files),\n"
            "    3,\n"
            "    256,\n"
            "    256,\n"
            "    dtype=torch.uint8,\n"
            ")\n"
            "```\n"
            "\n"
            "If an image includes a fourth alpha/transparency channel but the model expects RGB, the "
            "extra channel can be removed before placing the sample into the batch.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Converting image values into useful model input\n"
            "\n"
            "Neural networks usually operate on floating-point tensors rather than raw 8-bit image "
            "integers. Input scales also matter for optimization.\n"
            "\n"
            "### Simple rescaling\n"
            "\n"
            "For 8-bit pixels ranging from 0 to 255:\n"
            "\n"
            "```python\n"
            "batch = batch.float()\n"
            "batch /= 255.0\n"
            "```\n"
            "\n"
            "The values now lie roughly in `[0, 1]`.\n"
            "\n"
            "### Standardization\n"
            "\n"
            "Another common approach is to center each channel around zero and scale it using the "
            "channel standard deviation:\n"
            "\n"
            "```python\n"
            "n_channels = batch.shape[1]\n"
            "\n"
            "for c in range(n_channels):\n"
            "    mean = torch.mean(batch[:, c])\n"
            "    std = torch.std(batch[:, c])\n"
            "    batch[:, c] = (batch[:, c] - mean) / std\n"
            "```\n"
            "\n"
            "In a real training workflow, statistics should normally be computed from the **training "
            "data** and then reused consistently instead of being recomputed independently for every "
            "single batch.\n"
            "\n"
            "Other transformations such as resizing, cropping, or rotation may also be used to meet "
            "model input requirements or support training.\n"
            "\n"
            "{{exercise:M04.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Volumetric data: adding depth\n"
            "\n"
            "Some data represents a three-dimensional physical volume rather than a 2D picture. CT "
            "scans are an important example: multiple 2D slices represent anatomy at different "
            "positions through the body.\n"
            "\n"
            "[[IMAGE_NEEDED: CT volume built from slices | "
            "A stack of 2D grayscale scan slices arranged along a depth axis to form a 3D volume | "
            "Learner should notice that depth is a spatial dimension, unlike RGB channels which "
            "represent different measured features at the same pixel location]]\n"
            "\n"
            "A raw CT volume might have shape:\n"
            "\n"
            "```text\n"
            "D × H × W\n"
            "```\n"
            "\n"
            "If no explicit channel dimension is present, we can add one:\n"
            "\n"
            "```python\n"
            "vol = torch.from_numpy(vol_arr).float()\n"
            "vol = torch.unsqueeze(vol, 0)\n"
            "\n"
            "print(vol.shape)\n"
            "```\n"
            "\n"
            "Conceptually this changes:\n"
            "\n"
            "```text\n"
            "D × H × W\n"
            "```\n"
            "\n"
            "into:\n"
            "\n"
            "```text\n"
            "C × D × H × W\n"
            "```\n"
            "\n"
            "with `C = 1`.\n"
            "\n"
            "A batch of volumes then becomes:\n"
            "\n"
            "```text\n"
            "N × C × D × H × W\n"
            "```\n"
            "\n"
            "The key lesson is that volumetric data is not fundamentally alien to PyTorch. It is "
            "another multidimensional tensor whose axes have specific meanings.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Representing tabular data\n"
            "\n"
            "Tabular data usually contains one row per sample and one column per variable. A CSV, "
            "spreadsheet, or database table often has this basic structure.\n"
            "\n"
            "The challenge is that real tables may be **heterogeneous**: some columns represent "
            "continuous measurements, some represent ordered ratings, and others represent categories.\n"
            "\n"
            "A standard PyTorch tensor, however, is homogeneous. That means we need to decide how each "
            "column should be encoded numerically.\n"
            "\n"
            "### Loading a CSV as floating-point data\n"
            "\n"
            "The chapter uses a wine-quality dataset:\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "import torch\n"
            "\n"
            "wineq_numpy = np.loadtxt(\n"
            "    wine_path,\n"
            "    dtype=np.float32,\n"
            "    delimiter=';',\n"
            "    skiprows=1,\n"
            ")\n"
            "\n"
            "wineq = torch.from_numpy(wineq_numpy)\n"
            "```\n"
            "\n"
            "The dataset has shape approximately:\n"
            "\n"
            "```text\n"
            "(4898, 12)\n"
            "```\n"
            "\n"
            "meaning 4,898 samples and 12 columns.\n"
            "\n"
            "### Separate model inputs from the target\n"
            "\n"
            "If the final column is the value we want to predict, we should not leave it inside the "
            "input features.\n"
            "\n"
            "```python\n"
            "data = wineq[:, :-1]\n"
            "target = wineq[:, -1]\n"
            "```\n"
            "\n"
            "Now:\n"
            "\n"
            "```text\n"
            "data   -> input features\n"
            "target -> ground truth to predict\n"
            "```\n"
            "\n"
            "This separation is fundamental in supervised learning.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Continuous, ordinal, and categorical values\n"
            "\n"
            "Not every number means the same thing mathematically.\n"
            "\n"
            "### Continuous values\n"
            "\n"
            "Continuous measurements have meaningful numerical differences. For example, changes in "
            "distance or physical measurements can be compared quantitatively.\n"
            "\n"
            "The source further distinguishes ideas such as ratio scales and interval scales, but the "
            "main practical lesson is that arithmetic differences can be meaningful for genuine "
            "continuous measurements.\n"
            "\n"
            "### Ordinal values\n"
            "\n"
            "Ordinal values preserve **order**, but the distance between adjacent labels is not "
            "necessarily meaningful.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "small < medium < large\n"
            "```\n"
            "\n"
            "Mapping them to `1, 2, 3` captures ordering, but it does not prove that the step from "
            "small to medium has the same physical meaning as the step from medium to large.\n"
            "\n"
            "### Categorical values\n"
            "\n"
            "Categorical values are labels with no natural numeric distance or order.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "water, coffee, soda, milk\n"
            "```\n"
            "\n"
            "Assigning arbitrary integers to those categories does not make `milk > coffee` meaningful.\n"
            "\n"
            "[[IMAGE_NEEDED: Choosing a representation for column types | "
            "A simple flowchart distinguishing continuous, ordinal, and categorical variables and "
            "showing common representation choices such as normalized numeric values, ordered numeric "
            "or categorical treatment, and one-hot/embedding representation | Learner should notice "
            "that representation should preserve the real meaning of the variable rather than blindly "
            "treating every number as continuous]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Labels and one-hot encoding\n"
            "\n"
            "Suppose a target represents a discrete class. One simple representation is an integer "
            "class index:\n"
            "\n"
            "```python\n"
            "target = wineq[:, -1].long()\n"
            "```\n"
            "\n"
            "For many PyTorch classification losses, integer class indices are exactly what the "
            "training code expects.\n"
            "\n"
            "But categorical values used as **inputs** often need a different representation because "
            "the raw integer numbers can suggest false ordering or distance.\n"
            "\n"
            "### One-hot encoding\n"
            "\n"
            "A one-hot vector contains one `1` and zeros everywhere else.\n"
            "\n"
            "For four categories:\n"
            "\n"
            "```text\n"
            "class 0 -> [1, 0, 0, 0]\n"
            "class 1 -> [0, 1, 0, 0]\n"
            "class 2 -> [0, 0, 1, 0]\n"
            "class 3 -> [0, 0, 0, 1]\n"
            "```\n"
            "\n"
            "The positions distinguish categories without pretending there is a meaningful numerical "
            "distance between category IDs.\n"
            "\n"
            "### Using `scatter_`\n"
            "\n"
            "```python\n"
            "target_onehot = torch.zeros(target.shape[0], 10)\n"
            "target_onehot.scatter_(1, target.unsqueeze(1), 1.0)\n"
            "```\n"
            "\n"
            "`unsqueeze(1)` changes a 1D target vector into a column-shaped tensor so the index tensor "
            "has the dimensionality required by `scatter_`.\n"
            "\n"
            "Remember the underscore: `scatter_` modifies the destination tensor in place.\n"
            "\n"
            "### When should you use one-hot encoding?\n"
            "\n"
            "It is a natural choice for categories with no meaningful ordering. For ordinal variables, "
            "there is no universal answer: treating them as continuous introduces artificial distance, "
            "while treating them as categorical discards their ordering. The choice depends on the "
            "task and often benefits from experimentation.\n"
            "\n"
            "{{exercise:M04.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Normalize columns and inspect patterns with Boolean indexing\n"
            "\n"
            "Different numerical columns can live on very different scales. One feature may range "
            "around `0.2`, while another may be around `150`. Standardization puts features onto more "
            "comparable scales.\n"
            "\n"
            "```python\n"
            "data_mean = torch.mean(data, dim=0)\n"
            "data_var = torch.var(data, dim=0)\n"
            "\n"
            "data_normalized = (data - data_mean) / torch.sqrt(data_var)\n"
            "```\n"
            "\n"
            "Because `dim=0` reduces across rows, the result contains one statistic per column.\n"
            "\n"
            "Broadcasting then lets us subtract the feature mean from every sample.\n"
            "\n"
            "### Boolean masks\n"
            "\n"
            "PyTorch comparisons produce Boolean tensors:\n"
            "\n"
            "```python\n"
            "bad_indexes = target <= 3\n"
            "bad_data = data[bad_indexes]\n"
            "```\n"
            "\n"
            "The Boolean mask keeps rows whose corresponding mask value is `True`.\n"
            "\n"
            "This makes it easy to compare groups:\n"
            "\n"
            "```python\n"
            "bad_data = data[target <= 3]\n"
            "mid_data = data[(target > 3) & (target < 7)]\n"
            "good_data = data[target >= 7]\n"
            "```\n"
            "\n"
            "You can then inspect feature means within each group.\n"
            "\n"
            "### Why a simple threshold is not enough\n"
            "\n"
            "The source constructs a crude rule using one wine feature to predict quality. It finds "
            "some signal, but the rule misses many genuinely good samples and produces imperfect "
            "predictions.\n"
            "\n"
            "The educational point is important:\n"
            "\n"
            "> **Real outcomes often depend on multiple interacting variables. A single threshold can "
            "help us inspect a pattern, but it is not the same thing as learning a rich predictive model.**\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Time series: order is part of the data\n"
            "\n"
            "A normal table can often be shuffled without changing its meaning because each row is an "
            "independent sample. A time series is different: row order represents progression through "
            "time.\n"
            "\n"
            "The chapter uses hourly bike-sharing data. Each row is one hour containing variables such "
            "as weather, temperature, humidity, and bike counts.\n"
            "\n"
            "A flat table might have shape:\n"
            "\n"
            "```text\n"
            "hours × columns\n"
            "```\n"
            "\n"
            "but a model may benefit from an explicit daily structure.\n"
            "\n"
            "[[IMAGE_NEEDED: Flat time-series table to daily tensor | "
            "A 2D table of hourly rows being grouped into blocks of 24 and transformed into a 3D tensor "
            "with separate day, variable, and hour axes | Learner should notice that adding a time-period "
            "axis makes sequential structure explicit rather than treating every hour independently]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Reshaping time series into fixed-size sequences\n"
            "\n"
            "Suppose the original bike tensor has shape:\n"
            "\n"
            "```text\n"
            "(17520, 17)\n"
            "```\n"
            "\n"
            "That means 17,520 hourly rows and 17 variables.\n"
            "\n"
            "If each day has 24 consecutive hourly observations, we can group the storage into days:\n"
            "\n"
            "```python\n"
            "daily_bikes = bikes.view(-1, 24, bikes.shape[1])\n"
            "```\n"
            "\n"
            "The result is:\n"
            "\n"
            "```text\n"
            "(730, 24, 17)\n"
            "```\n"
            "\n"
            "Interpretation:\n"
            "\n"
            "```text\n"
            "days × hours × variables\n"
            "```\n"
            "\n"
            "`-1` tells PyTorch to infer the number of days from the total number of elements and the "
            "other requested dimensions.\n"
            "\n"
            "Because `view` reinterprets the same storage when compatible, it can reshape the tensor "
            "without an expensive data copy.\n"
            "\n"
            "The chapter then changes the axis order:\n"
            "\n"
            "```python\n"
            "daily_bikes = daily_bikes.transpose(1, 2)\n"
            "```\n"
            "\n"
            "giving:\n"
            "\n"
            "```text\n"
            "(730, 17, 24)\n"
            "```\n"
            "\n"
            "or:\n"
            "\n"
            "```text\n"
            "N × C × L\n"
            "```\n"
            "\n"
            "where:\n"
            "\n"
            "- `N` = number of daily samples,\n"
            "- `C` = variables/channels,\n"
            "- `L` = sequence length of 24 hours.\n"
            "\n"
            "[[IMAGE_NEEDED: N×C×L versus N×L×C sequence layouts | "
            "Two simplified 3D tensor diagrams comparing sample×variables×time with sample×time×variables | "
            "Learner should notice that both can contain the same values, but axis ordering determines "
            "how conveniently the model and code access complete variable sequences]]\n"
            "\n"
            "The choice of sequence length is also a modeling decision. Daily 24-hour chunks may expose "
            "daily rhythms; weekly 168-hour chunks may capture weekly behavior. The data must also be "
            "properly ordered and should not silently contain missing intervals if fixed-length grouping "
            "assumes continuous time.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Preparing time-series features for training\n"
            "\n"
            "Once time series are reshaped, the same representation questions return.\n"
            "\n"
            "The weather variable in the source has ordered levels. It can be treated in multiple ways:\n"
            "\n"
            "- categorical -> one-hot encode it,\n"
            "- approximately continuous/ordinal -> rescale its numeric values,\n"
            "- another specialized ordinal representation -> experiment deliberately.\n"
            "\n"
            "### One-hot encode a categorical time-series channel\n"
            "\n"
            "```python\n"
            "daily_weather_onehot = torch.zeros(\n"
            "    daily_bikes.shape[0],\n"
            "    4,\n"
            "    daily_bikes.shape[2],\n"
            ")\n"
            "\n"
            "daily_weather_onehot.scatter_(\n"
            "    1,\n"
            "    daily_bikes[:, 9, :].long().unsqueeze(1) - 1,\n"
            "    1.0,\n"
            ")\n"
            "```\n"
            "\n"
            "The encoded weather channels can then be concatenated onto the variable dimension:\n"
            "\n"
            "```python\n"
            "daily_bikes = torch.cat(\n"
            "    (daily_bikes, daily_weather_onehot),\n"
            "    dim=1,\n"
            ")\n"
            "```\n"
            "\n"
            "### Normalize continuous sequence variables\n"
            "\n"
            "A channel such as temperature can be mapped into `[0, 1]`:\n"
            "\n"
            "```python\n"
            "temp = daily_bikes[:, 10, :]\n"
            "temp_min = torch.min(temp)\n"
            "temp_max = torch.max(temp)\n"
            "\n"
            "daily_bikes[:, 10, :] = (\n"
            "    daily_bikes[:, 10, :] - temp_min\n"
            ") / (temp_max - temp_min)\n"
            "```\n"
            "\n"
            "or standardized:\n"
            "\n"
            "```python\n"
            "temp = daily_bikes[:, 10, :]\n"
            "daily_bikes[:, 10, :] = (\n"
            "    daily_bikes[:, 10, :] - torch.mean(temp)\n"
            ") / torch.std(temp)\n"
            "```\n"
            "\n"
            "{{exercise:M04.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Text must also become numbers\n"
            "\n"
            "Text may seem completely different from images and tables, but the same requirement "
            "applies: a neural network needs numerical tensors.\n"
            "\n"
            "The source introduces two intuitive granularities:\n"
            "\n"
            "- **character-level** representation,\n"
            "- **word-level** representation.\n"
            "\n"
            "Before either can work, text encoding itself matters. Python strings are Unicode, while "
            "older encodings such as ASCII cover a much smaller character set. For a simple English "
            "example, the chapter restricts character representation to ASCII-sized vectors.\n"
            "\n"
            "### Character one-hot encoding\n"
            "\n"
            "If a line contains 70 characters and our character vocabulary has 128 possible positions:\n"
            "\n"
            "```python\n"
            "letter_t = torch.zeros(len(line), 128)\n"
            "```\n"
            "\n"
            "Each row represents one character position in the text. A single `1` identifies which "
            "character is present.\n"
            "\n"
            "```python\n"
            "for i, letter in enumerate(line.lower().strip()):\n"
            "    letter_index = ord(letter) if ord(letter) < 128 else 0\n"
            "    letter_t[i][letter_index] = 1\n"
            "```\n"
            "\n"
            "This produces a sequence tensor shaped roughly as:\n"
            "\n"
            "```text\n"
            "sequence length × character vocabulary size\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Word-level one-hot encoding\n"
            "\n"
            "At the word level, we first build a **vocabulary**: a mapping from unique words to integer "
            "indices.\n"
            "\n"
            "```python\n"
            "word_list = sorted(set(clean_words(text)))\n"
            "word2index_dict = {\n"
            "    word: i for i, word in enumerate(word_list)\n"
            "}\n"
            "```\n"
            "\n"
            "If the vocabulary contains 7,261 unique words, every one-hot word vector has length 7,261.\n"
            "\n"
            "For an 11-word sentence:\n"
            "\n"
            "```python\n"
            "word_t = torch.zeros(11, len(word2index_dict))\n"
            "```\n"
            "\n"
            "and then one position is activated for each word.\n"
            "\n"
            "This works, but it immediately exposes a problem: **large vocabularies produce extremely "
            "wide, sparse vectors**.\n"
            "\n"
            "[[IMAGE_NEEDED: Character, word, and embedding text representations | "
            "A comparison showing character-level one-hot rows, word-level one-hot rows with a much "
            "larger vocabulary dimension, and a compact dense embedding vector for each word | "
            "Learner should notice the trade-off between sequence granularity, vocabulary size, and "
            "representation compactness]]\n"
            "\n"
            "Another limitation is that one-hot vectors do not encode semantic similarity. Two related "
            "words are just two different basis vectors, no closer numerically than unrelated words.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Embeddings: compact learned representations for categories\n"
            "\n"
            "An **embedding** maps a discrete item such as a word into a dense vector of floating-point "
            "numbers.\n"
            "\n"
            "Instead of representing a word using thousands of mostly-zero positions, we might represent "
            "it using, for example, a 100-dimensional dense vector.\n"
            "\n"
            "The goal is not merely compression. A useful embedding space can place items used in similar "
            "contexts into nearby regions.\n"
            "\n"
            "[[IMAGE_NEEDED: Semantic embedding space | "
            "A simple 2D conceptual embedding plot with related words clustered near one another and "
            "unrelated groups separated, making clear that real embeddings usually have many more "
            "dimensions | Learner should notice that distance and direction in an embedding can encode "
            "relationships that one-hot vectors do not express]]\n"
            "\n"
            "The source gives a conceptual manual example using semantic axes such as object type and "
            "color. Real embeddings use many more dimensions, and those axes usually do not correspond "
            "to human-labeled concepts directly.\n"
            "\n"
            "Classic embedding methods can learn vectors from word context. More modern language models "
            "can produce **context-sensitive** representations, meaning a word's vector can depend on "
            "the sentence in which it appears.\n"
            "\n"
            "### Embeddings are useful beyond text\n"
            "\n"
            "The chapter makes an important generalization: embeddings are useful whenever categorical "
            "spaces become too large for convenient one-hot encoding.\n"
            "\n"
            "Examples can include:\n"
            "\n"
            "- words,\n"
            "- product IDs,\n"
            "- user/item categories,\n"
            "- other discrete entities.\n"
            "\n"
            "Embeddings may be learned from scratch with the task or initialized from previously learned "
            "representations and then updated during **fine-tuning**.\n"
            "\n"
            "This makes text representation a blueprint for handling high-cardinality categorical data "
            "more broadly.\n"
            "\n"
            "{{exercise:M04.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## 15. The shared pattern across every data type\n"
            "\n"
            "Images, CT scans, spreadsheets, time series, and text look very different at the raw-data "
            "level. But their preparation follows the same reasoning process:\n"
            "\n"
            "```text\n"
            "raw data\n"
            "   |\n"
            "   v\n"
            "load with an appropriate file/data library\n"
            "   |\n"
            "   v\n"
            "convert values to numerical form\n"
            "   |\n"
            "   v\n"
            "arrange dimensions to reflect data structure\n"
            "   |\n"
            "   v\n"
            "encode categorical information appropriately\n"
            "   |\n"
            "   v\n"
            "normalize / scale numerical inputs when needed\n"
            "   |\n"
            "   v\n"
            "tensor ready for a model\n"
            "```\n"
            "\n"
            "The central skill is therefore not memorizing one tensor shape. It is learning to ask:\n"
            "\n"
            "- What does each axis represent?\n"
            "- Which values are continuous, ordinal, or categorical?\n"
            "- Is there a meaningful ordering in the data?\n"
            "- Does the model expect channels or sequence dimensions in a particular position?\n"
            "- Should the values be rescaled or standardized?\n"
            "- Is one-hot encoding practical, or would an embedding be better?\n"
            "\n"
            "Once those questions become natural, many apparently different data-preparation problems "
            "become variations of the same tensor-design task.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: If data is numeric, it is automatically model-ready\n"
            "\n"
            "> A CSV full of numbers can be fed directly into a neural network without thinking about the columns.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A number can represent a continuous measurement, an ordered rank, or an arbitrary category "
            "ID. Those meanings require different representation decisions.\n"
            "\n"
            "### Misconception 2: Tensor shape is only a technical detail\n"
            "\n"
            "> If the same values exist somewhere in the tensor, axis order does not matter.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Models interpret dimensions according to architectural conventions. `H×W×C` and `C×H×W` "
            "contain similar information but are not interchangeable if the model expects one specific layout.\n"
            "\n"
            "### Misconception 3: Integer category IDs behave like meaningful measurements\n"
            "\n"
            "> If red=1, green=2, and blue=3, then blue is three times red.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Those integers are arbitrary identifiers. One-hot encodings or embeddings avoid injecting "
            "a false numerical distance.\n"
            "\n"
            "### Misconception 4: One-hot encoding is always the best categorical representation\n"
            "\n"
            "> Every category should be expanded into a one-hot vector regardless of vocabulary size.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Large categorical spaces produce huge sparse vectors. Embeddings give compact dense "
            "representations and can learn useful relationships between entities.\n"
            "\n"
            "### Misconception 5: Time series are just ordinary tables\n"
            "\n"
            "> Rows can be shuffled because each row is still a valid record.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Time order contains information. Reshaping time series into explicit sequences helps "
            "preserve temporal structure that would otherwise be lost.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Channel | Feature plane associated with an image/volume, such as red, green, or blue. |\n"
            "| `C × H × W` | Common PyTorch layout for one image: channels, height, width. |\n"
            "| `N × C × H × W` | Common layout for a batch of images. |\n"
            "| `N × C × D × H × W` | Typical conceptual layout for batches of volumetric data. |\n"
            "| `permute` | Reorders tensor dimensions without necessarily copying underlying data. |\n"
            "| Normalization | General process of rescaling input data to a useful numerical range. |\n"
            "| Standardization | Transformation that centers data around zero and scales by standard deviation. |\n"
            "| Feature | Input variable used by a model. |\n"
            "| Target | Ground-truth value or label the model should predict. |\n"
            "| Continuous variable | Numeric variable with meaningful quantitative differences. |\n"
            "| Ordinal variable | Ordered category whose spacing is not necessarily meaningful. |\n"
            "| Categorical variable | Discrete label with no inherent numeric order or distance. |\n"
            "| One-hot encoding | Sparse category representation with one active position. |\n"
            "| Boolean mask | Tensor of True/False values used to filter or select data. |\n"
            "| Time series | Ordered observations whose sequence in time carries meaning. |\n"
            "| `view` | Reinterprets compatible tensor storage using a new shape. |\n"
            "| Sequence length | Number of ordered positions in one sequence sample. |\n"
            "| Vocabulary | Set of discrete text tokens that can be assigned indices. |\n"
            "| Character-level encoding | Representation where each sequence item is a character. |\n"
            "| Word-level encoding | Representation where each sequence item is a word/token. |\n"
            "| Embedding | Dense vector representation of a discrete item. |\n"
            "| Fine-tuning | Updating pretrained representations while learning a downstream task. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why must neural-network inputs ultimately be represented numerically?\n"
            "2. What does each axis in `N × C × H × W` mean?\n"
            "3. Why might an image loaded as `H × W × C` need `permute(2, 0, 1)`?\n"
            "4. What is the difference between rescaling pixels by 255 and standardizing them?\n"
            "5. How does volumetric data differ from a normal 2D image tensor?\n"
            "6. Why should a prediction target usually be removed from the model's input features?\n"
            "7. How do continuous, ordinal, and categorical variables differ?\n"
            "8. Why can integer category IDs be dangerous as model inputs?\n"
            "9. What information does one-hot encoding preserve and what does it intentionally avoid implying?\n"
            "10. Why does `target.unsqueeze(1)` help when using `scatter_` for one-hot encoding?\n"
            "11. How can Boolean masks be used to select rows in a tensor?\n"
            "12. Why is a time-series table fundamentally different from a table of independent rows?\n"
            "13. What does `view(-1, 24, C)` accomplish when hourly data is grouped into days?\n"
            "14. Why might `N × C × L` be preferable to `N × L × C` for a particular model or exercise?\n"
            "15. Why does word-level one-hot encoding become inefficient for large vocabularies?\n"
            "16. What advantage does an embedding offer over a one-hot vector?\n"
            "17. How are embeddings useful outside natural language processing?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Preparing data for deep learning means preserving meaning while converting the data into "
            "numbers and arranging those numbers into tensor dimensions that match the structure of the "
            "problem. Images, tables, sequences, and text differ mainly in what their axes and values mean—not "
            "in the fundamental requirement that the model ultimately receives well-designed numerical tensors.**\n"
        ),

        "estimated_minutes": 195,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "representation-principle", "title": "The central representation problem", "order": 1},
            {"id": "images", "title": "Representing images", "order": 2},
            {"id": "image-normalization", "title": "Image normalization", "order": 3},
            {"id": "volumetric-data", "title": "Volumetric data", "order": 4},
            {"id": "tabular-data", "title": "Representing tabular data", "order": 5},
            {"id": "variable-types", "title": "Continuous, ordinal, and categorical values", "order": 6},
            {"id": "one-hot-and-targets", "title": "Labels and one-hot encoding", "order": 7},
            {"id": "normalizing-and-filtering-tabular", "title": "Normalizing and filtering tabular data", "order": 8},
            {"id": "time-series", "title": "Time series and ordering", "order": 9},
            {"id": "time-series-shaping", "title": "Reshaping time series", "order": 10},
            {"id": "time-series-features", "title": "Preparing time-series features", "order": 11},
            {"id": "text-as-numbers", "title": "Text as numbers", "order": 12},
            {"id": "word-one-hot", "title": "Word-level one-hot encoding", "order": 13},
            {"id": "embeddings", "title": "Embeddings", "order": 14},
            {"id": "shared-pattern", "title": "The shared pattern across data types", "order": 15},
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M04.L01.EX01",
            "title": "Prepare an Image Tensor for a Neural Network",
            "lesson_code": "M04.L01",
            "section_id": "image-normalization",
            "placement": "after_section",
            "description": (
                "Practice converting an image array into a properly laid-out and normalized PyTorch tensor."
            ),
            "instructions": (
                "1. Load an RGB image using an image library that returns a NumPy array.\n"
                "2. Print the raw array shape and identify height, width, and channels.\n"
                "3. Convert it with `torch.from_numpy`.\n"
                "4. Use `permute` to obtain `C × H × W`.\n"
                "5. Convert the tensor to floating point and scale 8-bit pixel values to `[0, 1]`.\n"
                "6. Add a leading batch dimension so the final tensor is `1 × C × H × W`.\n"
                "7. Print every intermediate shape and explain what each dimension means."
            ),
            "expected_output": (
                "Executable code showing raw image shape, channel-first shape, normalized dtype/range, "
                "and final batched shape, plus a short interpretation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "image-loading",
                "permute",
                "normalization",
                "batch-dimension",
                "shape-reasoning",
            ],
        },
        {
            "id": "M04.L01.EX02",
            "title": "Choose the Right Representation for Table Columns",
            "lesson_code": "M04.L01",
            "section_id": "one-hot-and-targets",
            "placement": "after_section",
            "description": (
                "Practice distinguishing continuous, ordinal, and categorical variables and choosing encodings."
            ),
            "instructions": (
                "For each variable below, classify it as continuous, ordinal, or categorical and choose "
                "a reasonable representation for a neural network:\n"
                "1. temperature in Celsius,\n"
                "2. T-shirt size: small/medium/large,\n"
                "3. country name,\n"
                "4. product category ID,\n"
                "5. star rating from 1 to 5,\n"
                "6. body weight in kilograms.\n"
                "For each answer, explain what numerical meaning would be lost or falsely introduced "
                "if you chose a poor representation. Then one-hot encode a small example categorical "
                "tensor using either `scatter_` or another PyTorch method."
            ),
            "expected_output": (
                "A six-row classification table with representation choices and explanations, plus "
                "working one-hot encoding code."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "continuous-data",
                "ordinal-data",
                "categorical-data",
                "one-hot-encoding",
            ],
        },
        {
            "id": "M04.L01.EX03",
            "title": "Turn Hourly Rows into Daily Sequences",
            "lesson_code": "M04.L01",
            "section_id": "time-series-features",
            "placement": "after_section",
            "description": (
                "Practice reshaping flat time-series observations into fixed-length sequences."
            ),
            "instructions": (
                "Create a synthetic tensor with shape `(72, 5)` representing 72 hours and 5 variables.\n"
                "1. Reshape it into 3 days × 24 hours × 5 variables using `view` or `reshape`.\n"
                "2. Reorder it into `N × C × L` = `(3, 5, 24)`.\n"
                "3. Explain the meaning of each axis.\n"
                "4. Pick one continuous channel and standardize it across the available data.\n"
                "5. Explain what assumption would be violated if several hourly rows were missing from "
                "the middle of the original sequence."
            ),
            "expected_output": (
                "PyTorch code producing the requested shapes and normalization, plus an explanation "
                "of the time-ordering assumption."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "time-series",
                "view",
                "transpose",
                "sequence-shaping",
                "normalization",
            ],
        },
        {
            "id": "M04.L01.EX04",
            "title": "One-Hot Vectors vs. Embeddings",
            "lesson_code": "M04.L01",
            "section_id": "embeddings",
            "placement": "after_section",
            "description": (
                "Reason about why embeddings become useful when categorical vocabularies grow."
            ),
            "instructions": (
                "Suppose a vocabulary contains 50,000 words.\n"
                "1. How many elements are required to one-hot encode one word?\n"
                "2. How many nonzero values does that one-hot vector contain?\n"
                "3. Compare that with representing a word using a dense 256-dimensional embedding.\n"
                "4. Explain why an embedding can capture similarity between words while a basic one-hot "
                "representation does not.\n"
                "5. Name one non-text problem where an embedding could represent high-cardinality categories."
            ),
            "expected_output": (
                "A short quantitative comparison and an explanation of sparsity, compactness, and "
                "semantic/learned similarity."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "one-hot-encoding",
                "embeddings",
                "categorical-representation",
                "representation-efficiency",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M04.L01.QZ01",
        "title": "Real-World Data Representation — Knowledge Check",
        "lesson_code": "M04.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M04.L01.Q01",
                "section_id": "images",
                "question": "A loaded RGB image has shape `(720, 1280, 3)`. Which operation creates the common PyTorch `C × H × W` layout?",
                "options": [
                    "`img.permute(2, 0, 1)`",
                    "`img.view(720, 1280, 3)`",
                    "`img.unsqueeze(3)`",
                    "`img.mean(0)`",
                ],
                "correct": 0,
                "explanation": (
                    "`permute(2, 0, 1)` moves the channel dimension from the final position to the first."
                ),
            },
            {
                "id": "M04.L01.Q02",
                "section_id": "image-normalization",
                "question": "Why might 8-bit image data be converted to float and divided by 255?",
                "options": [
                    "To reorder RGB channels alphabetically.",
                    "To place pixel values roughly in the range `[0, 1]` for model input.",
                    "To create a target label automatically.",
                    "To add a batch dimension.",
                ],
                "correct": 1,
                "explanation": (
                    "Dividing 0–255 integer intensities by 255 converts them to a floating-point scale "
                    "between approximately 0 and 1."
                ),
            },
            {
                "id": "M04.L01.Q03",
                "section_id": "volumetric-data",
                "question": "What extra structural dimension distinguishes a volumetric scan from a standard 2D image?",
                "options": [
                    "A learning-rate dimension",
                    "A depth dimension",
                    "A loss dimension",
                    "A label dimension",
                ],
                "correct": 1,
                "explanation": (
                    "A volume stacks spatial slices along a depth axis, giving data such as `C × D × H × W`."
                ),
            },
            {
                "id": "M04.L01.Q04",
                "section_id": "tabular-data",
                "question": "Why should the target column normally be separated from the input feature tensor in supervised learning?",
                "options": [
                    "Otherwise the model would be given the answer it is supposed to predict.",
                    "Targets can never be stored in tensors.",
                    "The target must always be text.",
                    "PyTorch only allows ten input columns.",
                ],
                "correct": 0,
                "explanation": (
                    "The target is ground truth for evaluating and training the prediction. Including it "
                    "as an input leaks the answer into the model."
                ),
            },
            {
                "id": "M04.L01.Q05",
                "section_id": "variable-types",
                "question": "Which statement best describes an ordinal variable?",
                "options": [
                    "It has meaningful ordering but spacing between categories may not be meaningful.",
                    "It has no ordering and no category identity.",
                    "It must be a floating-point measurement.",
                    "It is always represented by an RGB channel.",
                ],
                "correct": 0,
                "explanation": (
                    "Ordinal categories have an order, but numeric distance between adjacent categories "
                    "does not necessarily represent equal real-world distance."
                ),
            },
            {
                "id": "M04.L01.Q06",
                "section_id": "one-hot-and-targets",
                "question": "Why is one-hot encoding useful for nominal categorical inputs?",
                "options": [
                    "It creates a meaningful distance between arbitrary category IDs.",
                    "It represents category identity without imposing an artificial ordering.",
                    "It always uses fewer numbers than an embedding.",
                    "It converts every category into a continuous measurement.",
                ],
                "correct": 1,
                "explanation": (
                    "One-hot encoding separates categories into independent positions rather than "
                    "pretending that their integer identifiers have ordered numerical meaning."
                ),
            },
            {
                "id": "M04.L01.Q07",
                "section_id": "normalizing-and-filtering-tabular",
                "question": "What does `data[target <= 3]` do when `target <= 3` produces a Boolean tensor aligned with the rows?",
                "options": [
                    "Sorts every feature column.",
                    "Selects rows whose corresponding mask values are `True`.",
                    "Moves the selected rows to a GPU.",
                    "One-hot encodes the target.",
                ],
                "correct": 1,
                "explanation": (
                    "Boolean advanced indexing filters the row dimension according to the True/False mask."
                ),
            },
            {
                "id": "M04.L01.Q08",
                "section_id": "time-series-shaping",
                "question": "What does `view(-1, 24, 17)` accomplish for compatible hourly data with 17 variables?",
                "options": [
                    "It discards all but 24 rows.",
                    "It groups the same stored values into samples of 24 consecutive hours and 17 variables.",
                    "It creates 24 random features.",
                    "It sorts the observations by target value.",
                ],
                "correct": 1,
                "explanation": (
                    "`view` changes the logical shape without changing the total element count, so hourly "
                    "rows can be grouped into fixed-length daily blocks."
                ),
            },
            {
                "id": "M04.L01.Q09",
                "section_id": "time-series",
                "question": "Why should time-series rows not automatically be treated as independent shuffled records?",
                "options": [
                    "PyTorch cannot store shuffled tensors.",
                    "Their ordering may carry predictive temporal relationships.",
                    "Time-series values cannot be normalized.",
                    "Every time series must be text.",
                ],
                "correct": 1,
                "explanation": (
                    "Earlier and later observations can be related, so preserving sequence structure may "
                    "be essential for the task."
                ),
            },
            {
                "id": "M04.L01.Q10",
                "section_id": "word-one-hot",
                "question": "What is a major weakness of word-level one-hot encoding for a large vocabulary?",
                "options": [
                    "It cannot distinguish words.",
                    "It produces very large sparse vectors and does not encode semantic similarity.",
                    "It always requires a GPU.",
                    "It changes word order automatically.",
                ],
                "correct": 1,
                "explanation": (
                    "Each word needs a vector as wide as the entire vocabulary, while unrelated and related "
                    "words are represented by equally separate basis positions."
                ),
            },
            {
                "id": "M04.L01.Q11",
                "section_id": "embeddings",
                "question": "What is a key advantage of embeddings?",
                "options": [
                    "They represent discrete items with compact dense vectors that can learn useful relationships.",
                    "They guarantee every model output is correct.",
                    "They eliminate the need for numeric tensors.",
                    "They preserve raw text files inside the network.",
                ],
                "correct": 0,
                "explanation": (
                    "Embeddings replace huge sparse categorical vectors with dense learned vectors that "
                    "can encode useful similarity and relationships."
                ),
            },
            {
                "id": "M04.L01.Q12",
                "section_id": "shared-pattern",
                "type": "open",
                "question": (
                    "You receive a new dataset type you have never used before. Describe the questions you "
                    "would ask to design an appropriate tensor representation before feeding it to a neural network."
                ),
            },
        ],
        "passing_score": 70,
    },
}
