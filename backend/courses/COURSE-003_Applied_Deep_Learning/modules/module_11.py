"""M11.L01 — Combining Data Sources into a Unified Dataset.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 12.
Instructor-authored curriculum adaptation.

Quality standard:
- balanced quiz-answer positions
- production-oriented data-pipeline practices
- realistic study-time estimate
- learning checkpoints after dense sections
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M11.L01"
MODULE_ORDER = 11
MODULE_TITLE = "Real-World Data Pipelines for 3D Medical Imaging"
MODULE_DESCRIPTION = (
    "Transform raw LUNA CT files and annotations into a clean PyTorch Dataset by parsing "
    "multiple data sources, reconciling coordinates, loading volumetric scans, clipping "
    "Hounsfield Units, converting physical coordinates to voxel indexes, cropping fixed-size "
    "candidate volumes, caching expensive work, splitting training/validation data, and visualizing samples."
)

SOURCE_CHAPTER = 12
SOURCE_PAGES = "Chapter 12 (page range not provided in source excerpt)"


TOPIC = {
    "title": "Combining Data Sources into a Unified Dataset",
    "slug": "applied-deep-learning-m11-l01",
    "description": (
        "A practical, production-minded lesson on building a custom PyTorch data pipeline for "
        "3D CT data: raw-file loading, annotation reconciliation, coordinate transforms, candidate "
        "cropping, Dataset implementation, caching, validation splitting, and visual inspection."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 5.5,
    "skill_tags": [
        "data-engineering",
        "pytorch-dataset",
        "medical-imaging",
        "ct-scan",
        "luna16",
        "simpleitk",
        "hounsfield-units",
        "coordinate-systems",
        "xyz-to-irc",
        "candidate-cropping",
        "caching",
        "diskcache",
        "training-validation-split",
        "data-leakage",
        "visualization",
    ],
    "prerequisite_ids": ["M10.L01"],

    "lesson": {
        "title": "Combining Data Sources into a Unified Dataset",
        "content": (
            "# Combining Data Sources into a Unified Dataset\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M11.L01  \n"
            "> **Source:** *Deep Learning with PyTorch, Second Edition*, Chapter 12.  \n"
            "> **Study expectation:** about **5.5 hours** including code tracing, checkpoints, and exercises.\n\n"
            "This chapter is where the lung-cancer project stops being a diagram and becomes an actual data pipeline.\n\n"
            "The goal is simple to state but substantial to implement:\n\n"
            "> **Given raw CT scan files plus annotation files, return a clean PyTorch training sample.**\n\n"
            "That requires far more than calling `torch.tensor(...)`.\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "- Explain the raw LUNA file layout and the purpose of series UIDs.\n"
            "- Explain how candidate and annotation CSV files complement each other.\n"
            "- Build a unified candidate-information structure from multiple imperfect sources.\n"
            "- Explain why fuzzy coordinate matching is needed in the source dataset.\n"
            "- Load MetaIO CT scans with `SimpleITK` and convert them to NumPy arrays.\n"
            "- Explain Hounsfield Units and why the chapter clips values to `[-1000, 1000]`.\n"
            "- Distinguish patient-space `(X,Y,Z)` coordinates from array `(I,R,C)` coordinates.\n"
            "- Explain origin, voxel spacing, and direction matrices.\n"
            "- Convert XYZ coordinates into IRC indexes.\n"
            "- Crop a fixed-size 3D candidate volume around a nodule location.\n"
            "- Implement the required `Dataset.__len__` and `Dataset.__getitem__` methods.\n"
            "- Produce model-ready tensors with an explicit channel dimension.\n"
            "- Explain why caching matters in expensive data pipelines.\n"
            "- Distinguish in-memory caching from on-disk caching.\n"
            "- Explain cache invalidation risk when data-processing code changes.\n"
            "- Construct reproducible training/validation splits.\n"
            "- Recognize data leakage and patient-level splitting concerns.\n"
            "- Use visualization and sanity checks as debugging tools.\n\n"
            "---\n\n"

            "## 1. The real task: raw files → one training sample\n\n"
            "The chapter focuses on step 1 of the cancer-detection project: **data loading**.\n\n"
            "The final training sample must combine information from several places:\n\n"
            "```text\n"
            "raw CT volume (.mhd + .raw)\n"
            "          +\n"
            "candidate annotations (.csv)\n"
            "          +\n"
            "coordinate metadata\n"
            "          ↓\n"
            "candidate center in voxel coordinates\n"
            "          ↓\n"
            "fixed-size 3D crop\n"
            "          ↓\n"
            "PyTorch tensors + metadata\n"
            "```\n\n"
            '{{image:raw-ct-data-to-pytorch-sample}}'
            '\n\n'
            "This is a reusable engineering lesson: serious ML projects often require a substantial bridge between **source data** and **model input**.\n\n"
            "---\n\n"

            "## 2. Understand the raw CT file structure\n\n"
            "Each LUNA CT scan is represented by two files sharing one unique **series UID**:\n\n"
            "```text\n"
            "<series_uid>.mhd\n"
            "<series_uid>.raw\n"
            "```\n\n"
            "The `.mhd` file contains metadata, while `.raw` stores the volumetric values.\n\n"
            "The series UID acts as the stable key connecting:\n\n"
            "- the CT scan on disk,\n"
            "- candidate rows in the CSV data,\n"
            "- annotation rows,\n"
            "- debugging and visualization.\n\n"
            "A robust data pipeline needs this kind of unique sample identity. It lets you trace a bad training example all the way back to its original scan.\n\n"
            "---\n\n"

            "## 3. `candidates.csv`: the broad candidate list\n\n"
            "The chapter begins with the easier metadata file.\n\n"
            "Each candidate row contains:\n\n"
            "```text\n"
            "seriesuid, coordX, coordY, coordZ, class\n"
            "```\n\n"
            "The source reports roughly **551,000 candidate rows**, with only about **1,351 marked as actual nodules**.\n\n"
            "The `class` flag means:\n\n"
            "```text\n"
            "0 -> candidate is not a nodule\n"
            "1 -> candidate is a nodule\n"
            "```\n\n"
            "This already reveals a major future challenge: the raw candidate set is extremely imbalanced.\n\n"
            "The coordinates are given in real-world patient coordinates, not directly as NumPy array indexes.\n\n"
            "---\n\n"

            "## 4. `annotations.csv`: useful size information\n\n"
            "The annotation file contains a smaller set of known nodules with fields such as:\n\n"
            "```text\n"
            "seriesuid, coordX, coordY, coordZ, diameter_mm\n"
            "```\n\n"
            "Its added value is **diameter**.\n\n"
            "Nodule size matters because a validation set containing only unusually large or unusually small nodules would not represent the real problem well.\n\n"
            "The source therefore uses diameter information to help preserve a spread of nodule sizes.\n\n"
            "But there is a problem: candidate and annotation coordinates do not always match exactly.\n\n"
            "---\n\n"

            "## 5. Real-world data sources rarely line up perfectly\n\n"
            "Two files may describe the same nodule using slightly different coordinates.\n\n"
            "That means we cannot simply join rows using exact equality on `(x, y, z)`.\n\n"
            "The chapter instead performs approximate matching within the same series UID.\n\n"
            "A simplified idea is:\n\n"
            "```python\n"
            "for annotation_center, annotation_diameter in annotations_for_scan:\n"
            "    close_enough = True\n"
            "    for axis in range(3):\n"
            "        delta_mm = abs(candidate_center[axis] - annotation_center[axis])\n"
            "        if delta_mm > annotation_diameter / 4:\n"
            "            close_enough = False\n"
            "            break\n"
            "```\n\n"
            "This is a bounding-box-style closeness check rather than an exact Euclidean-distance match.\n\n"
            "[[IMAGE_NEEDED: Fuzzy matching two nearby annotation centers | Two nearly overlapping 3D coordinate points labeled "
            "candidate.csv and annotations.csv inside the same nodule-sized region | Learner should notice that noisy metadata may "
            "require domain-aware approximate matching rather than exact equality]]\n\n"
            "The broader lesson is important:\n\n"
            "> **Data unification often requires assumptions. Make them explicit so they can be revisited later.**\n\n"
            "---\n\n"

            "## 6. Create one clean candidate representation\n\n"
            "The source uses a named tuple:\n\n"
            "```python\n"
            "from collections import namedtuple\n\n"
            "CandidateInfoTuple = namedtuple(\n"
            "    'CandidateInfoTuple',\n"
            "    'isNodule_bool, diameter_mm, series_uid, center_xyz',\n"
            ")\n"
            "```\n\n"
            "This object is not yet a training sample. It is a **sanitized interface to messy metadata**.\n\n"
            "That separation is excellent engineering practice:\n\n"
            "```text\n"
            "raw CSV quirks\n"
            "      ↓\n"
            "clean candidate metadata\n"
            "      ↓\n"
            "CT extraction\n"
            "      ↓\n"
            "PyTorch Dataset\n"
            "      ↓\n"
            "training loop\n"
            "```\n\n"
            "Training code should not be cluttered with CSV parsing and fuzzy coordinate matching.\n\n"

            "### Learning checkpoint 1 — Metadata unification\n\n"
            "You should now be able to answer:\n\n"
            "1. Why are there two CSV sources?\n"
            "2. Why can't their coordinates always be joined exactly?\n"
            "3. What is the purpose of `CandidateInfoTuple`?\n"
            "4. Why should messy-data cleanup be isolated from training code?\n\n"
            "{{exercise:M11.L01.EX01}}\n\n"
            "---\n\n"

            "## 7. Filter metadata to scans actually present on disk\n\n"
            "The source supports partially downloaded datasets.\n\n"
            "It first discovers available `.mhd` files and builds a set of their series UIDs.\n\n"
            "Then candidate rows belonging to absent scans can be skipped when `require_on_disk=True`.\n\n"
            "This makes development practical when only some LUNA subsets have been downloaded.\n\n"
            "It is another useful pattern:\n\n"
            "> **Your metadata index should reflect which underlying assets are actually available.**\n\n"
            "---\n\n"

            "## 8. Load one CT scan with `SimpleITK`\n\n"
            "The chapter does not write a custom binary parser. It uses a library that already understands the medical-image format.\n\n"
            "```python\n"
            "import SimpleITK as sitk\n"
            "import numpy as np\n\n"
            "ct_mhd = sitk.ReadImage(mhd_path)\n"
            "ct_a = np.array(\n"
            "    sitk.GetArrayFromImage(ct_mhd),\n"
            "    dtype=np.float32,\n"
            ")\n"
            "```\n\n"
            "`SimpleITK` also follows the `.mhd` metadata to consume the associated `.raw` data.\n\n"
            "After conversion, `ct_a` is a 3D NumPy array.\n\n"
            "There is no explicit color/channel axis because the scan contains one scalar intensity per voxel.\n\n"
            "[[IMAGE_NEEDED: MetaIO files to CT array | A .mhd metadata file and .raw binary file enter SimpleITK and produce one "
            "D×H×W NumPy array plus origin/spacing/direction metadata | Learner should notice that the parser hides file-format complexity "
            "but the pipeline still needs to understand the meaning of the loaded data]]\n\n"
            "---\n\n"

            "## 9. Hounsfield Units: understand the values, not only the bits\n\n"
            "CT voxel intensities are expressed in **Hounsfield Units (HU)**.\n\n"
            "Useful reference points in the chapter are approximately:\n\n"
            "| Material | HU |\n"
            "|---|---:|\n"
            "| Air | -1000 |\n"
            "| Water | 0 |\n"
            "| Dense bone | around +1000 or higher |\n\n"
            "The exact physical relationship is more nuanced, but the model will consume HU values directly.\n\n"
            "The source clips extreme values:\n\n"
            "```python\n"
            "ct_a.clip(-1000, 1000, ct_a)\n"
            "```\n\n"
            "Why?\n\n"
            "- values below the useful range can represent scanner field-of-view artifacts,\n"
            "- extremely dense material is not central to the target task,\n"
            "- large irrelevant outliers can distort downstream statistics and optimization.\n\n"
            "[[IMAGE_NEEDED: Hounsfield Unit range | A horizontal HU scale marking air near -1000, water near 0, soft tissue around "
            "intermediate values, and dense bone around +1000, with clipping boundaries highlighted | Learner should notice why the "
            "chapter limits the working intensity range]]\n\n"
            "---\n\n"

            "## 10. Patient coordinates and array coordinates are not the same thing\n\n"
            "Candidate locations in the CSV files are given in physical `(X,Y,Z)` coordinates measured in millimeters.\n\n"
            "But NumPy cropping requires array coordinates:\n\n"
            "```text\n"
            "(I, R, C)\n"
            "= index, row, column\n"
            "```\n\n"
            "You cannot use millimeter coordinates directly as array indexes.\n\n"
            "[[IMAGE_NEEDED: XYZ patient coordinates versus IRC array coordinates | A CT volume shown with one physical patient-space "
            "XYZ coordinate system and a separate array-index IRC system, with different origins and axis conventions | Learner should "
            "notice that coordinate conversion is required before indexing the voxel array]]\n\n"
            "---\n\n"

            "## 11. Three pieces of metadata define the mapping\n\n"
            "The conversion depends on:\n\n"
            "### Origin\n\n"
            "Where the array is positioned in patient-space coordinates.\n\n"
            "### Voxel spacing\n\n"
            "The physical millimeters represented by one step along each axis.\n\n"
            "### Direction matrix\n\n"
            "A `3 × 3` matrix describing axis orientation, including possible flips/rotations.\n\n"
            "The `Ct` object stores them:\n\n"
            "```python\n"
            "self.origin_xyz = XyzTuple(*ct_mhd.GetOrigin())\n"
            "self.vxSize_xyz = XyzTuple(*ct_mhd.GetSpacing())\n"
            "self.direction_a = np.array(\n"
            "    ct_mhd.GetDirection()\n"
            ").reshape(3, 3)\n"
            "```\n\n"
            "These values are as important as the voxel intensities if we want to locate annotated structures correctly.\n\n"
            "---\n\n"

            "## 12. Voxels are often not cubes\n\n"
            "A CT might use spacing similar to:\n\n"
            "```text\n"
            "1.125 mm × 1.125 mm × 2.5 mm\n"
            "```\n\n"
            "That means one slice step may cover more physical distance than one row or column step.\n\n"
            "If visualized using equal-sized screen pixels without correction, anatomy can look compressed or stretched.\n\n"
            "This is not necessarily a loading bug. It can simply be a consequence of anisotropic voxel spacing.\n\n"
            "Knowing this prevents wasted debugging effort and becomes even more important when resampling or combining scans later.\n\n"
            "---\n\n"

            "## 13. Convert XYZ millimeters into IRC voxel indexes\n\n"
            "The chapter describes the forward IRC→XYZ process as:\n\n"
            "1. reorder IRC into CRI so axes align with XYZ,\n"
            "2. multiply indexes by voxel spacing,\n"
            "3. apply the direction matrix,\n"
            "4. add the origin.\n\n"
            "The inverse XYZ→IRC reverses those operations.\n\n"
            "The source implementation is:\n\n"
            "```python\n"
            "def xyz2irc(coord_xyz, origin_xyz, vxSize_xyz, direction_a):\n"
            "    origin_a = np.array(origin_xyz)\n"
            "    vxSize_a = np.array(vxSize_xyz)\n"
            "    coord_a = np.array(coord_xyz)\n\n"
            "    cri_a = (\n"
            "        (coord_a - origin_a)\n"
            "        @ np.linalg.inv(direction_a)\n"
            "    ) / vxSize_a\n\n"
            "    cri_a = np.round(cri_a)\n"
            "    return IrcTuple(\n"
            "        int(cri_a[2]),\n"
            "        int(cri_a[1]),\n"
            "        int(cri_a[0]),\n"
            "    )\n"
            "```\n\n"
            "The formulas are worth understanding conceptually, even if you later treat the utility function as a tested black box.\n\n"
            "{{exercise:M11.L01.EX02}}\n\n"
            "---\n\n"

            "## 14. Crop around the candidate instead of feeding the whole CT\n\n"
            "The cancer-relevant structure occupies a tiny fraction of the full volume.\n\n"
            "The source therefore extracts a fixed-size local crop centered on each candidate.\n\n"
            "Conceptually:\n\n"
            "```python\n"
            "center_irc = xyz2irc(...)\n\n"
            "for axis, center_val in enumerate(center_irc):\n"
            "    start = int(round(center_val - width_irc[axis] / 2))\n"
            "    end = start + width_irc[axis]\n"
            "    slice_list.append(slice(start, end))\n\n"
            "ct_chunk = self.hu_a[tuple(slice_list)]\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Candidate crop from CT volume | A full 3D CT volume with a small candidate center marker, then a zoomed "
            "rectangular 3D crop extracted around that center | Learner should notice that the classifier receives a focused local volume "
            "rather than the complete patient scan]]\n\n"
            "The source notes that production code must also handle edge cases where the crop would extend outside the CT boundaries.\n\n"
            "---\n\n"

            "## 15. Implement a custom PyTorch `Dataset`\n\n"
            "PyTorch asks for two required methods:\n\n"
            "```python\n"
            "def __len__(self):\n"
            "    ...\n\n"
            "def __getitem__(self, ndx):\n"
            "    ...\n"
            "```\n\n"
            "`__len__` returns the number of samples.\n\n"
            "`__getitem__` must return a valid sample for every integer index from `0` through `len(dataset)-1`.\n\n"
            "This simple contract is what lets custom real-world data integrate with the rest of the PyTorch ecosystem.\n\n"
            "---\n\n"

            "## 16. Build the final sample tuple\n\n"
            "The chapter uses a crop width:\n\n"
            "```python\n"
            "width_irc = (32, 48, 48)\n"
            "```\n\n"
            "After extraction, the candidate NumPy array has shape:\n\n"
            "```text\n"
            "32 × 48 × 48\n"
            "```\n\n"
            "Then convert it to a float tensor and add the channel axis:\n\n"
            "```python\n"
            "candidate_t = torch.from_numpy(candidate_a)\n"
            "candidate_t = candidate_t.to(torch.float32)\n"
            "candidate_t = candidate_t.unsqueeze(0)\n"
            "```\n\n"
            "Final candidate shape:\n\n"
            "```text\n"
            "1 × 32 × 48 × 48\n"
            "```\n\n"
            "The returned sample includes:\n\n"
            "- the candidate volume tensor,\n"
            "- class information,\n"
            "- series UID,\n"
            "- center coordinate in IRC form.\n\n"
            "[[IMAGE_NEEDED: LunaDataset sample tuple | A 1×32×48×48 candidate tensor plus class tensor, series UID, and IRC center "
            "grouped into one Dataset return tuple | Learner should notice that training data can include both model inputs and metadata useful "
            "for debugging/evaluation]]\n\n"
            "The source's two-element class tensor is part of the downstream interface it establishes for later chapters; the consuming training code is introduced later.\n\n"

            "### Learning checkpoint 2 — Coordinate-to-sample pipeline\n\n"
            "Explain this without notes:\n\n"
            "```text\n"
            "candidate XYZ\n"
            " -> scan metadata\n"
            " -> XYZ-to-IRC conversion\n"
            " -> local 3D crop\n"
            " -> float tensor\n"
            " -> add channel axis\n"
            " -> Dataset sample tuple\n"
            "```\n\n"
            "If any transition is unclear, revisit sections 10–16.\n\n"
            "---\n\n"

            "## 17. The data pipeline can become the training bottleneck\n\n"
            "Without caching, requesting one candidate may require:\n\n"
            "1. locating the scan,\n"
            "2. reading a large CT from disk,\n"
            "3. converting it to floating point,\n"
            "4. clipping values,\n"
            "5. converting coordinates,\n"
            "6. extracting a comparatively tiny crop.\n\n"
            "Repeating this work for every epoch would waste enormous time.\n\n"
            "The chapter reports that the uncached dataset is dramatically slower than the cached version.\n\n"
            "This leads to a general principle:\n\n"
            "> **Optimization is not only about GPU kernels. A slow input pipeline can leave an expensive accelerator waiting for data.**\n\n"
            "---\n\n"

            "## 18. In-memory cache for CT objects\n\n"
            "The source uses:\n\n"
            "```python\n"
            "@functools.lru_cache(1, typed=True)\n"
            "def getCt(series_uid):\n"
            "    return Ct(series_uid)\n"
            "```\n\n"
            "This avoids reloading the same CT repeatedly when nearby accesses refer to the same scan.\n\n"
            "Only one scan is retained in this cache, so access order still matters.\n\n"
            "This is a good example of tailoring a cache to memory constraints: CT volumes are much larger than candidate crops.\n\n"
            "---\n\n"

            "## 19. On-disk cache for extracted candidate crops\n\n"
            "The source also memoizes the expensive crop operation using disk-backed caching:\n\n"
            "```python\n"
            "@raw_cache.memoize(typed=True)\n"
            "def getCtRawCandidate(series_uid, center_xyz, width_irc):\n"
            "    ct = getCt(series_uid)\n"
            "    ct_chunk, center_irc = ct.getRawCandidate(\n"
            "        center_xyz,\n"
            "        width_irc,\n"
            "    )\n"
            "    return ct_chunk, center_irc\n"
            "```\n\n"
            "After the cache has been populated, later epochs can read a small processed crop instead of reopening and processing the full CT.\n\n"
            "### Cache invalidation warning\n\n"
            "If the processing function changes materially but the cache key does not, stale cached outputs may silently survive.\n\n"
            "That can make experiments very confusing.\n\n"
            "A production pipeline should therefore version or clear caches whenever preprocessing semantics change.\n\n"
            "{{exercise:M11.L01.EX03}}\n\n"
            "---\n\n"

            "## 20. Construct `LunaDataset` from the cleaned candidate list\n\n"
            "The dataset begins with a copy of the unified candidate metadata:\n\n"
            "```python\n"
            "self.candidateInfo_list = copy.copy(\n"
            "    getCandidateInfoList()\n"
            ")\n"
            "```\n\n"
            "Copying matters because the source candidate list is cached. Dataset-specific filtering should not mutate the globally cached object.\n\n"
            "An optional `series_uid` filter lets developers inspect one scan in isolation, which is very useful for visualization and debugging.\n\n"
            "---\n\n"

            "## 21. Build a deterministic training/validation split\n\n"
            "The source designates every `N`th candidate as validation data.\n\n"
            "Conceptually:\n\n"
            "```python\n"
            "if isValSet_bool:\n"
            "    val_candidates = candidates[::val_stride]\n"
            "else:\n"
            "    train_candidates = candidates with those entries removed\n"
            "```\n\n"
            "Because the candidate list has a stable sort order, the split is reproducible.\n\n"
            "Earlier, nodules were ordered by diameter, which helps distribute different nodule sizes across the periodic split.\n\n"
            "This is a concrete example of using domain-relevant metadata to improve dataset representativeness.\n\n"
            "---\n\n"

            "## 22. Leakage can invalidate validation results\n\n"
            "A split is not useful merely because two Python lists are different.\n\n"
            "We must ask whether training samples provide unfair information about validation samples.\n\n"
            "The chapter calls out examples such as placing the same sample—or strongly related samples from the same underlying object—in both sets.\n\n"
            "For some tasks, the correct split unit should be **patient or scan**, not candidate.\n\n"
            "The source notes that this is task-dependent and must be considered explicitly.\n\n"
            "Production rule:\n\n"
            "> **Choose the split boundary at the level of independence you expect in real deployment.**\n\n"
            "---\n\n"

            "## 23. Training and validation must represent the operating environment\n\n"
            "The source gives three broad split requirements:\n\n"
            "1. both sets should contain the important variations expected in real inputs,\n"
            "2. unusual samples should appear only for a deliberate reason,\n"
            "3. training must not contain hints about validation that would not exist in production.\n\n"
            "The chapter performs a useful sanity check by inspecting the distribution of nodule diameters.\n\n"
            "Many nodules fall in the several-millimeter range, while some are substantially larger and some have missing diameter metadata.\n\n"
            "Simple exploratory checks like this can expose bad assumptions before expensive training begins.\n\n"
            "{{exercise:M11.L01.EX04}}\n\n"
            "---\n\n"

            "## 24. Visualize the data before trusting it\n\n"
            "Rendering is not decoration. It is a debugging technique.\n\n"
            "A visualization may reveal:\n\n"
            "- a crop is off-center,\n"
            "- a scan appears flipped,\n"
            "- spacing makes anatomy appear distorted,\n"
            "- one sample has unusual noise,\n"
            "- candidate metadata points to the wrong region,\n"
            "- intensity clipping behaves unexpectedly.\n\n"
            "[[IMAGE_NEEDED: CT candidate visualization workflow | A full CT slice with candidate marker followed by neighboring slices "
            "through the extracted crop | Learner should notice that visual inspection connects metadata, coordinate conversion, and final "
            "model input in one sanity check]]\n\n"
            "The source uses Jupyter and Matplotlib for this exploratory inspection.\n\n"
            "The important skill is not a particular plotting library. It is developing enough familiarity with the data that anomalies become noticeable.\n\n"
            "---\n\n"

            "## 25. A production-minded data-pipeline blueprint\n\n"
            "The chapter's implementation can be generalized into this architecture:\n\n"
            "```text\n"
            "RAW LAYER\n"
            "  .mhd / .raw / CSV files\n"
            "        ↓\n"
            "PARSING LAYER\n"
            "  SimpleITK + CSV parsing\n"
            "        ↓\n"
            "SANITIZATION LAYER\n"
            "  merge metadata + fuzzy matching + clipping\n"
            "        ↓\n"
            "GEOMETRY LAYER\n"
            "  XYZ ↔ IRC coordinate transforms\n"
            "        ↓\n"
            "SAMPLE EXTRACTION\n"
            "  candidate-centered 3D crop\n"
            "        ↓\n"
            "CACHE LAYER\n"
            "  reusable CT/candidate outputs\n"
            "        ↓\n"
            "PYTORCH DATASET\n"
            "  tensors + labels + metadata\n"
            "        ↓\n"
            "DATALOADER / TRAINING\n"
            "```\n\n"
            "Each layer has a distinct responsibility. That separation makes the system easier to test and change.\n\n"
            "---\n\n"

            "## 26. What should be tested before training?\n\n"
            "A robust implementation should verify at least:\n\n"
            "- candidate metadata parses correctly,\n"
            "- only downloaded series are referenced when required,\n"
            "- approximate annotation matching behaves as expected,\n"
            "- HU clipping produces the intended range,\n"
            "- XYZ→IRC and IRC→XYZ conversions are mutually consistent within rounding error,\n"
            "- candidate crop shapes are always correct,\n"
            "- boundary candidates do not crash extraction,\n"
            "- `Dataset.__len__` matches accessible indexes,\n"
            "- sample tensors have expected dtype/shape,\n"
            "- train and validation samples do not overlap,\n"
            "- cache invalidation is possible,\n"
            "- visualized crops correspond to the intended candidates.\n\n"
            "These checks are cheaper than discovering pipeline corruption halfway through model training.\n\n"
            "{{exercise:M11.L01.EX05}}\n\n"
            "---\n\n"

            "## 27. The complete mental model\n\n"
            "The chapter can be summarized as one transformation chain:\n\n"
            "```text\n"
            "raw medical-image files\n"
            " + imperfect annotation files\n"
            "          ↓\n"
            "unified candidate metadata\n"
            "          ↓\n"
            "3D CT arrays + scan geometry\n"
            "          ↓\n"
            "physical-coordinate conversion\n"
            "          ↓\n"
            "fixed-size candidate crops\n"
            "          ↓\n"
            "cached, model-ready tensors\n"
            "          ↓\n"
            "reproducible train/validation datasets\n"
            "          ↓\n"
            "visual sanity checks\n"
            "          ↓\n"
            "ready for model training\n"
            "```\n\n"
            "The most important lesson is not specific to medicine:\n\n"
            "> **Your model can only learn from the data pipeline you actually built, not the clean conceptual dataset you imagine you have.**\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: Data loading is just I/O boilerplate\n\n"
            "In this chapter, data loading determines coordinate correctness, intensity range, crop content, split integrity, and training speed. Those choices can directly determine model success.\n\n"
            "### Misconception 2: If two coordinates refer to the same nodule, they must be identical\n\n"
            "Independent annotation sources can disagree slightly. The source explicitly needs approximate matching.\n\n"
            "### Misconception 3: Millimeter coordinates can be used directly as NumPy indexes\n\n"
            "Patient-space coordinates must be transformed using origin, spacing, and direction metadata.\n\n"
            "### Misconception 4: A voxel is always cubic\n\n"
            "CT voxel spacing can differ by axis, especially between slice depth and in-slice dimensions.\n\n"
            "### Misconception 5: Caching only changes speed, so stale cache values are harmless\n\n"
            "A stale cache can return data produced by old preprocessing semantics and silently invalidate an experiment.\n\n"
            "### Misconception 6: Any non-overlapping train/validation lists guarantee an unbiased validation result\n\n"
            "Closely related samples, such as samples from the same patient, can still leak information depending on the task.\n\n"
            "### Misconception 7: Visualization is optional once shapes and dtypes are correct\n\n"
            "Shapes cannot reveal whether a crop is centered on the wrong anatomy or whether orientation/spacing interpretation is wrong.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Series UID | Unique identifier used to reference one CT scan across files and metadata. |\n"
            "| MetaIO | File format used by the LUNA-prepared CT data in the chapter. |\n"
            "| `.mhd` | Metadata/header file describing the CT volume and associated raw data. |\n"
            "| `.raw` | Binary file containing volumetric CT values. |\n"
            "| Candidate | Location that may or may not correspond to an actual lung nodule. |\n"
            "| Annotation | Human/reference metadata describing known nodules and properties such as diameter. |\n"
            "| Hounsfield Unit | CT intensity unit related to radiodensity. |\n"
            "| HU clipping | Limiting CT values to a task-relevant range such as `[-1000,1000]`. |\n"
            "| Patient coordinates | Physical `(X,Y,Z)` location measured in millimeters. |\n"
            "| IRC coordinates | CT-array `(index,row,column)` address. |\n"
            "| Origin | Physical location associated with the array coordinate origin. |\n"
            "| Voxel spacing | Physical size represented by one array step along each dimension. |\n"
            "| Direction matrix | Matrix mapping array axes/orientation into patient-space orientation. |\n"
            "| Candidate crop | Fixed-size 3D subvolume centered around a candidate location. |\n"
            "| `Dataset` | PyTorch indexed sample interface implementing `__len__` and `__getitem__`. |\n"
            "| In-memory cache | Fast temporary cache stored in process memory. |\n"
            "| On-disk cache | Persistent processed-data cache stored on disk. |\n"
            "| Cache invalidation | Removing/versioning cached outputs when producing code or assumptions change. |\n"
            "| Data leakage | Unfair information overlap between training and validation/testing. |\n"
            "| Representative split | Data partition whose variation reflects expected real-world inputs. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "1. What two files represent one LUNA CT scan?\n"
            "2. Why is the series UID important?\n"
            "3. What fields are found in `candidates.csv`?\n"
            "4. What extra information does `annotations.csv` provide?\n"
            "5. Why is exact coordinate equality not sufficient when merging the two CSV sources?\n"
            "6. What is the purpose of `CandidateInfoTuple`?\n"
            "7. Why does the pipeline optionally filter metadata to scans present on disk?\n"
            "8. What role does `SimpleITK` play?\n"
            "9. What is the shape semantics of the loaded CT array?\n"
            "10. What do approximately -1000 HU, 0 HU, and +1000 HU represent?\n"
            "11. Why does the source clip HU values?\n"
            "12. What is the difference between XYZ and IRC coordinates?\n"
            "13. What three pieces of scan metadata are required for coordinate conversion?\n"
            "14. Why can equal index distances along two axes represent different millimeter distances?\n"
            "15. What transformation steps convert IRC into XYZ?\n"
            "16. Why do we round when converting physical coordinates back to array indexes?\n"
            "17. Why crop candidate regions instead of using the whole CT for the classifier?\n"
            "18. What shape does the source use for one raw candidate crop?\n"
            "19. Why is a channel dimension added?\n"
            "20. What are the only two methods required by a basic custom PyTorch `Dataset`?\n"
            "21. Why is a copy made of the cached candidate-info list inside the dataset constructor?\n"
            "22. Why can data loading become the bottleneck even when a GPU is available?\n"
            "23. What is the difference between the source's in-memory and on-disk caches?\n"
            "24. When must a processing cache be cleared or versioned?\n"
            "25. Why does stable ordering matter for the chapter's stride-based validation split?\n"
            "26. What makes a training/validation split representative?\n"
            "27. Give one example of data leakage that can happen even with different samples.\n"
            "28. Why can inspecting nodule-size distribution be useful before training?\n"
            "29. What kinds of bugs can data visualization reveal that tensor-shape assertions cannot?\n"
            "30. Why should raw parsing, sanitization, geometry, caching, and Dataset code be kept as separate responsibilities?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**A production dataset is engineered, not merely loaded. The path from raw files to a model-ready tensor may require reconciling "
            "multiple metadata sources, understanding physical units, converting coordinate systems, cleaning intensity ranges, extracting the "
            "right region, caching expensive computations, enforcing honest data splits, and visually verifying that every transformation still "
            "represents the real-world object you intended.**\n"
        ),

        "estimated_minutes": 330,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "raw-to-sample", "title": "From raw files to a training sample", "order": 1},
            {"id": "raw-files", "title": "Raw CT file structure", "order": 2},
            {"id": "candidate-data", "title": "Candidate metadata", "order": 3},
            {"id": "annotation-data", "title": "Annotation metadata", "order": 4},
            {"id": "messy-data", "title": "Reconciling imperfect data sources", "order": 5},
            {"id": "candidate-info", "title": "Unified candidate representation", "order": 6},
            {"id": "filter-on-disk", "title": "Filtering to available scans", "order": 7},
            {"id": "loading-ct", "title": "Loading CT scans with SimpleITK", "order": 8},
            {"id": "hu", "title": "Hounsfield Units and clipping", "order": 9},
            {"id": "patient-vs-array", "title": "Patient versus array coordinates", "order": 10},
            {"id": "coordinate-metadata", "title": "Origin, spacing, and direction", "order": 11},
            {"id": "noncubic-voxels", "title": "Noncubic voxels", "order": 12},
            {"id": "xyz-to-irc", "title": "Converting XYZ to IRC", "order": 13},
            {"id": "candidate-crop", "title": "Extracting a candidate crop", "order": 14},
            {"id": "dataset-contract", "title": "Custom Dataset contract", "order": 15},
            {"id": "sample-tuple", "title": "Building the sample tuple", "order": 16},
            {"id": "why-cache", "title": "Why caching matters", "order": 17},
            {"id": "memory-cache", "title": "In-memory CT cache", "order": 18},
            {"id": "disk-cache", "title": "On-disk candidate cache", "order": 19},
            {"id": "dataset-init", "title": "Constructing LunaDataset", "order": 20},
            {"id": "train-val-split", "title": "Training and validation split", "order": 21},
            {"id": "data-leakage", "title": "Data leakage", "order": 22},
            {"id": "representative-splits", "title": "Representative splits", "order": 23},
            {"id": "visualize-data", "title": "Visualizing and sanity-checking data", "order": 24},
            {"id": "production-pipeline", "title": "Production-minded pipeline blueprint", "order": 25},
            {"id": "testing-checklist", "title": "Pre-training testing checklist", "order": 26},
            {"id": "complete-mental-model", "title": "Complete data-pipeline mental model", "order": 27},
        ],
    },

    "exercises": [
        {
            "id": "M11.L01.EX01",
            "title": "Unify Two Imperfect Metadata Sources",
            "lesson_code": "M11.L01",
            "section_id": "candidate-info",
            "placement": "after_section",
            "description": "Practice merging candidate and annotation metadata when coordinates do not match exactly.",
            "instructions": (
                "Create two tiny in-memory tables: candidate rows with `series_uid, xyz, is_nodule` and annotation rows with "
                "`series_uid, xyz, diameter_mm`. Introduce small coordinate differences for matching nodules. Implement a function "
                "that groups annotations by series UID, approximately matches each positive candidate to a nearby annotation using "
                "the chapter's axis-wise tolerance idea, and returns clean records containing nodule flag, diameter, series UID, and "
                "candidate center. Print matched and unmatched cases and document the assumption behind your tolerance."
            ),
            "expected_output": "Working merge code, clean candidate records, unmatched-case output, and a written matching assumption.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["data-cleaning", "fuzzy-matching", "metadata-unification", "namedtuple"],
        },
        {
            "id": "M11.L01.EX02",
            "title": "Verify XYZ ↔ IRC Coordinate Conversion",
            "lesson_code": "M11.L01",
            "section_id": "xyz-to-irc",
            "placement": "after_section",
            "description": "Build confidence that physical and array coordinate transformations are consistent.",
            "instructions": (
                "Implement `irc2xyz` and `xyz2irc` from the lesson. Use a synthetic origin, anisotropic voxel spacing, and "
                "identity direction matrix first. Convert several IRC points to XYZ and back. Then test a direction matrix that "
                "flips one axis. Explain why exact round-trip equality may depend on rounding when physical coordinates do not fall "
                "exactly at voxel centers."
            ),
            "expected_output": "Conversion functions, round-trip test cases, and an explanation of spacing/orientation/rounding.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["coordinate-systems", "linear-algebra", "voxel-spacing", "testing"],
        },
        {
            "id": "M11.L01.EX03",
            "title": "Benchmark the Candidate Cache",
            "lesson_code": "M11.L01",
            "section_id": "disk-cache",
            "placement": "after_section",
            "description": "Measure how caching changes data-pipeline performance.",
            "instructions": (
                "Following the chapter's exercise idea, iterate through up to 1000 dataset samples and time: "
                "(1) a cold first pass, (2) a second pass with caches populated, and (3) a run after clearing the cache. "
                "If full LUNA data is unavailable, simulate an expensive loader with a short delay and cache its extracted crop. "
                "Also compare ordered access with randomized access and explain why an LRU cache of only one CT is sensitive to access order."
            ),
            "expected_output": "Timing table for the requested runs plus a performance explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["caching", "benchmarking", "io-performance", "lru-cache"],
        },
        {
            "id": "M11.L01.EX04",
            "title": "Audit a Training/Validation Split",
            "lesson_code": "M11.L01",
            "section_id": "representative-splits",
            "placement": "after_section",
            "description": "Evaluate whether a split is representative and leakage-safe.",
            "instructions": (
                ('1. Use synthetic candidate records with series UID, patient ID, diameter and class.\n'
                 '2. Create split A by taking every tenth candidate, and split B by grouping candidates by patient.\n'
                 '3. For each split, report the class counts, the diameter ranges, and whether any patient appears in both sets.\n'
                 '4. Explain which split is safer when several candidates from one patient are strongly correlated, and why.')
            ),
            "expected_output": "Two split summaries, leakage checks, and a justified recommendation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["validation-split", "data-leakage", "representativeness", "group-splitting"],
        },
        {
            "id": "M11.L01.EX05",
            "title": "Create a Pre-Training Data-Pipeline Test Plan",
            "lesson_code": "M11.L01",
            "section_id": "testing-checklist",
            "placement": "after_section",
            "description": "Turn the chapter into a reusable engineering verification plan.",
            "instructions": (
                ('1. Write at least 12 tests covering metadata parsing, candidate/annotation matching, HU clipping, coordinate round trips, crop boundary handling, output shape/dtype, cache invalidation, split overlap, and visual spot checks.\n'
                 '2. For each test, state: input fixture, expected behavior, and what model-training failure the test prevents.')
            ),
            "expected_output": "A structured test table with at least 12 data-pipeline checks and their rationale.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["data-testing", "pipeline-quality", "debugging", "ml-engineering"],
        },
    ],

    "quiz": {
        "id": "M11.L01.QZ01",
        "title": "Combining Data Sources into a Unified Dataset — Knowledge Check",
        "lesson_code": "M11.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M11.L01.Q01",
                "section_id": "raw-files",
                "question": "What connects a CT's `.mhd`/`.raw` files with its metadata rows?",
                "options": [
                    "The batch index",
                    "The series UID",
                    "The Hounsfield Unit",
                    "The validation stride",
                ],
                "correct": 1,
                "explanation": "The series UID is the stable identifier used across files and annotation metadata.",
            },
            {
                "id": "M11.L01.Q02",
                "section_id": "candidate-data",
                "question": "What does the `class` field in the chapter's candidate data represent?",
                "options": [
                    "Whether the candidate is considered a nodule.",
                    "The CT scanner manufacturer.",
                    "The nodule diameter in millimeters.",
                    "The candidate's array index.",
                ],
                "correct": 0,
                "explanation": "The candidate class is a Boolean-like nodule/non-nodule flag.",
            },
            {
                "id": "M11.L01.Q03",
                "section_id": "messy-data",
                "question": "Why does the chapter need approximate coordinate matching?",
                "options": [
                    "The CT array contains no coordinates.",
                    "Candidates are stored as strings only.",
                    "Coordinates describing the same nodule can differ slightly between metadata files.",
                    "All nodules have identical diameters.",
                ],
                "correct": 2,
                "explanation": "Independent source files do not always use exactly identical center coordinates.",
            },
            {
                "id": "M11.L01.Q04",
                "section_id": "candidate-info",
                "question": "Why create a clean `CandidateInfoTuple` layer?",
                "options": [
                    "To perform GPU backpropagation directly.",
                    "To replace the CT volume.",
                    "To generate random candidates.",
                    "To isolate messy data reconciliation from downstream training code.",
                ],
                "correct": 3,
                "explanation": "A sanitized metadata interface keeps downstream code simpler and easier to reason about.",
            },
            {
                "id": "M11.L01.Q05",
                "section_id": "loading-ct",
                "question": "What does `SimpleITK` primarily provide in this chapter?",
                "options": [
                    "Parsing of the medical-image files into usable image data and metadata.",
                    "A neural-network optimizer.",
                    "A cross-entropy classifier.",
                    "Automatic train/validation splitting.",
                ],
                "correct": 0,
                "explanation": "SimpleITK handles the underlying medical-image file format and exposes the scan to Python.",
            },
            {
                "id": "M11.L01.Q06",
                "section_id": "hu",
                "question": "Why does the chapter clip CT intensities to approximately `[-1000, 1000]` HU?",
                "options": [
                    "To force every voxel to become binary.",
                    "To remove task-irrelevant extreme values and keep the working range controlled.",
                    "To convert millimeters into indexes.",
                    "To increase the number of CT slices.",
                ],
                "correct": 1,
                "explanation": "The source deliberately removes extreme values that are not useful for the target task.",
            },
            {
                "id": "M11.L01.Q07",
                "section_id": "patient-vs-array",
                "question": "Why can't candidate `(X,Y,Z)` coordinates be used directly to index the CT NumPy array?",
                "options": [
                    "XYZ is always normalized between 0 and 1.",
                    "NumPy supports only two dimensions.",
                    "XYZ is measured in physical patient space, while the array uses IRC voxel indexes.",
                    "The coordinates belong to another patient.",
                ],
                "correct": 2,
                "explanation": "Physical coordinates and array addresses use different origins, scales, and axis conventions.",
            },
            {
                "id": "M11.L01.Q08",
                "section_id": "coordinate-metadata",
                "question": "Which metadata is needed for the coordinate mapping described in the lesson?",
                "options": [
                    "Learning rate, batch size, and epochs",
                    "Class weight, loss, and optimizer",
                    "Series UID, nodule class, and cache path",
                    "Origin, voxel spacing, and direction matrix",
                ],
                "correct": 3,
                "explanation": "Those geometric values define the physical-to-array coordinate transform.",
            },
            {
                "id": "M11.L01.Q09",
                "section_id": "candidate-crop",
                "question": "Why extract a fixed-size crop around each candidate?",
                "options": [
                    "To let the classifier focus on a much smaller relevant region.",
                    "To convert the scan into RGB.",
                    "To remove all metadata.",
                    "To avoid using PyTorch Dataset.",
                ],
                "correct": 0,
                "explanation": "Candidate-centered crops reduce irrelevant background and constrain the classifier's task.",
            },
            {
                "id": "M11.L01.Q10",
                "section_id": "dataset-contract",
                "question": "Which methods are required by the basic custom Dataset contract discussed here?",
                "options": [
                    "`forward` and `backward`",
                    "`__len__` and `__getitem__`",
                    "`step` and `zero_grad`",
                    "`train` and `eval`",
                ],
                "correct": 1,
                "explanation": "These methods define dataset size and indexed sample retrieval.",
            },
            {
                "id": "M11.L01.Q11",
                "section_id": "sample-tuple",
                "question": "Why is `unsqueeze(0)` applied to the candidate crop?",
                "options": [
                    "To add another CT scan.",
                    "To convert HU into millimeters.",
                    "To add the explicit single-channel dimension expected by later model code.",
                    "To sort the candidate list.",
                ],
                "correct": 2,
                "explanation": "The raw crop is D×H×W; adding dimension 0 produces C×D×H×W with C=1.",
            },
            {
                "id": "M11.L01.Q12",
                "section_id": "disk-cache",
                "question": "What is a major danger of keeping old cache entries after preprocessing code changes?",
                "options": [
                    "The optimizer will switch to SGD.",
                    "The Dataset length becomes zero automatically.",
                    "The CT files are converted to text.",
                    "The pipeline may silently return outputs produced by obsolete processing logic.",
                ],
                "correct": 3,
                "explanation": "Stale caches can make experiments inconsistent with the current source code.",
            },
            {
                "id": "M11.L01.Q13",
                "section_id": "train-val-split",
                "question": "Why does stable candidate ordering matter to the chapter's every-Nth validation split?",
                "options": [
                    "It makes the partition reproducible.",
                    "It increases GPU memory.",
                    "It changes the Hounsfield scale.",
                    "It prevents coordinate conversion.",
                ],
                "correct": 0,
                "explanation": "The stride-based split only stays consistent if the underlying order is stable.",
            },
            {
                "id": "M11.L01.Q14",
                "section_id": "data-leakage",
                "question": "When might candidate-level splitting still leak information?",
                "options": [
                    "When candidates use floating-point tensors.",
                    "When strongly related samples from the same patient appear in both sets.",
                    "When validation uses fewer samples.",
                    "When a crop is centered correctly.",
                ],
                "correct": 1,
                "explanation": "Related samples can make validation artificially easy even if exact candidates differ.",
            },
            {
                "id": "M11.L01.Q15",
                "section_id": "visualize-data",
                "question": "What is the main reason to visualize candidate samples before training?",
                "options": [
                    "To increase the training-set size.",
                    "To replace all automated tests.",
                    "To develop intuition and detect semantic pipeline errors that shapes alone may miss.",
                    "To automatically rebalance classes.",
                ],
                "correct": 2,
                "explanation": "Visualization can reveal incorrect crops, orientation, noise, or other meaningful data problems.",
            },
            {
                "id": "M11.L01.Q16",
                "section_id": "complete-mental-model",
                "question": "Which statement best summarizes the chapter?",
                "options": [
                    "Model architecture is always more important than preprocessing.",
                    "Every data source should be converted directly into one giant tensor.",
                    "Caching removes the need for correct data transformations.",
                    "A reliable model-ready dataset must be engineered through parsing, cleaning, geometry, extraction, caching, splitting, and verification.",
                ],
                "correct": 3,
                "explanation": "The chapter is fundamentally about engineering trustworthy model-ready data from messy raw sources.",
            },
            {
                "id": "M11.L01.Q17",
                "section_id": "complete-mental-model",
                "type": "open",
                "question": (
                    "Trace one candidate from the raw LUNA files all the way to the final `LunaDataset` sample. "
                    "Your answer should include metadata merging, CT loading, HU clipping, XYZ→IRC conversion, "
                    "candidate cropping, tensor conversion, caching, and train/validation partitioning."
                ),
            },
        ],
        "passing_score": 70,
    },
}
