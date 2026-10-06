"""M03.L01 — It Starts with a Tensor.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 3.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"
MODULE_ORDER = 3
MODULE_TITLE = "Tensor Foundations"
MODULE_DESCRIPTION = (
    "Build a practical and mental model of PyTorch tensors: how they represent data, "
    "how indexing and broadcasting work, how dtype/device/storage/stride affect "
    "behavior and performance, and how tensors interoperate with NumPy and files."
)

SOURCE_CHAPTER = 3
SOURCE_PAGES = "Chapter 3 (page range not provided in source excerpt)"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "It Starts with a Tensor",
    "slug": "applied-deep-learning-m03-l01",
    "description": (
        "A complete introduction to PyTorch tensors as the fundamental data structure "
        "for deep learning, covering creation, shapes, indexing, broadcasting, dtypes, "
        "views, storage, strides, contiguity, devices, NumPy interoperability, and serialization."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 2.75,
    "skill_tags": [
        "pytorch",
        "tensors",
        "tensor-shape",
        "indexing",
        "broadcasting",
        "dtype",
        "storage",
        "stride",
        "views",
        "contiguity",
        "gpu",
        "numpy",
        "serialization",
        "module-03",
    ],
    "prerequisite_ids": ["M02.L01"],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "It Starts with a Tensor",
        "content": (
            "# It Starts with a Tensor\n"
            "\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M03.L01  \n"
            "> **Module:** Tensor Foundations  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, "
            "Chapter 3. This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why neural networks represent information as floating-point numbers.\n"
            "- Define a tensor as a multidimensional numerical array and reason about its dimensions and shape.\n"
            "- Create, inspect, index, slice, and modify PyTorch tensors.\n"
            "- Explain how broadcasting enables operations between compatible tensor shapes.\n"
            "- Choose and convert tensor data types using `dtype` and `to()`.\n"
            "- Recognize common categories of operations in the PyTorch tensor API.\n"
            "- Explain the relationship between a tensor and its underlying storage.\n"
            "- Reason about shape, storage offset, and stride.\n"
            "- Explain why slicing and transposing can create cheap views rather than copies.\n"
            "- Distinguish contiguous and noncontiguous tensors.\n"
            "- Move tensors between CPU and GPU devices.\n"
            "- Convert between PyTorch tensors and NumPy arrays and understand when memory is shared.\n"
            "- Save and reload tensors using PyTorch serialization and understand why HDF5 may be useful for interoperability.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Deep learning sees the world as numbers\n"
            "\n"
            "Images, text, sound, measurements, and labels may look completely different to us, "
            "but a neural network ultimately performs mathematical operations. That means real-world "
            "information has to be encoded into numerical representations before the model can use it.\n"
            "\n"
            "The chapter emphasizes a useful view of deep learning:\n"
            "\n"
            "> **A neural network transforms one numerical representation into another numerical representation.**\n"
            "\n"
            "The starting representation may correspond to something meaningful to humans, such as "
            "pixel values. The final representation may correspond to a class label or another useful "
            "output. Between those endpoints, the model creates **intermediate representations**.\n"
            "\n"
            "For image recognition, early internal representations might respond to simple structures "
            "such as edges or textures. Deeper representations may capture combinations that are useful "
            "for recognizing more complex structures. These intermediate values are learned for the task "
            "from examples rather than manually defined one by one.\n"
            "\n"
            "[[IMAGE_NEEDED: Input-to-intermediate-to-output representations | "
            "A simple neural-network pipeline showing a human-interpretable input on the left, several "
            "layers of floating-point intermediate representations in the middle, and a human-usable "
            "output on the right | Learner should notice that the network repeatedly transforms numeric "
            "representations and that the hidden intermediate representations are task-dependent]]\n"
            "\n"
            "PyTorch therefore needs an efficient way to store and manipulate large collections of "
            "numbers. That data structure is the **tensor**.\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Tensors: multidimensional arrays\n"
            "\n"
            "For the practical deep learning work in this course, a tensor is best understood as a "
            "**multidimensional array of numbers**.\n"
            "\n"
            "You can think of familiar mathematical objects as tensors of different dimensionalities:\n"
            "\n"
            "| Tensor form | Example interpretation |\n"
            "|---|---|\n"
            "| 0D | Scalar: one number |\n"
            "| 1D | Vector: an ordered list of numbers |\n"
            "| 2D | Matrix: rows and columns |\n"
            "| 3D | Stack of matrices, such as channels × height × width |\n"
            "| 4D | Often a batch of images: batch × channels × height × width |\n"
            "\n"
            "The **number of dimensions** tells us how many indices are needed to locate an individual "
            "scalar value. Tensor dimensions are zero-indexed: the leftmost axis is dimension `0`, "
            "the next is dimension `1`, and so on.\n"
            "\n"
            "For example, a tensor with shape `(4, 3, 3)` has three dimensions:\n"
            "\n"
            "- dimension 0 has size 4,\n"
            "- dimension 1 has size 3,\n"
            "- dimension 2 has size 3.\n"
            "\n"
            "[[IMAGE_NEEDED: Scalar, vector, matrix, and 3D tensor | "
            "A progression showing a single scalar, a one-dimensional vector, a two-dimensional matrix, "
            "and a three-dimensional stack with shape labels | Learner should notice that tensors "
            "generalize familiar scalar/vector/matrix structures to arbitrary numbers of dimensions]]\n"
            "\n"
            "### Why not just use Python lists?\n"
            "\n"
            "Python lists are convenient general-purpose containers, but they are not optimized for "
            "large numerical workloads. PyTorch tensors store homogeneous numerical values in a layout "
            "designed for efficient mathematical computation.\n"
            "\n"
            "A tensor also gives us features that plain Python lists do not provide naturally, such as:\n"
            "\n"
            "- multidimensional indexing,\n"
            "- vectorized mathematical operations,\n"
            "- efficient memory representation,\n"
            "- GPU execution,\n"
            "- integration with automatic differentiation later in the course.\n"
            "\n"
            "### Creating your first tensors\n"
            "\n"
            "```python\n"
            "import torch\n"
            "\n"
            "a = torch.ones(3)\n"
            "print(a)\n"
            "```\n"
            "\n"
            "This creates a one-dimensional tensor of size 3 filled with ones.\n"
            "\n"
            "You can index and modify it much like a list:\n"
            "\n"
            "```python\n"
            "print(a[1])\n"
            "a[2] = 2.0\n"
            "print(a)\n"
            "```\n"
            "\n"
            "You can also construct a tensor directly from Python data:\n"
            "\n"
            "```python\n"
            "points = torch.tensor([\n"
            "    [4.0, 1.0],\n"
            "    [5.0, 3.0],\n"
            "    [2.0, 1.0],\n"
            "])\n"
            "\n"
            "print(points.shape)\n"
            "```\n"
            "\n"
            "The shape is:\n"
            "\n"
            "```text\n"
            "torch.Size([3, 2])\n"
            "```\n"
            "\n"
            "Interpret that as **3 points × 2 coordinates per point**.\n"
            "\n"
            "### Indexing individual values and rows\n"
            "\n"
            "```python\n"
            "print(points[0, 1])  # y-coordinate of the first point\n"
            "print(points[0])     # the entire first point\n"
            "```\n"
            "\n"
            "Notice that `points[0]` is itself a tensor. As we will see later, it can be a **view** "
            "onto the same underlying data rather than a copied chunk of memory.\n"
            "\n"
            "{{exercise:M03.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Indexing and slicing tensors\n"
            "\n"
            "PyTorch adopts Python-style slice notation, extended naturally across tensor dimensions.\n"
            "\n"
            "For a Python list, you may already know:\n"
            "\n"
            "```python\n"
            "some_list = list(range(6))\n"
            "\n"
            "some_list[:]       # everything\n"
            "some_list[1:4]     # indices 1 through 3\n"
            "some_list[1:]      # index 1 to the end\n"
            "some_list[:4]      # beginning through index 3\n"
            "some_list[:-1]     # everything except the final element\n"
            "some_list[1:4:2]   # every second element in the selected range\n"
            "```\n"
            "\n"
            "The same style applies to tensors, but you can specify a slice for each dimension:\n"
            "\n"
            "```python\n"
            "points[1:]       # all rows after the first\n"
            "points[1:, :]    # same idea, explicitly keeping all columns\n"
            "points[1:, 0]    # rows after the first, first column only\n"
            "```\n"
            "\n"
            "### Adding a dimension\n"
            "\n"
            "A useful indexing trick is:\n"
            "\n"
            "```python\n"
            "points[None]\n"
            "```\n"
            "\n"
            "This adds a dimension of size 1. The same idea can be expressed more explicitly with:\n"
            "\n"
            "```python\n"
            "points.unsqueeze(dim=0)\n"
            "```\n"
            "\n"
            "This is exactly the kind of operation we used in the previous chapter when converting a "
            "single image tensor into a batch containing one image.\n"
            "\n"
            "A major skill in PyTorch is learning to read indexing expressions by asking:\n"
            "\n"
            "1. Which dimensions are being selected?\n"
            "2. Which dimensions are being reduced to a single index?\n"
            "3. Which dimensions are preserved as ranges?\n"
            "4. Is a new size-1 dimension being inserted?\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Broadcasting: operating on compatible shapes\n"
            "\n"
            "Broadcasting lets PyTorch perform element-wise operations between tensors whose shapes "
            "are not identical but are **compatible**.\n"
            "\n"
            "When comparing tensor dimensions for broadcasting, PyTorch aligns shapes from the right. "
            "For corresponding dimensions to be compatible, either:\n"
            "\n"
            "- their sizes are equal, or\n"
            "- one of the sizes is `1`.\n"
            "\n"
            "### Scalar broadcasting\n"
            "\n"
            "Consider:\n"
            "\n"
            "```text\n"
            "[1, 2, 3] + 10 -> [11, 12, 13]\n"
            "```\n"
            "\n"
            "Conceptually, the scalar is applied to each element. PyTorch does not need you to manually "
            "construct a second tensor `[10, 10, 10]`.\n"
            "\n"
            "### Broadcasting two tensors\n"
            "\n"
            "Suppose the shapes are:\n"
            "\n"
            "```text\n"
            "(1, 3)\n"
            "(3, 1)\n"
            "```\n"
            "\n"
            "The rightmost dimensions are `3` and `1`, which are compatible because one is 1. The next "
            "dimensions are `1` and `3`, which are also compatible. The result can have shape `(3, 3)`.\n"
            "\n"
            "[[IMAGE_NEEDED: Broadcasting shape alignment | "
            "A visual example showing a (1, 3) row tensor and a (3, 1) column tensor expanding "
            "conceptually to form a (3, 3) result, with dimensions aligned from the right | Learner "
            "should notice that a dimension of size 1 can be virtually expanded and that broadcasting "
            "does not require manually duplicating values]]\n"
            "\n"
            "### Broadcasting with images\n"
            "\n"
            "Suppose we have one RGB image:\n"
            "\n"
            "```python\n"
            "img_t = torch.randn(3, 5, 5)  # channels, rows, columns\n"
            "```\n"
            "\n"
            "and channel weights:\n"
            "\n"
            "```python\n"
            "weights = torch.tensor([0.2126, 0.7152, 0.0722])\n"
            "```\n"
            "\n"
            "To multiply one weight per channel across every row and column, we can reshape the weights:\n"
            "\n"
            "```python\n"
            "unsqueezed_weights = weights.unsqueeze(-1).unsqueeze(-1)\n"
            "print(unsqueezed_weights.shape)\n"
            "```\n"
            "\n"
            "Result:\n"
            "\n"
            "```text\n"
            "(3, 1, 1)\n"
            "```\n"
            "\n"
            "That shape is compatible with `(3, 5, 5)`. The channel dimension matches exactly, while "
            "the two `1` dimensions can broadcast across rows and columns.\n"
            "\n"
            "For a batch shaped `(2, 3, 5, 5)`, the same `(3, 1, 1)` weights can still broadcast because "
            "the missing leading dimension is treated compatibly when shapes are right-aligned.\n"
            "\n"
            "Broadcasting becomes extremely important later when we work with batches, model parameters, "
            "normalization, and vectorized loss calculations.\n"
            "\n"
            "{{exercise:M03.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Named tensors: why dimension meaning matters\n"
            "\n"
            "A tensor's shape tells us the size of each dimension, but it does not automatically tell us "
            "what each axis **means**.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "(2, 3, 5, 5)\n"
            "```\n"
            "\n"
            "might mean:\n"
            "\n"
            "```text\n"
            "(batch, channels, rows, columns)\n"
            "```\n"
            "\n"
            "If you forget that ordering, an otherwise valid-looking operation may be applied to the "
            "wrong dimension.\n"
            "\n"
            "The source chapter introduces **named tensors** as an experimental/prototype idea for "
            "attaching semantic names such as `channels`, `rows`, and `columns` to tensor dimensions.\n"
            "\n"
            "Example from that model:\n"
            "\n"
            "```python\n"
            "weights_named = torch.tensor(\n"
            "    [0.2126, 0.7152, 0.0722],\n"
            "    names=['channels'],\n"
            ")\n"
            "```\n"
            "\n"
            "and a tensor may be refined with dimension names before alignment and reduction.\n"
            "\n"
            "The chapter ultimately continues with **unnamed tensors** because the feature is presented "
            "there as experimental. The important educational point remains valuable even if you do not "
            "use named tensors:\n"
            "\n"
            "> **Always know what each tensor dimension represents. Shape correctness is not the same "
            "as semantic correctness.**\n"
            "\n"
            "A useful habit is to comment important shapes explicitly:\n"
            "\n"
            "```python\n"
            "batch_t = torch.randn(2, 3, 5, 5)  # [batch, channels, height, width]\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Tensor element types and `dtype`\n"
            "\n"
            "All elements inside a standard dense tensor have the same numerical type. PyTorch stores "
            "that type in the tensor's `dtype`.\n"
            "\n"
            "Different dtypes trade off numerical range, precision, memory, and compatibility with "
            "particular operations.\n"
            "\n"
            "Common types from the chapter include:\n"
            "\n"
            "| PyTorch dtype | Meaning |\n"
            "|---|---|\n"
            "| `torch.float32` / `torch.float` | 32-bit floating point |\n"
            "| `torch.float64` / `torch.double` | 64-bit floating point |\n"
            "| `torch.float16` / `torch.half` | 16-bit floating point |\n"
            "| `torch.bfloat16` | 16-bit brain floating point format |\n"
            "| `torch.int8` | signed 8-bit integer |\n"
            "| `torch.uint8` | unsigned 8-bit integer |\n"
            "| `torch.int16` / `torch.short` | signed 16-bit integer |\n"
            "| `torch.int32` / `torch.int` | signed 32-bit integer |\n"
            "| `torch.int64` / `torch.long` | signed 64-bit integer |\n"
            "| `torch.bool` | Boolean values |\n"
            "\n"
            "The chapter notes that 32-bit floating point is the standard default for floating-point "
            "tensor work in PyTorch and that neural-network computations commonly use it.\n"
            "\n"
            "### Explicitly choose a dtype\n"
            "\n"
            "```python\n"
            "double_points = torch.ones(10, 2, dtype=torch.double)\n"
            "short_points = torch.tensor([[1, 2], [3, 4]], dtype=torch.short)\n"
            "\n"
            "print(short_points.dtype)\n"
            "```\n"
            "\n"
            "### Convert an existing tensor\n"
            "\n"
            "You can use dtype-specific convenience methods:\n"
            "\n"
            "```python\n"
            "double_points = torch.zeros(10, 2).double()\n"
            "```\n"
            "\n"
            "or the more general `to()` method:\n"
            "\n"
            "```python\n"
            "double_points = torch.zeros(10, 2).to(torch.double)\n"
            "short_points = torch.ones(10, 2).to(dtype=torch.short)\n"
            "```\n"
            "\n"
            "### Why `int64` appears often\n"
            "\n"
            "The chapter highlights that tensors used as indices are expected to use 64-bit integer "
            "values in common indexing situations. Integer literals passed to `torch.tensor()` also "
            "commonly produce an `int64` tensor by default.\n"
            "\n"
            "### Boolean tensors\n"
            "\n"
            "Comparisons produce Boolean tensors:\n"
            "\n"
            "```python\n"
            "points > 1.0\n"
            "```\n"
            "\n"
            "Each element tells us whether the corresponding predicate is true or false.\n"
            "\n"
            "### Mixed dtypes\n"
            "\n"
            "When types are mixed in an operation, PyTorch may promote values to a larger compatible "
            "type. If memory and compute precision matter, it is important to know the dtypes of the "
            "operands rather than assume they remain unchanged.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Navigating the tensor API\n"
            "\n"
            "PyTorch provides a very large tensor API. You do not need to memorize every function. "
            "Instead, learn the major families of operations and how to discover what you need.\n"
            "\n"
            "The chapter organizes tensor functionality into categories such as:\n"
            "\n"
            "- **creation** — `ones`, `zeros`, `rand`, `from_numpy`,\n"
            "- **indexing/slicing/joining/mutating** — operations that select or rearrange data,\n"
            "- **mathematical operations** — numerical computations,\n"
            "- **pointwise operations** — one independent operation per element, such as `abs` or `cos`,\n"
            "- **reductions** — aggregate values such as `mean`, `std`, or norms,\n"
            "- **comparisons** — predicates and extrema,\n"
            "- **spectral operations** — frequency-domain computations,\n"
            "- **linear algebra operations** — vector and matrix routines,\n"
            "- **random sampling** — values drawn from probability distributions,\n"
            "- **serialization** — saving and loading,\n"
            "- **parallelism controls** — execution settings for CPU work.\n"
            "\n"
            "### Function form vs. method form\n"
            "\n"
            "Many operations are available both from the `torch` namespace and as tensor methods.\n"
            "\n"
            "These are conceptually equivalent:\n"
            "\n"
            "```python\n"
            "a = torch.ones(3, 2)\n"
            "\n"
            "a_t_1 = torch.transpose(a, 0, 1)\n"
            "a_t_2 = a.transpose(0, 1)\n"
            "```\n"
            "\n"
            "One of the most useful professional skills is not memorizing APIs, but becoming comfortable "
            "reading tensor shapes, testing small examples interactively, and consulting documentation "
            "when you need a specific operation.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Storage and views: what a tensor really points to\n"
            "\n"
            "Now we reach one of the most valuable low-level ideas in the chapter.\n"
            "\n"
            "A tensor object is not merely a bag of numbers. Conceptually, the chapter explains a tensor "
            "as a **view over an underlying one-dimensional storage of numerical values**.\n"
            "\n"
            "A 2D tensor such as:\n"
            "\n"
            "```python\n"
            "points = torch.tensor([\n"
            "    [4.0, 1.0],\n"
            "    [5.0, 3.0],\n"
            "    [2.0, 1.0],\n"
            "])\n"
            "```\n"
            "\n"
            "may be conceptually stored as a one-dimensional block:\n"
            "\n"
            "```text\n"
            "[4.0, 1.0, 5.0, 3.0, 2.0, 1.0]\n"
            "```\n"
            "\n"
            "The tensor metadata tells PyTorch how to interpret those values as rows and columns.\n"
            "\n"
            "[[IMAGE_NEEDED: Python objects versus tensor storage | "
            "A side-by-side diagram showing a Python list as references to individually boxed numeric "
            "objects and a tensor as a compact homogeneous contiguous block of unboxed numeric values | "
            "Learner should notice why tensors are more memory- and computation-friendly for large "
            "numerical collections]]\n"
            "\n"
            "### Views can share data\n"
            "\n"
            "When we do:\n"
            "\n"
            "```python\n"
            "second_point = points[1]\n"
            "```\n"
            "\n"
            "PyTorch can create a smaller tensor that refers to the **same underlying data** rather than "
            "copying the values into a new allocation.\n"
            "\n"
            "That is efficient—but it has an important consequence:\n"
            "\n"
            "```python\n"
            "points = torch.tensor([\n"
            "    [4.0, 1.0],\n"
            "    [5.0, 3.0],\n"
            "    [2.0, 1.0],\n"
            "])\n"
            "\n"
            "second_point = points[1]\n"
            "second_point[0] = 10.0\n"
            "\n"
            "print(points)\n"
            "```\n"
            "\n"
            "The original tensor changes because both tensors refer to shared data.\n"
            "\n"
            "### Use `clone()` when you need independence\n"
            "\n"
            "```python\n"
            "second_point = points[1].clone()\n"
            "second_point[0] = 10.0\n"
            "```\n"
            "\n"
            "Now the cloned tensor owns independent data, so changing it does not alter the original "
            "tensor.\n"
            "\n"
            "This distinction between **view** and **copy** is critical when debugging unexpected "
            "mutations and when writing memory-efficient code.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. In-place operations\n"
            "\n"
            "PyTorch uses a clear naming convention for many operations that modify a tensor directly: "
            "their method name ends in an underscore.\n"
            "\n"
            "For example:\n"
            "\n"
            "```python\n"
            "a = torch.ones(3, 2)\n"
            "a.zero_()\n"
            "```\n"
            "\n"
            "`zero_()` modifies `a` in place rather than returning a separate tensor filled with zeros.\n"
            "\n"
            "A useful convention to remember is:\n"
            "\n"
            "```text\n"
            "operation()   -> usually returns a result without mutating the source\n"
            "operation_()  -> modifies the tensor in place\n"
            "```\n"
            "\n"
            "In-place operations can save allocations, but they also make shared-storage behavior more "
            "important. If multiple tensor views refer to the same underlying data, mutating one may "
            "affect another.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Shape, storage offset, and stride\n"
            "\n"
            "A tensor view can be defined by combining its underlying storage with metadata describing "
            "how to interpret that storage. Three ideas are central in the chapter:\n"
            "\n"
            "- **size / shape** — how many elements exist along each dimension,\n"
            "- **storage offset** — where this tensor's first element begins inside the shared storage,\n"
            "- **stride** — how many storage positions to skip when moving by one index along each dimension.\n"
            "\n"
            "For our `(3, 2)` point tensor, a typical stride is:\n"
            "\n"
            "```text\n"
            "(2, 1)\n"
            "```\n"
            "\n"
            "Interpretation:\n"
            "\n"
            "- move one row down -> skip 2 storage elements,\n"
            "- move one column right -> skip 1 storage element.\n"
            "\n"
            "For a 2D tensor, the chapter gives the conceptual storage index formula:\n"
            "\n"
            "```text\n"
            "storage_offset + stride[0] * i + stride[1] * j\n"
            "```\n"
            "\n"
            "This metadata indirection is powerful because operations can sometimes change **how the "
            "same memory is viewed** without copying or rearranging the actual values.\n"
            "\n"
            "[[IMAGE_NEEDED: Tensor storage with size, offset, and stride | "
            "A one-dimensional storage block with indices, plus two tensor views laid over it; annotate "
            "one view with shape, storage offset, and per-dimension strides | Learner should notice that "
            "tensor indexing is translated into positions in shared storage using metadata]]\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Transpose, stride, and contiguity\n"
            "\n"
            "Transposing a matrix swaps dimensions. In PyTorch:\n"
            "\n"
            "```python\n"
            "points = torch.tensor([\n"
            "    [4.0, 1.0],\n"
            "    [5.0, 3.0],\n"
            "    [2.0, 1.0],\n"
            "])\n"
            "\n"
            "points_t = points.t()\n"
            "```\n"
            "\n"
            "Original shape:\n"
            "\n"
            "```text\n"
            "(3, 2)\n"
            "```\n"
            "\n"
            "Transposed shape:\n"
            "\n"
            "```text\n"
            "(2, 3)\n"
            "```\n"
            "\n"
            "The important implementation idea is that PyTorch can perform this transpose by changing "
            "tensor metadata—especially stride—rather than immediately copying every element into a new "
            "layout.\n"
            "\n"
            "For example, the original may have stride:\n"
            "\n"
            "```text\n"
            "(2, 1)\n"
            "```\n"
            "\n"
            "while the transpose may have:\n"
            "\n"
            "```text\n"
            "(1, 2)\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Transpose without copying | "
            "A diagram showing one shared storage block referenced by an original 3x2 tensor and a "
            "transposed 2x3 tensor, with different stride arrows for each | Learner should notice that "
            "the apparent matrix layout can change while the underlying storage remains the same]]\n"
            "\n"
            "### Higher-dimensional transpose\n"
            "\n"
            "PyTorch can swap selected dimensions in tensors with more than two axes:\n"
            "\n"
            "```python\n"
            "some_t = torch.ones(3, 4, 5)\n"
            "transpose_t = some_t.transpose(0, 2)\n"
            "\n"
            "print(transpose_t.shape)  # (5, 4, 3)\n"
            "```\n"
            "\n"
            "### What does contiguous mean?\n"
            "\n"
            "A tensor is **contiguous** when its logical ordering matches a straightforward sequential "
            "layout in memory according to PyTorch's expected row-major style.\n"
            "\n"
            "The original points tensor may be contiguous:\n"
            "\n"
            "```python\n"
            "points.is_contiguous()\n"
            "```\n"
            "\n"
            "while its transpose may not be:\n"
            "\n"
            "```python\n"
            "points_t.is_contiguous()\n"
            "```\n"
            "\n"
            "Some operations require contiguous memory. You can request a contiguous version with:\n"
            "\n"
            "```python\n"
            "points_t_cont = points_t.contiguous()\n"
            "```\n"
            "\n"
            "If the tensor is already contiguous, this does not needlessly rearrange it. If it is not, "
            "PyTorch creates a new layout whose storage order matches the tensor's logical order.\n"
            "\n"
            "The key idea is:\n"
            "\n"
            "> **Shape describes what the tensor looks like; stride describes how that logical tensor "
            "walks through memory.**\n"
            "\n"
            "{{exercise:M03.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Moving tensors to the GPU\n"
            "\n"
            "A PyTorch tensor has not only a `dtype`, but also a **device**—the processor/memory location "
            "where its data lives.\n"
            "\n"
            "The chapter explains that tensor computations can be moved from CPU memory to supported "
            "accelerator memory, with CUDA GPUs as a central example.\n"
            "\n"
            "### Create directly on a CUDA device\n"
            "\n"
            "```python\n"
            "points_gpu = torch.tensor(\n"
            "    [[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]],\n"
            "    device='cuda',\n"
            ")\n"
            "```\n"
            "\n"
            "### Move an existing tensor\n"
            "\n"
            "```python\n"
            "points_gpu = points.to(device='cuda')\n"
            "```\n"
            "\n"
            "Once data is on the GPU, operations on that tensor can be performed there:\n"
            "\n"
            "```python\n"
            "points_gpu = points_gpu * 2\n"
            "points_gpu = points_gpu + 4\n"
            "```\n"
            "\n"
            "The result remains on the GPU until explicitly moved back:\n"
            "\n"
            "```python\n"
            "points_cpu = points_gpu.to(device='cpu')\n"
            "```\n"
            "\n"
            "The chapter also shows convenience methods:\n"
            "\n"
            "```python\n"
            "points_gpu = points.cuda()\n"
            "points_cpu = points_gpu.cpu()\n"
            "```\n"
            "\n"
            "### Device and dtype together\n"
            "\n"
            "`to()` is especially useful because it can control both placement and type:\n"
            "\n"
            "```python\n"
            "x = x.to(device='cuda', dtype=torch.float32)\n"
            "```\n"
            "\n"
            "### Important practical rule\n"
            "\n"
            "Moving data between CPU and GPU has a cost. If every small operation copies data back and "
            "forth, transfer overhead can erase the benefit of GPU computation. The chapter's examples "
            "show the intended pattern: transfer the tensor, perform multiple operations on that device, "
            "and move results only when needed.\n"
            "\n"
            "[[IMAGE_NEEDED: CPU-to-GPU tensor workflow | "
            "A diagram showing a tensor copied from CPU RAM to GPU memory, several operations occurring "
            "on the GPU while the data remains there, and an explicit transfer back to CPU at the end | "
            "Learner should notice that device transfer and device computation are separate actions]]\n"
            "\n"
            "---\n"
            "\n"

            "## 13. NumPy interoperability\n"
            "\n"
            "NumPy is central to the scientific Python ecosystem, so PyTorch is designed to interoperate "
            "efficiently with NumPy arrays.\n"
            "\n"
            "### Tensor to NumPy\n"
            "\n"
            "```python\n"
            "points = torch.ones(3, 4)\n"
            "points_np = points.numpy()\n"
            "```\n"
            "\n"
            "For a CPU tensor, the chapter explains that the NumPy array can share the same underlying "
            "buffer with the tensor. That makes the conversion cheap—but introduces shared mutation.\n"
            "\n"
            "If you modify the shared NumPy array, the PyTorch tensor may reflect that change because "
            "they refer to the same data.\n"
            "\n"
            "### NumPy to tensor\n"
            "\n"
            "```python\n"
            "points_from_np = torch.from_numpy(points_np)\n"
            "```\n"
            "\n"
            "Again, memory can be shared rather than copied.\n"
            "\n"
            "### Important dtype difference\n"
            "\n"
            "The source chapter notes an important default difference:\n"
            "\n"
            "- PyTorch floating tensors commonly default to 32-bit floating point,\n"
            "- NumPy floating arrays commonly default to 64-bit floating point.\n"
            "\n"
            "So after conversion, always inspect dtype if your model or performance assumptions require "
            "`float32`.\n"
            "\n"
            "### GPU tensors need special treatment\n"
            "\n"
            "NumPy arrays live in CPU memory. A tensor on a GPU cannot simply expose its GPU storage as "
            "a normal NumPy array. The data has to be made available on the CPU first.\n"
            "\n"
            "The broader lesson is:\n"
            "\n"
            "> **PyTorch and NumPy work closely together, but always know whether data is shared or copied, "
            "what dtype you have, and which device owns the memory.**\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Dense tensors are not the only possible tensor implementation\n"
            "\n"
            "For most of this course, a tensor means the dense multidimensional arrays we have been using. "
            "The chapter briefly looks deeper into PyTorch's design: the user-facing tensor API can be "
            "implemented by different backends and memory strategies.\n"
            "\n"
            "Examples mentioned in the source include:\n"
            "\n"
            "- tensors on different hardware devices,\n"
            "- sparse tensors that store nonzero values plus index information,\n"
            "- backend dispatch that routes operations to the appropriate implementation.\n"
            "\n"
            "You do not need to master PyTorch dispatch internals now. The important architectural idea is:\n"
            "\n"
            "> **Your Python tensor operation can remain conceptually similar while PyTorch dispatches it "
            "to an implementation suitable for the tensor's dtype, device, and layout.**\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Saving and loading tensors\n"
            "\n"
            "If a tensor contains valuable data, we may want to persist it rather than rebuild it every "
            "time a program starts.\n"
            "\n"
            "### PyTorch-native serialization\n"
            "\n"
            "```python\n"
            "torch.save(points, '../data/ourpoints.t')\n"
            "```\n"
            "\n"
            "Load it again with:\n"
            "\n"
            "```python\n"
            "points = torch.load('../data/ourpoints.t')\n"
            "```\n"
            "\n"
            "The same functions can work with file objects.\n"
            "\n"
            "This is convenient when the data will be consumed by PyTorch again, but the chapter notes "
            "that a PyTorch-specific serialized file is not automatically an interoperable data format "
            "for unrelated software.\n"
            "\n"
            "### HDF5 for interoperable multidimensional data\n"
            "\n"
            "The chapter introduces HDF5 as a portable format for multidimensional arrays, accessible "
            "from Python through `h5py`.\n"
            "\n"
            "A tensor can first be exposed as NumPy data and stored in an HDF5 dataset:\n"
            "\n"
            "```python\n"
            "import h5py\n"
            "\n"
            "f = h5py.File('../data/ourpoints.hdf5', 'w')\n"
            "dset = f.create_dataset('coords', data=points.numpy())\n"
            "f.close()\n"
            "```\n"
            "\n"
            "A useful property highlighted by the source is that HDF5 datasets can be sliced while the "
            "bulk of the data remains on disk. You can load only the region you need:\n"
            "\n"
            "```python\n"
            "f = h5py.File('../data/ourpoints.hdf5', 'r')\n"
            "dset = f['coords']\n"
            "last_points = torch.from_numpy(dset[-2:])\n"
            "f.close()\n"
            "```\n"
            "\n"
            "The lesson is not that every project needs HDF5. It is that **serialization format should "
            "match how the data will be consumed**. PyTorch-native files are simple for PyTorch workflows; "
            "portable array formats are useful when other tools must read the data too.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: A tensor is just a Python list with brackets\n"
            "\n"
            "> Tensors and lists are basically the same storage structure.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A tensor stores homogeneous numerical data using an efficient low-level memory representation "
            "and provides optimized multidimensional numerical operations. Python lists are general-purpose "
            "collections of object references.\n"
            "\n"
            "### Misconception 2: Every slice or transpose copies all the data\n"
            "\n"
            "> If I create `points[1]` or `points.t()`, PyTorch always allocates and copies the values.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Many such operations can create views that share the same underlying storage and change only "
            "metadata such as size, offset, and stride.\n"
            "\n"
            "### Misconception 3: Same shape means same meaning\n"
            "\n"
            "> If two tensors have compatible shapes, the computation must be conceptually correct.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Shapes encode sizes, not semantics. A dimension could mean batch, channels, time, or something "
            "else. Broadcasting can produce a numerically valid result even when the operation targets the "
            "wrong conceptual axis.\n"
            "\n"
            "### Misconception 4: Moving a tensor to the GPU makes every program faster\n"
            "\n"
            "> Any tensor operation should be faster if I call `.cuda()` first.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Device transfers have overhead, and GPUs are most helpful when enough parallel numerical work "
            "exists to justify that overhead.\n"
            "\n"
            "### Misconception 5: NumPy conversion always creates an independent copy\n"
            "\n"
            "> If I call `.numpy()`, modifying one object cannot affect the other.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "For CPU tensors, PyTorch and NumPy can share the same underlying memory buffer. A mutation can "
            "therefore be visible through both objects.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Tensor | Multidimensional homogeneous numerical array used as PyTorch's core data structure. |\n"
            "| Scalar | Zero-dimensional tensor containing one value. |\n"
            "| Dimension / axis | One direction along which a tensor is indexed. |\n"
            "| Shape / size | Number of elements along each tensor dimension. |\n"
            "| Indexing | Selecting values using integer positions. |\n"
            "| Slicing | Selecting ranges of values along one or more dimensions. |\n"
            "| Broadcasting | Rules allowing element-wise operations between compatible shapes. |\n"
            "| `dtype` | Numeric data type stored by tensor elements. |\n"
            "| View | Tensor interpretation that can share underlying storage with another tensor. |\n"
            "| Clone | New tensor with independent copied data. |\n"
            "| Storage | Conceptual one-dimensional memory region holding tensor values. |\n"
            "| Storage offset | Position in storage corresponding to the first logical element of a tensor view. |\n"
            "| Stride | Number of storage elements skipped when advancing one index along a dimension. |\n"
            "| Contiguous tensor | Tensor whose logical ordering follows a direct sequential memory layout. |\n"
            "| In-place operation | Operation that modifies its input tensor; commonly marked with a trailing `_`. |\n"
            "| Device | Hardware/memory location where tensor data is stored, such as CPU or CUDA GPU. |\n"
            "| NumPy ndarray | NumPy's multidimensional array type, interoperable with PyTorch tensors. |\n"
            "| Serialization | Saving data structures to persistent storage so they can be loaded later. |\n"
            "| HDF5 | Portable hierarchical format for multidimensional array data. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why must real-world data eventually become numbers before a neural network can process it?\n"
            "2. What does the shape `(4, 3, 3)` tell you about a tensor?\n"
            "3. What is the difference between `points[1]` and `points[1:, :]` in terms of resulting dimensions?\n"
            "4. What two rules make dimensions compatible for broadcasting?\n"
            "5. Why can `(3, 1, 1)` channel weights multiply an image tensor shaped `(3, 5, 5)`?\n"
            "6. Why is `dtype` important for memory, precision, and valid operations?\n"
            "7. What does the trailing underscore in a method such as `zero_()` communicate?\n"
            "8. What is the difference between a tensor view and a clone?\n"
            "9. What do storage offset and stride tell PyTorch?\n"
            "10. How can a transpose change a tensor without immediately copying all values?\n"
            "11. Why can a transposed tensor be noncontiguous?\n"
            "12. What does `.contiguous()` do when needed?\n"
            "13. What happens conceptually when `x.to(device='cuda')` is called?\n"
            "14. Why should repeated CPU/GPU transfers be avoided?\n"
            "15. When can a NumPy array and PyTorch tensor share memory?\n"
            "16. Why might HDF5 be chosen instead of a PyTorch-only serialized file?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A PyTorch tensor is more than a multidimensional collection of numbers: it combines "
            "numerical data with shape, dtype, device, and memory-layout metadata, allowing the same "
            "underlying data to be indexed, broadcast, viewed, transposed, moved across hardware, and "
            "shared with the wider scientific Python ecosystem efficiently.**\n"
        ),

        "estimated_minutes": 165,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "world-as-numbers",
                "title": "Deep learning sees the world as numbers",
                "order": 1,
            },
            {
                "id": "tensor-basics",
                "title": "Tensors: multidimensional arrays",
                "order": 2,
            },
            {
                "id": "indexing-and-slicing",
                "title": "Indexing and slicing tensors",
                "order": 3,
            },
            {
                "id": "broadcasting",
                "title": "Broadcasting",
                "order": 4,
            },
            {
                "id": "named-tensors",
                "title": "Named tensors",
                "order": 5,
            },
            {
                "id": "dtype",
                "title": "Tensor element types and dtype",
                "order": 6,
            },
            {
                "id": "tensor-api",
                "title": "Navigating the tensor API",
                "order": 7,
            },
            {
                "id": "storage-and-views",
                "title": "Storage and views",
                "order": 8,
            },
            {
                "id": "in-place-operations",
                "title": "In-place operations",
                "order": 9,
            },
            {
                "id": "size-offset-stride",
                "title": "Shape, storage offset, and stride",
                "order": 10,
            },
            {
                "id": "transpose-and-contiguity",
                "title": "Transpose, stride, and contiguity",
                "order": 11,
            },
            {
                "id": "gpu-devices",
                "title": "Moving tensors to the GPU",
                "order": 12,
            },
            {
                "id": "numpy-interoperability",
                "title": "NumPy interoperability",
                "order": 13,
            },
            {
                "id": "generalized-tensors",
                "title": "Generalized tensor implementations",
                "order": 14,
            },
            {
                "id": "serialization",
                "title": "Saving and loading tensors",
                "order": 15,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M03.L01.EX01",
            "title": "Build and Read Tensor Shapes",
            "lesson_code": "M03.L01",
            "section_id": "tensor-basics",
            "placement": "after_section",
            "description": (
                "Practice creating tensors and interpreting dimensions, shapes, and indexing."
            ),
            "instructions": (
                "1. Create a tensor containing the three 2D points `(4, 1)`, `(5, 3)`, and `(2, 1)`.\n"
                "2. Print its shape and explain what each dimension means.\n"
                "3. Retrieve the complete second point.\n"
                "4. Retrieve only the y-coordinate of the first point.\n"
                "5. Create a tensor of zeros with shape `(4, 3, 2)` and explain how many dimensions "
                "it has and how many total scalar values it contains.\n"
                "6. Add a leading size-1 dimension to the points tensor using `unsqueeze(0)` and "
                "predict its new shape before running the code."
            ),
            "expected_output": (
                "Executable PyTorch code plus explanations of the resulting tensor shapes and indices."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "tensor-creation",
                "shape",
                "indexing",
                "unsqueeze",
            ],
        },
        {
            "id": "M03.L01.EX02",
            "title": "Predict Broadcasting Before Running It",
            "lesson_code": "M03.L01",
            "section_id": "broadcasting",
            "placement": "after_section",
            "description": (
                "Practice checking shape compatibility using PyTorch broadcasting rules."
            ),
            "instructions": (
                "For each pair of shapes below, predict whether element-wise broadcasting is possible. "
                "If it is possible, state the output shape. Explain your reasoning by aligning shapes "
                "from the right.\n"
                "1. `(3, 4)` and `(4,)`\n"
                "2. `(3, 1)` and `(1, 5)`\n"
                "3. `(2, 3, 5, 5)` and `(3, 1, 1)`\n"
                "4. `(2, 4)` and `(3, 4)`\n"
                "5. `(1, 3, 1)` and `(4, 1, 5)`\n"
                "Then verify at least three cases with small `torch.ones(...)` tensors."
            ),
            "expected_output": (
                "Five compatibility decisions with predicted result shapes where valid, plus code "
                "verifying at least three predictions."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "broadcasting",
                "shape-reasoning",
                "tensor-operations",
            ],
        },
        {
            "id": "M03.L01.EX03",
            "title": "Investigate Views, Strides, and Copies",
            "lesson_code": "M03.L01",
            "section_id": "transpose-and-contiguity",
            "placement": "after_section",
            "description": (
                "Use a small tensor to observe shared views, transpose metadata, contiguity, and cloning."
            ),
            "instructions": (
                "1. Create the `(3, 2)` points tensor used in the lesson.\n"
                "2. Print `points.shape` and `points.stride()`.\n"
                "3. Create `second_point = points[1]`, then print its shape, storage offset, and stride.\n"
                "4. Change one value through `second_point` and observe whether `points` changes.\n"
                "5. Repeat using `points[1].clone()` and explain the difference.\n"
                "6. Create `points_t = points.t()`. Print its shape, stride, and `is_contiguous()`.\n"
                "7. Call `.contiguous()` on the transpose and compare the stride before and after.\n"
                "8. Explain in your own words why transpose can be cheap before calling `.contiguous()`."
            ),
            "expected_output": (
                "A short notebook or script showing tensor metadata before and after slicing, cloning, "
                "transposing, and making a tensor contiguous, followed by a written explanation."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "views",
                "clone",
                "stride",
                "storage-offset",
                "transpose",
                "contiguity",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M03.L01.QZ01",
        "title": "It Starts with a Tensor — Knowledge Check",
        "lesson_code": "M03.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M03.L01.Q01",
                "section_id": "tensor-basics",
                "question": "What does the shape `(3, 2)` most directly tell you about a tensor?",
                "options": [
                    "It stores only three scalar values.",
                    "It has two dimensions with sizes 3 and 2.",
                    "It must be stored on a GPU.",
                    "It uses 3-bit integers and 2-bit floats.",
                ],
                "correct": 1,
                "explanation": (
                    "Shape lists the number of elements along each dimension. `(3, 2)` therefore "
                    "describes a two-dimensional tensor with 3 entries along dimension 0 and 2 along dimension 1."
                ),
            },
            {
                "id": "M03.L01.Q02",
                "section_id": "indexing-and-slicing",
                "question": "What does `points[None]` do to a tensor?",
                "options": [
                    "Deletes the tensor.",
                    "Adds a new dimension of size 1.",
                    "Moves the tensor to the GPU.",
                    "Converts all values to `None`.",
                ],
                "correct": 1,
                "explanation": (
                    "`None` in this indexing position inserts a size-1 dimension, similar to "
                    "`points.unsqueeze(0)`."
                ),
            },
            {
                "id": "M03.L01.Q03",
                "section_id": "broadcasting",
                "question": (
                    "When checking two dimensions for broadcasting compatibility, which condition is valid?"
                ),
                "options": [
                    "They must always be different.",
                    "They must both be prime numbers.",
                    "They are compatible if they are equal or if one of them is 1.",
                    "They are compatible only if both are 1.",
                ],
                "correct": 2,
                "explanation": (
                    "Broadcasting compares aligned dimensions from the right. Two dimensions are "
                    "compatible when their sizes match or one of them has size 1."
                ),
            },
            {
                "id": "M03.L01.Q04",
                "section_id": "dtype",
                "question": "What does a tensor's `dtype` describe?",
                "options": [
                    "Its filesystem location.",
                    "The numerical type used for its elements.",
                    "The number of model layers.",
                    "Whether the tensor is a view.",
                ],
                "correct": 1,
                "explanation": (
                    "`dtype` specifies the numerical representation of tensor elements, such as "
                    "float32, int64, or bool."
                ),
            },
            {
                "id": "M03.L01.Q05",
                "section_id": "in-place-operations",
                "question": "What does a trailing underscore commonly indicate in a PyTorch method such as `zero_()`?",
                "options": [
                    "The method is deprecated.",
                    "The method operates in place and mutates the tensor.",
                    "The method runs only on the GPU.",
                    "The method converts the tensor to NumPy.",
                ],
                "correct": 1,
                "explanation": (
                    "PyTorch commonly uses a trailing underscore to signal an in-place operation that "
                    "modifies the tensor rather than leaving the source unchanged."
                ),
            },
            {
                "id": "M03.L01.Q06",
                "section_id": "storage-and-views",
                "question": (
                    "Why might changing `second_point = points[1]` also change `points`?"
                ),
                "options": [
                    "PyTorch automatically retrains tensors.",
                    "`second_point` can be a view sharing the same underlying storage.",
                    "Every tensor in a program always shares all values.",
                    "Indexing converts data to global variables.",
                ],
                "correct": 1,
                "explanation": (
                    "Many indexing operations return views. The view and source can reference the same "
                    "underlying memory, so mutation through one can be visible through the other."
                ),
            },
            {
                "id": "M03.L01.Q07",
                "section_id": "size-offset-stride",
                "question": "What does stride tell PyTorch?",
                "options": [
                    "How many epochs a model should train.",
                    "How many storage elements to step over when advancing along each tensor dimension.",
                    "Which optimizer to use.",
                    "How many files are in a dataset.",
                ],
                "correct": 1,
                "explanation": (
                    "Stride describes how logical index movement maps to movement through underlying storage."
                ),
            },
            {
                "id": "M03.L01.Q08",
                "section_id": "transpose-and-contiguity",
                "question": "Why can a transpose be inexpensive?",
                "options": [
                    "It always deletes half of the values.",
                    "It can reuse the same storage while changing shape and stride metadata.",
                    "It converts floating point to integers.",
                    "It skips all numerical operations permanently.",
                ],
                "correct": 1,
                "explanation": (
                    "A transpose can often be represented as another view of the same storage with "
                    "different shape and stride values rather than by copying the data."
                ),
            },
            {
                "id": "M03.L01.Q09",
                "section_id": "gpu-devices",
                "question": "What does `x.to(device='cuda')` conceptually do?",
                "options": [
                    "Converts `x` into a Python list.",
                    "Places tensor data on a CUDA device so compatible operations can execute there.",
                    "Saves `x` to disk.",
                    "Automatically turns `x` into a neural network.",
                ],
                "correct": 1,
                "explanation": (
                    "The operation produces a tensor whose data is located on the selected CUDA device, "
                    "allowing tensor computations to use the GPU backend."
                ),
            },
            {
                "id": "M03.L01.Q10",
                "section_id": "numpy-interoperability",
                "question": (
                    "What important behavior can occur when converting a CPU PyTorch tensor to NumPy?"
                ),
                "options": [
                    "They can share the same underlying memory buffer.",
                    "The tensor is always deleted.",
                    "The NumPy array is automatically moved to a GPU.",
                    "The tensor becomes a string.",
                ],
                "correct": 0,
                "explanation": (
                    "For CPU data, PyTorch and NumPy can share the same buffer. This makes conversion "
                    "cheap but also means mutations may be visible from both sides."
                ),
            },
            {
                "id": "M03.L01.Q11",
                "section_id": "serialization",
                "question": "Why might HDF5 be preferred over `torch.save()` for some datasets?",
                "options": [
                    "HDF5 can be useful when data must be read interoperably by tools outside PyTorch.",
                    "HDF5 automatically trains models.",
                    "`torch.save()` cannot store tensors.",
                    "HDF5 requires every tensor to be on a GPU.",
                ],
                "correct": 0,
                "explanation": (
                    "PyTorch-native serialization is convenient inside PyTorch, while HDF5 is a broadly "
                    "supported multidimensional data format that may integrate better with other systems."
                ),
            },
            {
                "id": "M03.L01.Q12",
                "section_id": "transpose-and-contiguity",
                "type": "open",
                "question": (
                    "A tensor is transposed and becomes noncontiguous. Explain what changed conceptually "
                    "and why calling `.contiguous()` may allocate a new storage layout even though the "
                    "visible numerical values remain the same."
                ),
            },
        ],
        "passing_score": 70,
    },
}
