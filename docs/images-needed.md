# Images still needed

Source: `[[IMAGE_NEEDED: title | what it shows | what the learner should notice]]` markers in the course lesson files. COURSE-001 and COURSE-002 have none. A marker stays in the lesson until an image file and an `assets_manifest.json` entry exist, then it is replaced by `{{figure:<key>}}` (see [lesson-figures.md](lesson-figures.md)).


## COURSE-003_Applied_Deep_Learning — 128 images

- **M01.L01** — Feature engineering versus representation learning — A two-part diagram comparing a traditional ML pipeline where a practitioner manually creates features before a learning algorithm with a deep-learning pipeline where raw data enters a neural network that learns hierarchical features automatically during training  
  _Learner should notice:_ deep learning reduces manual feature design but typically increases dependence on data, training, and computation
- **M01.L01** — High-level PyTorch project workflow — A left-to-right pipeline showing raw data or storage, Dataset conversion to tensors, DataLoader batching, an untrained model, the training loop with loss and optimizer, a trained model, and deployment; include optional multi-GPU or multi-machine training beneath the training stage  
  _Learner should notice:_ the neural network is only one component in a complete deep learning system
- **M02.L01** — Pretrained image-classification inference pipeline — A diagram showing an input photograph being resized/cropped/normalized into a tensor, passed through a pretrained classifier, producing one score for each ImageNet class, followed by top-k label selection  
  _Learner should notice:_ inference requires both the trained network and the correct input/output processing around it
- **M02.L01** — Neural-network architecture and forward pass — A simplified left-to-right model diagram inspired by an image classifier, showing an input image passing through several learned processing blocks into a final vector of class scores; optionally annotate intermediate representations without reproducing source artwork  
  _Learner should notice:_ the input is progressively transformed and that the learned weights inside the blocks determine the transformations
- **M02.L01** — Inputs to diffusion inpainting — A conceptual three-input diagram showing a text prompt, an original image, and a black/white edit mask entering an inpainting pipeline and producing an edited image  
  _Learner should notice:_ the prompt controls what to generate, the image defines the starting scene, and the mask constrains where changes may occur
- **M02.L01** — Iterative diffusion inpainting process — A sequence of 4–6 stages showing the masked region beginning noisy and becoming gradually more structured while the unmasked background remains fixed, ending with a coherent localized edit  
  _Learner should notice:_ generation happens through repeated refinement rather than a single deterministic drawing step
- **M02.L01** — BLIP image-captioning mental model — A conceptual pipeline showing an input image entering an image encoder, producing an embedding or visual representation, then entering a text decoder that generates a natural-language caption  
  _Learner should notice:_ the model bridges two modalities by turning visual information into a representation that can condition language generation
- **M03.L01** — Input-to-intermediate-to-output representations — A simple neural-network pipeline showing a human-interpretable input on the left, several layers of floating-point intermediate representations in the middle, and a human-usable output on the right  
  _Learner should notice:_ the network repeatedly transforms numeric representations and that the hidden intermediate representations are task-dependent
- **M03.L01** — Scalar, vector, matrix, and 3D tensor — A progression showing a single scalar, a one-dimensional vector, a two-dimensional matrix, and a three-dimensional stack with shape labels  
  _Learner should notice:_ tensors generalize familiar scalar/vector/matrix structures to arbitrary numbers of dimensions
- **M03.L01** — Broadcasting shape alignment — A visual example showing a (1, 3) row tensor and a (3, 1) column tensor expanding conceptually to form a (3, 3) result, with dimensions aligned from the right  
  _Learner should notice:_ a dimension of size 1 can be virtually expanded and that broadcasting does not require manually duplicating values
- **M03.L01** — Python objects versus tensor storage — A side-by-side diagram showing a Python list as references to individually boxed numeric objects and a tensor as a compact homogeneous contiguous block of unboxed numeric values  
  _Learner should notice:_ why tensors are more memory- and computation-friendly for large numerical collections
- **M03.L01** — Tensor storage with size, offset, and stride — A one-dimensional storage block with indices, plus two tensor views laid over it; annotate one view with shape, storage offset, and per-dimension strides  
  _Learner should notice:_ tensor indexing is translated into positions in shared storage using metadata
- **M03.L01** — Transpose without copying — A diagram showing one shared storage block referenced by an original 3x2 tensor and a transposed 2x3 tensor, with different stride arrows for each  
  _Learner should notice:_ the apparent matrix layout can change while the underlying storage remains the same
- **M03.L01** — CPU-to-GPU tensor workflow — A diagram showing a tensor copied from CPU RAM to GPU memory, several operations occurring on the GPU while the data remains there, and an explicit transfer back to CPU at the end  
  _Learner should notice:_ device transfer and device computation are separate actions
- **M04.L01** — RGB image channels — A color image shown alongside separate red, green, and blue intensity maps  
  _Learner should notice:_ a color image is represented as multiple aligned numerical channels rather than one scalar per pixel
- **M04.L01** — Image layout conversion — A diagram showing an image tensor changing from H×W×C to C×H×W, with the same underlying pixel data but reordered logical axes  
  _Learner should notice:_ the meaning/order of dimensions changes even though the image content does not
- **M04.L01** — CT volume built from slices — A stack of 2D grayscale scan slices arranged along a depth axis to form a 3D volume  
  _Learner should notice:_ depth is a spatial dimension, unlike RGB channels which represent different measured features at the same pixel location
- **M04.L01** — Choosing a representation for column types — A simple flowchart distinguishing continuous, ordinal, and categorical variables and showing common representation choices such as normalized numeric values, ordered numeric or categorical treatment, and one-hot/embedding representation  
  _Learner should notice:_ representation should preserve the real meaning of the variable rather than blindly treating every number as continuous
- **M04.L01** — Flat time-series table to daily tensor — A 2D table of hourly rows being grouped into blocks of 24 and transformed into a 3D tensor with separate day, variable, and hour axes  
  _Learner should notice:_ adding a time-period axis makes sequential structure explicit rather than treating every hour independently
- **M04.L01** — N×C×L versus N×L×C sequence layouts — Two simplified 3D tensor diagrams comparing sample×variables×time with sample×time×variables  
  _Learner should notice:_ both can contain the same values, but axis ordering determines how conveniently the model and code access complete variable sequences
- **M04.L01** — Character, word, and embedding text representations — A comparison showing character-level one-hot rows, word-level one-hot rows with a much larger vocabulary dimension, and a compact dense embedding vector for each word  
  _Learner should notice:_ the trade-off between sequence granularity, vocabulary size, and representation compactness
- **M04.L01** — Semantic embedding space — A simple 2D conceptual embedding plot with related words clustered near one another and unrelated groups separated, making clear that real embeddings usually have many more dimensions  
  _Learner should notice:_ distance and direction in an embedding can encode relationships that one-hot vectors do not express
- **M05.L01** — Mental model of learning — A loop diagram showing input and target entering a model, model output compared with target through a loss function, gradients flowing backward to parameters, and parameters being updated before the next forward pass  
  _Learner should notice:_ learning is an iterative feedback process driven by prediction error
- **M05.L01** — Noisy thermometer measurements — A scatter plot with unknown thermometer reading on the horizontal axis and Celsius temperature on the vertical axis, showing an approximately linear trend with some noise  
  _Learner should notice:_ a straight line appears to be a reasonable first model even though the points are not perfectly aligned
- **M05.L01** — Absolute error versus squared error — Two simple loss curves centered at zero error: a V-shaped absolute-error curve and a smooth U-shaped squared-error curve  
  _Learner should notice:_ both are minimized at zero but squared error is smooth and grows more strongly for large errors
- **M05.L01** — Gradient descent as parameter knobs — A conceptual machine with two knobs labeled w and b and a loss display, with arrows showing adjustments toward lower loss  
  _Learner should notice:_ each parameter is adjusted according to how changing it affects the loss
- **M05.L01** — Numerical versus analytical gradient — A curve with one slope estimated from two nearby points and another tangent slope drawn exactly at a point  
  _Learner should notice:_ finite differences approximate local change whereas differentiation gives the local derivative directly
- **M05.L01** — Converging versus diverging gradient descent — Two bowl-shaped loss plots: one with steps jumping back and forth farther away from the minimum, and another with smaller steps approaching the minimum  
  _Learner should notice:_ the learning rate controls update size and can determine whether optimization converges or diverges
- **M05.L01** — Autograd forward and backward computation graph — A small graph showing parameters feeding a linear model, prediction feeding a loss node, then backward arrows from loss through the model to parameter gradients  
  _Learner should notice:_ the forward pass records dependencies and backward traverses them in reverse to apply the chain rule
- **M05.L01** — Training and validation split — A dataset divided into a larger training subset and a held-out validation subset, with parameter updates driven only by training data and validation data flowing only to an evaluation loss  
  _Learner should notice:_ validation observations are deliberately kept out of gradient-based fitting
- **M05.L01** — Training and validation loss scenarios — Four small plots showing: neither loss decreasing; training decreasing while validation worsens; both decreasing together; and both decreasing with a stable gap  
  _Learner should notice:_ identify no learning, overfitting, ideal generalization trend, and acceptable generalization with different absolute losses
- **M06.L01** — Same training loop, different model — A diagram showing input and target entering the familiar training loop, with the model box changing from a linear equation to a neural network while loss, backward pass, optimizer, and validation stay the same  
  _Learner should notice:_ the model architecture changes but the training mechanics remain
- **M06.L01** — Anatomy of an artificial neuron — Input x enters a multiply-by-weight step, bias b is added, and the result passes through activation f to produce output  
  _Learner should notice:_ the linear transformation followed by a fixed nonlinear function
- **M06.L01** — Simple multilayer neural network — Input vector, two hidden layers, and an output layer connected left to right  
  _Learner should notice:_ intermediate representations are passed layer to layer
- **M06.L01** — Tanh sensitive and saturated regions — A tanh curve with the center marked as sensitive and the flat tails marked as saturated  
  _Learner should notice:_ changes near zero affect output more strongly than changes in the tails
- **M06.L01** — Activation function comparison — A grid of Tanh, Sigmoid, ReLU, LeakyReLU, and Hardtanh curves on common axes  
  _Learner should notice:_ differences in range, slope, and saturated/flat regions
- **M06.L01** — Combining nonlinear neurons — Several shifted and scaled activation curves shown individually and then combined into a more complicated nonlinear curve  
  _Learner should notice:_ simple units can compose into functions much richer than any one unit
- **M06.L01** — Batched neural-network inputs and outputs — Several samples enter the same model in parallel, labeled B×N_in, with B×N_out at the output  
  _Learner should notice:_ dimension 0 carries independent samples through the same learned function
- **M06.L01** — Linear-Tanh-Linear neural network — Two depictions of the same network: a node-and-arrow view and a block view labeled Linear(1,13), Tanh, Linear(13,1)  
  _Learner should notice:_ both diagrams represent the same computation at different abstraction levels
- **M06.L01** — Linear fit versus neural-network fit — Thermometer scatter points with a straight linear fit and a slightly curved neural-network fit following some noisy samples  
  _Learner should notice:_ greater capacity can fit noise even when the true process is simple
- **M07.L01** — End-to-end bird-vs-airplane classifier — A pipeline showing CIFAR-10 images entering preprocessing, a neural-network classifier, class scores, loss during training, and predicted bird/airplane labels during inference  
  _Learner should notice:_ the image classification system contains data preparation, model, loss, optimization, and evaluation
- **M07.L01** — CIFAR-10 class samples — A small grid with one or more example 32×32 RGB images from each of the ten CIFAR-10 classes  
  _Learner should notice:_ the tiny image size, the visual ambiguity, and that each sample belongs to one discrete class
- **M07.L01** — PyTorch Dataset interface — A dataset box exposing __len__ and __getitem__, with __getitem__(i) returning an image and an integer label  
  _Learner should notice:_ a Dataset provides an access interface and does not necessarily need to hold every transformed sample permanently in memory
- **M07.L01** — CIFAR image before and after normalization — The same image shown conceptually before normalization and after channel standardization, with a note that the normalized tensor can contain values outside 0..1 even though no information was intentionally removed  
  _Learner should notice:_ normalized data may look visually strange while still being useful to the model
- **M07.L01** — Flattening an image into a feature vector — A 3×32×32 RGB image tensor being reshaped into one long 3072-element vector before entering a fully connected neural network  
  _Learner should notice:_ flattening preserves numerical values but removes the explicit 2D spatial layout
- **M07.L01** — Logits to probabilities with softmax — A vector of raw class scores entering softmax and producing nonnegative probabilities that sum to 1, with the highest logit remaining the highest probability  
  _Learner should notice:_ softmax changes scale but preserves ranking
- **M07.L01** — Negative log-likelihood curve — A curve of -log(p) for correct-class probability p from near 0 to 1  
  _Learner should notice:_ assigning very small probability to the true class receives a very large penalty while loss approaches zero as p approaches 1
- **M07.L01** — Full batch vs sample-wise vs minibatch optimization — Three diagrams showing one update after all samples, one update after each individual sample, and one update after each small batch  
  _Learner should notice:_ the trade-off between gradient stability and update frequency
- **M07.L01** — Dataset and DataLoader relationship — A Dataset exposing indexed samples, a shuffled index order, and a DataLoader grouping those indices into minibatches before yielding image/label tensors  
  _Learner should notice:_ Dataset defines access to individual items while DataLoader controls batching and sampling order
- **M07.L01** — Parameter explosion in a fully connected image layer — A flattened 3072-value image fully connected to 1024 hidden units, with an annotation showing a 1024×3072 weight matrix and over 3 million parameters  
  _Learner should notice:_ every hidden unit needs a separate connection to every input pixel
- **M07.L01** — Fully connected treatment of an image — A 2D image flattened into a long vector with dense connections from every pixel value to every hidden unit  
  _Learner should notice:_ the network uses many connections but has no built-in notion of local neighborhoods
- **M07.L01** — Same airplane shifted to a new image position — Two small images containing the same airplane-like pattern at different coordinates, plus a flattened-vector view showing that different feature positions become active  
  _Learner should notice:_ why a fully connected classifier must relearn similar patterns at different locations
- **M08.L01** — Fully connected image processing versus convolution — Left side shows a flattened image densely connected to hidden units; right side shows a small kernel applied locally at many positions  
  _Learner should notice:_ convolution reuses the same small set of weights instead of learning independent weights for every pixel-location relationship
- **M08.L01** — Sliding 3x3 convolution kernel — A small 3×3 kernel overlaying one neighborhood of an image, with corresponding cells multiplied and summed to produce one output pixel, then the kernel shown sliding to the next position  
  _Learner should notice:_ the identical kernel weights are reused at every location
- **M08.L01** — Conv2d channel transformation — Three RGB input channels feeding several 3×3 kernels and producing 16 output feature maps  
  _Learner should notice:_ one output channel combines information from all input channels using its own learned kernel bank
- **M08.L01** — Zero padding around a 2D input — A small image grid surrounded by one border of zero-valued ghost pixels, with a 3×3 kernel centered over an original corner pixel  
  _Learner should notice:_ padding lets the kernel produce outputs at boundary locations
- **M08.L01** — Blur kernel and vertical-edge kernel effects — Show the same simple image passed through a local averaging kernel and a vertical-edge detector, alongside the two 3×3 kernels  
  _Learner should notice:_ different local weight patterns emphasize different visual features
- **M08.L01** — Max pooling over 2x2 regions — A small activation map divided into non-overlapping 2×2 cells, with the maximum value from each cell copied into a smaller output map  
  _Learner should notice:_ strong feature responses survive while spatial resolution is halved
- **M08.L01** — Receptive field growing with depth — A sequence Conv3x3 -> MaxPool2x2 -> Conv3x3 with arrows tracing one deep output value back to a much larger area of the original image  
  _Learner should notice:_ small kernels can indirectly see large input regions when layers are stacked
- **M08.L01** — Complete baseline CNN with tensor shapes — A block diagram of two convolution/activation/pooling stages followed by flatten and two fully connected layers, annotated with the tensor shape after each stage  
  _Learner should notice:_ practice tracing channels and spatial dimensions
- **M08.L01** — CPU DataLoader to GPU model pipeline — DataLoader yields CPU minibatches, image and label tensors are transferred to GPU memory, the CNN runs on GPU, then scalar logging values return to Python  
  _Learner should notice:_ model parameters and input tensors must be on the same device
- **M08.L01** — Dropout during training versus evaluation — A feature map stack where random channels/activations are crossed out during training, beside the same network with all features active during evaluation  
  _Learner should notice:_ dropout deliberately injects randomness only while training
- **M08.L01** — Batch normalization over a minibatch — Several samples with the same feature/channel shown together, with mean and standard deviation computed across the minibatch and values rescaled before activation  
  _Learner should notice:_ normalization statistics come from the batch during training
- **M08.L01** — Residual block with skip connection — Input x splits into a learned convolutional path F(x) and an identity shortcut; the two paths are added before continuing  
  _Learner should notice:_ the shortcut provides a direct route for information and gradients around the learned block
- **M08.L01** — Closed-set classifier on an unknown class — A bird and airplane classifier receives three inputs: bird, airplane, and cat; the first two are classified appropriately while the cat is still forced into one known class with high confidence  
  _Learner should notice:_ high confidence does not imply the input belongs to the model's known distribution
- **M09.L01** — Prediction versus generation — Left side shows regression/classification with one input leading to a constrained target; right side shows a text prefix branching into many plausible next-token continuations  
  _Learner should notice:_ generation is handled by modeling a probability distribution rather than selecting one permanently fixed answer
- **M09.L01** — Vocabulary tokens and encoded sequence — A small character vocabulary mapping letters and the $ boundary token to integer IDs, then the name $ada$ shown as its token-ID sequence  
  _Learner should notice:_ the distinction between raw characters, tokens, and integer model inputs
- **M09.L01** — Character bigram matrix — A small heatmap-style matrix where rows are current characters and columns are possible next characters, with darker cells for more likely transitions  
  _Learner should notice:_ generation now depends on the previous token rather than a single global distribution
- **M09.L01** — Shifted next-token targets with padding — Several names of different lengths shown as rectangular input and target tensors, with targets shifted left and padded target cells marked -1/ignored  
  _Learner should notice:_ how one raw sequence becomes many next-token learning positions
- **M09.L01** — Embedding lookup table — Token IDs indexing rows of a learnable embedding matrix and returning dense vectors  
  _Learner should notice:_ embeddings are trainable parameters, not fixed handcrafted encodings
- **M09.L01** — Query-key-value intuition — A sequence of token representations transformed into Q, K, and V rows; one query compares against all keys and then retrieves a weighted mixture of the corresponding values  
  _Learner should notice:_ distinguish matching information (Q/K) from retrieved content (V)
- **M09.L01** — Dot-product self-attention matrix flow — Q multiplied by K-transpose to produce an N×N score matrix, softmax producing row-normalized attention weights, then multiplication by V producing contextualized outputs  
  _Learner should notice:_ each output position is a weighted combination of value vectors from the sequence
- **M09.L01** — Causal attention matrix — A lower-triangular attention grid where each row may attend to itself and earlier tokens but all future-token cells are blocked  
  _Learner should notice:_ why the matrix is triangular in an autoregressive decoder
- **M09.L01** — Multi-head self-attention — One token sequence projected into several parallel attention heads, each producing its own contextual representation, then head outputs concatenated back together  
  _Learner should notice:_ multiple heads let the same sequence be analyzed through different learned relationship patterns
- **M09.L01** — Token embedding plus positional embedding — For each sequence position, a token vector and position vector are added element-wise before entering Transformer blocks  
  _Learner should notice:_ content identity and sequence location are represented together
- **M09.L01** — BatchNorm versus LayerNorm — A small tensor diagram highlighting BatchNorm statistics across examples versus LayerNorm statistics across feature dimensions for each token representation  
  _Learner should notice:_ LayerNorm does not depend on other samples in the minibatch in the same way BatchNorm does
- **M09.L01** — Encoder-decoder Transformer and cross-attention — Source tokens flow through an encoder; decoder tokens use causal self-attention and a separate cross-attention connection into encoder outputs  
  _Learner should notice:_ distinguish self-attention inside one sequence from cross-attention between decoder queries and encoder keys/values
- **M09.L01** — Tokenization pipeline — Raw sentence entering normalization and splitting, then tokens mapped into vocabulary IDs with an unknown-token fallback  
  _Learner should notice:_ tokenizer design defines the units the Transformer actually receives
- **M09.L01** — Vision Transformer patch pipeline — An image divided into a grid of patches; each patch flattened/projected into a token embedding, a CLS token prepended, positional embeddings added, then the sequence passed into Transformer encoder blocks  
  _Learner should notice:_ image patches play the same structural role as sequence tokens
- **M10.L01** — Text generation versus image generation — Left side shows next-token probability generation; right side shows spatial image generation; both feed into a shared box labeled learn data distribution and sample new examples  
  _Learner should notice:_ different data structures can share the same generative objective
- **M10.L01** — VAE vs GAN vs diffusion — Three side-by-side simplified diagrams: encoder/decoder latent model, generator/discriminator adversarial model, and forward-noise/reverse-denoise diffusion process  
  _Learner should notice:_ all generate new samples but learn through different mechanisms
- **M10.L01** — Forward and reverse diffusion — A sequence of the same simple shape progressing from clean to heavily noised left-to-right, with a reverse arrow from noise back to structure  
  _Learner should notice:_ training relies on a known corruption process and generation relies on a learned denoising process
- **M10.L01** — Linear beta noise schedule — A plot of beta against timestep increasing from a small starting value to a larger final value  
  _Learner should notice:_ the amount of corruption is scheduled rather than arbitrary
- **M10.L01** — Closed-form diffusion at arbitrary timesteps — One clean point-cloud sample branches directly to several different noise levels t=0, 250, 500, 800, 999 without drawing every intermediate transition  
  _Learner should notice:_ training can jump directly to a random timestep rather than simulating all earlier steps
- **M10.L01** — Denoising model input embeddings — Noisy x-coordinate, noisy y-coordinate, and timestep each pass through their own embedding transform; the three embeddings are concatenated and fed into an MLP that outputs two noise values  
  _Learner should notice:_ the model conditions its prediction on both location and noise level
- **M10.L01** — Reverse diffusion sampling progression — Random 2D points at a late timestep gradually reorganizing through several intermediate snapshots into the PyTorch-logo point-cloud structure  
  _Learner should notice:_ generation is iterative rather than a single forward model call
- **M10.L01** — CT volume as stacked slices and voxels — Several grayscale CT slices stacked into a 3D volume, with one small rectangular voxel highlighted and labeled with depth/height/width spacing  
  _Learner should notice:_ CT is volumetric data and that voxel dimensions do not have to be cubic
- **M10.L01** — Lung-cancer project pipeline — Raw CT volume flows into data loading, then segmentation/candidate localization, then cropped candidate volumes into a 3D classifier, then candidate results combined for patient-level output  
  _Learner should notice:_ one hard problem has been decomposed into smaller interfaces
- **M10.L01** — Whole CT versus candidate crop — Left side shows a large chest CT slice/volume with one tiny highlighted nodule; right side shows a zoomed candidate crop around the nodule  
  _Learner should notice:_ how little of the full scan is relevant to the focused classification problem
- **M11.L01** — Raw CT data to PyTorch sample — Raw .mhd/.raw files and candidate CSV metadata flow through loading, coordinate conversion, cropping, tensor conversion, and finally a training-sample tuple  
  _Learner should notice:_ model-ready data is the result of several transformations, not one file-read call
- **M11.L01** — Fuzzy matching two nearby annotation centers — Two nearly overlapping 3D coordinate points labeled candidate.csv and annotations.csv inside the same nodule-sized region  
  _Learner should notice:_ noisy metadata may require domain-aware approximate matching rather than exact equality
- **M11.L01** — MetaIO files to CT array — A .mhd metadata file and .raw binary file enter SimpleITK and produce one D×H×W NumPy array plus origin/spacing/direction metadata  
  _Learner should notice:_ the parser hides file-format complexity but the pipeline still needs to understand the meaning of the loaded data
- **M11.L01** — Hounsfield Unit range — A horizontal HU scale marking air near -1000, water near 0, soft tissue around intermediate values, and dense bone around +1000, with clipping boundaries highlighted  
  _Learner should notice:_ why the chapter limits the working intensity range
- **M11.L01** — XYZ patient coordinates versus IRC array coordinates — A CT volume shown with one physical patient-space XYZ coordinate system and a separate array-index IRC system, with different origins and axis conventions  
  _Learner should notice:_ coordinate conversion is required before indexing the voxel array
- **M11.L01** — Candidate crop from CT volume — A full 3D CT volume with a small candidate center marker, then a zoomed rectangular 3D crop extracted around that center  
  _Learner should notice:_ the classifier receives a focused local volume rather than the complete patient scan
- **M11.L01** — LunaDataset sample tuple — A 1×32×48×48 candidate tensor plus class tensor, series UID, and IRC center grouped into one Dataset return tuple  
  _Learner should notice:_ training data can include both model inputs and metadata useful for debugging/evaluation
- **M11.L01** — CT candidate visualization workflow — A full CT slice with candidate marker followed by neighboring slices through the extracted crop  
  _Learner should notice:_ visual inspection connects metadata, coordinate conversion, and final model input in one sanity check
- **M12.L01** — Chapter 13 end-to-end training pipeline — LunaDataset feeds DataLoader batches into a 3D classifier; the training branch computes loss, backward, and optimizer step, while the validation branch computes read-only metrics  
  _Learner should notice:_ this is the first complete train-and-evaluate loop for the CT project
- **M12.L01** — Candidate samples collated into a 3D batch — Several C×D×H×W candidate tensors are stacked into an N×C×D×H×W batch by DataLoader  
  _Learner should notice:_ DataLoader adds the batch dimension while preserving the single CT-intensity channel
- **M12.L01** — DataLoader workers feeding a GPU — Multiple CPU worker processes load and prepare batches into a queue while the GPU consumes the previous batch  
  _Learner should notice:_ overlapping data preparation with GPU work reduces idle time
- **M12.L01** — LunaModel tail-backbone-head architecture — Input 3D crop enters BatchNorm3d tail, four repeated convolutional blocks form the backbone, then flattened features enter a linear two-class head  
  _Learner should notice:_ the familiar high-level vision-model organization
- **M12.L01** — Growing 3D receptive field through two convolutions — One deep output voxel traced backward through two 3×3×3 convolution neighborhoods into a larger 5×5×5 source region, followed by 2×2×2 pooling  
  _Learner should notice:_ small kernels compose into larger effective receptive fields
- **M12.L01** — Training versus validation loop — Parallel diagrams show training using train mode, forward, loss, backward, and optimizer step; validation uses eval mode, forward, metrics, and no_grad with no backward/update arrows  
  _Learner should notice:_ validation must not modify weights
- **M12.L01** — Overall accuracy split into per-class performance — One large overall-accuracy bar is decomposed into separate non-nodule and nodule accuracy/loss panels  
  _Learner should notice:_ how a strong majority-class score can hide catastrophic minority-class failure
- **M12.L01** — TensorBoard training and validation dashboard — Several time-series charts for overall loss, positive loss, negative loss, and percent correct with training and validation runs visible together  
  _Learner should notice:_ trends expose problems more clearly than isolated epoch numbers
- **M12.L01** — Misleading 99.7 percent accuracy under class imbalance — A dataset graphic with roughly 99.7 percent negative samples and 0.3 percent positive samples; a classifier predicts every item negative and still receives a 99.7 percent overall accuracy badge while positive recall is zero  
  _Learner should notice:_ immediately see why the aggregate score is misleading
- **M13.L01** — Four binary-classification quadrants — A clean 2×2 confusion-grid showing true positive, true negative, false positive, and false negative with nodule/non-nodule examples  
  _Learner should notice:_ immediately see that false positives and false negatives are different mistakes with different consequences
- **M13.L01** — Threshold tradeoff between positives and negatives — Overlapping distributions of negative and positive model scores with a movable vertical threshold; arrows show that moving left raises recall while moving right raises precision  
  _Learner should notice:_ threshold changes trade one error type for another
- **M13.L01** — Precision versus recall denominators — Two small diagrams highlight TP/(TP+FN) for recall and TP/(TP+FP) for precision using the same TP/FP/FN/TN grid  
  _Learner should notice:_ both metrics use TP but answer different questions
- **M13.L01** — F1 surface over precision and recall — A conceptual contour/surface plot where the best values occur when both precision and recall are high and balanced, while regions with one value near zero remain poor  
  _Learner should notice:_ why F1 discourages extreme one-sided behavior
- **M13.L01** — Gradient tug-of-war under 400-to-1 imbalance — A huge group of negative examples pulls model weights strongly toward negative predictions while a tiny positive group pulls in the opposite direction  
  _Learner should notice:_ why random initialization plus extreme imbalance can rapidly collapse to a majority-only solution
- **M13.L01** — Small false-positive rate on a huge negative class — A large block of 54,971 negative samples with only 1 percent highlighted as false positives, placed beside 136 true positive cases; the false-positive group is still several times larger  
  _Learner should notice:_ why precision can remain poor despite 99 percent negative accuracy
- **M13.L01** — Training versus validation positive loss divergence — Two curves over epochs: training positive loss falls toward zero while validation positive loss turns upward  
  _Learner should notice:_ identify the point where more training begins to harm generalization
- **M13.L01** — One nodule producing many augmented views — One original 3D candidate crop branches into mirrored, shifted, scaled, rotated, and noisy variants, all keeping the same positive label  
  _Learner should notice:_ augmentation changes appearance while preserving the task-relevant identity
- **M13.L01** — Valid CT rotation plane — A 3D CT candidate crop with the in-plane X-Y axes highlighted and a rotation arrow around the head-foot axis, while the anisotropic slice-depth axis is marked as special  
  _Learner should notice:_ why rotation is restricted instead of freely rotating across all 3D axes
- **M13.L01** — TensorBoard comparison of augmentation runs — Multiple validation curves for balanced baseline, rotation, noise, and fully augmented models across recall, precision, F1, and positive loss  
  _Learner should notice:_ different augmentations affect precision and recall differently and that full augmentation reduces overfitting
- **M14.L01** — Multi-stage CT pipeline with segmentation before classification — Raw CT slice enters a segmentation model, candidate regions are extracted, then passed into the existing classifier  
  _Learner should notice:_ segmentation answers where while classification answers what
- **M14.L01** — Semantic segmentation vs instance segmentation vs object detection — One medical-style image shown three times: semantic mask labels all tumor pixels as one class, instance segmentation gives separate IDs to separate tumors, and object detection uses bounding boxes  
  _Learner should notice:_ distinguish pixel-level categories, object identities, and bounding boxes
- **M14.L01** — Classification versus segmentation output — Same input image feeds two models; classifier returns one class vector, segmenter returns an image-sized mask  
  _Learner should notice:_ segmentation must preserve location information throughout the network
- **M14.L01** — SAM architecture — Input image enters a ViT image encoder; point/box/mask prompts enter a prompt encoder; both streams meet in a mask decoder that outputs masks and confidence  
  _Learner should notice:_ the three-component division of SAM
- **M14.L01** — Binary segmentation mask — Original image beside a black-and-white mask where the target object is white and background is black  
  _Learner should notice:_ every output pixel corresponds spatially to the input
- **M14.L01** — Point-prompt segmentation — Image with one marked point inside an object and three candidate masks produced around that region  
  _Learner should notice:_ the prompt guides which part of the image SAM should segment
- **M14.L01** — Extracting one 2D CT slice from a 3D volume — CT volume shown as stacked slices with one highlighted slice at the candidate depth; highlighted slice is pulled out as a 2D image  
  _Learner should notice:_ the adaptation required for a 2D model
- **M14.L01** — Fine-tuning dataset layout — Folder tree with CT images, mask images, and metadata.jsonl; one metadata record links series UID and center IRC to matching image and mask paths  
  _Learner should notice:_ the pairing and traceability structure
- **M14.L01** — SAM as mask teacher and SegFormer as deployable segmenter — Known point prompts plus CT slices go through SAM to create training masks; those image-mask pairs train SegFormer; trained SegFormer later receives only a CT image  
  _Learner should notice:_ why the second model removes the prompt requirement
- **M14.L01** — SegFormer encoder-decoder overview — CT image passes through transformer-style encoder stages at multiple scales, then a lightweight decoder fuses features and outputs a two-class pixel mask  
  _Learner should notice:_ segmentation retains multi-scale spatial information rather than collapsing to one class vector
- **M14.L01** — Fine-tuning train and validation loss curves — Two TensorBoard-style curves for SegFormer training and validation loss both trending downward  
  _Learner should notice:_ inspect whether validation follows training rather than diverging upward
- **M14.L01** — SegFormer inference comparison — Three panels: CT slice, target mask, predicted segmentation map  
  _Learner should notice:_ visually compare whether the predicted region overlaps the target nodule area

## COURSE-004_Applied_NLP_with_Transformers — 94 images

- **M01.L01** — Transformer evolution timeline — A simple chronological timeline showing the 2017 Transformer paper, ULMFiT, GPT, BERT, and the subsequent expansion of transformer models  
  _Learner should notice:_ modern transformer NLP emerged from the combination of a new architecture and practical transfer-learning methods
- **M01.L01** — RNN unrolled through time — A recurrent network shown both as a feedback loop and as an unrolled sequence of hidden states h1, h2, h3, h4  
  _Learner should notice:_ each step depends on the state produced by the previous step
- **M01.L01** — Encoder-decoder bottleneck — An RNN encoder reading several input tokens into a final hidden-state vector, followed by an RNN decoder generating output tokens one at a time  
  _Learner should notice:_ the single final encoder state forms a narrow information bottleneck between input and output
- **M01.L01** — Attention alignment matrix — A heatmap with source-language tokens on one axis and target-language tokens on the other, with darker cells showing stronger attention weights  
  _Learner should notice:_ strong cells can connect corresponding words even when their positions differ between languages
- **M01.L01** — Transformer self-attention overview — A simplified Transformer encoder-decoder diagram showing self-attention blocks followed by feed-forward networks, without detailed equations  
  _Learner should notice:_ recurrence is removed and attention is the main mechanism connecting token information
- **M01.L01** — Training from scratch versus transfer learning — Side-by-side diagram comparing a task model trained only on a small labeled dataset with a pretrained model adapted to that same downstream task  
  _Learner should notice:_ transfer learning reuses general knowledge instead of relearning everything from the task dataset
- **M01.L01** — ULMFiT three-stage workflow — A three-step flow labeled pretraining, domain adaptation, and task fine-tuning  
  _Learner should notice:_ how a broadly pretrained language model is progressively specialized
- **M01.L01** — Hugging Face ecosystem map — A simple hub-and-spoke diagram connecting the Hub with Transformers, Tokenizers, Datasets, and Accelerate  
  _Learner should notice:_ a practical NLP workflow is an ecosystem of interoperating tools rather than only a model architecture
- **M02.L01** — Transformer text-classification pipeline — A simple flow from raw tweet to Dataset processing, tokenizer, DistilBERT, classification output, and prediction on new text  
  _Learner should notice:_ text must pass through data preparation and tokenization before the transformer can classify it
- **M02.L01** — Emotion class distribution — A horizontal bar chart showing that some emotion classes are much more frequent than others  
  _Learner should notice:_ why class imbalance changes how raw accuracy should be interpreted
- **M02.L01** — Tweet length distribution by emotion — Boxplots of words per tweet grouped by emotion, all well below the DistilBERT input limit  
  _Learner should notice:_ these tweets are short enough that truncation is unlikely to remove important content
- **M02.L01** — Padding and attention mask — Two tokenized sequences of different lengths padded to the same width, with an attention mask showing 1 for real tokens and 0 for padding  
  _Learner should notice:_ padding fixes tensor shape while the mask prevents PAD positions from being treated as meaningful text
- **M02.L01** — Feature-extraction architecture — DistilBERT encoder shown as frozen, producing a hidden-state vector that is passed to a separate classifier such as logistic regression  
  _Learner should notice:_ only the final classifier is trained while the transformer body stays unchanged
- **M02.L01** — UMAP projection of emotion hidden states — A 2D projection with separate panels or colors for sadness, joy, love, anger, fear, and surprise  
  _Learner should notice:_ some emotions form similar regions while a 2D projection is only a simplified view of the original 768-dimensional space
- **M02.L01** — Feature-based confusion matrix — A normalized confusion matrix for the logistic-regression classifier using DistilBERT hidden states  
  _Learner should notice:_ the diagonal represents correct predictions while off-diagonal cells reveal specific class confusions
- **M02.L01** — Fine-tuning architecture — DistilBERT encoder connected to a classification head with both parts marked trainable and an arrow from loss/backpropagation updating the full model  
  _Learner should notice:_ contrast this with feature extraction, where the encoder is frozen
- **M02.L01** — Emotion prediction probabilities — A bar chart showing the model's class probabilities for a new positive tweet, with joy clearly highest  
  _Learner should notice:_ inference produces scores across classes and the final predicted class comes from the strongest score
- **M01.L02** — Transformer encoder-decoder overview — A clean diagram showing input tokens entering an encoder stack, encoder outputs feeding a decoder stack, and the decoder generating output tokens one by one  
  _Learner should notice:_ the encoder processes the source sequence while the decoder produces the target sequence autoregressively
- **M01.L02** — Transformer encoder layer zoom — One encoder block showing multi-head self-attention, residual connection, layer normalization, feed-forward network, and the second residual/normalization path  
  _Learner should notice:_ attention and the feed-forward network are separate stages and that the hidden dimension is preserved across the block
- **M01.L02** — Contextualized meaning of flies — Two short sentences containing the word 'flies', with attention links from 'flies' to context words such as 'time' and 'arrow' in one sentence and 'fruit' and 'banana' in the other  
  _Learner should notice:_ the same token can receive different contextual representations depending on surrounding words
- **M01.L02** — Scaled dot-product attention pipeline — A left-to-right diagram with Q and K entering a dot product, division by sqrt(d_k), softmax producing attention weights, and multiplication with V producing the output  
  _Learner should notice:_ Q and K determine relevance while V supplies the information that is actually aggregated
- **M01.L02** — Multi-head attention — One input sequence splitting into several parallel attention heads, each with its own Q/K/V projections, followed by concatenation and a final linear projection  
  _Learner should notice:_ heads process the same sequence in parallel but can learn different attention patterns
- **M01.L02** — Pre-norm versus post-norm — Side-by-side encoder-block diagrams showing where layer normalization sits relative to the residual connection in pre-norm and post-norm arrangements  
  _Learner should notice:_ focus on the ordering difference rather than memorizing every arrow
- **M01.L02** — Token plus position embeddings — A sequence showing token embeddings and position embeddings being added element-wise before entering the encoder stack  
  _Learner should notice:_ attention receives both token identity information and sequence-order information
- **M01.L02** — Transformer decoder with causal mask — A decoder layer showing masked self-attention first and encoder-decoder attention second, plus a small triangular attention mask  
  _Learner should notice:_ self-attention cannot see future target positions while cross-attention can read encoder outputs
- **M01.L02** — Transformer family tree — A three-branch family tree with encoder-only, decoder-only, and encoder-decoder at the top, then representative models from the chapter under each branch  
  _Learner should notice:_ use the diagram to categorize models by architecture rather than memorizing an unstructured list of names
- **M01.L03** — IOB2 named entity labeling — A short sentence with tokens shown in boxes and colored labels underneath for B-PER, I-PER, B-ORG, B-LOC, and O  
  _Learner should notice:_ B marks the start of an entity span, I continues it, and O means the token is not part of an entity
- **M01.L03** — Zero-shot cross-lingual transfer — A flow diagram where one multilingual XLM-R model is fine-tuned on labeled German NER data and then evaluated directly on French, Italian, and English without target-language fine-tuning  
  _Learner should notice:_ the task labels stay the same while the language changes
- **M01.L03** — Tokenizer pipeline — A four-stage pipeline labeled normalization, pretokenization, subword tokenizer model, and postprocessing, using one short multilingual-friendly example  
  _Learner should notice:_ subword splitting is only one stage of the complete tokenization process
- **M01.L03** — Sequence classification versus token classification — Side-by-side diagrams: sequence classification uses one pooled representation for one label, while NER sends every token hidden state through the same classifier to produce one entity label per token  
  _Learner should notice:_ the difference between one prediction per sequence and one prediction per token
- **M01.L03** — Word-to-subword NER label alignment — A word-level NER sequence above a subword-tokenized sequence, with arrows from each original word to its subwords; first subwords receive the real label and later subwords/special tokens receive -100/IGN  
  _Learner should notice:_ tokenization changes sequence length, so labels must be explicitly realigned before training
- **M01.L03** — NER error-analysis dashboard — A conceptual figure containing three panels: highest-loss tokens, a normalized confusion matrix highlighting B-ORG versus I-ORG confusion, and one high-loss sequence with token labels and predictions  
  _Learner should notice:_ useful error analysis moves from aggregate score to class-level, token-level, and example-level investigation
- **M01.L03** — Zero-shot versus target-language fine-tuning curve — A learning curve with number of French labeled training examples on the x-axis, F1 on the y-axis, a horizontal line for German-to-French zero-shot performance, and an increasing line for direct French fine-tuning  
  _Learner should notice:_ the preferred strategy can change as labeled target-language data becomes available
- **M01.L03** — Multilingual fine-tuning comparison — A simple grouped bar chart comparing German-only, each-language, and all-language fine-tuning across de, fr, it, and en using the chapter's F1 values  
  _Learner should notice:_ joint multilingual training improves the overall balance across languages in this experiment
- **M01.L04** — Autoregressive text generation loop — A step-by-step diagram showing prompt -> language model -> next-token probabilities -> selected token -> append token to prompt -> repeat  
  _Learner should notice:_ one new token is chosen per decoding step and the generated token becomes part of the next input
- **M01.L04** — Beam search with two beams — A small search tree showing a prompt expanding into candidate tokens, then multiple second-step candidates, with only the two highest-scoring partial sequences retained after each step  
  _Learner should notice:_ beam search explores several paths rather than committing to one greedy continuation immediately
- **M01.L04** — Temperature changes token probabilities — Three probability distributions over the same candidate tokens for low, medium, and high temperature, with low temperature sharply concentrated and high temperature flatter  
  _Learner should notice:_ temperature changes the distribution rather than directly specifying which token must be selected
- **M01.L04** — Top-k versus top-p sampling — A sorted next-token probability distribution with one fixed vertical cutoff illustrating top-k and one cumulative-probability threshold illustrating top-p  
  _Learner should notice:_ top-k keeps a fixed number of tokens while top-p adapts the number of candidates to the shape of the distribution
- **M01.L04** — Complete text-generation decoding workflow — A single flowchart from prompt and tokenizer through model logits, probability adjustments, decoding choices, selected token, and the feedback loop into the next generation step  
  _Learner should notice:_ clearly that the model and decoder are separate parts of the generation system
- **M01.L05** — Summarization as sequence-to-sequence learning — A long document entering an encoder-decoder transformer and a short summary coming out, with arrows showing compression from source sequence to target sequence  
  _Learner should notice:_ the output is a newly generated sequence rather than a fixed class label
- **M01.L05** — Long-document truncation problem — A long article represented as many text blocks, a model context window covering only the beginning, and later blocks faded or cut off  
  _Learner should notice:_ truncation can remove information that may be important for the final summary
- **M01.L05** — Comparison of summarization model families — A compact four-column visual for GPT-2, T5, BART, and PEGASUS showing decoder-only prompting for GPT-2 and encoder-decoder summarization for the other models, with their pretraining idea summarized beneath each  
  _Learner should notice:_ models differ both in architecture and in how closely their training objective matches summarization
- **M01.L05** — BLEU versus ROUGE intuition — Two overlapping sets labeled generated n-grams and reference n-grams, with BLEU highlighting the generated side as precision-oriented and ROUGE highlighting the reference side as recall-oriented  
  _Learner should notice:_ the directional difference without memorizing formulas
- **M01.L05** — Domain shift from news to dialogue — A side-by-side visual showing a structured news article with headline-style summary on the left and an informal chat dialogue with abstractive conversational summary on the right  
  _Learner should notice:_ the task name is the same but the data distribution and desired output style are different
- **M01.L05** — Teacher forcing in an encoder-decoder model — A training diagram where the encoder receives the source dialogue and the decoder receives the gold target summary shifted right by one token, with arrows showing next-token prediction at each decoder position  
  _Learner should notice:_ the decoder sees previous correct target tokens during training but never the current/future target token it is predicting
- **M01.L05** — Hierarchical long-document summarization — A long document split into several chunks, each producing a short partial summary, followed by a second summarization stage combining those partial summaries  
  _Learner should notice:_ one conceptual alternative to simply truncating a long document
- **M01.L07** — Two-stage question answering system — A question enters a retriever that selects relevant documents, then a reader extracts an answer span from one of those documents  
  _Learner should notice:_ document retrieval and answer extraction are separate problems in a practical QA system
- **M01.L07** — Extractive QA span-classification head — Question and context tokens enter a transformer encoder; each token hidden state feeds a small QA head that produces start and end logits, with the selected answer span highlighted inside the context  
  _Learner should notice:_ the answer is defined by two token positions
- **M01.L07** — Sliding window for long-context QA — A long token sequence with the question shown separately and several overlapping context windows beneath it; the answer span lies near a boundary but is fully captured in at least one window  
  _Learner should notice:_ why overlap/stride is necessary instead of simple truncation
- **M01.L07** — Retriever-reader QA architecture — Question -> document store -> retriever -> top-k documents -> optional reranker -> reader -> answer candidates, with clear separation of retrieval and reading stages  
  _Learner should notice:_ retrieval reduces the amount of text the expensive reader must process
- **M01.L07** — DPR bi-encoder architecture — A question enters one BERT-like encoder and a passage enters another; each produces a dense vector and their similarity determines relevance  
  _Learner should notice:_ the question and passage are encoded separately, which enables efficient retrieval over many stored passage vectors
- **M01.L07** — QA domain-adaptation path — A three-stage pipeline from pretrained MiniLM to SQuAD fine-tuning to SubjQA fine-tuning, contrasted with a shorter direct MiniLM-to-SubjQA path that performs worse in the chapter  
  _Learner should notice:_ the benefit of task transfer before small-domain adaptation
- **M01.L07** — QA component versus end-to-end evaluation — A diagram with separate metric boxes under retriever (Recall@k), reader (EM/F1 with gold contexts), and full system (end-to-end EM/F1 + latency)  
  _Learner should notice:_ every layer needs its own evaluation as well as a final system-level evaluation
- **M01.L07** — RAG architecture — Question -> dense retriever -> top-k passages -> sequence-to-sequence generator -> generated answer, with the retrieval stage visually connected to generation  
  _Learner should notice:_ RAG grounds generation in retrieved external documents rather than generating from the language model alone
- **M01.L07** — QA hierarchy of needs — A three-level pyramid with retrieval/search at the base, extractive QA in the middle, and generative QA/RAG at the top  
  _Learner should notice:_ strong retrieval is foundational and generative QA should build on a reliable evidence pipeline
- **M01.L06** — Transformer production optimization overview — A large accurate transformer on the left and four optimization paths labeled distillation, quantization, ONNX Runtime, and pruning leading toward a smaller/faster deployment model  
  _Learner should notice:_ several techniques can be combined rather than treated as mutually exclusive choices
- **M01.L06** — In-scope versus out-of-scope intent detection — Three small chat examples: one correctly routed in-scope query, one out-of-scope query incorrectly forced into a known intent, and one out-of-scope query correctly sent to a fallback response  
  _Learner should notice:_ production classification includes safe handling of unknown requests, not only predicting known intents
- **M01.L06** — Teacher-student knowledge distillation — One input branching into a large teacher and smaller student; teacher produces soft class probabilities, student produces its own probabilities, and the final student loss combines label loss with teacher-student distribution matching  
  _Learner should notice:_ the teacher guides training but is not needed for student inference after training
- **M01.L06** — Hard labels versus soft teacher probabilities — Three side-by-side bar charts: one-hot hard label, normal teacher softmax, and temperature-softened teacher probabilities  
  _Learner should notice:_ higher temperature reveals relative probabilities among non-winning classes
- **M01.L06** — FP32 to INT8 quantization — A continuous number line of floating-point weight values mapped onto a smaller set of discrete INT8 levels using a scale and zero point  
  _Learner should notice:_ quantization saves precision by grouping nearby floating-point values into shared integer levels
- **M01.L06** — Simplified ONNX computational graph — A small directed graph of model operators such as input, MatMul, Add, LayerNorm, and output, shown as connected nodes  
  _Learner should notice:_ ONNX describes the inference computation as a graph of standardized operations rather than a high-level Python model class
- **M01.L06** — Production optimization benchmark trade-off — A scatter plot with average latency on the x-axis and accuracy on the y-axis, bubble size representing model size, containing the BERT baseline, distilled model, quantized model, ORT model, and ORT-quantized model using the chapter's benchmark values  
  _Learner should notice:_ the optimized models move toward lower latency and smaller size without a large accuracy penalty
- **M01.L06** — Dense network versus pruned sparse network — Two small neural network diagrams side by side, one with dense connections and one with many connections removed  
  _Learner should notice:_ pruning reduces the number of active nonzero connections rather than merely reducing numerical precision
- **M01.L06** — Magnitude versus movement pruning — A side-by-side conceptual comparison where magnitude pruning ranks weights by absolute size and movement pruning ranks them using learned movement/importance scores during fine-tuning  
  _Learner should notice:_ the two methods answer 'which weights matter?' using different signals
- **M01.L08** — Low-label method decision tree — A decision tree beginning with 'Do you have labeled data?', then branching by amount of labeled data and availability of unlabeled data toward zero-shot, few-shot/embedding methods, domain adaptation/UDA/UST, or ordinary fine-tuning  
  _Learner should notice:_ the correct method depends on the available supervision, not on which technique sounds most advanced
- **M01.L08** — NLI zero-shot classification — One issue text acts as the premise and branches into several hypotheses such as 'This example is about new model', '...tokenization', and '...documentation'; each receives an entailment score  
  _Learner should notice:_ no task-specific classifier is trained; class names are expressed directly in natural language
- **M01.L08** — Text data augmentation examples — One source sentence branching into synonym replacement, random insertion, random swap, random deletion, and back-translation variants  
  _Learner should notice:_ augmentation attempts to vary surface form while preserving the original class label
- **M01.L08** — Embedding nearest-neighbor classifier — Several labeled text points represented in embedding space, a new query point, and lines connecting it to its nearest neighbors whose labels are aggregated  
  _Learner should notice:_ the pretrained representation does the heavy lifting without updating model weights
- **M01.L08** — FAISS clustered vector index — A 2D embedding space partitioned into several regions around centroid points, with one query vector first matched to a centroid and then compared with vectors inside that region  
  _Learner should notice:_ how partitioning avoids comparing the query with every stored embedding
- **M01.L08** — Domain-adaptive language-model training — A pipeline from general BERT pretraining to continued masked-language-model training on many unlabeled GitHub issues, then to a small supervised classifier  
  _Learner should notice:_ unlabeled domain text is used before the task-specific fine-tuning stage
- **M01.L08** — Unsupervised data augmentation consistency training — One unlabeled example branches into original and augmented text; both enter the same model and their output distributions are connected by a consistency/KL loss, alongside a normal supervised loss from labeled examples  
  _Learner should notice:_ UDA extracts a training signal from unlabeled text without inventing hard labels for every example
- **M01.L08** — Uncertainty-aware self-training loop — Labeled data trains a teacher; the teacher predicts pseudo-labels with uncertainty estimation on unlabeled data; selected pseudo-labeled examples train a student; the student becomes the next teacher and the loop repeats  
  _Learner should notice:_ both the iterative teacher-student cycle and the role of uncertainty in selecting pseudo-labels
- **M01.L10** — Fine-tuning versus training from scratch — A decision diagram comparing a small domain dataset flowing into pretrained-model fine-tuning versus a massive distinct domain corpus flowing into custom tokenizer training and fresh model pretraining  
  _Learner should notice:_ training from scratch requires both much more data and much more compute
- **M01.L10** — Corpus-to-model behavior pipeline — A large dataset containing useful patterns plus bias/noise/copyright/privacy risks feeding pretraining, followed by a model whose generated outputs reflect both the useful and undesirable corpus patterns  
  _Learner should notice:_ corpus choices propagate into model behavior
- **M01.L10** — Memory mapping versus streaming — Two side-by-side workflows: memory mapping shows a large local Arrow/cache file accessed through small memory windows, while streaming shows remote compressed files sending only the current batch to RAM  
  _Learner should notice:_ both avoid loading the complete corpus into memory
- **M01.L10** — Byte-level BPE for Python code — A short indented Python function mapped first into byte-aware symbols for spaces and newlines, then frequent byte combinations merged into larger BPE tokens  
  _Learner should notice:_ indentation and line breaks remain represented rather than being discarded
- **M01.L10** — Generic versus code-trained tokenizer — The same Python function tokenized by a generic GPT-2 tokenizer and by the custom CodeParrot tokenizer, with token counts shown below  
  _Learner should notice:_ the domain tokenizer groups indentation and common code patterns more efficiently
- **M01.L10** — Three pretraining objectives for code — Three side-by-side mini diagrams: CLM predicts future code with a decoder, MLM reconstructs masked code with an encoder, and seq2seq maps code to comments or comments to code with an encoder-decoder  
  _Learner should notice:_ task objective determines the appropriate architecture
- **M01.L10** — Constant-length CLM preprocessing — Several code files of different lengths are tokenized and concatenated with EOS markers, then sliced into equal 1024-token chunks  
  _Learner should notice:_ file boundaries are preserved with EOS tokens while training sequences stay fully packed
- **M01.L10** — Four-GPU data parallel training — A main data stream splits into four batches sent to four GPUs, each GPU contains the same model, local gradients flow into an averaging/reduce operation, and the averaged gradient is sent back to all four model copies  
  _Learner should notice:_ data is divided while each GPU maintains a synchronized copy of the model
- **M01.L10** — Training loss and perplexity curves — Two conceptual curves over processed tokens showing training loss and validation perplexity decreasing, with separate small-model and large-model curves  
  _Learner should notice:_ the larger model improves faster with respect to tokens processed even though the wall-clock training run is longer
- **M01.L10** — Functional evaluation for generated code — A programming prompt branches into several generated code candidates; each candidate runs through the same unit-test suite, producing pass/fail results; the final metric is based on functional success rather than text overlap  
  _Learner should notice:_ semantic correctness of code is best checked by execution
- **M01.L09** — Three transformer research directions — A central transformer branching into three paths labeled scaling, efficient attention, and multimodal/beyond-text learning  
  _Learner should notice:_ the chapter treats these as distinct but complementary ways of extending transformer capability
- **M01.L09** — Scaling laws on log-log axes — Three small charts showing test loss decreasing smoothly as compute, dataset size, and model size increase, with approximately straight trends on log-log axes  
  _Learner should notice:_ the similar power-law shape across N, D, and C
- **M01.L09** — Scaling challenge stack — A vertical stack labeled infrastructure, cost, dataset curation, model evaluation, and deployment surrounding a very large language model  
  _Learner should notice:_ scaling affects the entire ML lifecycle, not only training
- **M01.L09** — Quadratic self-attention growth — Attention matrices for short, medium, and long sequences shown growing from small square to much larger square, with n² highlighted  
  _Learner should notice:_ doubling sequence length roughly quadruples the pairwise attention-score space
- **M01.L09** — Atomic sparse attention patterns — Five small attention matrices showing global, band, dilated, random, and block-local patterns using filled cells for calculated scores and blank cells for skipped scores  
  _Learner should notice:_ compare how each pattern reduces the number of pairwise calculations
- **M01.L09** — Longformer and BigBird compound sparsity — Two attention matrices side by side: Longformer showing local band plus global rows/columns, and BigBird adding random sparse links  
  _Learner should notice:_ practical efficient-attention models combine multiple sparsity patterns
- **M01.L09** — Standard versus linearized attention — A side-by-side computational diagram: standard attention explicitly forms a QK^T matrix, while linearized attention applies feature maps and rearranged matrix products without materializing the full pairwise matrix  
  _Learner should notice:_ focus on the structural difference rather than the detailed algebra
- **M01.L09** — Vision Transformer patch pipeline — An image divided into equal square patches, each patch converted to an embedding, position embeddings added, then all patch tokens entering a transformer encoder  
  _Learner should notice:_ the analogy between image patches and text tokens
- **M01.L09** — TAPAS table question answering — A small table, a natural-language question above it, selected cells highlighted, and an optional aggregator such as SUM or COUNT producing the final answer  
  _Learner should notice:_ answering may require both cell selection and aggregation
- **M01.L09** — wav2vec 2.0 speech-recognition pipeline — An audio waveform entering convolutional feature extraction, then transformer context layers, then producing a text transcription  
  _Learner should notice:_ the combination of low-level audio feature processing and transformer-based contextual representation learning
- **M01.L09** — Multimodal document understanding with LayoutLM — A scanned invoice with text boxes and coordinates feeding text, visual, and layout embeddings into one transformer  
  _Learner should notice:_ document understanding combines what the text says with where it appears and what the page looks like
- **M01.L09** — CLIP contrastive learning — A batch of images and captions encoded into vectors with a similarity matrix; matching image-caption pairs highlighted along the diagonal and mismatched pairs shown off-diagonal  
  _Learner should notice:_ training rewards matching pairs and separates mismatches

## COURSE-005_Applied_LLM_Engineering — 184 images

- **M01.L01** — ...
- **M01.L01** — Language AI landscape — A simple map showing Language AI as the broader field, with branches for representation, classification, clustering, semantic search/retrieval, translation, and generation/LLMs  
  _Learner should notice:_ LLMs are one important part of Language AI rather than the entire field
- **M01.L01** — Recent history of Language AI — A timeline-style figure showing the progression from bag-of-words to word2vec, sequence models with attention, Transformers, BERT, GPT, and modern LLM systems  
  _Learner should notice:_ modern LLMs emerged through a sequence of improvements in representation and context handling
- **M01.L01** — Bag-of-words pipeline — A four-stage diagram: two input sentences → tokenization → combined vocabulary → count vectors  
  _Learner should notice:_ the method converts text into numbers by counting tokens, but does not encode rich meaning or context
- **M01.L01** — Semantic embedding space — A 2D conceptual projection with related words grouped close together and unrelated words farther apart  
  _Learner should notice:_ semantic similarity is represented by geometric closeness, while remembering that real embeddings usually have many dimensions
- **M01.L01** — Attention in translation — An encoder-decoder translation diagram with visible attention links between source and target words, including a strong link between “llamas” and its translated form  
  _Learner should notice:_ the decoder can focus on the most relevant source token instead of relying only on one compressed context vector
- **M01.L01** — Transformer encoder-decoder mental model — A simplified Transformer diagram with stacked encoder blocks on the left, stacked decoder blocks on the right, self-attention inside both, encoder-to-decoder attention, and a mask over future decoder positions  
  _Learner should notice:_ the difference between encoding the full input and autoregressively generating output without looking ahead
- **M01.L01** — BERT versus GPT architecture — A side-by-side conceptual diagram showing BERT as an encoder-only stack producing representations and GPT as a decoder-only stack producing text token by token  
  _Learner should notice:_ both are Transformer-based but optimized for different primary roles
- **M01.L01** — LLM training paradigm — A two-stage diagram contrasting traditional one-step task training with LLM pretraining on broad text followed by fine-tuning/post-training for a narrower task or instruction following  
  _Learner should notice:_ expensive general pretraining is reused, while adaptation happens afterward
- **M01.L01** — Hosted API versus local open model — A side-by-side diagram: application → external provider API → hosted proprietary model, versus application → locally hosted open model on user hardware  
  _Learner should notice:_ the trade-off between convenience/provider-managed compute and local control/privacy/hardware responsibility
- **M02.L01** — ...
- **M02.L01** — Tokens-to-embeddings overview — A left-to-right diagram showing raw text being split into tokens, tokens mapped to integer IDs, IDs mapped to embedding vectors, and vectors passed into a language model  
  _Learner should notice:_ tokenization and embedding are separate stages and that token IDs are identifiers rather than semantic vectors
- **M02.L01** — Visible text versus token pieces — Show one sentence with colored token boundaries, including at least one full-word token, one split word such as apolog + izing, punctuation as its own token, and a special token  
  _Learner should notice:_ tokens can be words, subwords, punctuation, or control symbols
- **M02.L01** — Tokenizer input-output pipeline — A diagram showing prompt text → tokenizer → token IDs → generative model → old plus newly generated token IDs → tokenizer decode → readable text  
  _Learner should notice:_ the model communicates through numerical token IDs on both the input and output sides
- **M02.L01** — Word vs subword vs character vs byte tokenization — Use the same short input and show four parallel rows demonstrating how it would be segmented as whole words, subwords, individual characters, and bytes  
  _Learner should notice:_ compare sequence length, vocabulary flexibility, and the ability to handle unseen text
- **M02.L01** — Comparison of real tokenizer behavior — A compact comparison graphic using one mixed input with English capitalization, emoji/non-English text, code indentation, and numbers, showing that BERT-like, GPT-like, and code-focused tokenizers preserve and split information differently  
  _Learner should notice:_ tokenizer choices affect case, unknown symbols, whitespace, number segmentation, and sequence length
- **M02.L01** — Vocabulary embedding matrix — Show a tokenizer vocabulary column with token IDs pointing to rows in a matrix where each row contains a dense vector  
  _Learner should notice:_ every vocabulary token has a learned vector and that the token ID acts as the lookup key
- **M02.L01** — Static versus contextual token embedding — Show the word “bank” appearing in a financial sentence and a river sentence; start from the same token-level lookup concept and end with two different contextual vectors  
  _Learner should notice:_ the language model changes a token's representation according to surrounding context
- **M02.L01** — From token IDs to contextual embeddings — Show “Hello world” becoming [CLS], Hello, world, [SEP], then token IDs, then raw embedding vectors entering the language model, then four contextual output vectors of width 384  
  _Learner should notice:_ connect sequence length with token positions and understand what the [1, 4, 384] output shape represents
- **M02.L01** — Sentence-to-vector embedding — Show a complete sentence entering a text embedding model and emerging as one vector, followed by three example application branches: semantic search, categorization, and RAG retrieval  
  _Learner should notice:_ the difference between many per-token vectors and one vector representing a whole text
- **M02.L01** — Word2vec sliding window — Show a short sentence with one center word highlighted and two neighboring words on each side inside a sliding window; draw positive training pairs from the center to each neighbor  
  _Learner should notice:_ how ordinary running text is converted into many word-pair training examples
- **M02.L01** — Positive and negative word2vec pairs — Two groups of word pairs: genuine context neighbors labeled 1 and sampled unrelated pairs labeled 0, feeding a small neural network  
  _Learner should notice:_ embeddings improve because the model learns to separate observed contextual relationships from negative samples
- **M02.L01** — Playlist-to-song-embeddings recommender — Show playlists as sequences of song IDs feeding a Word2Vec-style model, producing one vector per song, followed by nearest-neighbor lookup that returns similar songs  
  _Learner should notice:_ the same algorithmic idea used for word context can model item similarity from playlist co-occurrence
- **M03.L01** — Autoregressive token generation loop — Show an initial prompt entering the model, one output token being selected, that token appended to the prompt, and the enlarged sequence entering the model again for the next step  
  _Learner should notice:_ generation is an iterative loop rather than one operation that writes the whole answer at once
- **M03.L01** — One Transformer forward pass — Show tokenizer → token embeddings → stacked Transformer decoder blocks → final hidden vectors → LM head → score for every vocabulary token  
  _Learner should notice:_ the Transformer does not directly output a word; the LM head converts a hidden representation into vocabulary-wide next-token scores
- **M03.L01** — LM head vocabulary scoring — Show one final hidden vector entering the LM head and expanding into a ranked list of candidate vocabulary tokens with scores, with “Paris” highlighted as the chosen candidate  
  _Learner should notice:_ the dimensional jump from one hidden vector to one score per vocabulary entry
- **M03.L01** — Parallel token processing streams — Show several input token embeddings entering parallel vertical streams through the same stack of Transformer blocks, with attention links connecting token positions  
  _Learner should notice:_ both parallel per-position processing and the cross-position interaction introduced by attention
- **M03.L01** — KV cache generation comparison — Side-by-side diagram of generation without cache repeatedly recalculating all previous token streams versus generation with cached keys/values where only the new token stream requires fresh computation  
  _Learner should notice:_ caching avoids duplicated attention work for previous positions
- **M03.L01** — Simplified Transformer block — Show input vectors entering self-attention, then a feedforward/MLP stage, then output vectors continuing to the next Transformer block  
  _Learner should notice:_ remember attention as contextual information mixing and the feedforward network as per-position transformation/processing
- **M03.L01** — Attention intuition with pronoun reference — Show “The dog chased the squirrel because it” with the current token “it” highlighted and attention links of different strengths to earlier words, especially dog and squirrel  
  _Learner should notice:_ attention lets the current representation incorporate information from relevant earlier positions
- **M03.L01** — Query-key-value projection — Show the same set of token input vectors branching through three learned projection matrices W_Q, W_K, and W_V to create query, key, and value representations  
  _Learner should notice:_ Q, K, and V are different learned views of the same underlying token representations
- **M03.L01** — Two-step attention calculation — First panel shows current query compared with keys to create relevance weights; second panel multiplies those weights by value vectors and sums them into one output vector  
  _Learner should notice:_ connect query/key interaction with scoring and values with information transfer
- **M03.L01** — Multi-head attention — Show one input sequence branching into several parallel attention heads, each with different attention patterns, then recombining into a single output  
  _Learner should notice:_ multi-head attention repeats the same core mechanism in parallel with different learned projections
- **M03.L01** — Full versus local attention — Show two triangular decoder-attention grids: one where each position can see all previous positions, and one where each position sees only a recent local window  
  _Learner should notice:_ the efficiency-versus-context tradeoff
- **M03.L01** — MHA vs MQA vs GQA — Three side-by-side diagrams showing multi-head attention with unique Q/K/V per head, multi-query attention with unique Q but one shared K/V set, and grouped-query attention with unique queries and several shared K/V groups  
  _Learner should notice:_ exactly what is being shared in each design
- **M03.L01** — Flash Attention memory intuition — Show a GPU diagram with slower/larger HBM and faster/smaller SRAM, comparing inefficient repeated data movement with a tiled/reuse-oriented attention computation  
  _Learner should notice:_ Flash Attention targets memory movement and execution efficiency rather than changing what attention conceptually means
- **M03.L01** — Original versus modern Transformer block — Side-by-side simplified diagrams showing the original attention + feedforward block with normalization/residual structure and a newer block with pre-normalization, RMSNorm-style labels, grouped-query attention, and modern feedforward activation  
  _Learner should notice:_ the skeleton remains recognizable while important implementation details evolve
- **M03.L01** — Sequence packing — Show several short documents packed into one fixed-length training context with boundaries between documents and little padding at the end  
  _Learner should notice:_ why packing improves space utilization and why position handling must respect document boundaries
- **M03.L01** — RoPE placement in attention — Show query and key projections followed by a rotary positional transformation before Q×K relevance scoring; values remain on the information-combination path  
  _Learner should notice:_ RoPE injects position into Q and K immediately before attention relevance scoring
- **M03.L01** — Complete next-token generation pipeline — A detailed left-to-right or top-to-bottom diagram showing text → tokenizer → IDs → embeddings → positional handling → repeated Transformer blocks containing attention and MLP → last hidden vector → LM head → vocabulary scores → decoding → selected token → append to context → repeat, with KV cache shown beside attention  
  _Learner should notice:_ be able to use this figure as the final mental model for the entire chapter
- **M04.L01** — Text classification overview — Show several example text inputs flowing into a language model/classifier and emerging as labels such as Positive, Negative, Billing Issue, and Shipping Issue  
  _Learner should notice:_ classification converts unstructured text into a small predefined set of labels
- **M04.L01** — Four classification routes — Four side-by-side pipelines showing task-specific model, frozen embeddings plus classifier, zero-shot label similarity, and generative prompting  
  _Learner should notice:_ the same classification goal can be solved with very different model architectures and training requirements
- **M04.L01** — Task-specific versus embedding classification — Show a pretrained task-specific encoder going directly from text to sentiment label beside a frozen embedding encoder producing a vector that then feeds logistic regression  
  _Learner should notice:_ the first model performs the task directly while the second separates feature extraction from classification
- **M04.L01** — Task-specific sentiment inference — Show a movie-review sentence flowing through tokenizer → pretrained sentiment encoder → negative/neutral/positive score outputs, with negative and positive mapped into the chapter's binary labels  
  _Learner should notice:_ the model has already learned the classification task and no new training is being performed here
- **M04.L01** — Binary confusion matrix — A 2×2 matrix labeled TN, FP, FN, TP using negative and positive movie reviews on the axes, with correct cells visually distinguished from error cells  
  _Learner should notice:_ be able to identify all four outcomes before learning precision and recall
- **M04.L01** — Precision vs recall intuition — Show a collection of actual positive items and predicted-positive items as overlapping sets, with TP in the overlap, FP in predicted-only, and FN in actual-only; annotate precision as purity of predictions and recall as coverage of true positives  
  _Learner should notice:_ the different questions precision and recall answer
- **M04.L01** — Frozen embeddings plus logistic regression — Show movie reviews entering a frozen embedding model, producing fixed-size vectors, then those vectors and labels feeding a small trainable logistic-regression classifier  
  _Learner should notice:_ only the small classifier is trained while the embedding model remains unchanged
- **M04.L01** — Zero-shot label embeddings — Show a review sentence and two label descriptions (“A negative review”, “A positive review”) each passing through the same embedding model into vectors  
  _Learner should notice:_ natural-language labels become comparable vectors without supervised fitting
- **M04.L01** — Cosine zero-shot classification — Show one document embedding as an arrow and two candidate-label vectors; one label vector has a smaller angle/higher similarity and is selected  
  _Learner should notice:_ classification is performed by semantic proximity rather than a separately trained classifier
- **M04.L01** — Generative classification versus task-specific classification — Show task-specific model: text → numeric class scores, beside generative model: instruction + text → generated class word  
  _Learner should notice:_ generative classification requires explicitly expressing the task in the prompt
- **M04.L01** — T5 text-to-text unification — Show several tasks such as sentiment classification, summarization, and question answering all converted into textual prompts entering the same encoder-decoder model and producing textual outputs  
  _Learner should notice:_ how text-to-text framing unifies tasks
- **M04.L01** — Closed-model evaluation caveats — Show an API-based classifier with three warning branches: usage cost, rate limits/retries, and unknown training-data overlap with benchmark datasets  
  _Learner should notice:_ model quality is only one part of production evaluation
- **M05.L01** — Supervised classification versus unsupervised clustering — Left side shows labeled documents being assigned to predefined categories; right side shows unlabeled documents automatically forming semantic groups  
  _Learner should notice:_ clustering discovers structure rather than learning predefined labels
- **M05.L01** — Cluster to topic — Show a cluster containing several semantically related documents, then extract representative keywords, then assign a human-readable topic concept  
  _Learner should notice:_ clustering groups documents while topic representation helps explain what each group is about
- **M05.L01** — Three-step clustering pipeline — Show documents → embedding model → high-dimensional vectors → UMAP dimensionality reduction → low-dimensional vectors → HDBSCAN → clusters/outliers  
  _Learner should notice:_ memorize the order and role of the three stages
- **M05.L01** — Document embedding space — Show several short document snippets becoming dense vectors and then points in a conceptual semantic space where similar topics lie near one another  
  _Learner should notice:_ clustering works on vectors, not raw strings
- **M05.L01** — High-dimensional to low-dimensional representation — Show a cloud of conceptual high-dimensional document vectors being compressed into a lower-dimensional space while trying to keep neighboring groups together  
  _Learner should notice:_ dimensionality reduction as structure-preserving compression rather than dropping random features
- **M05.L01** — Centroid clustering versus density clustering — Show k-means forcing all points into a fixed number of centroid-centered groups beside HDBSCAN discovering dense irregular groups and leaving isolated points as outliers  
  _Learner should notice:_ why density clustering is attractive when the number of clusters is unknown
- **M05.L01** — Cluster visualization with outliers — A 2D scatter plot concept showing several colored document clusters and gray outliers, with a warning callout that 2D positions are an approximation of the original high-dimensional embedding space  
  _Learner should notice:_ use plots for exploration, not as proof of semantic structure
- **M05.L01** — BERTopic two-stage pipeline — First stage shows embedding → UMAP → HDBSCAN clustering; second stage shows cluster documents combined and processed with c-TF-IDF to generate ranked topic keywords  
  _Learner should notice:_ remember semantic grouping and topic representation as related but separable stages
- **M05.L01** — Document TF to class-level TF — Show several documents inside one cluster being merged conceptually into one class-level text, then count words over the whole cluster  
  _Learner should notice:_ BERTopic represents topics at cluster level rather than treating each document independently
- **M05.L01** — c-TF-IDF intuition — Show two clusters with word-frequency bars: common stop words are frequent in both and receive low discriminative weight, while a topic-specific word such as “translation” is frequent in one cluster and receives high weight  
  _Learner should notice:_ why frequency alone is not enough
- **M05.L01** — BERTopic as Lego blocks — Show interchangeable blocks for embedding, reduction, clustering, and topic representation, with example alternatives underneath each block  
  _Learner should notice:_ components can be swapped independently
- **M05.L01** — Topic representation refinement — Show documents already clustered, c-TF-IDF producing candidate topic keywords, and an additional representation block reranking/refining those keywords without reclustering documents  
  _Learner should notice:_ why topic-level refinement can be much cheaper than document-level processing
- **M05.L01** — MMR keyword diversification — Show a redundant candidate list with several near-duplicate words being filtered into a smaller list containing relevant but more diverse concepts  
  _Learner should notice:_ MMR trades some redundancy for broader topic coverage
- **M05.L01** — Generative topic labeling — Show one topic cluster producing a small set of representative documents plus top keywords, these entering a generative model once, and a concise human-readable topic label emerging  
  _Learner should notice:_ why generative labeling is applied per topic instead of per document
- **M05.L01** — Complete text clustering and topic modeling pipeline — Show unlabeled documents → embedding model → UMAP → HDBSCAN → clusters/outliers → c-TF-IDF → topic keywords → optional KeyBERT/MMR/generative representation blocks → human-readable topics and visualizations  
  _Learner should notice:_ be able to use this figure as the final mental model for the chapter
- **M06.L01** — Prompt engineering feedback loop — Show task requirements → draft prompt → LLM output → evaluate output → revise prompt → repeat  
  _Learner should notice:_ prompt engineering is an optimization loop rather than a one-time wording exercise
- **M06.L01** — Chat template transformation — Show a Python messages list with user/assistant roles on the left and the model-specific serialized prompt with special role and end tokens on the right  
  _Learner should notice:_ the chat API/pipeline transforms conversational messages into a model-specific token sequence
- **M06.L01** — Deterministic versus sampled next-token selection — Show one probability distribution over candidate next tokens; left path always selects the highest candidate, right path samples among candidates according to adjusted probabilities  
  _Learner should notice:_ distinguish model probabilities from the decoding policy that chooses the actual output token
- **M06.L01** — Temperature comparison — Show the same candidate-token distribution at low and high temperature, with low temperature sharply concentrated on top choices and high temperature flatter across more alternatives  
  _Learner should notice:_ temperature as reshaping the distribution rather than directly adding random words
- **M06.L01** — top-p versus top-k — Show one ranked token probability list; highlight a cumulative-probability nucleus for top-p and exactly the top K entries for top-k  
  _Learner should notice:_ top-p uses probability mass while top-k uses a fixed candidate count
- **M06.L01** — Prompt anatomy basics — Show a prompt divided into three labeled blocks—Instruction, Data, and Output Indicator—with arrows showing how each constrains the model response  
  _Learner should notice:_ a prompt can be designed from modular components
- **M06.L01** — Modular prompt components — Show a prompt assembled from separate labeled blocks: Persona, Instruction, Context, Format, Audience, Tone, and Data  
  _Learner should notice:_ prompt design as composable rather than as one unstructured paragraph
- **M06.L01** — Zero-shot one-shot few-shot — Three prompt diagrams: instruction only, instruction plus one demonstration, and instruction plus several demonstrations  
  _Learner should notice:_ the difference is the number of examples supplied in the current context
- **M06.L01** — Prompt chaining pipeline — Show product features entering Prompt 1 to generate name/slogan, then those outputs plus original features entering Prompt 2 to generate a sales pitch  
  _Learner should notice:_ how intermediate outputs become inputs to later stages
- **M06.L01** — Reasoning-oriented prompt structure — Show problem → intermediate substeps/calculations → final answer, with a note that the visible explanation is generated output rather than a guaranteed view of hidden internal computation  
  _Learner should notice:_ the purpose of structured intermediate reasoning without confusing it with model internals
- **M06.L01** — Self-consistency voting — Show one prompt branching into several independently sampled reasoning/output paths and then a majority-vote or aggregation node  
  _Learner should notice:_ how repeated sampling trades additional compute for robustness
- **M06.L01** — Tree-style solution exploration — Show one problem branching into several candidate intermediate ideas, each evaluated, weak branches pruned, and promising branches expanded toward a final answer  
  _Learner should notice:_ the contrast between one linear solution path and deliberate branch exploration
- **M06.L01** — Generation plus validation architecture — Show LLM generation flowing through separate checks for schema, allowed values, safety/policy, and factual/task validation before output is accepted  
  _Learner should notice:_ production reliability requires layers beyond prompting
- **M06.L01** — Normal sampling versus constrained sampling — Left side shows a wide set of possible next tokens including invalid outputs; right side shows a grammar filter removing illegal candidates so only schema-valid tokens can be selected  
  _Learner should notice:_ constraints act during decoding rather than merely asking the model politely
- **M07.L01** — LLM system building blocks — Show an LLM in the center connected to model I/O, prompt templates/chains, memory, tools, and agent logic  
  _Learner should notice:_ the language model is one component inside a larger application architecture
- **M07.L01** — Modular LLM framework — Show independent blocks labeled Model, Prompt, Memory, Tool, Chain, Agent connected through arrows, with a note that frameworks orchestrate these components  
  _Learner should notice:_ the framework as glue/orchestration rather than the intelligence itself
- **M07.L01** — Quantization intuition — Show the same numerical value represented with high precision and reduced precision, followed by a large model shrinking in memory footprint  
  _Learner should notice:_ quantization as reduced parameter precision rather than deleting entire model layers
- **M07.L01** — Basic chain — Show user variable → prompt template → formatted model prompt → LLM → response  
  _Learner should notice:_ a chain turns repeated formatting logic into a reusable workflow
- **M07.L01** — Sequential story chain — Show input summary flowing into title generation, then summary + title into character generation, then all previous outputs into story generation  
  _Learner should notice:_ intermediate outputs become named inputs to later stages
- **M07.L01** — Stateless calls versus memory-backed conversation — Left side shows two independent calls where the second cannot see the first; right side shows conversation history appended to the second call so the model can use earlier information  
  _Learner should notice:_ application memory works by re-supplying relevant prior information
- **M07.L01** — Full conversation buffer — Show an expanding chat history block copied into every new prompt before the latest user message  
  _Learner should notice:_ memory is achieved by repeatedly sending old text back to the model
- **M07.L01** — Windowed conversation memory — Show a long conversation timeline where only the latest two interaction blocks are highlighted and inserted into the next prompt while older blocks are discarded  
  _Learner should notice:_ how a fixed memory window trades history coverage for bounded prompt size
- **M07.L01** — Conversation summary memory — Show raw chat turns going into a summarizer LLM, producing a compact running summary that is inserted into the main assistant prompt  
  _Learner should notice:_ summary memory as compression rather than simple deletion
- **M07.L01** — Chain versus agent — Left side shows a fixed predefined chain of steps; right side shows an agent choosing among several tools/actions based on the current task  
  _Learner should notice:_ fixed orchestration versus dynamic action selection
- **M07.L01** — LLM tool use — Show an agent receiving a user question and selecting among a web search tool, calculator, and direct answer path, then receiving tool results back  
  _Learner should notice:_ tools as external capabilities selected by orchestration logic
- **M07.L01** — ReAct-style loop — Show Question → Plan/Thought → Action → Tool → Observation → back to Plan/Thought, eventually ending in Final Answer  
  _Learner should notice:_ how tool results become new context for subsequent decisions
- **M07.L01** — Agent reliability controls — Show an agent/tool loop surrounded by controls for tool permissions, source capture, validation, logging, human review, and error handling  
  _Learner should notice:_ autonomy must be paired with guardrails and observability
- **M07.L01** — Complete memory-agent-tool system — Show user request entering an agent with access to memory, search, calculator, and validation; observations flow back to the agent before a final response  
  _Learner should notice:_ how the chapter’s separate components combine into one application
- **M08.L01** — Keyword search versus semantic search — Show the same query entering two pipelines: keyword search matching shared words and semantic search matching a differently worded but meaning-equivalent passage  
  _Learner should notice:_ semantic relevance does not require exact query terms
- **M08.L01** — Basic RAG motivation — Show a question going first to search, retrieved evidence entering the LLM together with the question, and the LLM producing an answer with source references  
  _Learner should notice:_ retrieval supplies evidence before generation
- **M08.L01** — Retrieval reranking RAG stack — Show a three-stage pipeline with dense/lexical retrieval producing candidates, reranker reordering them, and a generative model answering from the top evidence  
  _Learner should notice:_ retrieval, reranking, and generation as distinct jobs
- **M08.L01** — Dense retrieval embedding space — Show query and several document points in a vector space, with the nearest two documents highlighted as retrieved results  
  _Learner should notice:_ connect semantic similarity with nearest-neighbor retrieval
- **M08.L01** — Vector indexing and retrieval — Two phases: indexing phase with documents → chunks → embeddings → vector index, and query phase with query → embedding → nearest-neighbor lookup → retrieved chunks  
  _Learner should notice:_ distinguish offline indexing from online query retrieval
- **M08.L01** — BM25 versus dense retrieval example — Show the same query with BM25 selecting a passage that shares the word “science,” while dense retrieval selects a passage about “scientific accuracy”  
  _Learner should notice:_ lexical overlap versus semantic relevance
- **M08.L01** — Hybrid search architecture — Show one query branching to BM25 and dense retrieval, candidate lists being merged, then sent to reranking  
  _Learner should notice:_ hybrid search as combining complementary retrieval signals
- **M08.L01** — Whole document vector versus chunk vectors — Show one long document mapped to a single compressed vector on the left, and the same document split into multiple topic-specific chunks with separate vectors on the right  
  _Learner should notice:_ why multiple chunk vectors preserve more retrievable detail
- **M08.L01** — Chunking strategies — Show one document split four ways: sentence chunks, paragraph chunks, fixed multi-sentence chunks, and overlapping chunks with shared boundary text  
  _Learner should notice:_ chunk size and overlap change retrieval behavior
- **M08.L01** — Retrieval fine-tuning positive and negative pairs — Show one relevant document with two positive query arrows being pulled closer and one irrelevant query arrow being pushed farther away after training  
  _Learner should notice:_ retrieval fine-tuning as shaping the geometry around task-specific relevance
- **M08.L01** — Two-stage retrieval and reranking — Show a huge corpus narrowed by a fast first-stage retriever to a small candidate set, followed by a slower relevance reranker producing the final ordered results  
  _Learner should notice:_ why reranking is normally applied to a shortlist rather than the whole corpus
- **M08.L01** — Bi-encoder versus cross-encoder — Left side shows query and document encoded independently then compared; right side shows query and document entering the same model together to produce one relevance score  
  _Learner should notice:_ why cross-encoders can judge relevance more deeply but are more expensive
- **M08.L01** — Retrieval evaluation test set — Show a query linked to a corpus with certain documents marked relevant, then a search system returning a ranked list that can be scored against those relevance judgments  
  _Learner should notice:_ search evaluation requires labeled relevance data
- **M08.L01** — Average Precision calculation — Show a ranked list with relevant items highlighted at positions 1 and 3, annotate precision@1 and precision@3, then average them  
  _Learner should notice:_ AP rewards earlier relevant documents
- **M08.L01** — Basic RAG pipeline — Show question → retriever → top evidence chunks → prompt containing question + context → LLM → grounded answer with citations  
  _Learner should notice:_ memorize retrieval first, generation second
- **M08.L01** — Local RAG components — Show documents indexed by an embedding model into a local FAISS vector store, with question → retriever → context → prompt → local LLM → answer  
  _Learner should notice:_ RAG can be implemented entirely from modular local components
- **M08.L01** — Query rewriting — Show a long conversational user message being condensed by an LLM into a short search-optimized query before retrieval  
  _Learner should notice:_ user language and retrieval language can differ
- **M08.L01** — Multi-hop RAG — Show first retrieval producing entities, then each entity generating follow-up queries whose evidence is combined into a final answer  
  _Learner should notice:_ later retrieval depends on earlier retrieval results
- **M08.L01** — Agentic RAG architecture — Show an LLM/controller choosing among several retrieval tools/data sources, inspecting observations, issuing follow-up queries, then generating a final grounded answer  
  _Learner should notice:_ connect advanced RAG with the agent/tool ideas from Chapter 7
- **M08.L01** — RAG evaluation dimensions — Show a RAG answer surrounded by evaluation checks for retrieval quality, faithfulness, answer relevance, citation precision/recall, fluency, and utility  
  _Learner should notice:_ RAG quality is multidimensional
- **M08.L01** — Complete semantic search and RAG architecture — Show offline indexing with chunking/embeddings/vector database and online flow with query rewrite → hybrid retrieval → reranker → context assembly → generator → cited answer, with evaluation attached to both retrieval and generation  
  _Learner should notice:_ use this as the final architecture map for the chapter
- **M09.L01** — Multimodal model overview — Show several modalities—text, image, audio, video, sensors—feeding a multimodal model, with text as one possible output  
  _Learner should notice:_ input modality support and output modality support are separate capabilities
- **M09.L01** — Text Transformer versus Vision Transformer — Left side shows text → tokens → embeddings → Transformer encoder; right side shows image → patches → patch embeddings → Transformer encoder  
  _Learner should notice:_ tokenization and patching play analogous preprocessing roles
- **M09.L01** — Image patching — Show a single image divided into a regular grid of patches, then the patches flattened into a sequence P1, P2, P3, ...  
  _Learner should notice:_ image patching as the visual analogue of converting a sentence into a token sequence
- **M09.L01** — Patch embedding pipeline — Show image patch → flattened pixel vector → linear projection → dense patch embedding, repeated for several patches before entering a Transformer encoder  
  _Learner should notice:_ how raw visual data is turned into Transformer-compatible numerical representations
- **M09.L01** — Shared image-text embedding space — Show image embeddings and text embeddings as points in the same vector space, with matching image-caption pairs close together and unrelated pairs farther apart  
  _Learner should notice:_ why shared embedding geometry enables cross-modal comparison
- **M09.L01** — CLIP dual encoder — Show a text encoder and an image encoder processing a caption and its matching image separately, producing two embeddings in the same vector space  
  _Learner should notice:_ CLIP as a dual-encoder alignment model
- **M09.L01** — CLIP contrastive training matrix — Show a batch of images on one axis and captions on the other, forming a similarity matrix where diagonal matching pairs are highlighted as positives and off-diagonal pairs are negatives  
  _Learner should notice:_ why batch-wise contrastive learning provides both positive and negative examples
- **M09.L01** — CLIP applications — Show a shared embedding space branching into zero-shot classification, image search from text, text search from image, clustering, and generation conditioning  
  _Learner should notice:_ one aligned representation space enables many applications
- **M09.L01** — Image preprocessing tensor shape — Show a normal RGB image being resized/normalized into a tensor labeled [batch=1, channels=3, height=224, width=224]  
  _Learner should notice:_ be able to interpret the four tensor dimensions
- **M09.L01** — BLIP-2 high-level architecture — Show frozen Vision Transformer → trainable Q-Former → projection → frozen LLM, clearly marking which components are frozen and which bridge is trainable  
  _Learner should notice:_ BLIP-2 as connecting pretrained models instead of retraining everything
- **M09.L01** — BLIP-2 stage 1 objectives — Show image and caption inputs entering Q-Former training with three output branches labeled contrastive alignment, image-text matching, and image-grounded text generation  
  _Learner should notice:_ remember the three complementary objectives
- **M09.L01** — Soft visual prompt bridge — Show Q-Former visual outputs passing through a linear projection into a sequence of LLM-compatible embedding vectors inserted before textual prompt embeddings  
  _Learner should notice:_ how image information becomes conditioning context for the LLM
- **M09.L01** — Aspect-ratio preprocessing caution — Show a wide original image being transformed into a square 224×224 model input, with visual distortion highlighted  
  _Learner should notice:_ recognize that preprocessing itself can alter visual information
- **M09.L01** — Image captioning pipeline — Show an image entering processor → vision encoder/Q-Former → LLM → generated caption  
  _Learner should notice:_ captioning as visual input conditioned text generation
- **M09.L01** — Visual question answering — Show an image and textual question entering the multimodal model together, producing a text answer tied to visual evidence  
  _Learner should notice:_ distinguish VQA from unconditional image captioning
- **M09.L01** — Multimodal chat memory — Show one persistent image plus conversation history—Q1/A1, Q2/A2—being assembled into the next multimodal prompt  
  _Learner should notice:_ connect multimodal chat with application-managed conversation memory
- **M09.L01** — CLIP versus BLIP-2 — Side-by-side diagram: CLIP maps image/text to shared embeddings for similarity, while BLIP-2 maps image features through Q-Former/projection into an LLM for text generation  
  _Learner should notice:_ clearly distinguish multimodal retrieval embeddings from multimodal generation
- **M09.L01** — Complete multimodal architecture map — Show three stacked stages: ViT patch representation, CLIP shared image-text embedding alignment, and BLIP-2 visual-to-language generation bridge  
  _Learner should notice:_ use this figure as the chapter’s final mental map
- **M10.L01** — Text to embedding — Show a document, sentence, and phrase entering an embedding model and each becoming a dense numerical vector  
  _Learner should notice:_ embeddings as learned numerical representations rather than arbitrary encodings
- **M10.L01** — Semantic space versus sentiment space — Show the same documents organized in two embedding spaces: one grouping by semantic topic and another grouping by positive/negative sentiment  
  _Learner should notice:_ fine-tuning changes what “similarity” means
- **M10.L01** — Contrastive learning geometry — Show an anchor sentence, a positive sentence being pulled closer in vector space, and a negative sentence being pushed farther away  
  _Learner should notice:_ contrastive learning as reshaping embedding geometry through comparisons
- **M10.L01** — Cross-encoder architecture — Show sentence A and sentence B concatenated with a separator and passed through one Transformer that produces a similarity score  
  _Learner should notice:_ the pair must be processed together for every comparison
- **M10.L01** — Bi-encoder versus cross-encoder — Left side shows cross-encoder processing a pair together for one score; right side shows the same shared encoder independently generating reusable embeddings that can later be compared  
  _Learner should notice:_ why bi-encoders scale better for retrieval
- **M10.L01** — NLI as contrastive data — Show one premise with an entailment hypothesis, neutral hypothesis, and contradiction hypothesis branching from it  
  _Learner should notice:_ how NLI labels naturally create different similarity relationships
- **M10.L01** — STSB evaluation — Show human-labeled sentence similarity scores compared with cosine similarity produced from model embeddings, then compute a correlation metric  
  _Learner should notice:_ evaluation checks whether embedding geometry agrees with human similarity judgments
- **M10.L01** — Multi-task embedding evaluation — Show one embedding model evaluated across several task families such as similarity, classification, clustering, and retrieval  
  _Learner should notice:_ why broad evaluation is more informative than one benchmark score
- **M10.L01** — Cosine similarity loss — Show two sentence embeddings with a target similarity score; training adjusts their angle so predicted cosine similarity approaches the labeled value  
  _Learner should notice:_ cosine loss as matching vector similarity to human/data-provided similarity
- **M10.L01** — Multiple Negatives Ranking loss — Show one anchor compared against one positive and several in-batch negative candidates, with the positive required to receive the highest similarity  
  _Learner should notice:_ MNR as a ranking problem within a batch
- **M10.L01** — Easy versus semi-hard versus hard negatives — Show an anchor query with three negative answers: unrelated, topically related, and highly similar but incorrect  
  _Learner should notice:_ difficult negatives force the model to learn finer semantic distinctions
- **M10.L01** — Augmented SBERT overview — Show small gold dataset → train cross-encoder teacher → label many unlabeled sentence pairs → silver dataset → combine gold + silver → train bi-encoder/SBERT  
  _Learner should notice:_ memorize the teacher-labeler-student workflow
- **M10.L01** — TSDAE denoising autoencoder — Show original sentence → word deletion/noise → damaged sentence → encoder → single sentence embedding → decoder → reconstructed original sentence  
  _Learner should notice:_ reconstruction pressure teaches the embedding to preserve sentence information
- **M10.L01** — Domain adaptation — Show a generic source-domain embedding model being adapted using unlabeled target-domain documents, producing a new model whose representation space better reflects target terminology and concepts  
  _Learner should notice:_ domain adaptation as specialization rather than training from nothing
- **M10.L01** — Embedding model development lifecycle — Show objective definition → data pairs/negatives → model/loss → training → evaluation → error analysis → better data/domain adaptation → retraining  
  _Learner should notice:_ embedding development as an iterative data-and-objective loop
- **M11.L01** — Frozen versus fine-tuned classifier — Left side shows frozen BERT feeding a trainable classifier; right side shows both BERT and classification head trainable with backward arrows through the whole network  
  _Learner should notice:_ the difference between fixed feature extraction and end-to-end task adaptation
- **M11.L01** — Task-specific BERT classifier — Show tokenized text entering pretrained BERT, pooled representation entering a small feedforward classification head, and gradients flowing backward through both components  
  _Learner should notice:_ joint optimization
- **M11.L01** — Dynamic batch padding — Show three token sequences of different lengths being padded to the length of the longest sequence in that batch  
  _Learner should notice:_ why padding is required for tensor batches without padding every sample to a global maximum
- **M11.L01** — Layer-freezing spectrum — Show BERT embeddings + 12 encoder blocks + classifier, with three configurations: all trainable, only classifier trainable, and only later encoder blocks plus classifier trainable  
  _Learner should notice:_ freezing as a continuum rather than an all-or-nothing choice
- **M11.L01** — Partial BERT freezing — Show early encoder blocks locked and later encoder blocks plus classifier unlocked, with gradient flow only through the trainable tail  
  _Learner should notice:_ why partial fine-tuning can preserve adaptability while reducing compute
- **M11.L01** — Few-shot classification — Show two classes with only a small handful of labeled examples feeding a model that must classify unseen text  
  _Learner should notice:_ the low-label-data setting
- **M11.L01** — Three-stage SetFit pipeline — Show class-labeled examples → positive/negative pair generation → contrastive SentenceTransformer fine-tuning → embeddings → classifier  
  _Learner should notice:_ memorize the three SetFit stages
- **M11.L01** — Two-stage versus three-stage adaptation — Show standard pretrained model → task fine-tuning beside pretrained model → continued domain MLM → task fine-tuning  
  _Learner should notice:_ where domain adaptation fits
- **M11.L01** — Token masking versus whole-word masking — Show one tokenized sentence where a single subword is masked versus another where all subwords belonging to one word are masked  
  _Learner should notice:_ why whole-word masking is a harder prediction task
- **M11.L01** — MLM before versus after domain adaptation — Show the same masked sentence with general BERT predicting generic nouns and movie-domain-adapted BERT predicting film-related nouns  
  _Learner should notice:_ evidence that continued pretraining shifts the model toward domain language
- **M11.L01** — Document classification versus NER — Left side shows one review receiving one sentiment label; right side shows one sentence with entity labels attached to individual token spans  
  _Learner should notice:_ the shift from sequence-level to token-level prediction
- **M11.L01** — BIO entity span — Show “Dean Palmer” with Dean labeled B-PER and Palmer labeled I-PER, plus “Rangers” labeled B-ORG and non-entities labeled O  
  _Learner should notice:_ how BIO tags preserve phrase boundaries
- **M11.L01** — Word-to-subword label mismatch — Show one labeled word such as “Maarten/B-PER” split into Ma, ##arte, ##n, creating multiple token positions that need aligned labels  
  _Learner should notice:_ why token classification requires special preprocessing
- **M11.L01** — NER subtoken inference — Show “Maarten” tokenized into Ma / ##arte / ##n with B-PER / I-PER / I-PER, then reconstructed visually as one person entity span  
  _Learner should notice:_ connect subtoken predictions back to a human-readable entity
- **M11.L01** — Chapter 11 adaptation map — Show five branches from a pretrained representation model: full sequence fine-tuning, partial freezing, SetFit, continued MLM then classification, and token-level NER  
  _Learner should notice:_ use this as the final decision map for the chapter
- **M12.L01** — Three-stage LLM training pipeline — Show an untrained Transformer progressing through pretraining → base model, supervised fine-tuning → instruction/chat model, and preference tuning → aligned model  
  _Learner should notice:_ memorize the different purpose of each stage
- **M12.L01** — Base model continuation versus instruction model — Show the same user question sent to a base model that continues with more questions and an instruction-tuned model that answers directly  
  _Learner should notice:_ why instruction following is a separate learned behavior
- **M12.L01** — SFT training example — Show user instruction + desired assistant response converted into a training sequence where the model learns to predict the response tokens conditioned on the user message  
  _Learner should notice:_ SFT still uses token prediction but on curated instruction data
- **M12.L01** — Full fine-tuning versus PEFT — Show a full model with every block highlighted as trainable beside a mostly frozen model with only small adapter/LoRA components highlighted  
  _Learner should notice:_ PEFT as reducing the trainable parameter set
- **M12.L01** — Swappable adapters — Show one shared frozen Transformer backbone with several small adapter sets that can be swapped for medical, NER, and legal tasks  
  _Learner should notice:_ the storage and modularity benefit
- **M12.L01** — LoRA matrix update — Show large frozen matrix W plus a low-rank update ΔW formed by multiplying two narrow matrices A and B, producing effective weight W + ΔW  
  _Learner should notice:_ LoRA learns a compact weight change rather than replacing the full matrix
- **M12.L01** — Numerical precision and memory — Show one weight represented in 32-bit, 16-bit, 8-bit, and 4-bit forms with decreasing memory use and increasing approximation  
  _Learner should notice:_ the core quantization tradeoff
- **M12.L01** — QLoRA architecture — Show frozen 4-bit base model weights with small trainable LoRA matrices attached to selected projection layers  
  _Learner should notice:_ why QLoRA can fine-tune models that would otherwise exceed available VRAM
- **M12.L01** — Instruction-tuning chat template — Show raw conversation messages being serialized into model-specific user/assistant tokens and end-of-message markers  
  _Learner should notice:_ connect chat templates from Chapter 6 with SFT training data
- **M12.L01** — Gradient accumulation — Show four small mini-batches processed sequentially, gradients accumulated, then one optimizer update  
  _Learner should notice:_ how small-memory training can emulate a larger batch size
- **M12.L01** — LoRA adapter merge — Show frozen base model and separate LoRA adapter being combined into one merged model for inference  
  _Learner should notice:_ adapter-only storage versus merged deployment
- **M12.L01** — Perplexity intuition — Show a phrase ending before the next token, with one model assigning high probability to the correct continuation and another distributing probability poorly  
  _Learner should notice:_ perplexity as next-token predictive confidence
- **M12.L01** — LLM-as-a-judge pairwise evaluation — Show two candidate model responses to one prompt being compared by a separate judge model that returns a preference  
  _Learner should notice:_ automated qualitative comparison
- **M12.L01** — Goodhart's Law in LLM evaluation — Show a model optimizing one metric upward while broader usefulness drops, illustrating benchmark gaming/over-optimization  
  _Learner should notice:_ why evaluation needs multiple independent perspectives
- **M12.L01** — Reward model — Show prompt + generated response entering a reward model derived from an instruction-tuned model, with the language-modeling head replaced by a scalar scoring head  
  _Learner should notice:_ how generative output can be converted into a trainable preference score
- **M12.L01** — Preference data collection — Show one prompt sent to the same model twice to create response A and B, then a human chooses one as preferred  
  _Learner should notice:_ how pairwise feedback becomes training data
- **M12.L01** — Reward-model-based RLHF pipeline — Show preference collection → reward model training → policy/LLM optimization with reward feedback  
  _Learner should notice:_ the full alignment loop
- **M12.L01** — DPO versus reward-model RLHF — Left side shows preference data → reward model → PPO → LLM; right side shows preference data directly comparing frozen reference and trainable model probabilities  
  _Learner should notice:_ why DPO removes the explicit reward-model training stage
- **M12.L01** — SFT then DPO — Show a base model first receiving instruction tuning and then preference tuning, with each stage labeled by the type of data it uses  
  _Learner should notice:_ why instruction following and preference alignment are separate capabilities
- **M12.L01** — Complete generative fine-tuning lifecycle — Show pretraining → base LLM → SFT with LoRA/QLoRA option → instruction model → evaluation → reward-model/PPO or DPO preference tuning → aligned model → deployment evaluation  
  _Learner should notice:_ use this as the final mental map for Chapter 12

## COURSE-006_Production_AI_Engineering — 96 images

- **M01.L01** — From traditional ML to AI engineering — A two-lane diagram comparing the traditional workflow of collecting data and training a task-specific model with the foundation-model workflow of selecting an existing model, adapting it, evaluating it, and integrating it into an application  
  _Learner should notice:_ AI engineering shifts much of the effort from model creation toward model adaptation and product development
- **M01.L01** — Tokenization example — A short English sentence visually split into several word and subword tokens, including at least one word divided into two tokens  
  _Learner should notice:_ tokens are not always identical to words and that tokenization controls the units the model processes
- **M01.L01** — Masked versus autoregressive language models — A side-by-side diagram where the masked model fills a blank using context on both sides and the autoregressive model predicts the next token using only preceding tokens  
  _Learner should notice:_ the different information available to each model during prediction
- **M01.L01** — Multimodal foundation model — A diagram with text tokens and image tokens entering the same model and a generated output token leaving it  
  _Learner should notice:_ the model can condition its output on multiple modalities rather than text alone
- **M01.L01** — Foundation-model use-case map — A compact map or wheel showing coding, visual generation, writing, education, conversational bots, information aggregation, data organization, and workflow automation around a central foundation model  
  _Learner should notice:_ one general-purpose model can support many application categories
- **M01.L01** — Crawl-Walk-Run automation maturity — A three-stage diagram showing mandatory human review, internal direct AI use, and higher automation with possible external-user interaction  
  _Learner should notice:_ automation can increase gradually as confidence and evidence improve
- **M01.L01** — Three-layer AI engineering stack — A vertical stack with Application Development on top, Model Development in the middle, and Infrastructure at the bottom, with two or three example responsibilities inside each layer  
  _Learner should notice:_ most application builders can begin at the top and move down only when more control is necessary
- **M01.L01** — Product-first AI engineering workflow — A simple loop showing idea -> existing foundation model -> product prototype -> user feedback -> evaluation -> better data/model adaptation -> improved product  
  _Learner should notice:_ modern AI teams can validate the product earlier instead of waiting for a custom model to be trained first
- **M02.L01** — Foundation-model design map — A four-part diagram showing training data, architecture/scale, post-training, and sampling all feeding into downstream model behavior  
  _Learner should notice:_ application behavior is influenced by choices made both during training and during inference
- **M02.L01** — Uneven multilingual representation — A simple bar chart contrasting one highly represented language with several low-resource languages in a web-scale dataset  
  _Learner should notice:_ model exposure to languages can differ dramatically and that this can influence downstream performance
- **M02.L01** — Seq2seq versus transformer — A side-by-side diagram showing an RNN encoder-decoder compressing input into a sequential representation versus a transformer where output generation can attend directly to relevant previous tokens  
  _Learner should notice:_ attention gives the model richer access to earlier information and that transformer input processing is more parallelizable
- **M02.L01** — Query-Key-Value attention — A simplified attention diagram with one query comparing against several keys, producing attention weights that determine how strongly the corresponding values contribute to the result  
  _Learner should notice:_ the difference between deciding relevance with Q/K and retrieving information through V
- **M02.L01** — Simplified transformer architecture — A vertical diagram showing token/position embeddings, repeated transformer blocks containing attention and MLP modules, then an output layer producing token scores  
  _Learner should notice:_ a transformer is a stack of repeated blocks rather than a single attention operation
- **M02.L01** — Dense model versus mixture of experts — A simple diagram where every block is active in a dense model, while a router sends each token to only a small subset of expert blocks in an MoE model  
  _Learner should notice:_ the difference between total and active parameters
- **M02.L01** — Pre-training to post-training pipeline — A three-stage diagram showing self-supervised pre-training, supervised finetuning, and preference finetuning  
  _Learner should notice:_ conversational behavior is shaped after the base model has already learned broad capabilities
- **M02.L01** — Logits to sampled token — A pipeline showing a vector of raw logits, softmax converting them to probabilities, and one token being selected according to a sampling strategy  
  _Learner should notice:_ the model first scores all candidate tokens and sampling happens only after those scores are produced
- **M02.L01** — Top-k versus top-p — A token-probability bar chart showing top-k selecting a fixed number of highest tokens while top-p selects however many tokens are needed to reach a cumulative probability threshold  
  _Learner should notice:_ top-k fixes the count while top-p adapts the count to the distribution
- **M02.L01** — Constrained sampling for structured output — A diagram showing raw logits over many tokens being filtered by a grammar so that only tokens valid for the target structure remain before sampling  
  _Learner should notice:_ invalid tokens can be prevented during generation instead of repaired afterward
- **M02.L01** — Snowballing hallucination — A causal chain showing an initial incorrect generated assumption followed by several later tokens/statements that become increasingly wrong because they are conditioned on the first mistake  
  _Learner should notice:_ how an early error can compound during autoregressive generation
- **M03.L01** — Evaluation around failure modes — A diagram showing an AI application in the center, surrounded by possible failure areas such as factual errors, unsafe outputs, poor retrieval, tool failure, latency, and user dissatisfaction, with evaluation methods mapped to those risks  
  _Learner should notice:_ evaluation should be designed from concrete failure modes rather than generic scores
- **M03.L01** — Entropy and cross entropy intuition — A visual with two probability distributions: a predictable two-choice distribution and a less predictable multi-choice distribution, plus a second panel showing a model distribution approximating a true data distribution  
  _Learner should notice:_ entropy belongs to the data distribution while cross entropy also reflects model mismatch
- **M03.L01** — Functional correctness evaluation — A flow diagram showing an AI-generated solution being executed or applied to several test cases, producing pass/fail results  
  _Learner should notice:_ the system is judged by behavior rather than textual resemblance
- **M03.L01** — Semantic embedding space — A 2D conceptual embedding plot where semantically related sentences cluster together even when their wording differs, while unrelated sentences appear far apart  
  _Learner should notice:_ semantic similarity operates on meaning rather than word overlap
- **M03.L01** — AI judge system — A diagram showing generated answer plus evaluation prompt entering a judge model, which returns a score and explanation, with model version, prompt version, and sampling settings labeled as parts of the judge  
  _Learner should notice:_ the judge is more than the underlying model name
- **M03.L01** — Pairwise comparison graph — Several model nodes connected by pairwise matches with win rates, followed by a rating algorithm producing a ranked list  
  _Learner should notice:_ ranking is inferred from a network of comparisons rather than one absolute score per model
- **M04.L01** — Evaluation-driven development loop — A loop showing define criteria -> build prototype -> evaluate -> improve -> deploy -> collect production evidence -> refine criteria  
  _Learner should notice:_ evaluation starts before implementation and continues throughout the application's lifecycle
- **M04.L01** — Local versus global factual consistency — A split diagram where local factuality compares an answer directly against provided context, while global factuality first retrieves trusted external evidence and then verifies the answer  
  _Learner should notice:_ global verification adds an evidence-discovery problem
- **M04.L01** — Search-augmented factuality evaluator — A four-stage pipeline showing response decomposition, self-contained claims, web or knowledge search, and claim verification  
  _Learner should notice:_ long-form factuality can be reduced to verifying smaller atomic claims
- **M04.L01** — Quality-cost-latency tradeoff — A three-axis conceptual diagram or Pareto frontier where some models are higher quality but slower/more expensive and others are cheaper/faster with lower quality  
  _Learner should notice:_ model selection is a multi-objective problem
- **M04.L01** — Model-selection funnel — A four-stage funnel from all models -> hard-attribute filtering -> public benchmark shortlist -> private evaluation -> production monitoring  
  _Learner should notice:_ public benchmarks narrow candidates but do not make the final choice
- **M04.L01** — API versus self-hosted decision matrix — A two-column matrix comparing external APIs and self-hosted models across privacy, performance, functionality, cost, control, finetuning, and on-device deployment  
  _Learner should notice:_ neither option is universally better; the right choice depends on application constraints
- **M04.L01** — Public versus private leaderboard — A diagram showing public benchmarks feeding a coarse shortlist, then application-specific benchmarks, weights, cost, and latency producing a private model ranking  
  _Learner should notice:_ public rankings are only an early filter
- **M04.L01** — Component, turn, and task evaluation — A layered diagram showing intermediate component metrics at the bottom, turn-level quality in the middle, and end-to-end task success at the top  
  _Learner should notice:_ a reliable pipeline measures both local failures and the final user outcome
- **M04.L01** — Simpson's paradox in model evaluation — A two-group table where Model A performs better than Model B inside each subgroup but Model B has a higher aggregated score due to different group sizes  
  _Learner should notice:_ why aggregate metrics must be inspected alongside slice-level results
- **M06.L01** — Instructions versus query-specific context — A diagram showing a shared system instruction combined with query-specific retrieved/tool-generated context before entering the model  
  _Learner should notice:_ instructions stay relatively stable while context changes for each query
- **M06.L01** — Basic RAG architecture — A simple pipeline showing query -> retriever -> external memory -> retrieved chunks -> prompt construction -> generator -> answer  
  _Learner should notice:_ the two core components: retriever and generator
- **M06.L01** — TF-IDF and inverted index intuition — A small corpus with an inverted index mapping rare and common query terms to documents, plus relevance scores  
  _Learner should notice:_ frequent terms inside one document help, but terms common across every document carry less weight
- **M06.L01** — Semantic retrieval pipeline — A diagram showing documents embedded and stored in a vector database, then a query embedded by the same model and matched to nearby vectors  
  _Learner should notice:_ indexing and querying must use compatible embeddings
- **M06.L01** — Exact k-NN versus ANN — A side-by-side diagram where exact search compares against every vector while ANN navigates only a small graph/cluster subset  
  _Learner should notice:_ the accuracy-versus-speed tradeoff
- **M06.L01** — Hybrid retrieval with RRF — BM25 and vector search running in parallel, producing two ranked lists that are fused into one final ranking before reranking/generation  
  _Learner should notice:_ how lexical and semantic evidence complement each other
- **M06.L01** — Chunk size and overlap tradeoff — One document shown first as large chunks and then as smaller overlapping chunks  
  _Learner should notice:_ how overlap protects boundary information while smaller chunks increase index volume
- **M06.L01** — Contextual retrieval — A document split into chunks, each chunk receiving a short title/summary/entity context before being embedded and indexed  
  _Learner should notice:_ the added context makes isolated chunks easier to retrieve correctly
- **M06.L01** — Tabular RAG workflow — A pipeline showing user question -> relevant schema selection -> text-to-SQL -> database execution -> result -> response generation  
  _Learner should notice:_ structured data retrieval often requires tool execution rather than nearest-neighbor document search
- **M06.L01** — Agent loop — A loop showing user goal -> planner -> tool/action -> environment -> observation -> planner, repeating until completion  
  _Learner should notice:_ the model receives feedback from the environment rather than producing one isolated answer
- **M06.L01** — Decoupled planning and execution — A loop showing plan generation -> plan validation -> execution -> outcome evaluation -> replan, with invalid plans returning to the planner before any tool is called  
  _Learner should notice:_ validation can prevent expensive or dangerous execution
- **M06.L01** — Agent control-flow patterns — Four small diagrams for sequential, parallel, conditional, and loop execution  
  _Learner should notice:_ complex agents need more than a simple list of tool calls
- **M06.L01** — ReAct and reflection loop — A circular diagram showing plan/thought -> action/tool -> observation -> evaluation/reflection -> updated plan  
  _Learner should notice:_ observation is fed back into future decisions rather than ignored
- **M06.L01** — Three-level AI memory hierarchy — A hierarchy showing model weights as internal knowledge, active context as short-term memory, and external persistent stores as long-term memory  
  _Learner should notice:_ the tradeoff between persistence, capacity, and access
- **M06.L01** — Memory management flow — New observation entering a decision node with branches insert, merge, replace, ignore, plus retrieval from long-term memory back into active context  
  _Learner should notice:_ useful memory requires active management, not only storage
- **M07.L01** — Prompting versus finetuning — A side-by-side diagram where prompting changes instructions/context around fixed model weights while finetuning updates some or all model weights  
  _Learner should notice:_ the adaptation happens in different places
- **M07.L01** — Finetuning family — A branching diagram from a pre-trained model to continued pre-training, supervised finetuning, preference finetuning, infilling, and long-context finetuning  
  _Learner should notice:_ 'finetuning' is an umbrella for several different training objectives
- **M07.L01** — RAG versus finetuning decision tree — A decision tree starting with model failure, branching into missing/outdated information toward RAG and behavior/format/style failure toward finetuning, with a later branch allowing both  
  _Learner should notice:_ failure diagnosis should drive the adaptation method
- **M07.L01** — Forward and backward pass — A small neural-network diagram showing forward activations and backward gradients, with loss feeding into parameter updates  
  _Learner should notice:_ training stores extra information absent from normal inference
- **M07.L01** — Inference versus training memory — A stacked bar comparison showing inference memory as weights + activations/KV and training memory adding gradients + optimizer states + larger activation requirements  
  _Learner should notice:_ why a model that fits for inference may still not fit for finetuning
- **M07.L01** — Quantization memory tradeoff — The same model shown at 32-bit, 16-bit, 8-bit, and 4-bit with decreasing memory blocks and a warning that lower precision can introduce numerical error  
  _Learner should notice:_ the near-linear memory reduction with bits per value
- **M07.L01** — Adapter PEFT versus soft prompts — A transformer diagram with one version showing small trainable adapter modules inside the network and another showing trainable soft vectors prepended to model inputs/layers  
  _Learner should notice:_ both freeze most base weights but adapt the model at different locations
- **M07.L01** — LoRA matrix update — A large frozen matrix W beside two small trainable matrices A and B whose product forms a low-rank update added to W  
  _Learner should notice:_ only A and B receive gradient updates
- **M07.L01** — Multi-LoRA serving — One shared base model connected to many small customer/task adapters that are swapped at runtime  
  _Learner should notice:_ the expensive base weights are stored once
- **M07.L01** — LoRA versus QLoRA — Side-by-side diagram where LoRA uses a higher-precision frozen base plus small adapters, while QLoRA stores the frozen base in 4-bit NF4 and trains small adapters with temporary dequantization  
  _Learner should notice:_ QLoRA reduces the base-model memory, not merely adapter size
- **M07.L01** — Task-vector merging — One base model with two finetuned models producing delta/task vectors, then the vectors being combined and added back to the base  
  _Learner should notice:_ merging can operate on changes from the shared base rather than raw full weights
- **M07.L01** — Layer stacking and upscaling — Two copies of a smaller model whose layers are partly stacked and partly combined to create a deeper larger model  
  _Learner should notice:_ stacking changes the architecture and normally requires more training
- **M08.L01** — Dataset engineering lifecycle — A circular workflow showing define behavior -> acquire/annotate -> synthesize -> verify -> inspect/process -> train/evaluate -> return to curation  
  _Learner should notice:_ dataset engineering is iterative rather than linear
- **M08.L01** — Human versus AI tool workflow — A side-by-side flow showing a human using browser UI steps and an AI making direct API/tool calls  
  _Learner should notice:_ copying human actions exactly may produce inefficient agent training data
- **M08.L01** — Quality coverage quantity triangle — A triangle with quality, coverage/diversity, and quantity at the corners, with strong training data in the center  
  _Learner should notice:_ increasing only one dimension cannot compensate for failures in the others
- **M08.L01** — Dataset-size performance curve — A learning curve showing performance rising quickly with early examples and gradually flattening  
  _Learner should notice:_ diminishing returns and how the slope informs whether more annotation is worthwhile
- **M08.L01** — Synthetic-data motivations — Five branches from synthetic data labeled quantity, coverage, quality, privacy, and distillation  
  _Learner should notice:_ synthetic data is not only a way to make a dataset bigger
- **M08.L01** — Instruction-data synthesis pipeline — Seed tasks/topics feeding instruction generation, response generation, verification, filtering, and final SFT dataset  
  _Learner should notice:_ generation must be followed by verification and coverage analysis
- **M08.L01** — Verified coding-data synthesis — Program problem -> generated code -> parser/linter -> unit tests -> correction loop -> verified example, with optional translation/back-translation branches  
  _Learner should notice:_ bad generated examples are rejected rather than blindly added to training
- **M08.L01** — Synthetic-data feedback loop — Real distribution -> model -> synthetic dataset biased toward common cases -> next model -> even narrower distribution, with rare cases fading  
  _Learner should notice:_ how repeated synthetic-only training can erase the tails
- **M08.L01** — Dataset inspection dashboard — Histograms for input length, response length, language, topic, and annotator score alongside a manual-example viewer  
  _Learner should notice:_ aggregate statistics and raw-example inspection complement each other
- **M08.L01** — Deduplication strategies — Three branches showing pairwise similarity, hashing/bucketing, and vector/dimensionality reduction candidate search  
  _Learner should notice:_ the tradeoff between exhaustive accuracy and scalable candidate filtering
- **M09.L01** — Three levels of inference optimization — A layered diagram showing model-level, hardware-level, and service-level optimizations feeding latency and cost outcomes  
  _Learner should notice:_ inference efficiency is a systems problem, not only a model problem
- **M09.L01** — Roofline model intuition — A simplified roofline graph with a bandwidth-limited rising region and compute-limited flat region  
  _Learner should notice:_ optimization depends on which side of the bottleneck the workload occupies
- **M09.L01** — Prefill versus decode — A two-phase LLM inference diagram showing parallel input processing during prefill and one-token-at-a-time generation during decode  
  _Learner should notice:_ the different compute profiles
- **M09.L01** — TTFT and TPOT timeline — A request timeline marking request arrival, first token, subsequent tokens, and completion  
  _Learner should notice:_ how first-token delay and per-token generation contribute differently to total latency
- **M09.L01** — Throughput versus goodput — A bar of all completed requests with only the SLO-satisfying portion highlighted as goodput  
  _Learner should notice:_ raw throughput can overstate useful serving capacity
- **M09.L01** — Accelerator memory hierarchy — A memory pyramid showing CPU DRAM at large/slow bottom, GPU HBM in the middle, and small/fast on-chip SRAM/registers at the top  
  _Learner should notice:_ the capacity-versus-bandwidth tradeoff across memory levels
- **M09.L01** — Speculative decoding — A draft model proposing K tokens and a target model accepting the longest valid prefix in one verification pass  
  _Learner should notice:_ how verification parallelizes work that would otherwise be sequential
- **M09.L01** — KV-cache reuse — Several decoding steps where old K/V vectors remain cached and only the newest token's K/V is added  
  _Learner should notice:_ caching removes recomputation but grows memory over the sequence
- **M09.L01** — Paged KV cache — A comparison between fragmented contiguous KV allocations and page/block-based allocations packed flexibly into GPU memory  
  _Learner should notice:_ how paging reduces wasted memory space
- **M09.L01** — Operator fusion — A before/after diagram where operator A writes an intermediate tensor to memory and operator B reloads it, versus a fused kernel keeping the intermediate on-chip  
  _Learner should notice:_ the avoided memory traffic
- **M09.L01** — Static versus dynamic batching — A timeline of arriving requests where static waits for a full batch and dynamic launches when full or timeout occurs  
  _Learner should notice:_ the throughput-versus-queueing-latency tradeoff
- **M09.L01** — Continuous batching — A batch-slot timeline where one request finishes early and is immediately replaced by a new request while longer requests continue  
  _Learner should notice:_ why variable-length workloads benefit from in-flight batching
- **M09.L01** — Prompt caching — Two requests sharing a long system prompt where the first request computes/caches the prefix and the second reuses it while only processing the new user suffix  
  _Learner should notice:_ which computation is avoided
- **M09.L01** — Parallelism families — A comparison of replica parallelism (full copies), tensor parallelism (split operator tensors), pipeline parallelism (split layers), and context parallelism (split sequence)  
  _Learner should notice:_ what dimension each strategy partitions
- **M10.L01** — Progressive AI architecture — A left-to-right sequence starting with user->model and progressively adding context, guardrails, router/gateway, cache, agent loops, observability, and orchestration  
  _Learner should notice:_ each component is introduced to address a specific production need
- **M10.L01** — Context-enhanced architecture — User query flowing into retrieval/tools, retrieved context joining the query, then both entering the model  
  _Learner should notice:_ external information is constructed per query rather than memorized inside every prompt
- **M10.L01** — PII masking workflow — Input containing private data -> sensitive-data detector -> placeholder substitution -> external model -> placeholder response -> trusted reverse map -> final restored response  
  _Learner should notice:_ which parts must remain inside the trust boundary
- **M10.L01** — Model gateway — Multiple applications connecting to one gateway which fans out to several commercial and self-hosted model endpoints  
  _Learner should notice:_ model access and policies are centralized
- **M10.L01** — Semantic-cache lookup — Query -> embedding -> vector search over cached queries -> similarity threshold -> cache hit or normal model pipeline  
  _Learner should notice:_ an incorrect similarity decision can return an incorrect answer
- **M10.L01** — Evaluation-monitoring feedback loop — Offline evaluation -> deployment -> monitoring/observability -> production failures -> new evaluation cases -> next release  
  _Learner should notice:_ evaluation and production monitoring form one learning loop
- **M10.L01** — AI request trace — A horizontal timeline showing router, retrieval, model, tool, guardrail, and final response spans with latency/cost annotations  
  _Learner should notice:_ how one trace connects component-level failures to the user-visible result
- **M10.L01** — AI product data flywheel — Product -> users -> interaction/feedback data -> evaluation/training/personalization -> improved product  
  _Learner should notice:_ product usage can become a model-improvement advantage only when feedback is responsibly captured
- **M10.L01** — Workflow-integrated feedback — A generated suggestion with actions accept, edit, regenerate, ignore, and share, each producing different feedback strengths  
  _Learner should notice:_ useful feedback can be collected as a natural side effect of accomplishing the task
- **M10.L01** — Feedback bias map — A central 'user feedback' node connected to leniency, randomness, position, length/preference, and recency bias  
  _Learner should notice:_ raw feedback needs interpretation before it becomes training or product truth
- **M10.L01** — Degenerate feedback loop — Ranking -> exposure -> user feedback -> model update -> stronger ranking, shown as an amplifying cycle  
  _Learner should notice:_ model outputs influence the data that later trains the model

## COURSE-007_AI_Agents_With_MCP — 61 images

- **M01.L01** — Evolution from chatbot to augmented LLM — A four-stage diagram showing basic LLM chat, RAG with a vector database, function calling with an execution environment, and an augmented LLM with retrieval, tools, and memory  
  _Learner should notice:_ each stage adds capability around the model rather than replacing the model itself
- **M01.L01** — Agent Reason-Act-Observe loop — A circular diagram with Reason → Act → Observe → Reason, with environment inputs such as tools, files, prompt, and history feeding the Act stage and tool results feeding Observe  
  _Learner should notice:_ the next action depends on observed feedback, which is what makes the process adaptive
- **M01.L01** — Fixed workflow versus autonomous agent — Two side-by-side diagrams: left shows a predetermined code-controlled chain of LLM calls; right shows an LLM choosing among tools inside repeated action-feedback loops  
  _Learner should notice:_ both may use LLMs and tools, but control of the path is different
- **M01.L01** — M×N integration problem transformed into M+N with MCP — First panel shows three model applications each connected separately to four tools, producing twelve links; second panel shows the applications connecting through MCP clients to MCP servers so each side needs only its protocol connection  
  _Learner should notice:_ how a shared protocol removes repeated pairwise connectors
- **M01.L01** — MCP host-client-server architecture — A diagram showing a host application containing an LLM and MCP client, the client communicating across a transport with an MCP server, and the server exposing tools, resources, and prompts  
  _Learner should notice:_ the MCP client belongs to the host side, while capabilities are exposed by the server side
- **M01.L01** — Local and remote MCP transports — A split diagram showing a local host and MCP server connected through stdio on one side, and a host connecting to a remote MCP server through Streamable HTTP on the other; annotate that JSON-RPC messages travel through either transport  
  _Learner should notice:_ the protocol message model stays consistent even though the transport changes
- **M02.L01** — Host application with LLM and MCP clients — A diagram showing a user interacting with one host application that contains both an LLM-provider client and an MCP client; the LLM client points to the model API while the MCP client points to an MCP server  
  _Learner should notice:_ the two clients solve different communication problems but are coordinated by the same host
- **M02.L01** — Wrapped MCP client layer hierarchy — A layered diagram showing Host Application → application MCPClient wrapper → SDK Client → Transport → MCP Server  
  _Learner should notice:_ the wrapper is an application design choice that adds control without replacing the SDK client
- **M02.L01** — stdio versus Streamable HTTP client connection — A side-by-side architecture: left shows Host + MCP Client launching a local MCP Server subprocess via stdio; right shows Host + MCP Client sending requests to a remote MCP Server URL over Streamable HTTP  
  _Learner should notice:_ stdio manages a local process while Streamable HTTP targets a remote service
- **M02.L01** — Tool discovery and invocation sequence — A sequence diagram with Host → MCP Client → MCP Server for list_tools, then Host/LLM selecting one tool, MCP Client calling it, and the server returning one or more content blocks  
  _Learner should notice:_ discovery happens before execution and that tool results may be multimodal or multi-part
- **M02.L01** — End-to-end MCP tool-use loop — A sequence diagram showing User → Host → LLM; LLM returns tool request; Host → MCP Client → MCP Server; tool result returns to Host; Host sends tool result back to LLM; LLM either asks for another tool or returns final text to User  
  _Learner should notice:_ the model never executes the server function directly—the host and MCP client perform the call
- **M02.L01** — Intelligent MCP resource loading — A flow diagram showing user query plus available resource descriptions feeding a selector, selected names mapped to URIs, resources loaded through MCP, then relevant text/image context attached to the user's message  
  _Learner should notice:_ resource discovery, selection, reading, and prompt injection are separate steps
- **M02.L01** — Dynamic MCP prompt lifecycle — A diagram showing list_prompts → user selects prompt → host collects required arguments → get_prompt(name, arguments) → server returns PromptMessage objects → host converts them into model conversation messages  
  _Learner should notice:_ MCP supplies the prompt definition while the host owns argument collection and presentation
- **M02.L02** — Bidirectional MCP client capabilities — A diagram showing Host + MCP Client in the center, server-provided primitives flowing from MCP Server to Host, and client-provided capabilities sampling/roots/elicitation flowing back toward the server through callbacks  
  _Learner should notice:_ the client becomes an active boundary, not merely a passive connector
- **M02.L02** — MCP Multi Round-Trip Request flow — A sequence diagram with Client sending request, Server returning InputRequiredResult, Client callback collecting information, Client retrying with inputResponses and a new request ID, then Server returning the final result  
  _Learner should notice:_ the server's extra request is part of a client-originated workflow
- **M02.L02** — Roots as coordination vs real access control — A diagram showing a user-selected project directory passed as an MCP root to a server, while a separate host-side permission boundary enforces actual filesystem access  
  _Learner should notice:_ the root is a hint/scope declaration, while security enforcement must exist elsewhere
- **M02.L02** — Elicitation user-consent flow — A sequence diagram showing Server requesting information, Client displaying server identity and schema, User choosing accept/decline/cancel, and accepted structured data returning through the client  
  _Learner should notice:_ the client protects the user from silent server data collection
- **M02.L02** — OAuth flow for a remote MCP server — A diagram showing User/Host, MCP Client as OAuth client, Authorization Server, and MCP Server as resource server; show token issuance and authenticated MCP request  
  _Learner should notice:_ the authorization server is separate from MCP even though the MCP client uses its token
- **M02.L02** — Provider-neutral tool adapter pattern — A diagram showing MCP Server → MCP Client → InternalTool representation branching into Anthropic adapter, OpenAI adapter, and another provider adapter → selected LLM  
  _Learner should notice:_ model-specific translation happens after MCP-native discovery
- **M02.L02** — Multi-server session group — A diagram with one host/client wrapper containing ClientSessionGroup and three separate sessions connected to three MCP servers; show aggregated tools/resources/prompts and namespaced tool names  
  _Learner should notice:_ many sessions are managed together but server identity must still be preserved
- **M02.L02** — Tool context optimization patterns — A three-panel comparison: full refreshed tool list, search_tools progressive disclosure, and code execution with typed stubs inside an isolated sandbox  
  _Learner should notice:_ the tradeoff between simplicity, token savings, extra round trips, and security complexity
- **M02.L02** — MCP recovery and resubscription flow — A diagram showing stdio crash recovery on one side and Streamable HTTP retry/backoff on the other, with a shared branch for refreshing capabilities and restoring subscriptions  
  _Learner should notice:_ recovery strategy differs by transport but both require refresh and careful retry
- **M03.L01** — MCP server as a reusable distribution layer — A before-and-after diagram showing several applications each maintaining custom integrations versus several MCP clients connecting to one reusable MCP server  
  _Learner should notice:_ MCP moves integration knowledge out of each host application and into a reusable server boundary
- **M03.L01** — MCP server transport comparison — Two panels: stdio with a client launching a local server subprocess and reading/writing streams; Streamable HTTP with a client sending POST requests to a remote /mcp endpoint and optionally receiving an SSE response stream  
  _Learner should notice:_ the local process lifecycle versus remote request/response lifecycle
- **M03.L01** — Granular REST wrapper versus agent-oriented MCP tool — Left panel shows one user intent requiring three or more small API-shaped MCP tools; right panel shows one end-to-end agent-oriented tool calling internal helper/API steps behind the server  
  _Learner should notice:_ internal composition can remain granular while the model-facing action stays simple
- **M03.L01** — MCPServer tool inference — A diagram mapping Python function name, docstring, parameter type hints, and return annotation into MCP tool name, description, input schema, and output schema  
  _Learner should notice:_ how normal Python design decisions become part of the protocol-facing tool definition
- **M03.L01** — MCP tool lifecycle — A sequence diagram showing list discovery, model tool selection, tools/call, server execution, tool result returning to the model, plus an optional list-changed notification path  
  _Learner should notice:_ discovery and execution are separate phases
- **M03.L01** — MCP prompt lifecycle and composition — A diagram showing prompts/list discovery, user selecting a prompt, prompts/get with arguments, server returning user/assistant messages, and optional links to tools/resources  
  _Learner should notice:_ prompts are server-distributed but normally user-selected and client-integrated
- **M03.L01** — Fixed resource versus resource template — A diagram showing one fixed URI mapping to one resource and a templated URI such as file:///{filename} mapping to many concrete resources, with loading deferred until resources/read  
  _Learner should notice:_ templates scale discovery without loading every possible resource upfront
- **M03.L01** — MCP resource discovery-read-subscribe lifecycle — A sequence diagram showing resources/list, resource selection, resources/read, contextual use by the application, and a modern subscriptions/listen stream receiving a resource/list or resource update notification  
  _Learner should notice:_ the separation between metadata discovery, content loading, and later update awareness
- **M03.L02** — Advanced MCP server capability map — A two-column diagram with server utilities on one side and client-provided capabilities on the other, both feeding into tools/prompts/resources  
  _Learner should notice:_ utilities improve operation while client capabilities let server workflows obtain external input
- **M03.L02** — MCP completion lifecycle — A sequence diagram where the user types progressively more text, the client sends repeated completion requests, and the server returns a narrowing list of suggestions  
  _Learner should notice:_ completion frequency is client-controlled, so server-side rate limiting may be necessary
- **M03.L02** — MCP Python Context hierarchy — A tree diagram showing Context at the top and its mcp_server, session, client_capabilities, and request_context branches with their major properties  
  _Learner should notice:_ one injected object exposes both static server state and per-request state
- **M03.L02** — Long-running tool with progress updates — A sequence diagram showing Client calling a tool, Server executing in stages, Server sending periodic progress notifications, and finally returning the tool result  
  _Learner should notice:_ progress messages improve UX without changing the final result contract
- **M03.L02** — MCP resolver dependency flow — A flow diagram showing model-provided arguments and Context feeding resolvers, resolvers obtaining elicitation/sampling/roots values, and the SDK injecting those results before the tool body runs  
  _Learner should notice:_ resolved parameters are not chosen by the model
- **M03.L02** — Elicitation resolver flow — A sequence diagram showing tool call → resolver → client UI → user accept/decline/cancel → validated result → tool body  
  _Learner should notice:_ user input is injected by the SDK rather than filled by the model
- **M03.L02** — Roots coordination versus real sandboxing — A diagram showing a client-declared root passed to a local server, plus a separate true sandbox/OS-permission boundary around the server process  
  _Learner should notice:_ roots describe intended scope but the sandbox enforces actual scope
- **M03.L03** — MCP server production lifecycle — A pipeline from server implementation through testing, evaluations, security hardening, packaging/deployment, and publication  
  _Learner should notice:_ passing unit tests is only one stage of production readiness
- **M03.L03** — Inspector-driven MCP development loop — A circular workflow showing code change → reconnect Inspector → discover capability → execute happy path → inspect messages → test edge cases → code change  
  _Learner should notice:_ testing happens continuously during development rather than after the server is finished
- **M03.L03** — Software tests versus LLM evaluations — A side-by-side diagram: deterministic software test checks function correctness while evaluation sends natural-language tasks to models and measures tool choice/prompt behavior/cost  
  _Learner should notice:_ both are required because they measure different failure modes
- **M03.L03** — Layered defenses against injected input — A diagram where untrusted model/user/content input passes through validation, least-privilege permissions, sandbox boundaries, and controlled tool execution before reaching database/filesystem/network resources  
  _Learner should notice:_ security does not depend on one text filter
- **M03.L03** — Three-layer MCP server security architecture — A stacked diagram with infrastructure isolation at the bottom, access control in the middle, and observability/supply-chain/HITL controls at the top  
  _Learner should notice:_ strong security combines prevention, authorization, and detection/response
- **M03.L03** — Lethal Trifecta triangle — A triangle labeled Private Data, Untrusted Content, and Third-Party Communication, with a warning in the center and examples of controls that remove one edge  
  _Learner should notice:_ security can improve by structurally breaking the dangerous combination
- **M03.L03** — Remote MCP deployment stack — A layered diagram showing cloud/container → Uvicorn → ASGI app → mounted MCP server → /mcp endpoint, with OAuth/gateway in front  
  _Learner should notice:_ how MCP can fit into a conventional scalable web-service deployment
- **M04.L01** — MCP abstraction stack — A layered diagram showing application → MCP protocol/session → transport → network/process layer, with one JSON-RPC message flowing downward and upward  
  _Learner should notice:_ the transport does not decide tool semantics; it only carries protocol messages
- **M04.L01** — MCP error layers — A three-layer diagram for transport, protocol, and application errors, with each layer mapped to connection exception, JSON-RPC error response, or isError tool result  
  _Learner should notice:_ not every failure is encoded in the same message type
- **M04.L01** — Embedded binary versus ResourceLink — A comparison showing image bytes Base64-encoded inside a JSON-RPC payload versus a lightweight resource link containing URI/metadata and deferred retrieval  
  _Learner should notice:_ the payload and context savings of lazy/out-of-band loading
- **M04.L01** — Session and transport message flow — A sequence diagram showing Host → ClientSession → dispatcher → in-memory write stream → transport → wire → server transport → read stream → dispatcher → handler  
  _Learner should notice:_ where transport responsibility starts and ends
- **M04.L01** — stdio transport internals — A diagram showing ClientSession connected via two anyio memory stream pairs to stdin_writer/stdout_reader tasks, which in turn connect to the server subprocess's stdin/stdout  
  _Learner should notice:_ the separation between in-memory session streams and OS process pipes
- **M04.L01** — Modern Streamable HTTP lifecycle — A diagram showing ClientSession write stream → post_writer → multiple independent POST request tasks → /mcp endpoint → JSON or per-request SSE responses → read stream  
  _Learner should notice:_ each request owns its own HTTP exchange rather than sharing one permanent connection
- **M04.L01** — Modern input_required versus subscriptions/listen — Two side-by-side sequences: one showing input_required then a client follow-up POST, and one showing an explicitly requested subscriptions/listen POST whose SSE response stays open for change events  
  _Learner should notice:_ both preserve client initiation
- **M04.L01** — Custom MCP transport contract — A diagram with Session on the left, two anyio memory stream pairs in the middle, custom read/write tasks, framing/serialization, and an arbitrary wire protocol on the right  
  _Learner should notice:_ which stream endpoints belong to the session versus the transport
- **M04.L01** — stdio versus HTTP transport threat models — Two panels: stdio risks centered on local process privileges/environment/secrets, Streamable HTTP risks centered on network interception/authentication/origin exposure  
  _Learner should notice:_ transport choice changes which security controls matter most
- **M05.L01** — MCP ecosystem beyond the core protocol — A diagram with Core MCP in the center and branches for registry/discovery, governance/gateways, context management, testing, extensions, and contribution/governance  
  _Learner should notice:_ the core protocol is only one layer of the larger MCP ecosystem
- **M05.L01** — Official MCP Registry discovery flow — A diagram showing server publisher → package registry + official MCP Registry metadata → clients/agents querying the Registry  
  _Learner should notice:_ the official Registry points to distributable artifacts rather than necessarily hosting the server code itself
- **M05.L01** — MCP Registry and subregistry ecosystem — Official Registry at top, several public/private subregistries beneath it, and multiple clients connected downstream; include an enterprise private subregistry with vetted-only entries  
  _Learner should notice:_ subregistries can filter and enrich upstream data rather than simply copy it
- **M05.L01** — Direct inbound MCP access versus tunnel architecture — Two-panel comparison: direct public inbound connection to internal server versus internal server making outbound connection to edge proxy that clients use  
  _Learner should notice:_ how the tunnel removes the direct public inbound port
- **M05.L01** — Code Mode architecture — A diagram showing LLM receiving compact API → generating code → isolated sandbox → multiple MCP/API calls internally → final result returned to model  
  _Learner should notice:_ multiple deterministic operations can happen without repeated model round trips
- **M05.L01** — MCP core plus extensions — Core MCP in the center with separate extension modules for Apps, OAuth Client Credentials, Enterprise-Managed Authorization, and Tasks  
  _Learner should notice:_ extensions augment but do not redefine the core protocol
- **M05.L01** — MCP Tasks durable state machine — A state diagram with working ↔ input_required and terminal states completed, failed, cancelled; show client polling tasks/get using taskId  
  _Learner should notice:_ task durability is independent of one connection staying alive
- **M05.L01** — SEP lifecycle — A flowchart from idea → discussion → PR → sponsor → draft → review → accepted → reference implementation → conformance tests → final → future release  
  _Learner should notice:_ implementation and interoperability testing are part of specification work, not an afterthought

## COURSE-008_Vision_Language_and_Multimodal_AI_Engineering — 98 images

- **M01.L01** — DCT compression intuition — Show one image block, its DCT coefficient grid with most energy concentrated near the low-frequency corner, a thresholded coefficient grid, and a reconstructed block  
  _Learner should notice:_ visually important structure can often be preserved even after many small high-frequency coefficients are removed
- **M01.L01** — 1D convolution and feature map — Show a step-like one-dimensional signal, the [-1, 1] kernel sliding over pairs, and the resulting feature map with spikes at changes  
  _Learner should notice:_ connect a spike in the feature map with a transition in the original signal
- **M01.L01** — 2D edge-detection kernels — Show a small grayscale patch beside representative vertical and horizontal Prewitt/Sobel kernels and the corresponding edge-response maps  
  _Learner should notice:_ kernel values determine which orientation or visual pattern becomes strong in the feature map
- **M01.L01** — CNN first-layer feature maps — Show one input image, several small learned 3x3 filters, and multiple resulting feature maps  
  _Learner should notice:_ one convolutional layer detects many different patterns in parallel
- **M01.L01** — Four visual computer-vision tasks — Show the same scene as classification, object detection, semantic segmentation, and instance segmentation outputs  
  _Learner should notice:_ the visual backbone may be shared while the task output and head change
- **M01.L01** — Backbone-neck-head pipeline — Show an input image flowing through a generic backbone, feature-refinement neck, and task head into an output  
  _Learner should notice:_ transfer learning commonly reuses the backbone while neck/head design can be task specific
- **M01.L01** — ResNet residual and bottleneck block — Show both a simple residual block and a bottleneck 1x1 → 3x3 → 1x1 block with the shortcut path  
  _Learner should notice:_ the shortcut bypasses several transformations and is added back to the processed signal
- **M01.L01** — Unrolled RNN — Show tokens x1, x2, x3, x4 entering sequential RNN cells with hidden states h1, h2, h3, h4 flowing forward  
  _Learner should notice:_ later computation depends on a chain of earlier hidden states
- **M01.L01** — Vision Transformer patch pipeline — Show a 224x224 image split into 16x16 patches, patch flattening/projection, position embeddings, a transformer encoder, and a classification head  
  _Learner should notice:_ the analogy between image patches in ViT and tokens in a text transformer
- **M01.L01** — CLIP similarity matrix — Show N image embeddings on rows, N text embeddings on columns, with the matching diagonal highlighted and off-diagonal mismatches suppressed  
  _Learner should notice:_ contrastive learning rewards aligned image-text pairs rather than requiring a fixed category label
- **M01.L01** — Modern VLM projection layer — Show image patches entering a vision encoder, visual tokens entering a projection layer, projected visual tokens concatenated or combined with text embeddings, and both entering a text decoder  
  _Learner should notice:_ the connector translates between representation spaces rather than converting pixels directly into final sentences
- **M01.L01** — VLM staged training — Show stage 1 with frozen image encoder and frozen language decoder while the multimodal projector is trainable, followed by a later stage where more of the network can be fine-tuned  
  _Learner should notice:_ pretrained components can be connected before expensive end-to-end tuning
- **M01.L01** — Hugging Face model repository anatomy — Show a generic model repository page with model card, files/versions, and community areas called out  
  _Learner should notice:_ know where to look for usage instructions, weights/configs, and community troubleshooting
- **M01.L01** — Two-stage multimodal retrieval system — Show an offline image-indexing path and an online text-query path meeting at a vector index  
  _Learner should notice:_ image embeddings can be computed ahead of time, while only the query embedding and nearest-neighbor search are needed online
- **M01.L02** — Early image-captioning architecture — Show an image entering a CNN encoder, the visual feature vector flowing into an RNN/LSTM decoder, and a caption being generated word by word  
  _Learner should notice:_ image captioning as an encoder-decoder mapping from visual representation to language
- **M01.L02** — VQA evolution — Show three stages: CNN+RNN fusion, attention-guided VQA, and transformer-based multimodal VQA  
  _Learner should notice:_ how question-conditioned visual focus becomes more explicit and representations become more general
- **M01.L02** — Visual reasoning workflow — Show a complex visual input such as an invoice or labeled product, several highlighted evidence regions, intermediate reasoning steps, and a final answer  
  _Learner should notice:_ the answer depends on combining multiple observations rather than one local recognition
- **M01.L02** — NDCG ranking intuition — Show one query with five ranked results, relevance grades above each result, stronger visual emphasis on early positions, and a comparison with the ideal ranking  
  _Learner should notice:_ the same relevant items receive a better score when high-relevance results appear earlier
- **M01.L02** — Hierarchical document understanding — Show a document page being decomposed into text blocks, table regions, figures, and spatial layout, followed by a semantic reasoning layer and a final answer  
  _Learner should notice:_ document AI must reason over both content and layout
- **M01.L02** — Multimodal document RAG — Show a user question entering a visual document retriever, several pages being ranked, the top page being passed with the question into a VLM, and a grounded answer coming out  
  _Learner should notice:_ distinguish retrieval from generation and see why both are needed
- **M01.L02** — Video understanding and temporal grounding — Show sampled video frames along a timeline, a text query, highlighted relevant frames, and predicted start/end timestamps  
  _Learner should notice:_ the model must connect content across time rather than interpret one frame independently
- **M01.L02** — VLM-assisted annotation pipeline — Show raw factory images entering a generalist VLM, automatically generated bounding boxes being reviewed, then a smaller detector being trained and deployed  
  _Learner should notice:_ how expensive general models can bootstrap efficient task-specific models
- **M01.L02** — Two VLM segmentation output strategies — Show one branch producing polygon/SVG geometry and another producing learned location/segmentation tokens that are decoded into a mask  
  _Learner should notice:_ a VLM can represent masks indirectly rather than outputting a raw pixel matrix token by token
- **M01.L03** — Training paradigms versus training stages — Create a two-axis diagram. One axis lists HOW: supervised, unsupervised, self-supervised, semi-supervised, contrastive. The other lists WHEN: pretraining, midtraining, post-training, alignment. Show that a stage can use multiple paradigms rather than implying a one-to-one mapping  
  _Learner should notice:_ "contrastive learning" and "pretraining" are not competing terms because they answer different questions
- **M01.L03** — Streaming multimodal data pipeline — Show a very large remote multimodal dataset feeding a stream of image-chat samples into preprocessing and then into the GPU training loop  
  _Learner should notice:_ the full dataset does not need to exist in local storage before training begins
- **M01.L03** — Minimal autoregressive VLM — Show two parallel paths: image→processor→vision encoder→projector and text→tokenizer→embedding layer. Merge them by concatenation before a causal LLM, then show logits  
  _Learner should notice:_ exactly where the two modalities become one sequence
- **M01.L03** — Cross-entropy intuition — Show two next-token distributions for the target token "sun": one with high probability on "sun" and low loss, one with probability spread over incorrect tokens and high loss  
  _Learner should notice:_ connect loss magnitude to how surprised the model is by the true next token
- **M01.L03** — Batch-size-1 loss curve — Show a raw noisy loss curve over training steps plus a smoothed downward trend  
  _Learner should notice:_ noisy individual steps can coexist with overall learning progress
- **M01.L03** — Naive vs constrained padding — Show variable-length samples padded to the longest sample, then the same set with a fixed 512-token threshold where an outlier is excluded  
  _Learner should notice:_ the trade-off between compute waste and discarded data
- **M01.L03** — Packing progression — Show four panels using the same variable-length samples: naive padding, constrained padding, naive packing, and balanced/greedy packing  
  _Learner should notice:_ gray padding shrink as packing becomes smarter
- **M01.L03** — Image placeholder replacement — Show a packed token sequence containing <  
  _Learner should notice:_ image
- **M01.L03** — Batch-size comparison — Show two loss curves over training steps: batch size 1 with high variance and batch size 4 with packing showing a smoother trend  
  _Learner should notice:_ connect larger effective batches with lower gradient variance, not assume that smoothing alone guarantees generalization
- **M01.L03** — Prefill versus decode with KV cache — Show the full prompt processed once during prefill, creating per-layer K/V cache. Then show each generated token computing only new Q/K/V while attending to cached K/V  
  _Learner should notice:_ history is still available even though most old attention projections are not recomputed
- **M01.L03** — High-resolution tiling — Show one dense screenshot first downscaled to 256x256 with unreadable details, then divided into a grid of multiple 256x256 tiles with readable local details  
  _Learner should notice:_ why tiling improves visibility but multiplies visual-token count
- **M01.L03** — Pixel-shuffle token compression — Show a 2D grid of visual tokens before compression and a smaller grid after compression where each remaining token has a deeper channel representation  
  _Learner should notice:_ the spatial-token versus channel-width trade-off
- **M01.L04** — Cascaded versus live multimodal interface — Left: microphone → ASR → transcript → text model → TTS → audio. Right: one stateful live session receiving audio + visual frames + text and returning streamed audio/text/tool events  
  _Learner should notice:_ the number of explicit processing boundaries and where information can be lost in the cascade
- **M01.L04** — Modality-to-representation diagram — Show text, image, and audio inputs each passing through their own preprocessing/ encoder path into vector representations that enter a shared multimodal context  
  _Learner should notice:_ raw media is converted into learned numerical representations before cross-modal reasoning
- **M01.L04** — Point-and-ask multimodal fusion — Show a user pointing at one component on a circuit board while asking "What is this part?" Then show spoken-text representation, pointing/visual-region representation, and dialog context converging into one answer  
  _Learner should notice:_ why neither speech nor image is sufficient by itself
- **M01.L04** — Training-stage data evolution — Show pretraining with large noisy/broad caption-style data flowing into a general VLM, followed by post-training with smaller high-quality Q&A, OCR, reasoning, document and task data  
  _Learner should notice:_ later stages use more task-specific supervision
- **M01.L04** — Video-data cost stack — Show one video branching into storage, frame decoding, temporal annotation, and training I/O challenges  
  _Learner should notice:_ video data engineering is an infrastructure problem as well as an annotation problem
- **M01.L04** — Dataset-building funnel — Show a wide raw-data input narrowing through sourcing, filtering, diversity validation, annotation, quality validation, and finally training-ready shards  
  _Learner should notice:_ data volume decreases while per-sample processing cost increases
- **M01.L04** — Hierarchical dataset taxonomy — Show broad categories branching into several subcategories and a separate "other" branch, with sample counts beside each category  
  _Learner should notice:_ how taxonomy supports both diversity analysis and dataset rebalancing
- **M01.L04** — WebDataset sharding — Show a large dataset split into tar shards, each shard containing image/text/ metadata files with matching basenames, then multiple training nodes reading different shard ranges  
  _Learner should notice:_ why sharding improves distributed input throughput
- **M01.L04** — General-to-specialized mixture — Show a pie/stack concept with general conversation, pure text, target-domain data, and bridge data, with arrows indicating specialization while preserving general capability  
  _Learner should notice:_ mixture design as a balance, not "add as much domain data as possible
- **M01.L04** — End-to-end multimodal learning lifecycle — Show real-world modalities → representations → multimodal model → output/tool use, and underneath show the training-data path from raw media → filtering → annotation → shards → mixture → training → evaluation → feedback to data  
  _Learner should notice:_ connect application-time multimodality with training-time data engineering
- **M01.L05** — Post-training roadmap — Show pretrained VLM branching into SFT, preference alignment, and verifiable-reward optimization, with LoRA/DoRA/QLoRA shown as efficiency tools underneath  
  _Learner should notice:_ distinguish the learning objective from the efficiency method
- **M01.L05** — Multimodal SFT chat template — Show system → user(image + text) → assistant(target answer), and distinguish inference formatting from training formatting  
  _Learner should notice:_ where the target response lives during supervised training
- **M01.L05** — LoRA low-rank update — Show frozen pretrained weight W plus two trainable low-rank matrices A and B whose product BA is added to W  
  _Learner should notice:_ why two thin matrices require far fewer trainable parameters than a full d×k update
- **M01.L05** — LoRA versus DoRA — Left: LoRA adds low-rank BA to a frozen weight. Right: DoRA separates weight magnitude and direction, then applies low-rank adaptation to direction  
  _Learner should notice:_ the structural difference rather than memorize formulas
- **M01.L05** — QLoRA memory concept — Show a large frozen base model compressed to 4-bit NF4 with small full/trainable adapter matrices attached, contrasting it with a full-precision full-fine-tune  
  _Learner should notice:_ which parameters are quantized, frozen, and trainable
- **M01.L05** — RLHF three-stage pipeline — Show SFT policy → generate candidate responses → human pairwise preferences → reward model → policy optimization  
  _Learner should notice:_ the reward model is learned from comparisons
- **M01.L05** — PPO-style RLHF versus DPO — Left: human preferences → reward model → PPO policy optimization. Right: chosen/rejected pairs → direct preference objective → policy  
  _Learner should notice:_ DPO removes the explicit reward-model-training stage
- **M01.L05** — GRPO group-relative loop — Show one prompt generating several candidate responses, each receiving a score, scores normalized relative to the group, then policy update with KL anchor to the reference  
  _Learner should notice:_ why the method is called group-relative
- **M01.L06** — Attention intuition — Show the words in "The AI community building the future" with stronger arrows from AI to future and community and weaker arrows to less relevant words  
  _Learner should notice:_ attention as weighted information gathering rather than a hard one-to-one lookup
- **M01.L06** — Scaled dot-product attention pipeline — Show Q and K multiplied to form score matrix, divide by sqrt(d_k), softmax to attention weights, then multiply by V to produce contextualized outputs  
  _Learner should notice:_ connect the formula to the four conceptual steps
- **M01.L06** — Self-attention versus cross-attention — Left: one mixed sequence generates Q/K/V internally. Right: text generates Q while image features generate K and V  
  _Learner should notice:_ the exact source difference between the two attention types
- **M01.L06** — Flamingo-style architecture — Show frozen vision encoder → perceiver resampler → compact visual tokens feeding gated cross-attention blocks interleaved through frozen LLM layers  
  _Learner should notice:_ distinguish frozen pretrained blocks from newly trainable fusion components
- **M01.L06** — Zero-initialized gated visual injection — Show frozen LLM hidden state flowing through a residual path while a new cross-attention path is multiplied by a gate starting at zero and gradually opening during training  
  _Learner should notice:_ why the new adapter does not corrupt the pretrained LLM at initialization
- **M01.L06** — Unified sequence VLM — Show image → vision encoder → linear projector → visual tokens inserted into a text-token sequence → one LLM using ordinary self-attention  
  _Learner should notice:_ compare this directly with the separate cross-attention path
- **M01.L06** — Fair VLM architecture comparison — Show two architectures receiving equal total token budgets, equal image/text content, same optimizer and training steps, contrasting with an unfair setup where one model receives more text tokens  
  _Learner should notice:_ why matched training input is necessary for causal comparison
- **M01.L06** — Early, intermediate, and late fusion — Show three parallel diagrams: early mixes visual/text features before joint processing; intermediate keeps separate encoders but injects cross-attention during processing; late combines final modality-specific decisions  
  _Learner should notice:_ fusion timing as a spectrum
- **M01.L06** — Evolution from single-vector captioning to modern VLMs — Show Show-and-Tell image→one vector→LSTM, Flamingo image→64 visual tokens→cross attention, and SmolVLM image→many projected visual tokens→LLM self-attention  
  _Learner should notice:_ how the visual bottleneck becomes progressively richer
- **M01.L07** — VLM inference pipeline — Show image → vision encoder → visual tokens merging with prompt tokens before the LLM, followed by prefill and autoregressive decode  
  _Learner should notice:_ the image may be encoded once but its visual tokens remain in the context
- **M01.L07** — Prefill and decode timeline — Show one large prefill block processing all image/text input tokens in parallel, then many smaller sequential decode steps, each reading the growing KV cache  
  _Learner should notice:_ why prefill happens once while decode repeats
- **M01.L07** — KV cache during generation — Show prefill creating cached K/V blocks for all input tokens, then each decode step appending one new K/V block while reusing old ones  
  _Learner should notice:_ connect cache growth to autoregressive generation
- **M01.L07** — MHA vs GQA vs MQA — Show many Q heads and how K/V heads are separately paired in MHA, grouped in GQA, and fully shared in MQA  
  _Learner should notice:_ KV-head sharing as a memory optimization
- **M01.L07** — Naive attention versus FlashAttention — Left: full NxN attention matrix repeatedly written/read from HBM. Right: Q/K/V processed in tiles kept in SRAM with incremental exact softmax  
  _Learner should notice:_ the optimization is mainly about data movement
- **M01.L07** — Component-wise VLM quantization — Show vision encoder and projector kept high precision while large LLM backbone is quantized to lower bit width  
  _Learner should notice:_ why optimizing the largest component yields most of the memory savings
- **M01.L07** — PagedAttention memory layout — Compare fixed maximum KV-cache allocations with many unused spaces against small cache pages allocated only as each request grows  
  _Learner should notice:_ how paging reduces memory waste and fragmentation
- **M01.L07** — Base model plus edge adapters — Show one quantized base VLM stored on-device with several tiny interchangeable LoRA adapters for different tasks  
  _Learner should notice:_ why PEFT helps distribution as well as training
- **M01.L08** — Document AI task map — Show one document page branching into direct QA, OCR/parsing, layout analysis, classification, field extraction, retrieval, and multimodal RAG  
  _Learner should notice:_ Document AI is a family of tasks rather than one single model problem
- **M01.L08** — Generative versus extractive document QA — Show the same document/question feeding two systems: one generating a natural sentence, the other highlighting and returning the exact answer span  
  _Learner should notice:_ flexibility versus constrained extraction
- **M01.L08** — OCR text versus structured document conversion — Compare plain OCR output with a structured representation containing heading, table, picture, caption, and list tags  
  _Learner should notice:_ why structure matters beyond recognizing characters
- **M01.L08** — Single-vector versus multivector document retrieval — Left: one page compressed into one embedding compared with one query embedding. Right: page represented by many token embeddings and query represented by multiple token embeddings with late interaction  
  _Learner should notice:_ the memory-versus-fine-grained-matching trade-off
- **M01.L08** — LayoutLMv3 versus Donut — Left: external OCR text + boxes + image patches entering LayoutLMv3 encoder. Right: document image directly entering Donut encoder-decoder and generating structured text  
  _Learner should notice:_ OCR-dependent versus OCR-free architecture
- **M01.L08** — Bounding-box coordinate rescaling — Show one original document page with a text box, then the resized model input with the corresponding scaled box and coordinate tokens  
  _Learner should notice:_ why original pixel coordinates cannot be copied unchanged after image resizing
- **M01.L08** — Multimodal document RAG — Show PDF → page images → multimodal retriever → top relevant page → VLM with user query → answer  
  _Learner should notice:_ retrieval and answer generation as separate model stages
- **M01.L09** — Video-language task map — Show one video branching into classification, embedding-based retrieval, captioning, summarization, and question answering  
  _Learner should notice:_ distinguish label output, vector output, and free-form text output
- **M01.L09** — 3D convolution versus (2+1)D factorization — Show one full 3D spatiotemporal kernel on the left and separate per-frame 2D spatial filtering followed by 1D temporal filtering on the right  
  _Learner should notice:_ factorization as the recurring efficiency principle
- **M01.L09** — Joint, factorized, and hierarchical video attention — Show full all-to-all patch/frame attention, separate spatial-then-temporal attention, and local segment processing followed by segment-level attention  
  _Learner should notice:_ progressively stronger scaling strategies
- **M01.L09** — Temporal position encoding — Show visually identical/similar frame tokens receiving different time-position signals before attention  
  _Learner should notice:_ why attention needs explicit order information
- **M01.L09** — End-to-end Video-RAG — Show long videos split into segments, embedded and indexed; a query retrieves top clips, optional reranker reorders them, and a generative video VLM answers using only selected clips  
  _Learner should notice:_ retrieval and generation as complementary cost tiers
- **M01.L09** — Spatial pooling, temporal pooling, and frame selection — Show per-frame patch averaging, across-frame averaging, and selecting only keyframes as three separate token-reduction paths  
  _Learner should notice:_ compare what information each strategy removes
- **M01.L10** — Any-to-any multimodal system — Show text, image, audio, and video entering a multimodal reasoning system with text, image, speech/audio, and video outputs  
  _Learner should notice:_ any-to-any concerns both input and output modalities, not only multimodal perception
- **M01.L10** — Three any-to-any architecture families — Show unified discrete vocabulary, hybrid shared transformer with text tokens + continuous media latents, and late-conditioning MLLM → connector → specialized generator  
  _Learner should notice:_ compare where multimodal generation actually occurs
- **M01.L10** — Transitional Janus-style architecture — Show one continuous visual encoder for understanding and a separate VQ-based image tokenizer for generation, both connected to the autoregressive transformer  
  _Learner should notice:_ why this sits between pure monolithic and more factorized architectures
- **M01.L10** — Single codebook versus RVQ — Show one choice from one large visual codebook versus multiple sequential small codebooks that refine the representation  
  _Learner should notice:_ how combinatorial expressivity improves without exploding the LLM vocabulary
- **M01.L10** — Diffusion forward and reverse process — Show a clean media latent progressively becoming noise during training and the learned reverse process turning noise back into structured content  
  _Learner should notice:_ iterative refinement instead of one-shot token prediction
- **M01.L10** — Block-causal multimodal attention — Show text tokens with triangular causal attention, an image latent block with full bidirectional internal attention, and later text attending back to the entire image block  
  _Learner should notice:_ why different modality blocks require different masks
- **M01.L10** — Late-conditioning pipeline — Show prompt + query tokens → frozen/strong MLLM → query states → connector → swappable Image DiT, TTS, or Video DiT generators  
  _Learner should notice:_ why the connector is the modular handoff point
- **M01.L10** — Dual conditioning for image editing — Show source image + edit instruction feeding a frozen VLM semantic path, source image feeding a VAE latent path, and both conditioning an MMDiT renderer  
  _Learner should notice:_ distinguish "what to change" from "what to preserve
- **M01.L10** — Joint versus staged multimodal training — Left: shared model receiving understanding and generation losses simultaneously with conflicting gradient arrows. Right: phase 1 understanding, freeze MLLM, phase 2 train connector/generator  
  _Learner should notice:_ why staging can preserve earlier capabilities
- **M01.L11** — Agency spectrum — Show tool routing → structured tool calling → multistep ReAct agent, with increasing autonomy and increasing complexity/risk  
  _Learner should notice:_ agency is a design continuum
- **M01.L11** — ReAct loop — Show task → think/plan → action/tool → observation → completion decision → either final answer or memory and another cycle  
  _Learner should notice:_ feedback as the defining feature of agent behavior
- **M01.L11** — GUI localization versus agentic control — Left: screenshot + target → one predicted click coordinate. Right: screenshot + goal → reasoning model chooses multiple UI actions over several steps  
  _Learner should notice:_ distinguish perception/localization from full control
- **M01.L11** — Agent trust boundary — Show untrusted web content and third-party tools outside a security boundary, with a permission/validation layer before sensitive tools, files, or APIs  
  _Learner should notice:_ why tool-capable agents need explicit trust controls
- **M01.L11** — Asynchronous VLA action queue — Show policy server generating chunk B while robot executes chunk A from a queue; when remaining actions fall below threshold, robot sends a new observation  
  _Learner should notice:_ inference/control pipelining
- **M01.L11** — Common VLA architecture — Show cameras + instruction + proprioception → pretrained VLM → cached context tokens → diffusion/flow-matching action expert → action chunk → robot controller  
  _Learner should notice:_ the VLM as semantic context and the action expert as the continuous-action generator

## COURSE-009-Enterprise-RAG-Engineering — 83 images

- **M01.L01** — Basic RAG architecture — A user query flowing first to a retrieval component that fetches relevant information from a private knowledge source, then to an LLM that receives both the query and retrieved context and produces the final answer  
  _Learner should notice:_ retrieval happens before generation and that the LLM is grounded by external context
- **M01.L01** — RAG ingestion and query stack — A two-lane diagram: the ingestion lane starts from sources such as databases, PDFs, and knowledge tools, then moves through extraction, chunking, embeddings, and a vector store; the query lane starts with a user query, performs retrieval with semantic/lexical or hybrid search, optional reranking, passes context to an LLM, and finishes with citations and guardrails  
  _Learner should notice:_ ingestion prepares knowledge ahead of time, while the query flow uses that prepared knowledge for each user request
- **M01.L01** — Semantic retrieval in embedding space — A conceptual diagram with one query point and several document-chunk points, highlighting nearby semantically related chunks and distant unrelated chunks  
  _Learner should notice:_ semantic similarity is based on vector proximity rather than exact word overlap
- **M01.L01** — LangChain RAG query chain — A flow diagram showing the incoming question splitting into two paths: one to the retriever and document formatter for context, and one passed through unchanged as the question; both enter the prompt, then the LLM, then the string output parser  
  _Learner should notice:_ the same user question drives retrieval and is also preserved as the question supplied to the LLM
- **M01.L01** — RAG-powered tutor and examiner — Course materials flowing through ingestion into a vector database, then an AI agent interacting with a student in two modes: tutor mode answering student questions and examiner mode asking and grading questions  
  _Learner should notice:_ both tutoring and assessment are grounded in the same approved course knowledge
- **M01.L01** — Retrieval-powered personalized advertising — User context such as current interests and prior purchases flowing alongside a searchable product knowledge base into retrieval, followed by an LLM generating a personalized advertisement  
  _Learner should notice:_ retrieval chooses relevant product information while generation adapts the message to the user\'s context
- **M01.L01** — Agentic RAG loop — An agent receiving a complex question, planning, calling retrieval as a tool, evaluating returned evidence, optionally reformulating the query and retrieving again, then producing a final response  
  _Learner should notice:_ the feedback loop and that retrieval can occur multiple times rather than only once
- **M01.L01** — Two multimodal RAG strategies — Side-by-side comparison: left converts images/tables/diagrams into text before retrieval and generation; right preserves original modalities, retrieves multimodal content, and sends it to a vision-language or multimodal LLM  
  _Learner should notice:_ the trade-off between normalizing everything into text and preserving the original modality
- **M01.L01** — Knowledge-graph-enhanced RAG — A small graph of entities connected by labeled relationships, with a query requiring two or more hops across the graph before evidence is supplied to an LLM  
  _Learner should notice:_ how explicit relationships help connect facts that may be scattered across different documents
- **M01.L02** — Base RAG stack overview — Two horizontal flows: ingestion ' 'as source data → parsing → chunking → embedding/indexing → vector ' 'database, and query as user query → query rewriting → embedding/search → ' 'reranking → prompt → generative LLM → answer  
  _Learner should notice:_ ' 'ingestion prepares knowledge ahead of time while the query flow runs for ' 'every request
- **M01.L02** — PDF visual layout versus logical text — A two-column PDF ' 'page represented as positioned text boxes, next to a correct and an ' 'incorrect extracted reading order  
  _Learner should notice:_ PDF ' 'coordinates do not automatically encode paragraph or column order
- **M01.L02** — Parser decision ladder — A decision flow starting with ' 'structured parser, then OCR for scanned text, then VLM/LLM fallback for ' 'complex high-value layouts, with validation after each stage  
  _Learner should notice:_ Learner ' 'should notice that generative parsing is a fallback capability rather than ' 'the automatic first choice
- **M01.L02** — Chunking strategies comparison — One paragraph shown under ' 'fixed-size, sentence/paragraph, recursive, document-structure, and ' 'semantic chunking with different boundary placements  
  _Learner should notice:_ ' 'notice how each strategy preserves a different kind of structure
- **M01.L02** — Embedding similarity heatmap — A 4×4 heatmap for happy, ' 'joyful, pessimistic, and not optimistic sentences, with the highest ' 'off-diagonal similarity between semantically related pairs  
  _Learner should notice:_ Learner ' 'should notice that geometric similarity tracks meaning more closely than ' 'word overlap
- **M01.L02** — HNSW hierarchy — A four-level graph from sparse landmark ' 'nodes at the top to dense local vectors at the bottom, with a query path ' 'descending toward a nearby vector  
  _Learner should notice:_ the ' 'coarse-to-fine search that avoids scanning every vector
- **M01.L02** — Metadata-filtered vector search — A large set of ' 'company-report vectors narrowed first by company and date metadata, then ' 'searched semantically  
  _Learner should notice:_ exact structured ' 'constraints and semantic similarity solve different parts of the retrieval ' 'problem
- **M01.L02** — End-to-end RAG failure propagation — A pipeline from ' 'parsing through chunking, embedding, retrieval, reranking, prompting, and ' 'generation with example failure labels under each stage  
  _Learner should notice:_ ' 'notice that a bad final answer may originate several stages before the ' 'LLM
- **M01.L03** — Enterprise RAG scaling map — Diagram showing data volume, ' 'query load, data complexity, retrieval quality, guardrails, and UX ' 'surrounding a central RAG pipeline  
  _Learner should notice:_ scale ' 'affects several interacting dimensions, not one component
- **M01.L03** — Distributed ingestion pipeline — Source documents fan out ' 'to parsing, cleaning, chunking, metadata extraction, embedding workers, ' 'then converge on vector and metadata stores with retries and observability ' '  
  _Learner should notice:_ parallel stages, checkpoints, and failure ' 'isolation
- **M01.L03** — Conditional document triage — Decision tree routing native ' 'PDFs, scanned PDFs, HTML, and malformed files through parser, OCR, ' 'boilerplate removal, or quarantine paths  
  _Learner should notice:_ ' 'different document qualities require different preprocessing
- **M01.L03** — Two-stage retrieval architecture — Large corpus narrowed ' 'by metadata and hybrid candidate generation, then cross-encoder reranking ' 'selects a small final context  
  _Learner should notice:_ stage 1 optimizes ' 'recall while stage 2 spends more compute on precision
- **M01.L03** — Hybrid retrieval fusion — Parallel semantic vector search ' 'and lexical BM25 search produce ranked lists that are fused before ' 'reranking  
  _Learner should notice:_ semantic meaning and exact-term ' 'evidence are complementary
- **M01.L03** — RAG trust boundaries — System instructions separated from ' 'user query and retrieved documents, with sanitization and output checks ' 'around the LLM  
  _Learner should notice:_ retrieved context is untrusted ' 'data and not an instruction source
- **M01.L03** — Hallucination detection and correction flow — Query goes ' 'through retrieval and generation, answer is checked for faithfulness, ' 'failing answers route to correction/regeneration/refusal, passing answers ' 'return to user  
  _Learner should notice:_ detection is a decision point, not ' 'the end of the pipeline
- **M01.L03** — Evidence-first RAG response UI — Answer with inline ' 'citations, expandable source passages, progress state, ' 'confidence/faithfulness signal, and feedback controls  
  _Learner should notice:_ ' 'notice how provenance and user controls are integrated into the answer ' 'experience
- **M01.L04** — POC-to-production RAG transition — A side-by-side diagram ' 'showing a small POC stack on the left and a distributed production stack ' 'with security, monitoring, scaling, staging, and CI/CD on the right  
  _Learner should notice:_ ' 'Learner should notice that production adds operational systems around the ' 'same core RAG logic
- **M01.L04** — RAG response-quality failure tree — Decision tree from a ' 'bad answer through data coverage, retrieval, generation faithfulness, and ' 'prompt design  
  _Learner should notice:_ the recommended debugging order and ' 'that not every bad answer is an LLM problem
- **M01.L04** — Fan-out/gather RAG query architecture — Diagram showing an ' 'orchestrator calling semantic and lexical search in parallel, gathering ' 'candidates, reranking, then calling the LLM  
  _Learner should notice:_ ' 'parallel independent work reduces additive latency
- **M01.L04** — Multi-level RAG caching — Layered diagram showing ' 'full-response, retrieval, and chunk caches around the orchestrator and ' 'retrieval services  
  _Learner should notice:_ each cache skips a ' 'different amount of downstream work
- **M01.L04** — RAG defense-in-depth security layers — Diagram showing ' 'ingestion security, encrypted data stores with RBAC, permission-filtered ' 'retrieval, protected LLM generation, and monitored output  
  _Learner should notice:_ ' 'notice that security constraints must persist across every ' 'transformation
- **M01.L04** — Cascading LLM router — Diagram showing a query router ' 'sending simple requests to a low-cost model and difficult requests to a ' 'more powerful expensive model, with both paths feeding monitoring  
  _Learner should notice:_ ' 'Learner should notice the quality-cost trade-off and the need to observe ' 'routing decisions
- **M01.L04** — Reference production RAG architecture — Full ingestion and ' 'query-flow diagram with extraction, chunking, embedding, vector and ' 'lexical search, reranking, masking, LLM generation, guardrails, caching, ' 'and security  
  _Learner should notice:_ the separation of services and ' 'parallel query paths
- **M01.L04** — Observability plane across RAG microservices — Production ' 'RAG pipeline with a horizontal logging-metrics-tracing layer connected to ' 'every service  
  _Learner should notice:_ observability is cross-cutting ' 'rather than a separate final component
- **M01.L04** — Continuous RAG production lifecycle — Circular lifecycle ' 'showing plan, test, deploy, monitor, learn, and upgrade, with data hygiene ' 'and evaluation surrounding the loop  
  _Learner should notice:_ ' 'production RAG is continuously maintained and improved
- **M01.L05** — DIY RAG versus RAG platform — Show an application ' 'connected either to many individually managed RAG components or to one ' 'standardized platform API backed by managed components  
  _Learner should notice:_ Notice that the ' 'main difference is ownership of infrastructure complexity, not the ' 'disappearance of the RAG stages
- **M01.L05** — RAG platform control plane — Put security, accuracy, cost, ' 'performance, governance and observability in a central platform layer ' 'serving several RAG applications  
  _Learner should notice:_ Notice that policy and infrastructure ' 'can be standardized while applications remain different
- **M01.L05** — RAG sprawl versus centralized platform — Left side shows ' 'departments each running their own vector DB, embedding model, LLM and ' 'ingestion pipeline; right side shows the same departments sharing a ' 'governed platform  
  _Learner should notice:_ Notice duplicated infrastructure and inconsistent ' 'controls on the sprawl side
- **M01.L05** — SaaS VPC on-premises responsibility spectrum — Show three ' 'deployment columns with increasing customer responsibility and increasing ' 'control from SaaS to VPC to on-premises  
  _Learner should notice:_ Notice that greater control also ' 'transfers more infrastructure and operations back to the customer
- **M01.L05** — Corpus configuration anatomy — Show corpus name/key, ' 'embedding model, document content and filter attributes feeding a ' 'searchable corpus  
  _Learner should notice:_ Notice that metadata and embedding configuration are ' 'designed before large-scale ingestion
- **M01.L05** — One query API expanding into the RAG query pipeline — Show ' 'a single client request expanding inside the platform into hybrid search, ' 'context expansion, reranking, generation and factual-consistency scoring  
  _Learner should notice:_ ' 'Notice that the API hides orchestration while preserving configurable ' 'controls
- **M01.L06** — RAG evaluation layers — Show ingestion → retrieval → ' 'generation → user/system outcomes with metrics attached to each layer  
  _Learner should notice:_ ' 'Notice that final answer quality is downstream of multiple independently ' 'measurable stages
- **M01.L06** — Generation failure map — Show retrieved context feeding an ' 'LLM, with branches for hallucination, ignored evidence, and off-target ' 'answer  
  _Learner should notice:_ Notice that all three failures can occur even when retrieval ' 'itself is correct
- **M01.L06** — Precision recall trade-off in RAG — Show top-k retrieval ' 'expanding from a small clean set to a larger noisier set, with recall ' 'rising and precision potentially falling  
  _Learner should notice:_ Notice that selecting k changes ' 'both context completeness and context noise
- **M01.L06** — MRR MAP and nDCG comparison — Show the same ranked list ' 'annotated with how MRR looks only at the first relevant result, MAP ' 'rewards every relevant position, and nDCG additionally uses graded ' 'relevance  
  _Learner should notice:_ Notice that the metrics answer different ranking questions
- **M01.L06** — UMBRELA scoring workflow — Show query + retrieved chunk → ' 'LLM judge → 0/1/2/3 relevance score for each candidate  
  _Learner should notice:_ Notice that no ' 'human-labeled golden chunk is required for the returned candidates
- **M01.L06** — AutoNuggetizer concept — Show retrieved evidence ' 'decomposed into vital and optional nuggets, then compare the generated ' 'answer against each nugget for coverage  
  _Learner should notice:_ Notice that this evaluates ' 'completeness of evidence use rather than only hallucination
- **M01.L06** — Offline and online evaluation flywheel — Show offline ' 'benchmark and CI gate feeding production, production sampled ' 'asynchronously, failures and user feedback returning to the benchmark  
  _Learner should notice:_ ' 'Notice how real-world failures continuously improve the offline test ' 'set
- **M01.L06** — RAG evaluation dashboard — Show five groups for ingestion, ' 'retrieval, generation, user outcomes, and system health with ' 'representative metrics  
  _Learner should notice:_ Notice that model quality and operational quality ' 'are monitored together
- **M01.L07** — AI agent evolution timeline — A timeline from Actor Model ' 'and BDI agents through voice assistants, ReAct, tool calling, and modern ' 'LLM agents.  
  _Learner should notice:_ Autonomy predates LLMs; LLMs mainly change flexibility, ' 'language understanding, and planning.
- **M01.L07** — The agentic stack — Three layers: reasoning LLM, ' 'orchestration, and tools/external systems, with tool calls downward and ' 'observations upward.  
  _Learner should notice:_ The LLM requests actions; orchestration executes ' 'them.
- **M01.L07** — Orchestrator-worker pattern — A central orchestrator ' 'assigns isolated subtasks to several specialist workers and combines their ' 'outputs.  
  _Learner should notice:_ Centralized coordination improves predictability while ' 'preserving specialization.
- **M01.L07** — The agentic loop — A cycle of Observation -> Reasoning & ' 'Planning -> Action -> new Observation, with a termination path to Final ' 'Answer.  
  _Learner should notice:_ Each action changes the state that the next decision sees.
- **M01.L07** — MCP overview — An AI application connects through MCP ' 'clients to standardized servers that expose tools and data.  
  _Learner should notice:_ MCP ' 'decouples agents from implementation-specific APIs.
- **M01.L07** — MCP host-client-server architecture — Show an agent host ' 'containing MCP clients connected to several MCP servers, each wrapping a ' 'tool or data source.  
  _Learner should notice:_ The client speaks MCP; each server adapts MCP ' 'requests to an underlying capability.
- **M01.L07** — MCP and A2A together — Show agents communicating ' 'horizontally through A2A while each agent accesses tools vertically ' 'through MCP.  
  _Learner should notice:_ MCP connects agents to capabilities; A2A connects agents to ' 'other agents.
- **M01.L07** — Agent memory architecture — Show short-term session memory ' 'and long-term semantic memory both feeding the active agent context.  
  _Learner should notice:_ ' 'Short-term memory preserves the current task; long-term memory retrieves ' 'reusable historical facts.
- **M01.L07** — Agent execution trace — A hierarchical trace showing user ' 'request, LLM decisions, tool-call spans, tool outputs, retries, and final ' 'response with timings.  
  _Learner should notice:_ The trace exposes hidden inefficiency and the ' 'first failing step.
- **M01.L08** — Conversion vs native multimodal RAG — Side-by-side ' 'architecture showing non-text data converted to text/JSON versus raw ' 'multimodal embeddings/VLM path  
  _Learner should notice:_ Notice where information is transformed ' 'and where expensive multimodal reasoning occurs
- **M01.L08** — Table extraction pipeline — Document page -> table ' 'detection/grid recovery -> cell OCR/semantic roles -> normalized ' 'dataframe/JSON  
  _Learner should notice:_ Notice that structure must be recovered before values are ' 'interpreted
- **M01.L08** — Table-aware RAG flow — Table summary embedded for ' 'retrieval, pointer to full dataframe/JSON, full table loaded for ' 'generation  
  _Learner should notice:_ Notice retrieval representation differs from generation ' 'representation
- **M01.L08** — Image summarization vs multimodal retrieval — ' 'Caption-based text retrieval path beside raw-image/shared-embedding path  
  _Learner should notice:_ ' 'Compare ingestion cost, query cost, and retained visual detail
- **M01.L08** — Shared text-image embedding space — Text encoder and image ' 'encoder mapping matched concepts into nearby vectors  
  _Learner should notice:_ Notice that ' 'different modalities become directly comparable
- **M01.L08** — Multimedia RAG timeline — Audio waveform/video track -> ' 'ASR + diarization + timestamps + frame/segment extraction -> indexed ' 'evidence  
  _Learner should notice:_ Notice provenance is preserved through timecodes
- **M01.L08** — The red-button problem — Video frame showing technician ' "pressing a red emergency stop while transcript says 'do this'  
  _Learner should notice:_ Notice why " 'transcript-only retrieval loses the referent
- **M01.L08** — Multimodal citation UI — Answer with links to table ' 'cell/page, image thumbnail, and audio/video timestamp  
  _Learner should notice:_ Notice how every ' 'claim can be inspected at its original source
- **M01.L08** — Production multimodal RAG architecture — Modality router ' 'feeding text, table, image, ASR/video processors into stores, retrieval, ' 'generator, citations, evaluation  
  _Learner should notice:_ Notice separate modality processing but ' 'shared query orchestration
- **M01.L09** — Example movie knowledge graph — Show Person and Movie ' 'nodes connected by DIRECTED and ACTED_IN edges  
  _Learner should notice:_ ' 'typed nodes, typed edges, and direction
- **M01.L09** — Chunk enrichment workflow — Show vector retrieval ' 'returning a chunk, graph lookup adding entity metadata, then enriched ' 'context entering the LLM  
  _Learner should notice:_ vector search finds the ' 'text while the graph supplies missing facts
- **M01.L09** — Hybrid graph retrieval workflow — Show natural-language ' 'query branching into vector search and text-to-Cypher graph search, then ' 'merging evidence  
  _Learner should notice:_ the graph acts as a parallel ' 'retrieval channel
- **M01.L09** — Entity linking and canonicalization — Show several aliases ' 'such as IBM, I.B.M., and International Business Machines converging into ' 'one canonical node  
  _Learner should notice:_ deduplication preserves ' 'one real-world identity
- **M01.L09** — Microsoft GraphRAG overview — Show source documents ' 'becoming an entity graph, graph communities, hierarchical community ' 'summaries, and query-focused summarization  
  _Learner should notice:_ the ' 'difference between local chunks and global summaries
- **M01.L09** — GraphRAG local versus global search — Contrast seed-node ' 'neighborhood expansion with top-down search over community summaries  
  _Learner should notice:_ ' 'Learner should notice that query scope determines the search strategy
- **M01.L09** — Graph database deployment choices — Compare self-managed ' 'cluster, managed cloud graph service, and embedded graph library  
  _Learner should notice:_ Learner ' 'should notice the trade-off between control and operational burden
- **M01.L09** — Living graph update pipeline — Show CDC from databases and ' 'event-driven processing from document storage both feeding incremental ' 'graph MERGE/DELETE operations  
  _Learner should notice:_ freshness is ' 'maintained incrementally rather than by full rebuilds
- **M01.L09** — Knowledge-Enhanced RAG production architecture — Show ' 'ingestion into vector and graph stores, query routing, vector retrieval, ' 'graph enrichment/hybrid graph retrieval, evidence merge, reranking, and ' 'LLM generation  
  _Learner should notice:_ the graph is an additional ' 'evidence channel, not a replacement for the RAG stack
- **M01.L10** — Late-interaction retrieval — Compare one-vector-per-chunk ' 'dense retrieval with token-level document vectors matched to query tokens ' 'at query time  
  _Learner should notice:_ accuracy versus storage/memory ' 'trade-off
- **M01.L10** — One-shot RAG versus agentic RAG — Side-by-side flow: ' 'retrieve once→generate versus plan→retrieve/tool→observe→retry→answer  
  _Learner should notice:_ ' 'Learner should notice iterative control and bounded loops
- **M01.L10** — Federated retrieval architecture — Agent/orchestrator ' 'querying data warehouse, enterprise search, legal vault, and operational ' 'DB in place, with provenance returning to one answer  
  _Learner should notice:_ ' 'notice data stays in native governed systems
- **M01.L10** — RAG as enterprise attention mechanism — Large enterprise ' 'dataset filtered into a compact high-value context window for the LLM  
  _Learner should notice:_ ' 'Learner should notice retrieval allocates scarce model attention
- **M01.L10** — Proactive RAG workspace — Support agent screen with ticket ' 'context automatically triggering retrieval of schematics and similar ' 'resolved tickets into a sidebar  
  _Learner should notice:_ intent is inferred ' 'from current work context
- **M01.L10** — Local-first edge RAG — Secure enterprise boundary ' 'containing vector store, retrieval services, and local SLM, contrasted ' 'with external API architecture  
  _Learner should notice:_ the reasoning ' 'engine moves to the data
- **M01.L10** — RAG chain of provenance — Trace linking user query, prompt ' 'version, retrieved document IDs/versions, model version, generated answer, ' 'and citations into an immutable audit record  
  _Learner should notice:_ ' 'reproducibility and accountability
- **M01.L10** — Future RAG reference architecture — Show query/context ' 'router branching to standard retrieval, late-interaction/multimodal ' 'retrieval, graph retrieval, federated tools, and agentic loop; feed ' 'selected context to local or hosted LLM under governance/evaluation ' 'controls  
  _Learner should notice:_ selective sophistication rather than one ' 'monolithic pipeline

## COURSE-010-AI-Service-Engineering-with-FastAPI — 86 images

- **M01.L01** — Generative model training and sampling — A simple two-stage diagram showing a butterfly-image dataset flowing into model training, followed by a trained model being sampled to produce several new butterfly images with visible variation  
  _Learner should notice:_ the separation between training and inference and that generated outputs are related to, but not identical to, the training examples
- **M01.L01** — VAE latent-space concept — A diagram showing several high-dimensional inputs being encoded into points or clusters in a compact 2D latent-space illustration, with selected latent points decoded into reconstructed or newly generated outputs  
  _Learner should notice:_ the latent space is a compressed learned representation and that new outputs can be produced by sampling points within it
- **M01.L01** — Hard-to-visualize generated scene — A surreal biomechanical forest containing metallic roots, glowing leaves, gears, digital displays, crystalline ground, organic veins, and a shifting luminous sky, matching the chapter's example concept without requiring exact reproduction of the source figure  
  _Learner should notice:_ how text-to-image generation can make an abstract or difficult-to-visualize description concrete enough to discuss and refine
- **M01.L01** — Generative AI service architecture — A system diagram with a client sending a request to a FastAPI web server; inside the server show routing, authentication/authorization, context retrieval, model access, validation/guardrails, and tool execution; connect the service to databases, external APIs, and other data sources  
  _Learner should notice:_ the model is only one component and that the server controls access, enriches context, validates outputs, and routes responses
- **M01.L02** — FastAPI Swagger UI — A screenshot or recreated local development view of a FastAPI `/docs` page showing at least two endpoints, their HTTP methods, parameters, and the interactive 'Try it out' workflow  
  _Learner should notice:_ endpoint documentation and interactive testing are generated from the API definitions rather than being written manually
- **M01.L02** — FastAPI hierarchical dependency graph — A dependency graph in which `get_db` feeds `get_current_user`, which feeds an authorization dependency, which then feeds multiple route handlers; show that the same lower-level dependency can be reused  
  _Learner should notice:_ dependencies can depend on other dependencies and that reusable results flow upward toward controllers
- **M01.L02** — Onion/layered FastAPI architecture — A concentric onion diagram with domain/business logic near the center and progressively outer layers for repositories/data adapters, services/providers, controllers, and API routers; include arrows or annotations showing dependencies directed inward  
  _Learner should notice:_ each layer has a distinct responsibility and that higher-level logic should not be tightly coupled to low-level implementation details
- **M01.L03** — RNN versus transformer sequence processing — Side-by-side diagram: an RNN processing tokens sequentially through a carried state vector, and a transformer processing the whole sequence with attention connections between distant tokens  
  _Learner should notice:_ RNN information flows step-by-step while transformer attention can directly represent long-range token relationships
- **M01.L03** — Multi-head attention map — A sentence with several words connected by weighted lines in multiple small attention-head panels; line thickness should represent stronger or weaker learned relationships  
  _Learner should notice:_ different heads can focus on different contextual relationships within the same sequence
- **M01.L03** — Tokenization to embeddings — A pipeline showing a sentence split into tokens, tokens mapped to integer IDs, and each ID mapped to a multi-dimensional floating-point embedding vector; optionally show a small 2D embedding plot with semantically related tokens closer together  
  _Learner should notice:_ the transformation from human-readable language to numeric model representations
- **M01.L03** — FastAPI plus Streamlit prototype architecture — A diagram showing browser user → Streamlit client → FastAPI `/generate/text` endpoint → local model → response back through FastAPI → Streamlit chat display  
  _Learner should notice:_ Streamlit is the client/UI while FastAPI remains the backend service
- **M01.L03** — Text-to-audio synthesis pipeline — A four-stage diagram showing text entering a semantic model, then coarse acoustics, then fine acoustics, then an audio codec that produces a waveform  
  _Learner should notice:_ audio generation is a pipeline of representations rather than a single direct text-to-file conversion
- **M01.L03** — Stable Diffusion training and inference — A two-part diagram: forward process gradually corrupting/encoding an image toward noise, and reverse inference process starting from noisy latent representation and iteratively denoising it while conditioned by a text prompt  
  _Learner should notice:_ generation uses iterative denoising controlled by prompt information
- **M01.L03** — Vertices, edges, and faces in a 3D mesh — A simple low-poly 3D object with individual vertices marked as points, selected edges highlighted as line segments, and one or two polygon faces filled or shaded  
  _Learner should notice:_ how points connect into edges and edges form surface polygons
- **M01.L03** — Three GenAI model-serving strategies — Three side-by-side diagrams showing (1) model load per request, (2) one model preloaded at application startup and reused by requests, and (3) FastAPI calling an external model server/provider  
  _Learner should notice:_ compare flexibility, memory use, latency, and infrastructure separation across the three strategies
- **M01.L03** — Monitoring middleware request lifecycle — Diagram showing client request entering monitoring middleware, passing to a model-serving route, returning through the same middleware where duration/status/request ID are captured, then going back to the client  
  _Learner should notice:_ one middleware layer can monitor many endpoints consistently
- **M01.L04** — Static type error in an IDE — A Python editor showing a function annotated to accept an integer timestamp and an incorrect call passing a string, with the type checker highlighting the argument mismatch  
  _Learner should notice:_ the problem is surfaced before the code is run in production
- **M01.L04** — Dictionary to dataclass refactor — Side-by-side illustration showing several loose function parameters or dictionary fields being grouped into a typed `Message` dataclass passed as one object  
  _Learner should notice:_ related values become one explicit data contract
- **M01.L04** — FastAPI request validation boundary — A client sending a request body through a Pydantic request model; valid input continues to the route while invalid input branches to a structured validation error response  
  _Learner should notice:_ malformed data is rejected before normal business/model logic runs
- **M01.L04** — Pydantic Settings configuration flow — Diagram showing `.env` / deployment environment variables flowing into an `AppSettings` model, where URL/secret/type validation occurs, then validated settings being supplied to the FastAPI application  
  _Learner should notice:_ configuration is validated at startup rather than read as arbitrary strings everywhere
- **M01.L04** — Typed FastAPI Swagger schema — A FastAPI Swagger/OpenAPI page showing a POST `/generate/text` request schema with model, prompt, and temperature fields plus a structured response model  
  _Learner should notice:_ the typed Pydantic contract becomes visible to API consumers automatically
- **M01.L05** — Concurrency versus parallelism timeline — Three horizontal diagrams showing sequential execution, concurrent interleaved execution on one worker, and parallel execution on several workers/cores  
  _Learner should notice:_ concurrency overlaps progress while parallelism executes work simultaneously on separate compute resources
- **M01.L05** — AsyncIO event loop scheduling — Diagram showing an event loop scheduling three coroutines; one awaits a network request, another awaits file I/O, while a third runs, then the first two resume when their events complete  
  _Learner should notice:_ coroutines pause and resume without losing state
- **M01.L05** — FastAPI event loop versus thread pool — Two-path diagram: async nonblocking handler running on the event loop and sync handler delegated to a thread-pool worker; add a warning path showing a blocking sync call inside an async handler freezing the event loop  
  _Learner should notice:_ `async def` requires nonblocking dependencies
- **M01.L05** — End-to-end RAG pipeline — Diagram showing document upload → text extraction → chunking/cleaning → embeddings → vector database, then user query → query embedding → semantic search → retrieved text chunks → augmented prompt → LLM answer  
  _Learner should notice:_ the separate ingestion path and query-time retrieval path
- **M01.L05** — FastAPI plus external vLLM architecture — Diagram showing users → main FastAPI application for validation/RAG/business logic → asynchronous HTTP call → vLLM inference server → multiple GPU resources → response back to FastAPI  
  _Learner should notice:_ model inference no longer blocks the application server process
- **M01.L05** — Static versus continuous batching — Side-by-side time-grid diagrams showing a fixed static batch with idle white slots after shorter sequences finish versus a continuous batch where new requests immediately replace completed sequences  
  _Learner should notice:_ how continuous batching reduces idle GPU capacity
- **M01.L05** — Paged attention memory mapping — Diagram showing a logical KV-cache sequence divided into blocks, a block table mapping those logical blocks to noncontiguous physical GPU-memory pages, and only required pages being accessed during attention  
  _Learner should notice:_ the analogy to virtual memory and the reduction of contiguous-memory waste
- **M01.L06** — Traditional response versus streaming AI response — Side-by-side timeline showing a normal HTTP request where nothing appears until full completion, versus a streaming request where partial text chunks arrive throughout model generation  
  _Learner should notice:_ streaming improves time-to-first-visible-output without necessarily reducing total generation time
- **M01.L06** — Short polling lifecycle — Timeline showing a client sending repeated GET status requests every few seconds, with several `pending` responses followed by one `completed` response  
  _Learner should notice:_ the repeated request overhead even when nothing has changed
- **M01.L06** — SSE connection — Diagram showing one initial client HTTP connection to a server, followed by many server-to-client events over the same persistent connection; arrows after the handshake should point only from server to client  
  _Learner should notice:_ SSE is persistent but unidirectional
- **M01.L06** — SSE versus WebSocket — Side-by-side persistent connections: SSE with only server-to-client event arrows and WebSocket with arrows in both directions  
  _Learner should notice:_ directionality is the central architectural difference
- **M01.L06** — WebSocket lifecycle — State diagram showing CONNECTING → OPEN → CLOSING → CLOSED, with handshake on entry to OPEN and close-frame exchange during CLOSING  
  _Learner should notice:_ a WebSocket is a managed long-lived connection with explicit lifecycle states
- **M01.L07** — Database system hierarchy — Diagram showing database server → database → schema → table/collection → rows/documents, with SQL and NoSQL branches  
  _Learner should notice:_ different database products still share a broad hierarchy of server, logical databases, structures, and records
- **M01.L07** — Multi-database GenAI architecture — Diagram showing a GenAI/RAG application connected to PostgreSQL for users/conversations, a vector database for embeddings, a graph database for document relationships, Redis for caching, and a document database for flexible prompt templates  
  _Learner should notice:_ database choice is per problem rather than one database replacing every other type
- **M01.L07** — Conversation-message relational schema — Simple ER diagram showing `conversations` with primary key `id`, and `messages` with primary key `id` plus foreign key `conversation_id`; draw a one-to-many relationship and note cascade delete  
  _Learner should notice:_ how relational modeling connects conversation history
- **M01.L07** — Repository pattern in layered architecture — Diagram showing FastAPI router/controller → service → repository → SQLAlchemy → PostgreSQL, with Pydantic schemas at the API boundary  
  _Learner should notice:_ database access is isolated from HTTP and higher-level business logic
- **M01.L07** — Code and database migration history — Parallel timelines showing Git commits for application code and Alembic revisions for database schema; arrows should show application versions aligning with schema versions across development/staging/production  
  _Learner should notice:_ schema evolution is versioned and deployed deliberately
- **M01.L08** — Authentication versus authorization — Two-stage access diagram showing a user first proving identity, then passing a second permission check for a resource/action  
  _Learner should notice:_ knowing who the user is does not automatically grant access
- **M01.L08** — Authentication methods overview — Four-column diagram for Basic credentials, token/JWT, OAuth identity provider, and public/private-key authentication, each showing the client and server interaction at a high level  
  _Learner should notice:_ recognize that authentication mechanisms prove identity in different ways
- **M01.L08** — JWT anatomy — Diagram showing a JWT split into header, payload, and signature, with example claims such as user ID, role, issuer, and expiration  
  _Learner should notice:_ Base64-style encoding makes token parts compact/readable but the signature is what protects integrity
- **M01.L08** — User-token entity relationship — ER diagram showing users → tokens as a one-to-many relationship, with user role/hashed password and token expiry/active state highlighted  
  _Learner should notice:_ token records make revocation and session tracking possible
- **M01.L08** — Password hashing and salting — Registration path showing password + random salt → password-hash algorithm → stored salted hash, and login path showing candidate password verified against the stored hash  
  _Learner should notice:_ the plain password is never stored and that the salt makes identical passwords produce different hash records
- **M01.L08** — JWT lifecycle — Flow showing login → issue signed short-lived JWT → client sends Bearer token → server verifies signature/claims and active token record → allow request; separate branches for expiry and logout/revocation  
  _Learner should notice:_ token issuance is only the start of the lifecycle
- **M01.L08** — OAuth2 authorization code flow — Sequence diagram showing user/browser → GenAI app → identity provider login/consent → redirect callback with authorization code → backend exchanges code for token → backend calls provider resource API  
  _Learner should notice:_ the user's provider password stays with the identity provider
- **M01.L08** — OAuth state/CSRF protection — Two OAuth callback paths: legitimate flow where stored state matches returned state and proceeds, and attacker/forged flow where state mismatches and is rejected  
  _Learner should notice:_ state binds the callback to the original login attempt
- **M01.L08** — Actor-action-resource authorization decision — Diagram showing user/actor + requested action + resource + policy data entering an authorization decision box and producing ALLOW or DENY  
  _Learner should notice:_ authorization is a separate decision function after authentication
- **M01.L08** — RBAC for GenAI models — Diagram showing authenticated USER and ADMIN roles flowing through an authorization guard; USER can access text generation while ADMIN can access text and image/premium models  
  _Learner should notice:_ model access is enforced in application logic
- **M01.L08** — ReBAC hierarchy — Graph showing a user connected as member of a team, team linked to a private folder, and folder containing conversations/threads; permission inheritance flows through relationships  
  _Learner should notice:_ access can come from relationships rather than one global role
- **M01.L08** — ABAC GenAI policy — Policy diagram showing attributes such as `user.plan=paid`, `resource.is_public`, and `upload.has_pii` being evaluated to allow or deny premium-model/document actions  
  _Learner should notice:_ policies can be dynamic and context-sensitive
- **M01.L08** — Hybrid authorization model — Diagram combining three policy inputs—role, relationship, and attributes—into one authorization decision; examples include ADMIN role, team membership, and public-resource attribute  
  _Learner should notice:_ how multiple policy models can participate in one decision
- **M01.L09** — GenAI attack surface — A defensive architecture diagram showing user inputs, external documents, model, tools/plugins, downstream systems, and stored sensitive data, with risk markers at prompt injection, malicious external content, unsafe output handling, excessive tool permissions, and resource exhaustion  
  _Learner should notice:_ GenAI security spans inputs, model behavior, outputs, integrations, and infrastructure
- **M01.L09** — GenAI service with input and output guardrails — Side-by-side comparison of a plain user → LLM → output pipeline and a protected user → input guardrails → LLM → output guardrails → user/downstream system pipeline  
  _Learner should notice:_ validation happens on both sides of the model
- **M01.L09** — Guardrail threshold trade-off — A horizontal score scale from low to high with a movable threshold; mark false-positive region on one side and false-negative risk on the other  
  _Learner should notice:_ threshold selection trades user friction against safety/abuse risk
- **M01.L09** — Rate limiting versus throttling — Side-by-side diagram where rate limiting rejects requests after a quota is reached, while throttling lets traffic continue but slows processing/transmission  
  _Learner should notice:_ rate limiting controls admission while throttling controls pace
- **M01.L09** — Four rate-limiting algorithms — Four compact diagrams: token bucket refilling tokens, leaky bucket queue draining steadily, fixed-window counter per time box, and sliding-window rolling timeline  
  _Learner should notice:_ compare burst tolerance, smoothness, and state complexity
- **M01.L09** — Distributed rate limiting with Redis — Load balancer distributing requests to three FastAPI instances, all reading/writing the same Redis rate-limit counters  
  _Learner should notice:_ why per-process memory cannot enforce one global quota across replicas
- **M01.L10** — AI service optimization map — Diagram splitting optimization goals into performance (latency, throughput, memory, cost) and quality (reliability, structure, alignment), with techniques connected to each side: batching/caching/quantization and structured output/prompting/fine-tuning  
  _Learner should notice:_ each technique addresses a specific bottleneck rather than being a universal improvement
- **M01.L10** — Keyword versus semantic cache — Side-by-side flow: keyword cache compares exact text keys, semantic cache embeds queries and compares vectors; show two differently worded but equivalent questions missing exact cache yet hitting semantic cache  
  _Learner should notice:_ semantic caching uses meaning rather than exact wording
- **M01.L10** — Semantic cache in RAG — Diagram showing user query → embedding → semantic cache; cache hit returns documents directly, cache miss queries document vector store and stores retrieved documents in cache before prompt augmentation and LLM generation  
  _Learner should notice:_ this cache avoids repeated retrieval while preserving fresh generation
- **M01.L10** — Prompt/context caching — Diagram showing one large document/system prompt cached once, then several small user requests referencing the same cached context instead of reprocessing the entire prefix  
  _Learner should notice:_ the cached object is repeated input context/state, not the generated answer
- **M01.L10** — Model quantization pipeline — Flow showing FP32/high-precision model weights → calibration/scaling/quantization → lower-precision INT8/INT4 model → inference, with memory footprint decreasing along the path  
  _Learner should notice:_ quantization changes numeric representation rather than deleting model layers
- **M01.L10** — Precision ladder — Vertical ladder showing FP32 → FP16/BF16 → INT8 → INT4 → lower-bit formats, with memory decreasing downward and potential quantization error/quality risk increasing  
  _Learner should notice:_ the memory-versus-precision trade-off
- **M01.L10** — Free-form JSON versus schema-driven structured output — Side-by-side pipeline where prompt-only JSON can produce malformed text and parser failure, while schema-driven output produces validated fields matching a Pydantic model  
  _Learner should notice:_ why structured output improves downstream reliability
- **M01.L10** — Role-Context-Task prompt template — Three stacked blocks labeled Role, Context, Task feeding into the LLM, followed by a more precise output  
  _Learner should notice:_ clear role, relevant context, and explicit task jointly reduce ambiguity
- **M01.L10** — Agentic tool-calling loop — Diagram showing user → LLM → tool/function request → application validates/executes tool → observation returned to LLM → final answer, with an authorization/validation gate before execution  
  _Learner should notice:_ the model proposes actions while application code controls actual tool execution
- **M01.L11** — Unit integration and E2E boundaries — Three diagrams over one GenAI pipeline: unit boundary around one function, integration boundary around two interacting components, and E2E boundary around the full user workflow  
  _Learner should notice:_ test scope expands from isolated logic to complete workflows
- **M01.L11** — Verification and validation V-model — V-shaped diagram with requirements and design descending toward implementation on the left, then unit/integration/E2E verification ascending on the right  
  _Learner should notice:_ tests verify implementation while validation begins from having the correct requirements
- **M01.L11** — Testing strategies comparison — Three simplified diagrams comparing testing pyramid, trophy, and honeycomb distributions across static/unit/integration/E2E and other testing types  
  _Learner should notice:_ the chapter favors strong integration coverage for dependency-heavy GenAI services
- **M01.L11** — RAG pipeline with test boundaries — Diagram of file upload → loader → transform/chunk → embeddings/vector DB → retrieval → LLM answer, with colored boundary boxes showing unit, integration, behavioral, and E2E test scopes  
  _Learner should notice:_ one pipeline can be tested at several different boundaries
- **M01.L11** — Pytest yield fixture lifecycle — Timeline showing setup → yield fixture into test → assertions → teardown, with a database client created and later closed  
  _Learner should notice:_ cleanup is part of fixture ownership rather than being scattered across tests
- **M01.L11** — Five test doubles — Comparison diagram for fake, dummy, stub, spy, and mock, showing increasing emphasis from simplified replacement/data supply to recording and verifying interactions  
  _Learner should notice:_ all isolate dependencies but differ in behavior and verification purpose
- **M01.L11** — RAG precision and recall sets — Venn-style diagram showing expected relevant documents and retrieved documents with overlap as true positives; annotate recall as overlap/expected and precision as overlap/retrieved  
  _Learner should notice:_ recall measures completeness while precision measures signal-to-noise
- **M01.L11** — Auto-evaluation testing loop — Diagram showing test prompt → model under test → candidate response → evaluator model → structured score → assertion threshold  
  _Learner should notice:_ evaluator-based tests add a second probabilistic model to the testing system
- **M01.L11** — Vertical versus horizontal E2E — Side-by-side RAG diagrams: vertical test moving through layers for one upload/storage feature, horizontal test following an entire user scenario from upload through question answering  
  _Learner should notice:_ vertical tests are feature-focused while horizontal tests follow broader user journeys
- **M01.L12** — Deployment options for a GenAI service — Four branches from one FastAPI/GenAI application to VM, serverless function, managed application platform, and container deployment  
  _Learner should notice:_ deployment choice depends on workload and operational requirements rather than one universal method
- **M01.L12** — VM architecture — Physical host hardware → hypervisor → multiple VMs, each with its own guest OS and application  
  _Learner should notice:_ each VM carries a full guest operating system and receives virtualized hardware resources
- **M01.L12** — Virtualization versus containerization — Side-by-side stacks: VMs each containing a guest OS above a hypervisor, versus containers sharing one host OS kernel above a container runtime  
  _Learner should notice:_ why containers are generally lighter than virtual machines
- **M01.L12** — Docker architecture — Docker client sends commands to Docker daemon; daemon builds/manages images, creates containers, manages networks/volumes, and communicates with a registry  
  _Learner should notice:_ the distinction between build artifact (image) and running instance (container)
- **M01.L12** — Docker layered filesystem — Stack showing base OS/Python layer, dependency layer, application-code layer, and a top writable container layer; several containers share immutable image layers  
  _Learner should notice:_ image layers are reusable while each running container gets its own ephemeral writable layer
- **M01.L12** — Docker storage mounts — Container connected to three storage types: Docker-managed volume on disk, bind-mounted host directory, and tmpfs in host RAM  
  _Learner should notice:_ the persistence and ownership model differs for each mount type
- **M01.L12** — Container networking mental model — Host containing FastAPI, PostgreSQL, Redis, and Qdrant containers connected through an internal Docker network; only FastAPI has a host-published port  
  _Learner should notice:_ internal service-to-service communication does not require publishing every database port
- **M01.L12** — User-defined bridge network with DNS — A `genai-net` bridge containing `server`, `db`, and `redis`; arrows use service names such as `db:5432` while unrelated containers sit outside the network  
  _Learner should notice:_ automatic name-based discovery and isolation
- **M01.L12** — Docker Compose GenAI stack — Compose-defined server and database containers connected to `genai-net`; DB uses a persistent volume, server exposes port 8000, and secrets/environment values enter the server  
  _Learner should notice:_ Compose describes the whole local stack declaratively
- **M01.L12** — Docker image optimization funnel — Large unoptimized image entering a funnel of minimal base image, externalized artifacts, cache/layer optimization, `.dockerignore`, and multi-stage build, producing a much smaller final production image  
  _Learner should notice:_ several independent techniques compound to reduce size and build time
- **M01.L12** — Multi-stage Docker build — Three stages labeled Base/Builder, Production, and Development; arrows show only selected artifacts copied from earlier stages into a small production image while dev tools remain in the development stage  
  _Learner should notice:_ build-time tooling does not need to ship in the final production image

## COURSE-011_Cloud_Deployment_and_CI_CD_for_AI_Engineers — 71 images

- **M08.L01** — AWS root versus IAM daily-access model — A diagram showing Root User protected with 2FA and used for account-level control, while an IAM developer user belongs to a developer group with scoped service policies  
  _Learner should notice:_ the separation between account ownership and routine development access
- **M08.L01** — EC2 security-group access model — A diagram showing a trusted developer IP or corporate VPN on the internet sending TCP traffic to EC2 only on ports 22, 8501, 8502, and 8504, while other sources are blocked  
  _Learner should notice:_ a security group filters traffic before it reaches the instance
- **M08.L02** — EC2 SSH connection anatomy — A diagram showing local computer + private PEM key → TCP 22 security-group rule → EC2 Elastic IP → Amazon Linux ec2-user shell  
  _Learner should notice:_ the separate roles of private key, network rule, public address, and Linux username
- **M08.L02** — Two SSH trust relationships — A split diagram showing Local Laptop → EC2 using the downloaded EC2 PEM key, and EC2 → GitHub using the EC2-generated ED25519 key whose public half is registered in GitHub  
  _Learner should notice:_ these are separate key pairs for separate connections
- **M08.L02** — First direct EC2 application access — A flow showing browser → EC2 Elastic IP:8501 → security group → Streamlit process running inside the Python virtual environment  
  _Learner should notice:_ this is direct instance exposure before the later load-balancer layer
- **M08.L03** — Network Load Balancer fronting EC2 — A diagram showing a trusted external client reaching an internet-facing AWS Network Load Balancer, which forwards through TCP target groups to the EC2 instance's private IP  
  _Learner should notice:_ the load balancer becomes the public gateway while EC2 is reached as a backend target
- **M08.L03** — Multi-port NLB target-group map — A central Network Load Balancer with four TCP listeners—22, 8501, 8502, 8504—each pointing to a correspondingly named target group that registers the same EC2 private IP on the matching port  
  _Learner should notice:_ one EC2 host can expose multiple backend services through separate listener/target-group pairs
- **M08.L03** — Streamlit request through NLB — A request-flow diagram from browser → load-balancer DNS:8501 → TCP listener → tg-8501 → EC2 private IP:8501 → Streamlit  
  _Learner should notice:_ the application process has not changed; the network entry path has
- **M08.L04** — Final domain and HTTPS architecture — A high-level flow showing Browser → custom domain DNS → AWS load-balancer layer → EC2 → Nginx TLS termination → Streamlit container  
  _Learner should notice:_ the custom domain identifies the service while Nginx presents the certificate and proxies to the application
- **M08.L04** — CSR and private-key relationship — A diagram showing OpenSSL generating `private.key` (keep secret) and `your_domain_csr.crt` (send to certificate provider), then the provider issuing a certificate that will later be paired with the private key in Nginx  
  _Learner should notice:_ the private key never needs to be sent to the certificate provider
- **M08.L04** — Nginx reverse proxy in Docker Compose — A diagram showing browser HTTPS traffic reaching an Nginx container with mounted certificate/private key, then Nginx forwarding internally to `streamlit_calc:8501` over the Compose network  
  _Learner should notice:_ Streamlit handles the application while Nginx handles TLS and proxying
- **M08.L05** — Chapter 5 multi-service architecture — A diagram showing Nginx with TLS in front of three Docker services: Streamlit on internal 8501, Flask on 8502, and Jenkins on 8080, with external secure ports 8501, 8502, and 8504  
  _Learner should notice:_ the external Jenkins port differs from the internal Jenkins port
- **M08.L05** — Jenkins persistent volume and UID/GID mapping — A diagram showing the EC2 host Jenkins directory owned for the shared group, mounted into `/var/jenkins_home`, with Docker Compose passing Jenkins UID and GID from `.env`  
  _Learner should notice:_ how host permissions and container identity must align
- **M08.L05** — Model training flow — A flow diagram showing synthetic data → DataFrame → 80/20 split → RandomForest training on training set → predictions on validation set → accuracy/precision/recall/classification report  
  _Learner should notice:_ the separation between model fitting and evaluation
- **M08.L05** — Authenticated ML API deployment — A flow showing client with credentials and JSON payload → HTTPS/Nginx → Flask authentication → deserialized Random Forest model → prediction score → JSON response  
  _Learner should notice:_ where authentication occurs relative to prediction logic
- **M08.L06** — Port-based URLs versus subdomain URLs — A before/after diagram. Before: one domain with :8501, :8502, :8504. After: streamlit.domain, flask.domain, jenkins.domain all entering through ports 80/443  
  _Learner should notice:_ service identity moves from the port number into the hostname
- **M08.L06** — Host-based Nginx routing — A diagram showing all external HTTPS traffic arriving on port 443, then Nginx selecting one of three upstreams based on hostname: streamlit → 8501, flask → 8502, jenkins → 8080  
  _Learner should notice:_ public port 443 is shared while internal service ports remain distinct
- **M08.L06** — SAN CSR structure — A diagram showing csr.conf with primary domain and three SAN subdomains feeding OpenSSL, producing private.key and a CSR whose SAN list is then verified  
  _Learner should notice:_ the certificate request explicitly names every hostname to be secured
- **M08.L06** — Jenkins URL mismatch — A before/after diagram showing Nginx/DNS routing to `jenkins.domain` while Jenkins still believes its URL is `domain:8504`, then showing both aligned after updating Jenkins Location  
  _Learner should notice:_ application-level URL configuration must match infrastructure routing
- **M08.L07** — AWS-to-GCP conceptual migration — A side-by-side diagram showing the same Streamlit/Flask/Jenkins/Nginx application stack, with AWS EC2/networking on the left and GCP Compute Engine/firewall/static IP on the right  
  _Learner should notice:_ the application architecture is preserved while cloud-specific infrastructure changes
- **M08.L07** — GCP VM bootstrap — A diagram showing Compute Engine VM creation → startup script → Python + Docker + Docker Compose + Git installation → Docker service enabled → version checks  
  _Learner should notice:_ the machine configuration is automated rather than repeated manually
- **M08.L07** — GCP Level 1 direct Streamlit access — A flow showing browser → GCP static IP:8501 → firewall rule targeting vm-network-tag → Compute Engine VM → Streamlit process  
  _Learner should notice:_ the similarity to the earlier direct EC2 deployment
- **M08.L07** — Three-level GCP deployment progression — A three-stage diagram: Level 1 static-IP Streamlit on 8501 → Level 2 full multi-service SSL stack on 8501/8502/8504 → Level 3 subdomains over 80/443  
  _Learner should notice:_ how the chapter grows complexity incrementally
- **M08.L08** — VM-to-image-to-replicas — A diagram showing a configured GCP VM disk being preserved, converted into a custom image, then reused to create multiple identical VM instances  
  _Learner should notice:_ the image becomes the reusable machine blueprint
- **M08.L08** — Managed instance group autoscaling — A graph/diagram showing one instance under normal load, utilization rising toward 80%, the managed instance group adding a second instance, and traffic being distributed across both  
  _Learner should notice:_ min/max boundaries and metric-driven scaling
- **M08.L08** — Global GCP load-balancing architecture — A world-scale diagram showing one global HTTPS load-balancer frontend with certificate, feeding a backend service connected to Europe and US managed instance groups, each containing autoscaled VMs and health checks  
  _Learner should notice:_ the separation between global frontend and regional backend capacity
- **M08.L08** — DNS shift from VM to global load balancer — A before/after diagram. Before: four A records point to one VM static IP. After: the same A records point to one global load-balancer IP, which distributes to Europe and US instance groups  
  _Learner should notice:_ DNS names remain stable while backend architecture becomes multi-region
- **M08.L09** — VM deployment versus serverless deployment — A side-by-side diagram showing VM deployment where the engineer manages OS, Docker, services, scaling, and application versus Cloud Run where the engineer provides a container and Google manages infrastructure and scaling  
  _Learner should notice:_ serverless removes infrastructure-management responsibility rather than eliminating physical servers
- **M08.L09** — Cloud Run build-and-deploy flow — A diagram showing local/uploaded source → Cloud Build → container registry → Cloud Run service → managed instances → service URL and metrics  
  _Learner should notice:_ image creation and service deployment are separate stages
- **M08.L09** — VM backend versus serverless NEG backend — A comparison showing Chapter 8 global load balancer → managed instance group → VMs, versus Chapter 9 load balancer → serverless NEG → Cloud Run service  
  _Learner should notice:_ the backend attachment object changes when moving from VMs to serverless
- **M08.L09** — Cloud Run global HTTPS routing — A diagram showing HTTPS frontend on port 443 → host rules → Flask backend service → flask-neg → flask-app and Streamlit backend service → streamlit-neg → streamlit-app  
  _Learner should notice:_ hostname routing selects separate serverless backends
- **M08.L09** — IAP versus Cloud Armor access models — A split diagram. Left: human browser → Google sign-in/IAP → backend. Right: trusted machine IP → Cloud Armor allow rule → backend, all other IPs → 403  
  _Learner should notice:_ authentication and IP allow-listing solve different access-control problems
- **M08.L10** — VM AWS stack versus Fargate stack — A before/after architecture. Before: EC2 + Docker Compose + Nginx + Flask + Streamlit + Jenkins. After: ALB → ECS Fargate Flask/Streamlit tasks, with ECR and CloudWatch around them  
  _Learner should notice:_ Fargate replaces server/container-host management while ALB replaces Nginx's public routing role
- **M08.L10** — ECR image publishing workflow — A diagram showing Flask and Streamlit source folders → local Docker builds → ECR authentication → separate ECR repositories → image URIs consumed by ECS task definitions  
  _Learner should notice:_ ECR is the handoff point between local build and Fargate runtime
- **M08.L10** — ALB and ECS security-group boundary — A diagram showing internet/trusted client → alb-sg → ALB → ecs-sg-tasks → Flask:5000 and Streamlit:8501 Fargate tasks, with direct internet-to-task traffic blocked  
  _Learner should notice:_ task security rules trust the ALB security group rather than public client IPs
- **M08.L10** — ALB host-based routing — A diagram showing one ALB listener with three rules: flask hostname → flask-tg, streamlit hostname → streamlit-tg, default/unmatched → fixed 403  
  _Learner should notice:_ the ALB replaces the earlier Nginx host-routing layer
- **M08.L10** — Fargate logging path — A diagram showing Flask/Streamlit Fargate task stdout/stderr → CloudWatch Logs → either CloudWatch log group UI or ECS service Logs tab  
  _Learner should notice:_ operational debugging no longer depends on SSH access to a host
- **M08.L10** — HTTPS ALB termination — A diagram showing browser HTTPS → ALB port 443 with ACM certificate → host rule → Flask or Streamlit target group → Fargate task over internal application port  
  _Learner should notice:_ TLS terminates at the ALB rather than inside the application container
- **M08.L10** — Fargate task autoscaling — A diagram showing one ECS service with task definition size fixed, task count increasing from 1 to multiple replicas as average CPU crosses a target, then shrinking within min/max bounds  
  _Learner should notice:_ the difference between per-task resources and number of tasks
- **M01.L01** — Breaking the wall of confusion — A before-and-after diagram. On the left, Development and Operations are separated by a wall and exchange a large risky release. On the right, Dev, Ops, QA, Security, and Product collaborate around one continuous delivery flow with shared feedback arrows  
  _Learner should notice:_ DevOps changes the organizational flow and ownership model, not merely the toolset
- **M01.L01** — DevOps infinity loop — An infinity-loop diagram containing the eight stages Plan, Code, Build, Test, Release, Deploy, Operate, and Monitor, with arrows showing continuous movement and monitoring feedback returning toward planning  
  _Learner should notice:_ the lifecycle is cyclic and overlapping rather than a one-way project sequence
- **M01.L01** — CI versus Continuous Delivery versus Continuous Deployment — Three horizontal pipelines. CI stops after a tested build artifact; Continuous Delivery continues through staging but shows a manual approval gate before production; Continuous Deployment continues automatically into production  
  _Learner should notice:_ the main distinction between Delivery and Deployment is the final production approval gate
- **M01.L01** — Cloud service model responsibility stack — A layered stack comparing on-premises, IaaS, PaaS, and SaaS across networking, storage, servers, virtualization, operating system, runtime, application, and data, clearly showing which layers are managed by the customer versus the provider  
  _Learner should notice:_ moving from IaaS to PaaS to SaaS trades direct control for less operational responsibility
- **M01.L01** — VS Code DevOps workspace anatomy — A screenshot-style diagram of VS Code with the Explorer, Search, Source Control, Run/Debug, Extensions icons, editor pane, and integrated terminal labeled  
  _Learner should notice:_ source files, Git workflow, extensions, and terminal commands can be managed from one workspace
- **M02.L01** — Git three-tree workflow — A diagram showing Working Directory → Staging Area → Local Repository, with `git add` on the first arrow and `git commit` on the second. Also show `git status` observing the working/staging state  
  _Learner should notice:_ editing a file is not the same as staging it, and staging it is not the same as committing it
- **M02.L01** — GitFlow branch model — A branching diagram showing long-lived `main` and `develop` branches, feature branches created from and merged into `develop`, release branches from `develop` merging into both `main` and `develop`, and hotfix branches from `main` merging back into both `main` and `develop`  
  _Learner should notice:_ each supporting branch type has a distinct purpose and merge path
- **M02.L01** — GitHub new-repository screen — A GitHub repository-creation page showing repository name, description, visibility choice, README initialization option, and create button  
  _Learner should notice:_ the minimum settings needed to initialize a repository before cloning it
- **M02.L01** — Pull request review page — A GitHub pull-request page showing base branch, compare branch, PR title/description, Files changed tab, reviewer area, automated check status, and merge area  
  _Learner should notice:_ a PR is a review and discussion workflow around a proposed branch merge
- **M02.L01** — Git merge-conflict markers — A code-editor view showing `<<<<<<< HEAD`, `=======`, and `>>>>>>> main`, with annotations identifying current change, incoming change, and the final manually resolved line  
  _Learner should notice:_ Git presents both competing versions and requires a human to decide the intended final content
- **M03.L01** — Containers versus virtual machines — A side-by-side architecture diagram. VM side: hardware/host, hypervisor, multiple guest OS layers, each with libraries and app. Container side: hardware/host OS, container engine, multiple containers sharing the host kernel, each with libraries and app  
  _Learner should notice:_ VMs repeat the guest operating system while containers share the host kernel
- **M03.L01** — Dockerfile to image to container — A three-stage flow: Dockerfile instructions → `docker build` → Docker image → `docker run` → running container, with one image branching to multiple containers  
  _Learner should notice:_ a Dockerfile builds an image and an image can create multiple containers
- **M03.L01** — Docker host-to-container port mapping — A network flow diagram showing Browser → localhost:4000 on host → Docker mapping → port 8080 inside container → Gunicorn/Flask  
  _Learner should notice:_ host port 4000 and container port 8080 are different endpoints connected by `-p 4000:8080`
- **M03.L01** — Build-run-push Docker workflow — A left-to-right diagram showing source + Dockerfile → docker build → local image → docker run → local container, with another arrow from local image → docker tag/docker push → Docker Hub registry → docker pull/run on another machine  
  _Learner should notice:_ the same versioned image artifact can move from local development to a registry and then to another environment
- **M04.L01** — Click-ops versus Infrastructure as Code — A side-by-side diagram. Left side shows a human manually clicking through cloud-console screens to create resources. Right side shows version-controlled Terraform files flowing through Terraform into cloud APIs to create the same resources  
  _Learner should notice:_ IaC turns manual infrastructure steps into repeatable, reviewable configuration
- **M04.L01** — Terraform code-state-cloud relationship — A three-part diagram showing HCL configuration on the left, `terraform.tfstate` in the middle as the mapping layer, and real AWS resources on the right  
  _Learner should notice:_ state connects Terraform resource addresses in code to real infrastructure objects
- **M04.L01** — Terraform init-plan-apply workflow — A flow diagram showing HCL files → `terraform init` downloads providers → `terraform plan` previews create/modify/destroy actions → human review → `terraform apply` → AWS resource and updated state  
  _Learner should notice:_ plan is the safety preview before apply changes real infrastructure
- **M04.L01** — Terraform variables and outputs — A diagram showing `terraform.tfvars` and input variables feeding into `main.tf`, Terraform creating an S3 bucket, then an output block exposing the bucket ARN  
  _Learner should notice:_ variables parameterize configuration while outputs expose useful resource attributes
- **M05.L01** — Continuous Integration feedback loop — A loop showing developer commit → push/pull request → CI runner → build → automated tests → pass/fail feedback returning immediately to the developer  
  _Learner should notice:_ CI's main value is fast feedback after small integrations
- **M05.L01** — CI, Continuous Delivery, Continuous Deployment pipeline — A horizontal pipeline showing Code → Build → Test as CI, then Release → Deploy → Operate, with a manual gate before production for Continuous Delivery and no manual gate for Continuous Deployment  
  _Learner should notice:_ Delivery and Deployment differ mainly at the final production release gate
- **M05.L01** — GitHub Actions hierarchy — A hierarchy diagram showing Event → Workflow → Jobs → Runner per job → ordered Steps, with some steps using reusable Actions and others executing shell commands  
  _Learner should notice:_ the difference between a workflow, job, step, action, and runner
- **M05.L01** — CD staging architecture — A system diagram showing GitHub push → GitHub Actions build-and-push job → Docker build → AWS ECR → image URI output → deploy job → Terraform → AWS App Runner staging service → service URL  
  _Learner should notice:_ how the Docker image URI becomes the bridge between the build job and Terraform deployment
- **M06.L01** — From Docker container to Kubernetes orchestration — A progression diagram showing one Docker container on a laptop, then many containers across multiple servers, followed by Kubernetes managing placement, health, networking, scaling, and updates  
  _Learner should notice:_ orchestration solves lifecycle and scale problems that appear after containerization
- **M06.L01** — Kubernetes cluster architecture — A diagram with the control plane at the top connected through the Kubernetes API to three worker Nodes below, each running Pods  
  _Learner should notice:_ the control plane manages desired state while Nodes run workloads
- **M06.L01** — Kubernetes reconciliation loop — A circular diagram showing desired state = 3 Pods, actual state = 2 Pods, controller detects difference, creates replacement Pod, actual state returns to 3  
  _Learner should notice:_ self-healing comes from continuous desired-vs-actual reconciliation
- **M06.L01** — Kubernetes Service traffic routing — A diagram showing Browser → NodePort → Service with stable DNS/IP → two Flask Pods labeled app=flask-app, with arrows from the Service load-balancing across both Pods  
  _Learner should notice:_ the Service is stable while Pods can be replaced
- **M06.L01** — Helm chart templating model — A diagram showing Helm Chart templates + values.yaml → Helm render/install → generated Deployment, Service, ConfigMap, and other Kubernetes resources → Kubernetes cluster  
  _Learner should notice:_ the same templates can be reused with different environment-specific values
- **M07.L01** — Monitoring versus observability — A side-by-side diagram. Monitoring side shows predefined dashboards watching CPU, memory, latency, and errors. Observability side shows an engineer starting with an unexpected symptom and exploring correlated logs, metrics, and traces to discover a root cause  
  _Learner should notice:_ monitoring answers predefined questions while observability supports exploratory investigation
- **M07.L01** — Distributed trace waterfall — A trace waterfall for one request showing Frontend, Auth Service, User Service, and Database spans with horizontal duration bars, where the Database span is dramatically longer than the others  
  _Learner should notice:_ traces reveal where one request spends its time across services
- **M07.L01** — ELK centralized logging pipeline — A diagram showing multiple application containers sending logs into Logstash, Logstash transforming and forwarding them to Elasticsearch, and Kibana querying Elasticsearch for search and dashboards  
  _Learner should notice:_ logs from many services converge into one searchable system
- **M07.L01** — Prometheus and Grafana metric flow — A diagram showing application /metrics endpoints being scraped by Prometheus, Prometheus storing time-series data, and Grafana querying Prometheus to build latency, error-rate, CPU, and memory dashboards  
  _Learner should notice:_ Prometheus collects/stores metrics while Grafana visualizes them
- **M07.L01** — End-to-end observability incident workflow — A flow showing Alert → Grafana metric spike → distributed trace bottleneck → Kibana log error → identified root cause → remediation → follow-up improvement  
  _Learner should notice:_ how different telemetry sources answer different parts of the same incident

## COURSE-012_AI_Agents_Foundations — 61 images

- **M01.L01** — Reactive LLM versus goal-directed agent — A side-by-side diagram. Left: User -> LLM -> Text response -> Stop. Right: User goal -> Agent -> Plan -> Tool actions -> Observe results -> Continue/finish  
  _Learner should notice:_ the agent has a continuing control loop instead of a single prompt-response interaction
- **M01.L01** — Assistant versus agent control boundary — Two flows. Assistant: user approval before each tool action. Agent: user gives a goal, agent plans and uses several tools, with explicit gates only around selected high-stakes actions  
  _Learner should notice:_ the main difference is where human approval enters the workflow, not whether tools exist
- **M01.L01** — Sense-plan-act-learn cycle — A circular four-stage diagram labeled Sense -> Plan -> Act -> Learn -> Sense, with small annotations: input/context, task decomposition, tool execution, result evaluation  
  _Learner should notice:_ Learn feeds the next cycle rather than ending the process
- **M01.L01** — Agent connected to an MCP server — Diagram showing Agent -> MCP server -> several reusable tools/services. Include a small discovery step labeled list_tools before tool execution  
  _Learner should notice:_ the integration boundary is standardized and reusable across agents
- **M01.L01** — Five functional layers of an AI agent — A layered or connected diagram containing Persona; Tools & Actions; Reasoning & Planning; Knowledge & Memory; Evaluation & Feedback. Use arrows to show interaction rather than a strict top-to-bottom pipeline  
  _Learner should notice:_ the layers organize capabilities but do not define a fixed runtime order
- **M01.L01** — Three multi-agent coordination patterns — One figure with three mini-diagrams: (1) Agent Flow as a left-to-right assembly line, (2) Orchestration as a central hub with worker spokes, and (3) Collaboration as peer agents connected to one another  
  _Learner should notice:_ be able to identify the control structure of each pattern at a glance
- **M01.L02** — LLM training versus inference — A two-part diagram. Left: training text -> tokenization -> prediction -> loss -> backpropagation -> updated weights. Right: prompt -> tokenization -> model -> next-token probabilities -> sampling -> generated token -> repeated generation  
  _Learner should notice:_ training changes model weights, while inference uses the already-trained weights to generate tokens
- **M01.L02** — Plain text versus JSON tokenization — Show the same semantic information written once as simple prose and once as JSON, with token boundaries highlighted so the JSON representation visibly contains more token pieces  
  _Learner should notice:_ formatting characters and field names also consume tokens
- **M01.L02** — Free-form output versus typed agent output — Top flow: Agent A -> variable prose -> parser risk -> Agent B. Bottom flow: Agent A -> strict schema -> validated object -> Agent B  
  _Learner should notice:_ typed output creates a stable contract between workflow steps
- **M01.L02** — Sequential tool chain versus parallel tool calls — Left: Tool A -> result -> Tool B -> result. Right: one agent step fans out to Tool A, Tool B, and Tool C simultaneously, then merges results  
  _Learner should notice:_ dependency determines whether calls must be sequential or can safely run in parallel
- **M01.L03** — Before MCP versus with MCP — Left: one agent connected to filesystem, database, web API, and SaaS service through four different custom connectors. Right: the agent connects through MCP to reusable servers that wrap those services  
  _Learner should notice:_ MCP standardizes the integration boundary rather than eliminating the underlying services
- **M01.L03** — MCP three-part architecture — A left-to-right diagram showing MCP client -> MCP server -> underlying service, with examples under the client such as agent/desktop/IDE and examples under the service such as filesystem/database/API  
  _Learner should notice:_ MCP sits between the AI application and the real external capability
- **M01.L03** — STDIO versus remote SSE connection — Left: Agent launches MCP server subprocess and communicates through stdin/stdout. Right: Agent connects over HTTP to a separately running MCP server  
  _Learner should notice:_ the difference in process ownership, networking, and sharing
- **M01.L03** — MCP Inspector workflow — A small debugging flow: MCP server -> Inspector -> list tools -> inspect schema -> run tool manually -> inspect raw response, followed by Agent integration only after success  
  _Learner should notice:_ server behavior should be verified independently before blaming the agent
- **M01.L03** — Internal tools versus MCP-separated tools — Left: Agent and record_event/load_journal functions inside one process sharing direct state. Right: Agent connects through MCP to a standalone Time Travel Tracker server that privately owns the journal implementation  
  _Learner should notice:_ the interface remains visible while implementation details become isolated
- **M01.L04** — Monolithic agent versus structured multi-agent system — Left: one overloaded agent with many tools and responsibilities. Right: several specialized agents connected through a clear flow, each with a small tool set  
  _Learner should notice:_ decomposition reduces responsibility per agent but adds coordination boundaries
- **M01.L04** — Four Cs of multi-agent architecture — A diagram with four labeled blocks: Decision-making, Control, Communication, Coordination. Under each, show one guiding question: Who decides? Who acts? What context moves? How does execution proceed?  
  _Learner should notice:_ use these four questions as an architecture checklist
- **M01.L04** — Multi-agent coordination strategies — A visual showing small diagrams for sequential, parallel, hierarchy, critique loop, router branching, and peer-to-peer network  
  _Learner should notice:_ these are execution shapes that can be composed, not competing frameworks
- **M01.L04** — Decomposing a monolithic research agent — Left: one agent attached to three MCP/tool groups: research, planning, filesystem. Right: Research Agent -> Planning Agent -> Filesystem Agent, with each agent attached only to its matching tools  
  _Learner should notice:_ how specialization shrinks each agent's tool and instruction surface
- **M01.L04** — Agent flow graph and trace relationship — Show a static graph Research -> Planning -> Filesystem beside a runtime timeline showing actual calls, tool use, latency, and a handoff event  
  _Learner should notice:_ a graph documents possible structure while a trace shows what actually happened
- **M01.L05** — Decomposition versus planning — Left: one large goal breaking into several subproblems. Right: the same subproblems connected by arrows showing order, dependencies, and parallel branches  
  _Learner should notice:_ decomposition defines the pieces while planning defines how the pieces fit together
- **M01.L05** — ReAct loop — A circular flow labeled Reason -> Act -> Observe -> Reason, with a branch after Observe to either continue or finish  
  _Learner should notice:_ tool output becomes new evidence for the next decision
- **M01.L05** — Tree-of-Thought search — A branching tree from one problem into three candidate paths, with scores on leaves, two branches crossed out as pruned, and one promising branch expanded further  
  _Learner should notice:_ ToT is search plus evaluation, not simply 'think more'
- **M01.L05** — Agent with Sequential Thinking scratchpad — Show Agent/LLM connected to a Sequential Thinking MCP server. The scratchpad contains Thought 1, Thought 2, revision of Thought 1, branch B, and status metadata. Also show ordinary action tools beside it  
  _Learner should notice:_ the MCP server stores structured reasoning state while the agent still makes decisions
- **M01.L06** — External storage versus bounded context — Show a large database/vector store containing many documents and memories on the left, a retrieval filter in the middle, and a small context window feeding an LLM on the right  
  _Learner should notice:_ retrieval selects a small relevant subset from a much larger store
- **M01.L06** — RAG ingestion and retrieval phases — Two-column diagram. Ingestion: Document -> Chunk -> Embedding Model -> Vector DB. Retrieval: Query -> Embedding -> Similarity Search -> Retrieved Chunks -> LLM -> Answer  
  _Learner should notice:_ clearly see that embedding and generation are separate operations
- **M01.L06** — Cosine similarity intuition — Draw two vector pairs from the same origin: one pair with a small angle labeled high similarity, and another with a large angle labeled low similarity  
  _Learner should notice:_ cosine comparison focuses on direction rather than vector length
- **M01.L06** — Semantic embedding clusters in 3D — A 3D scatter plot with visually grouped clusters such as sky/blue sentences, dog/fox sentences, and breakfast/food sentences  
  _Learner should notice:_ semantically related texts cluster near one another after dimensionality reduction
- **M01.L06** — Hybrid retrieval with Reciprocal Rank Fusion — Show keyword search producing ranked list A and vector search producing ranked list B, then an RRF fusion block merging them into one final ranked list  
  _Learner should notice:_ fusion combines rank positions from different scoring systems
- **M01.L06** — Graph memory example — Show entity nodes for a person, city, organization, and concept connected by labeled edges such as lives_in, works_at, knows, and prefers  
  _Learner should notice:_ graphs explicitly encode relationships rather than only semantic similarity
- **M01.L06** — Memory compression pipeline — Show many small memory cards entering semantic clusters, each cluster being summarized into one compact memory card, then stored back into a cleaner vector database  
  _Learner should notice:_ compression reduces redundancy by replacing clusters with summaries
- **M01.L07** — Agent evaluation feedback loop — Show an agent producing outputs, several evaluation sources around it (tests, human, grounding agent, critic), an evaluation store, and an arrow from the stored findings back to system improvement  
  _Learner should notice:_ evaluation creates an improvement loop rather than acting as a one-time test
- **M01.L07** — Independent evaluation versus colluding evaluation — Left: generator and evaluator share the same blind spot and both approve a wrong answer. Right: generator is checked by a differently configured evaluator plus periodic human review  
  _Learner should notice:_ multiple agents do not automatically equal independent evidence
- **M01.L07** — TDAD cycle — Circular diagram: Define benchmark -> Run agent multiple times -> Diagnose failure -> Make minimum prompt/tool/model change -> Regression test -> Refactor -> back to benchmark  
  _Learner should notice:_ stochastic testing requires repeated evaluation, not one passing run
- **M01.L07** — Grounding versus critic versus evaluator agent — Three side-by-side blocks: Grounding Agent checks Answer against Source Context; Critic Agent checks Generated Output against Rubric; Evaluation Agent checks Agent Response against Benchmark/Expected Behavior  
  _Learner should notice:_ be able to distinguish the question each evaluator answers
- **M01.L07** — Rubric evaluation matrix — A table-like visual with rows Accuracy, Grounding, Tool Use, Completeness, Error Handling and columns scores 1 through 5, with short descriptions for weak versus strong performance  
  _Learner should notice:_ rubrics make multiple quality dimensions explicit
- **M01.L07** — From trace annotation to regression dataset — Show Trace -> Reviewer annotation -> Stored labeled span -> Dataset -> New agent version -> Regression experiment  
  _Learner should notice:_ how one manual observation becomes reusable evaluation data
- **M01.L08** — Three agent consumption patterns — Show three side-by-side architectures: Browser/App with embedded agent; App -> API -> Backend Agent; App/Agent -> MCP/API/A2A -> Containerized Agent Service  
  _Learner should notice:_ agent placement changes the trust boundary and communication path
- **M01.L08** — Realtime browser agent security boundary — Show Browser Realtime Agent requesting an ephemeral credential from Backend Auth, then connecting to the realtime model. The permanent provider key remains only on the backend  
  _Learner should notice:_ the browser never receives the long-lived server credential
- **M01.L08** — Agent container anatomy — Show Host Machine -> Docker Container containing Python runtime, application code, dependencies, and Agent API, with port mapping to the host and secrets injected at runtime rather than baked into the image  
  _Learner should notice:_ what belongs inside the image versus what should be supplied at runtime
- **M01.L08** — Docker Compose multi-agent stack — Show Web/Realtime service connected to Image Agent and Web Search Agent containers, with each service in its own container and all managed by one Compose file  
  _Learner should notice:_ Compose coordinates deployment without merging the services into one process
- **M01.L08** — Front-door agent topology — Show User -> Front-Door Agent, then three downstream paths: immediate low-latency tool, synchronous API worker, and queued long-running worker. Include different latency labels on each path  
  _Learner should notice:_ one user-facing agent can delegate to backends with different runtime characteristics
- **M01.L08** — End-to-end agent observability — Show UI -> Gateway -> Agent -> Tool -> Model with trace spans across the whole path. Beside it list Operational, Quality, and Product metrics plus structured logs with PII redaction  
  _Learner should notice:_ observability covers both technical operation and whether the agent actually delivers value
- **M01.L08** — Agent threat model surfaces and assets — Show Client -> Gateway -> Agent Runtime -> Tool/MCP Servers -> Model Provider/Storage, with callouts for API keys, user data, PII, tool credentials, logs, and write permissions at the relevant surfaces  
  _Learner should notice:_ different attack surfaces expose different assets
- **M01.L09** — Three layers of the agentic loop — Show nested or stacked layers: Layer 1 internal SPAL inside one agent, Layer 2 external task loop around the agent, and Layer 3 orchestrator/collaboration meta loop controlling several agents or task loops  
  _Learner should notice:_ each higher layer expands control beyond the previous loop
- **M01.L09** — Four core loop elements — A loop diagram around four labeled concepts: Goal, Plan, State, Decision. Show arrows indicating that state and plan are updated each iteration while the decision controls whether another cycle begins  
  _Learner should notice:_ iteration alone is not enough; the loop needs explicit memory and stopping logic
- **M01.L09** — Layered termination gate — Show an iteration result entering a decision gate with checks for hard limit, cost budget, goal satisfied, quality threshold, and stagnation. Any stop condition leads to exit; otherwise flow returns to the next iteration  
  _Learner should notice:_ stopping is layered rather than delegated entirely to agent self-assessment
- **M01.L09** — Layer 2 versus Layer 3 control — Left: deterministic code loop controls one agent. Right: an orchestrator agent or peer-agent team controls the outer loop and delegates work  
  _Learner should notice:_ Layer 3 promotes decision/control from ordinary code to agent reasoning
- **M01.L09** — Collaboration loop with consensus — Show Researcher -> Critic -> Synthesizer around a shared CollaborationState. Each contributes to the state; a consensus gate checks recent agrees_goal_met flags before either ending or starting another round  
  _Learner should notice:_ peers share context and jointly influence termination
- **M01.L10** — Reasoning primitives versus cognitive architecture — Left: separate boxes for CoT, ReAct, ToT, Reflexion used independently. Right: a cognitive architecture that dynamically selects and monitors these primitives through feedback  
  _Learner should notice:_ the new capability is strategy selection and adaptation, not simply more reasoning
- **M01.L10** — Five cognitive-agent failure modes — Create a diagnostic map with five rows: confident wrong answer, broken record, rigid plan, overcommitted guess, shallow composition. For each, show the missing capability and the module that addresses it  
  _Learner should notice:_ be able to use the diagram as a troubleshooting map
- **M01.L10** — Three theoretical foundations mapped to architecture — Three columns: Minsky -> specialized modules; Baars -> shared cognitive workspace; Kahneman -> fast/deep routing through attention  
  _Learner should notice:_ each theory contributes one concrete design principle
- **M01.L10** — Full cognitive agent architecture — Show the cognitive workspace in the center with Perception, Planning, Execution, Evaluation, Attention, and Memory around it. Show the outer agentic loop wrapping the architecture  
  _Learner should notice:_ modules coordinate through the shared workspace instead of passing isolated messages only
- **M01.L10** — Attention routing decision tree — Show a decision tree from workspace signals to FAST_RESPOND, RESPOND, META_PLAN, PLAN, ESCALATE, MEMORY, EXECUTE, or EVALUATE  
  _Learner should notice:_ attention dynamically breaks the fixed cognitive sequence based on signals
- **M01.L10** — Cognitive cycle inside the agentic loop — Show an outer loop labeled Agentic Loop containing an inner Perception -> Planning -> Execution -> Evaluation cycle with Attention routing inside. Memory sits alongside the inner cycle  
  _Learner should notice:_ the macro loop versus micro cognitive cycle distinction
- **M01.L10** — Knowledge-boundary awareness — Show three zones labeled Within Knowledge, Edge of Knowledge, Outside Knowledge, with signals from retrieval quality, memory coverage, and confidence feeding the classifier. Outside leads to SIGNAL_UNCERTAINTY  
  _Learner should notice:_ uncertainty behavior is triggered by multiple architecture signals
- **M01.L11** — Five-layer production checklist — Stack five horizontal layers labeled Persona, Tools & Actions, Reasoning & Planning, Knowledge & Memory, Evaluation & Feedback. Inside each layer show 3-4 best-practice keywords from the lesson  
  _Learner should notice:_ production quality depends on all five layers rather than one clever prompt
- **M01.L11** — Persona as API contract — A contract card with five fields: Role, Responsibilities, Boundaries, Output Schema, Uncertainty/Fallback. Beside it show an example SupportMentor persona  
  _Learner should notice:_ persona design defines operational behavior, not just tone
- **M01.L11** — Partitioned RAG architecture — Show one logical knowledge system divided into tenant, role, product, version, and date partitions. A query passes through metadata/ACL filters before semantic or lexical search  
  _Learner should notice:_ retrieval boundaries are enforced before content reaches the LLM
- **M01.L11** — Customer support agentic system — Show User -> Triage -> Retrieval -> Grounding -> optional Business API -> Guardrail -> Answer -> User feedback, plus a direct escalation branch to Human  
  _Learner should notice:_ 'support agent' is actually a coordinated system of specialized roles
- **M01.L11** — Deep-research brain and hands architecture — Show Research Planner as the brain in the center, delegating to Web Searcher, Extractor, Analyst, Critic, and Writer. Workers return results to the planner; critic can route back for more research  
  _Learner should notice:_ the separation between strategic state and stateless specialist execution

## COURSE-013_Applied_Data_Analysis_with_Python — 154 images

- **M01.L01** — Raw data to business decision pipeline — A horizontal workflow showing raw transactions → cleaning → exploration → metrics/models → visualizations → interpretation → business decision  
  _Learner should notice:_ analysis involves multiple linked stages rather than only charts or code
- **M01.L01** — CRISP-DM cycle — A circular flowchart with Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment and feedback arrows to earlier stages  
  _Learner should notice:_ the process is iterative and teams may revisit earlier stages
- **M01.L01** — Standard data-analysis workflow — A five-stage visual showing Collect → Preprocess → Analyze → Interpret → Storytelling, with a final stakeholder decision box  
  _Learner should notice:_ storytelling is treated as part of the analytical process
- **M01.L01** — Data-team role map — A collaborative diagram showing Data Engineer → reliable data → Data Analyst/Data Scientist → models/insights → ML Engineer production systems, with NLP Engineer shown as a language-specialized engineering branch  
  _Learner should notice:_ the roles overlap and cooperate
- **M01.L01** — Anaconda Navigator concept view — A simplified launcher-style diagram showing Anaconda Navigator opening JupyterLab, Jupyter Notebook, Spyder, VS Code, and package/environment management  
  _Learner should notice:_ Anaconda is a distribution/environment ecosystem, not a programming language
- **M01.L01** — IPython help workflow — A small visual showing typing a partial NumPy function → tab completion → selecting np.arange → using help(np.arange) or np.arange?  
  _Learner should notice:_ interactive documentation is part of normal programming practice
- **M01.L01** — Notebook anatomy — A notebook screen containing a Markdown heading, Python code cell, output table, chart, and interpretation text with labels  
  _Learner should notice:_ how narrative and computation are interleaved
- **M01.L01** — Analytics tooling scale — A left-to-right progression showing local Python/Pandas → Jupyter exploration → IDE application development → Databricks/PySpark distributed workloads  
  _Learner should notice:_ different tools become useful as project scale and operational complexity grow
- **M02.L01** — NumPy shape intuition — Show a 1D array with shape (6,), a 2D 2×3 matrix with shape (2,3), and a simple 3D block labeled (2,2,3)  
  _Learner should notice:_ shape describes the size of each axis
- **M02.L01** — 2D NumPy indexing grid — A 2×2 matrix containing 5,6,7,8 with labels [0,0], [0,1], [1,0], [1,1] attached to each cell  
  _Learner should notice:_ connect row/column coordinates to actual values
- **M02.L01** — Axis 0 versus axis 1 — A 3×3 matrix with arrows showing axis=0 operating row-wise/vertically and axis=1 operating column-wise/horizontally, plus small stack/split examples  
  _Learner should notice:_ develop an intuitive mental model of NumPy axes
- **M02.L01** — NumPy assignment view copy memory model — Three small diagrams: assignment with two names pointing to one object, view with two objects sharing one data buffer, copy with separate buffers  
  _Learner should notice:_ why changing a view can affect the original but changing a copy does not
- **M02.L01** — NumPy slicing number line — A number line for values 0–9 showing positive indices above, negative indices below, and highlighted slices for [3:6], [-3:], and [2:7:2]  
  _Learner should notice:_ stop-exclusion and how negative indices count from the right
- **M02.L01** — Fancy indexing selection — A 5×4 matrix highlighting complete rows for row-index selection and then two individual cells for paired row/column fancy indexing  
  _Learner should notice:_ distinguish row selection from paired-coordinate selection
- **M02.L01** — Broadcasting scalar across matrix — A 2×2 matrix plus scalar 3, with arrows from the scalar to each cell and the resulting matrix  
  _Learner should notice:_ NumPy applies the scalar across all compatible elements
- **M02.L01** — Split-apply-combine — A table split into three color-coded continent groups, each group showing a mean calculation, then recombined into a compact summary table  
  _Learner should notice:_ groupby as a three-stage transformation rather than a mysterious method call
- **M02.L01** — Four DataFrame join types — A compact Venn-style or table-matching diagram showing inner, outer, left, and right joins using the same two small employee tables  
  _Learner should notice:_ which unmatched rows are preserved in each join
- **M02.L01** — Pivot table transformation — Show raw rows Weather/Food/Number on the left and a summarized matrix Weather × Food on the right with arrows labeled index, columns, values, aggfunc  
  _Learner should notice:_ how raw records become a cross-tab summary
- **M02.L01** — Datetime feature engineering — Show one timestamp such as 2024-10-03 10:30 splitting into year=2024, month=10, day=3, hour=10, minute=30, weekday, day-of-year, quarter, day name, month name  
  _Learner should notice:_ datetime as a rich source of derived features
- **M03.L01** — Attribute-type decision tree — A branching diagram: categorical → nominal/ordinal; numeric → interval/ratio; numeric also branching to discrete/continuous  
  _Learner should notice:_ the statistical method starts with understanding the kind of variable
- **M03.L01** — Mean median mode with an outlier — Show a small number line with clustered values and one extreme outlier; mark mean shifting toward the outlier, median staying central, and mode at the repeated value  
  _Learner should notice:_ why different center measures answer different questions
- **M03.L01** — Positive zero negative skew — Three distribution curves showing left-skewed, symmetric, and right-skewed shapes, with the long tail clearly highlighted  
  _Learner should notice:_ identify skew direction by the direction of the tail
- **M03.L01** — Kurtosis shapes — Three overlapping curves labeled platykurtic, mesokurtic, leptokurtic with visibly different tail/peak shapes  
  _Learner should notice:_ focus on relative tail weight rather than memorizing only the curve height
- **M03.L01** — Correlation intuition scatterplots — Five mini scatterplots labeled strong positive, weak positive, near zero, weak negative, strong negative  
  _Learner should notice:_ connect correlation sign and magnitude with visual patterns
- **M03.L01** — Central Limit Theorem — Show a non-normal population on the left and four sampling distributions of the mean for increasing n values becoming narrower and more bell-shaped  
  _Learner should notice:_ distinguish the population distribution from the distribution of sample means
- **M03.L01** — t-test selection guide — Three branches: one group vs fixed mean → one-sample; two unrelated groups → independent; same subjects before/after → paired  
  _Learner should notice:_ be able to select the correct t-test from the study design
- **M03.L01** — Statistical test selection map — Decision tree using outcome type, number of groups, independent vs paired, and categorical vs numeric to reach t-test, ANOVA, Mann–Whitney, Wilcoxon, Kruskal–Wallis, or Chi-square  
  _Learner should notice:_ use study design—not test-name memorization—to choose a method
- **M03.L01** — A/B testing pipeline — Control old page and treatment new page randomly assigned from users, then conversions collected, sample-size/power check, z-test, confidence intervals, and decision  
  _Learner should notice:_ A/B testing as an end-to-end experimental workflow
- **M03.L01** — Bayes update diagram — Prior probability → observe evidence/likelihood → Bayes calculation → posterior probability, with the numeric source example 0.30, 0.72, 0.50 → 0.432  
  _Learner should notice:_ Bayes as updating belief after evidence
- **M04.L01** — Scalar vector matrix tensor hierarchy — Show a single number, a 1D vector, a 2D grid, and a 3D stack of grids with dimension labels 0D, 1D, 2D, 3D  
  _Learner should notice:_ connect dimensionality with data structure complexity
- **M04.L01** — Matrix multiplication row by column — Two 2×2 matrices with the first row of A and first column of B highlighted, showing 1×5 + 2×7 = 19  
  _Learner should notice:_ how each output cell is constructed
- **M04.L01** — Polynomial curve fitting — Scatter points with cubic fitted curve overlaid and labels indicating original observations versus fitted curve  
  _Learner should notice:_ fitting as approximation rather than interpolation of every point
- **M04.L01** — Matrix rank and redundant rows — A 3×3 matrix where row 1 and row 2 are identical, visually bracket them as redundant, and annotate rank=2  
  _Learner should notice:_ connect rank with independent information
- **M04.L01** — Eigenvector transformation intuition — Show a transformation applied to several vectors where one special vector stays on the same line but changes length; label it eigenvector v and scaling λ  
  _Learner should notice:_ “direction preserved, magnitude scaled”
- **M04.L01** — SVD decomposition — Show matrix A splitting into U × Sigma × V-transpose, with Sigma highlighted as diagonal singular strengths  
  _Learner should notice:_ remember the three-factor structure
- **M04.L01** — PMF PDF CDF comparison — Discrete bars for PMF, continuous bell-shaped density for PDF, and cumulative rising curve from 0 to 1 for CDF  
  _Learner should notice:_ distinguish probability mass, density, and cumulative probability
- **M04.L01** — Bernoulli distribution — Two bars at 0 and 1 with probabilities 1-p and p  
  _Learner should notice:_ connect Bernoulli with a single binary trial
- **M04.L01** — Normal distribution anatomy — Bell curve centered at mean μ, showing symmetry and standard-deviation distances on both sides  
  _Learner should notice:_ associate the normal distribution with symmetry around μ
- **M04.L01** — Sample-size effect on normal histogram — Three histograms labeled n=15, n=100, n=1000 generated from the same normal distribution; small looks irregular, large looks smooth and bell-shaped  
  _Learner should notice:_ sampling variability in histogram shape
- **M04.L01** — Masked image array comparison — Four-panel layout: original image, randomly masked image, log-transformed original, log-transformed masked image  
  _Learner should notice:_ masking as metadata controlling which array elements participate normally in operations
- **M05.L01** — From raw values to visual insight — Show the same yearly sales values as a small table on the left and a line chart on the right, highlighting the 2021 dip and 2025 peak  
  _Learner should notice:_ why patterns can become easier to recognize visually
- **M05.L01** — Scatter plot interpretation — Scatter points trending upward with arrows labeling positive direction, one slightly off-trend point, and no connecting line  
  _Learner should notice:_ the overall point pattern communicates relationship
- **M05.L01** — Chart-selection quartet — Four mini-panels showing pie for part-to-whole, bar for category comparison, histogram for distribution, and bubble for three-variable relationship  
  _Learner should notice:_ distinguish the analytical purpose of each chart
- **M05.L01** — Matplotlib subplot anatomy — A 2x2 figure labeled fig as whole canvas and axes[0,0], axes[0,1], axes[1,0], axes[1,1] as individual panels  
  _Learner should notice:_ the figure/axes hierarchy
- **M05.L01** — Seaborn lmplot with hue — Scatterplot of satisfaction vs evaluation with two colors for left=0 and left=1, and a separate simple scatter + regression-line example  
  _Learner should notice:_ the roles of regression line and hue
- **M05.L01** — Histogram KDE box violin comparison — Four mini visualizations of the same synthetic distribution showing histogram bins, KDE curve, box plot, and violin shape  
  _Learner should notice:_ these plots reveal different aspects of distribution
- **M05.L01** — Pairplot anatomy — Small 3x3 pairplot-style grid with diagonal distributions and off-diagonal scatterplots, with labels pointing to diagonal vs relationship cells  
  _Learner should notice:_ how pairplot summarizes many pairwise views
- **M05.L01** — Gantt-style timeline — Horizontal task bars across a time axis with different drivers in different colors and one overlapping interval highlighted  
  _Learner should notice:_ connect start/finish data with timeline visualization
- **M05.L01** — Plotly interaction controls — One interactive chart with a button group, dropdown, and year slider labeled to show how each control changes trace visibility or selected data  
  _Learner should notice:_ Plotly controls modify figure state without rebuilding a new page
- **M05.L01** — Dash callback flow — Dropdown component on left → Input(value) → callback function → Output(figure) → bar chart on right  
  _Learner should notice:_ Dash reactive programming as a data-flow connection
- **M05.L01** — Dash real-time update loop — dcc.Interval every 2 seconds → callback → append new temperature → DataFrame → Plotly line chart → updated graph  
  _Learner should notice:_ periodic dashboard refresh as a loop
- **M06.L01** — CSV round-trip — CSV text file → pd.read_csv() → DataFrame → processing → df.to_csv() → output CSV, with index/header controls labeled  
  _Learner should notice:_ reading and writing as two directions of the same workflow
- **M06.L01** — Row-oriented versus columnar concept — A small table shown once grouped by rows for ordinary text/tabular thinking and once grouped by columns for Parquet-style analytical storage  
  _Learner should notice:_ the meaning of columnar storage conceptually
- **M06.L01** — Database connection lifecycle — Python program → connection → cursor → execute SQL → commit/fetch → close, with arrows showing write and read branches  
  _Learner should notice:_ remember the recurring relational-database access pattern
- **M06.L01** — Four NoSQL models — Four panels: MongoDB document, Cassandra wide-column rows, Redis key→value, Neo4j nodes/relationships  
  _Learner should notice:_ why different NoSQL systems fit different data shapes
- **M06.L01** — Cloud object storage workflow — Local Python/DataFrame files → SDK → S3 bucket or Azure container → object/blob → download back for processing  
  _Learner should notice:_ connect cloud storage with scalable file-based workflows
- **M06.L01** — REST versus GraphQL — REST side with multiple endpoints /users /orders /products; GraphQL side with one endpoint receiving a field-specific query and returning selected JSON  
  _Learner should notice:_ the chapter's high-level distinction
- **M07.L01** — Data cleaning decision flow — Raw messy dataset → EDA → diagnose missing/outliers/inconsistency → choose treatment → validate cleaned dataset, with a warning branch for overcleaning  
  _Learner should notice:_ cleaning as a reasoning workflow rather than a delete-everything process
- **M07.L01** — MCAR MAR MNAR comparison — Three panels: MCAR random sensor glitch, MAR missing salary related to observed age, MNAR missing debt related to debt itself  
  _Learner should notice:_ connect missingness mechanism with what drives the missing value
- **M07.L01** — dropna row versus column behavior — Small table with highlighted missing cells; show listwise row deletion, threshold-based row retention, and axis=1 column deletion as three separate outcomes  
  _Learner should notice:_ what is actually removed by each option
- **M07.L01** — Z-score outlier intuition — Bell-shaped distribution with mean at center and ±1σ, ±2σ, ±3σ marked; two extreme points beyond ±3σ highlighted  
  _Learner should notice:_ the threshold as distance from the mean in standard-deviation units
- **M07.L01** — Box plot anatomy and IQR rule — Horizontal box plot labeled Q1, median, Q3, IQR, lower/upper whisker bounds and two external outlier points  
  _Learner should notice:_ connect the visual box plot to the Q1 ± 1.5×IQR calculation
- **M07.L01** — Euclidean-style versus Mahalanobis-style distance intuition — Elliptical correlated data cloud with one point measured relative to covariance-aware contour rather than simple circular distance  
  _Learner should notice:_ Mahalanobis distance accounts for feature correlation
- **M07.L01** — Label encoding versus one-hot encoding — Three categories shown as integers 0/1/2 on one side and separate binary columns on the other  
  _Learner should notice:_ why label encoding implies order while one-hot encoding does not
- **M07.L01** — Standardization versus Min-Max — Same five input values mapped to standardized values around zero and Min-Max values from 0 to 1  
  _Learner should notice:_ the methods change scale in different ways
- **M07.L01** — Human-in-the-loop GenAI cleaning — Raw data → GenAI suggests Pandas script → human review → run on copy → validate metrics/distributions → approve cleaned data  
  _Learner should notice:_ GenAI assists but does not replace analytical judgment
- **M08.L01** — Tabular versus time-series order — On the left, ordinary rows that can be shuffled; on the right, dated observations connected in chronological order with arrows showing dependency through time  
  _Learner should notice:_ why temporal order must be preserved
- **M08.L01** — Lag and autocorrelation intuition — Show a daily revenue sequence and a copy shifted by one day; connect today with yesterday and label lag=1  
  _Learner should notice:_ autocorrelation as comparing the series with a shifted version of itself
- **M08.L01** — Time-series components — Four panels showing upward trend, repeating seasonal wave, irregular long cycle, and random noise  
  _Learner should notice:_ visually distinguish the four components
- **M08.L01** — Raw series versus 7-day moving average — Noisy daily revenue line in light tone with smoother 7-day SMA overlaid  
  _Learner should notice:_ smoothing as reducing short-term fluctuations
- **M08.L01** — Additive seasonal decomposition — One observed series split into four aligned panels: observed, trend, seasonal, residual  
  _Learner should notice:_ how a time series can be separated into components
- **M08.L01** — Stationary versus non-stationary series — Left panel fluctuating around constant mean/variance; right panel upward trend and changing level  
  _Learner should notice:_ visually distinguish stable statistical behavior from changing behavior
- **M08.L01** — Differencing intuition — Three aligned lines: original trending series, first difference centered around stable level, seasonal difference removing weekly repeating pattern  
  _Learner should notice:_ how differencing changes the target from level to change
- **M08.L01** — PACF selection intuition — PACF stem plot with lag 0 ignored, confidence band shaded, and one significant spike at lag 7 highlighted  
  _Learner should notice:_ connect significant PACF spikes with AR lag reasoning in the chapter
- **M08.L01** — ARIMA parameter map — A box labeled ARIMA(p,d,q) with p→past observations, d→differencing, q→past errors  
  _Learner should notice:_ remember the role of each parameter
- **M08.L01** — Additive versus multiplicative seasonality — Two time series with repeating cycles: constant seasonal amplitude versus amplitude increasing with trend  
  _Learner should notice:_ why the seasonal model form matters
- **M08.L01** — Point forecast versus interval forecast — Historical observed line extending into a dashed forecast line with shaded upper/lower 95% band  
  _Learner should notice:_ distinguish a single predicted path from forecast uncertainty
- **M08.L01** — Time-series train-test split — Timeline with early 80–90% labeled Train and final contiguous block labeled Test; contrast with a crossed-out randomly shuffled split  
  _Learner should notice:_ remember that chronological structure must be preserved
- **M08.L01** — Four-panel residual diagnostics — Standardized residuals, residual histogram/KDE, Q-Q plot, residual ACF correlogram, with labels describing the desired pattern in each  
  _Learner should notice:_ residuals as a final check on model assumptions
- **M09.L01** — Regression versus classification — Left side shows points with a fitted numeric prediction line and continuous output; right side shows two colored classes separated by a boundary  
  _Learner should notice:_ immediately distinguish continuous prediction from class assignment
- **M09.L01** — OLS residuals and best-fit line — Scatter points, one regression line, vertical residual segments from points to line, and a note that OLS minimizes the sum of squared residual lengths  
  _Learner should notice:_ what is being optimized
- **M09.L01** — Homoscedastic versus heteroscedastic residuals — Two residual-vs-fitted panels: even random spread around zero versus funnel-shaped spread  
  _Learner should notice:_ constant versus changing residual variance
- **M09.L01** — Multicollinearity and VIF — Two highly correlated predictor arrows feeding the same target, with inflated coefficient uncertainty shown, plus a simple VIF scale <5 / 5–10 / >10  
  _Learner should notice:_ connect correlated predictors with unstable coefficient estimates
- **M09.L01** — Underfitting good fit overfitting — Same curved dataset shown with straight underfit line, smooth degree-2 fit, and highly wiggly degree-17 fit  
  _Learner should notice:_ model complexity and generalization visually
- **M09.L01** — Logistic regression probability curve — S-shaped probability curve crossing a horizontal 0.5 threshold, with class 0 points on one side and class 1 points on the other  
  _Learner should notice:_ probability converted into a class by a decision boundary
- **M09.L01** — KNN classification and scaling — New point surrounded by neighbors, show K=3 vote, plus side panel showing unscaled income dominating age distance and scaled coordinates correcting it  
  _Learner should notice:_ connect distance-based learning with feature scaling
- **M09.L01** — CART versus ID3 split criteria — Parent node splitting into two child nodes; left panel calculates weighted Gini, right panel parent entropy minus child entropy = information gain  
  _Learner should notice:_ both criteria seek purer child groups
- **M09.L01** — Confusion matrix with churn example — 2x2 matrix labeled TP FP FN TN with short churn-business consequence inside each cell  
  _Learner should notice:_ connect metric formulas to business mistakes
- **M09.L01** — Precision-recall business trade-off — Slider/threshold diagram: lower threshold gives more predicted churners, higher recall/lower precision; higher threshold gives fewer predicted churners, higher precision/lower recall  
  _Learner should notice:_ connect decision thresholds with business error costs
- **M09.L01** — Train-test split — Dataset block divided into 80% training and 20% held-out test; arrows show model fitted only on training, then evaluated once on test  
  _Learner should notice:_ unseen-data evaluation
- **M09.L01** — Five-fold cross-validation — Five horizontal rows with one different fold highlighted as validation in each row and the other four as training  
  _Learner should notice:_ repeated rotation of validation data
- **M10.L01** — High-dimensional reduction concept — Many original feature axes compressed into a 2D projection while some information is preserved and some is lost  
  _Learner should notice:_ dimensionality reduction as representation, not deletion of arbitrary columns
- **M10.L01** — PCA 3D-to-2D projection — 3D point cloud with PC1 and PC2 arrows and a best-fit projection plane, then the same points represented on the 2D PC1-PC2 plane  
  _Learner should notice:_ PCA as rotation and projection onto maximum-variance directions
- **M10.L01** — PCA cumulative explained variance curve — Number of components on x-axis, cumulative variance on y-axis, horizontal 95% line and intersection near seven components  
  _Learner should notice:_ how component count is selected from retained variance
- **M10.L01** — PCA drift health map — PC1-PC2 scatter with baseline cloud A and shifted cloud B, plus a small loading panel showing engagement features driving PC1  
  _Learner should notice:_ how one fitted PCA coordinate system enables population drift comparison
- **M10.L01** — K-Means iterative process — Four frames showing initial random centroids, point assignment, centroid movement, and converged clusters  
  _Learner should notice:_ assignment-update repetition
- **M10.L01** — Elbow method — Inertia curve from K=1 to K=10 with strong drop then flattening and elbow at K=2  
  _Learner should notice:_ diminishing returns rather than simply choosing maximum K
- **M10.L01** — Agglomerative dendrogram anatomy — Dendrogram with leaves, merge branches, distance axis, horizontal cut line, and resulting clusters colored  
  _Learner should notice:_ cluster count comes from where the tree is cut
- **M10.L01** — DBSCAN point types — Dense cluster with epsilon circle around a core point, nearby border point, and distant noise point, labeled core/border/noise  
  _Learner should notice:_ eps and MinPts geometrically
- **M10.L01** — Global versus local anomalies — Main dense cloud with one far-away global outlier and one point inside/near a secondary cluster but sparse relative to neighbors, labeled local anomaly  
  _Learner should notice:_ distinguish global distance from local density deviation
- **M10.L01** — Isolation Forest path intuition — Two random-split trees: distant anomaly isolated in 2 splits and normal dense point isolated after many splits  
  _Learner should notice:_ why shorter isolation path implies anomaly
- **M10.L01** — LOF k-distance and reachability — Central point A, four nearest neighbors, circle to 4th neighbor, another point B with labels for direct distance and reachability distance  
  _Learner should notice:_ how local neighborhoods are defined
- **M10.L01** — MV and EM evaluation curves — Side-by-side ideal versus weak Mass-Volume curves and ideal versus weak Excess-Mass curves with directional annotations  
  _Learner should notice:_ the source's unsupervised score-evaluation intuition
- **M10.L01** — Isolation Forest versus LOF results — Same synthetic user population shown twice: Isolation Forest highlighting distant bot points and LOF highlighting locally unusual compromised accounts plus some others  
  _Learner should notice:_ why global and local detectors can disagree
- **M11.L01** — Ensemble intuition — Three different base models making partly different mistakes, then an aggregation block producing a stronger final prediction  
  _Learner should notice:_ error diversification and combination
- **M11.L01** — Bias-variance trade-off — Underfit linear model, appropriate fit, overfit high-degree model, with arrows indicating high bias on one side and high variance on the other  
  _Learner should notice:_ connect ensemble motivation with model error types
- **M11.L01** — Bootstrap sampling — Original dataset of five colored observations feeding three same-sized bootstrap samples with repeated and omitted observations  
  _Learner should notice:_ sampling with replacement
- **M11.L01** — Random Forest workflow — Bootstrap samples feeding multiple trees; each tree shows random feature subset at splits; outputs aggregate into final class/probability  
  _Learner should notice:_ both row and feature randomness
- **M11.L01** — Bagging versus boosting — Left: parallel independent learners aggregating; right: sequential learners with arrows from previous errors to next learner  
  _Learner should notice:_ immediately see parallel versus corrective training
- **M11.L01** — AdaBoost reweighting — Same training points across three rounds; misclassified points become larger/heavier, next weak learner focuses on them, final weighted ensemble combines learners  
  _Learner should notice:_ adaptive sample weighting
- **M11.L01** — Voting ensemble with model-specific preprocessing — Raw data branches to linear/KNN preprocessing with scaling and to tree preprocessing without scaling, then three models feed soft-voting block  
  _Learner should notice:_ per-model pipelines inside one ensemble
- **M11.L01** — Out-of-fold stacking — Training data split into five folds, each base model trains on four and predicts the held-out fold; OOF columns then feed a level-1 meta-model  
  _Learner should notice:_ how stacking avoids training the meta-model on leaked base predictions
- **M12.L01** — Artificial neuron — Inputs x1...xn multiplied by weights, summed with bias, passed through activation function, producing output  
  _Learner should notice:_ identify every component of one neuron
- **M12.L01** — Feedforward versus recurrent network — Left shows one-direction layer flow; right shows a hidden-state recurrent loop carrying information from previous time step  
  _Learner should notice:_ why sequence models have memory
- **M12.L01** — Sigmoid versus tanh — Two S-shaped curves, sigmoid from 0 to 1 and tanh from -1 to 1, with saturation regions marked  
  _Learner should notice:_ range and zero-centering difference
- **M12.L01** — Neural-network regularization toolkit — Network diagram showing L1/L2 on weights, dropout disabling neurons, early-stopping curve, image augmentation, and batch normalization  
  _Learner should notice:_ regularization can act in several different ways
- **M12.L01** — Forward pass and backpropagation — Network with arrows forward from input to prediction/loss and arrows backward carrying gradients to weight updates  
  _Learner should notice:_ the two-direction training cycle
- **M12.L01** — CNN architecture — Image flowing through convolution + ReLU + pooling blocks, then flattening, dense layers, and Softmax classification  
  _Learner should notice:_ the full spatial-feature pipeline
- **M12.L01** — Convolution operation — 5x5 image patch, highlighted 3x3 region, 3x3 kernel, element-wise multiplication and sum producing one feature-map cell  
  _Learner should notice:_ exactly how one convolution output is created
- **M12.L01** — Max pooling — 4x4 feature map divided into 2x2 windows producing a 2x2 output of maximum values  
  _Learner should notice:_ downsampling
- **M12.L01** — Unrolled RNN — One recurrent cell unrolled over t-1, t, t+1 with hidden state flowing between time steps and inputs/outputs at each step  
  _Learner should notice:_ temporal memory
- **M12.L01** — LSTM cell — Cell state running through the unit with forget gate, input gate, candidate update, and output gate, with sigmoid/tanh labels  
  _Learner should notice:_ how information is selectively kept, updated, and exposed
- **M12.L01** — Autoencoder architecture — Input image compressed by encoder into small latent bottleneck, then expanded by decoder to reconstructed output  
  _Learner should notice:_ compression and reconstruction
- **M12.L01** — Denoising autoencoder comparison — Three rows for the same CIFAR examples: noisy input, clean original, denoised reconstruction  
  _Learner should notice:_ what the denoising objective actually produces
- **M13.L01** — Text-analysis pipeline — Raw customer reviews flowing through preprocessing, vectorization, model, and insights such as sentiment/spam/topic  
  _Learner should notice:_ the end-to-end role of text analysis
- **M13.L01** — Regex cleaning example — Raw review with URL, emoji, punctuation, digits; arrows identify URL extraction and character replacement; cleaned result underneath  
  _Learner should notice:_ pattern-based transformations visually
- **M13.L01** — Stemming vs lemmatization vs POS-aware lemmatization — Same inflected words flowing through Porter stemmer, default WordNet, and POS-aware WordNet with outputs compared  
  _Learner should notice:_ accuracy vs simplicity trade-off
- **M13.L01** — Bag-of-Words matrix — Three short documents on left, vocabulary across columns on right, count matrix filled with 0/1/2 values  
  _Learner should notice:_ how text becomes a sparse numeric matrix
- **M13.L01** — Sparse one-hot versus dense embedding — Same word represented by long sparse one-hot vector and compact dense vector; nearby points for semantically similar words  
  _Learner should notice:_ why embeddings are compact and semantic
- **M13.L01** — Static vs contextual bank embeddings — Static model maps both “bank” usages to same vector; transformer maps financial-bank and river-bank tokens to different contextual points  
  _Learner should notice:_ context-dependent representation
- **M13.L01** — Classical sentiment pipeline — Review text → regex cleaner → TF-IDF unigrams+bigrams → MultinomialNB → negative/neutral/positive  
  _Learner should notice:_ one reproducible pipeline
- **M13.L01** — Classical text ML versus transformer — Left: clean→TF-IDF→Naive Bayes, fast/interpretable; right: tokenizer→DistilBERT→classifier, contextual/heavier; decision factors between them  
  _Learner should notice:_ when complexity is justified
- **M14.L01** — Image array representations — Same small image shown as grayscale 2D matrix, RGB 3-channel stack, and RGBA 4-channel stack  
  _Learner should notice:_ connect visible pixels with array dimensions
- **M14.L01** — BGR versus RGB comparison — Same butterfly displayed incorrectly from BGR in Matplotlib and correctly after BGR→RGB conversion  
  _Learner should notice:_ immediately see channel-order error
- **M14.L01** — Forced resizing distortion — Original rectangular butterfly beside forced 224×224 version, with arrows showing changed width-height proportion  
  _Learner should notice:_ why aspect ratio preservation matters
- **M14.L01** — Crop versus letterbox — Same rectangular butterfly converted to square using center crop and black-border padding  
  _Learner should notice:_ compare content loss versus introduced borders
- **M14.L01** — HSV masking workflow — Butterfly → HSV channels → combined H/S/V thresholds → binary orange mask → selected orange wing preview  
  _Learner should notice:_ why multiple HSV conditions are combined
- **M14.L01** — Denoising comparison — Same noisy butterfly shown with Gaussian blur, median filtering, and bilateral filtering, with edge/detail trade-offs annotated  
  _Learner should notice:_ compare filter behavior rather than memorize one winner
- **M14.L01** — Brightness contrast exposure clipping — Original image plus brightness-added, contrast-scaled, exposure-multiplied versions and white clipping mask  
  _Learner should notice:_ distinguish additive, pivot-scaling, multiplicative, and saturation effects
- **M14.L01** — Canny thresholds — Same grayscale butterfly with low-threshold noisy edge map, reasonable edge map, and high-threshold missing/broken edges  
  _Learner should notice:_ threshold sensitivity
- **M14.L01** — Shi-Tomasi corners — Butterfly with red keypoint dots concentrated at wing tips, spots, and strong intersections  
  _Learner should notice:_ distinguish point features from edge maps
- **M14.L01** — Contour measurements — Binary object contour with area shaded, perimeter highlighted, centroid dot, and circularity note  
  _Learner should notice:_ connect object geometry with numerical descriptors
- **M14.L01** — Haar versus DNN face detection — Same group photo with bounding boxes from Haar on left and confidence-scored DNN boxes on right  
  _Learner should notice:_ both are detectors, not identity recognizers
- **M15.L01** — RNN versus transformer sequence processing — Left shows sequential token-by-token recurrent processing; right shows all tokens connected through attention in parallel  
  _Learner should notice:_ the transformer motivation
- **M15.L01** — Scaled dot-product attention — Q and K matrices form score matrix, divide by sqrt(dk), softmax creates attention weights, weights multiply V to create output  
  _Learner should notice:_ each operation in the attention formula
- **M15.L01** — Multi-head attention — One input sequence projected into several parallel attention heads, then concatenated and passed through output projection  
  _Learner should notice:_ multiple simultaneous relationship views
- **M15.L01** — Transformer block — Token+position input → multi-head attention → Add & Norm → feed-forward → Add & Norm → output  
  _Learner should notice:_ attention as one component rather than the whole transformer
- **M15.L01** — Transformer architecture families — Three panels for encoder-only classification, decoder-only generation, and encoder-decoder sequence-to-sequence  
  _Learner should notice:_ architecture-task relationships
- **M15.L01** — Three LLM adaptation paths — Same pretrained model branching to prompting, full fine-tuning, and LoRA/PEFT, annotated with no-weight-change / all-weights / small-adapter update  
  _Learner should notice:_ compare adaptation cost and control
- **M15.L01** — Effective prompt anatomy — Prompt box divided into instruction, context, constraints, and output format, feeding an LLM and producing controlled output  
  _Learner should notice:_ prompt design as structured specification
- **M15.L01** — Full fine-tuning versus LoRA — Full FT duplicates and updates all base weights; LoRA freezes base and trains two small low-rank matrices attached to selected layers  
  _Learner should notice:_ parameter-efficiency visually
- **M15.L01** — Semantic search workflow — Documents and query separately embedded, cosine similarity computed, top-k documents returned  
  _Learner should notice:_ distinguish embedding retrieval from LLM generation
- **M15.L01** — Retrieve-then-answer / RAG-style flow — User query → query embedding → vector similarity against document embeddings → top context → answer model → grounded response  
  _Learner should notice:_ retrieval and answering as separate stages
- **M15.L01** — AI coding task lifecycle — Repository context + bounded task → AI edit → tests/checks → diff/review → accept/reject  
  _Learner should notice:_ AI coding as reviewable engineering workflow

## COURSE-014-image-processing-computer-vision-engineering — 167 images

- **M01.L01** — Image as matrix and tensor — Show one grayscale image beside a 2D intensity matrix and one RGB image beside a 3D H x W x 3 tensor with R, G, and B channels  
  _Learner should notice:_ connect visible pixels to numerical array elements and understand why grayscale is 2D while RGB is 3D
- **M01.L01** — Digital image-processing pipeline — A left-to-right flow diagram showing acquisition, image I/O/representation, preprocessing, segmentation, feature extraction, recognition/detection/classification, and output visualization/storage  
  _Learner should notice:_ low-level pixel operations prepare data for higher-level interpretation
- **M01.L01** — BGR versus RGB channel order — Show the same color image displayed once with OpenCV BGR values interpreted directly as RGB and once after BGR-to-RGB conversion  
  _Learner should notice:_ the color distortion caused by channel-order mismatch
- **M01.L01** — RGB versus HSV representation — Show an RGB cube beside an HSV cylinder/cone-style representation with Hue, Saturation, and Value clearly labeled  
  _Learner should notice:_ HSV separates color type, colorfulness, and brightness rather than directly storing red, green, and blue intensities
- **M01.L01** — CIE 1931 chromaticity diagram — A standard CIE 1931 xy chromaticity diagram with the visible-color boundary and an example device gamut triangle  
  _Learner should notice:_ a device usually reproduces only a subset of the perceivable chromaticity region
- **M01.L01** — HSV channel manipulation — Show one source image beside three outputs where hue, saturation, and value are changed independently  
  _Learner should notice:_ each HSV component affects a different visual property
- **M01.L01** — Image array coordinates — Show an image grid with origin at the top-left and arrows for column/x to the right and row/y downward, beside a generic Cartesian plot for comparison  
  _Learner should notice:_ why mixing row-column indexing with x-y plotting can place overlays incorrectly
- **M01.L01** — Core image manipulations montage — Show one original image with outputs for crop, mask, brightness increase, contrast increase, horizontal flip, alpha blend, and sepia  
  _Learner should notice:_ connect each array/numerical operation to its visual effect
- **M02.L01** — Image manipulation mental model — A diagram with one input image branching into pixel-value transforms, geometric-coordinate transforms, and channel/compositing transforms, with 2–3 examples under each branch  
  _Learner should notice:_ many different APIs reduce to a few reusable mathematical ideas
- **M02.L01** — Selective-color mask workflow — Show the original image, its hue channel or hue wheel, the Boolean mask for a selected color, and the final color-pop output  
  _Learner should notice:_ the mask—not a special photo effect function—controls which pixels keep their color
- **M02.L01** — Noise model comparison — Show the same clean grayscale image beside Gaussian, salt-and-pepper, Poisson, and speckle versions  
  _Learner should notice:_ compare the visual structure of each noise model rather than treating all noise as the same phenomenon
- **M02.L01** — Forward versus inverse image warping — Show an input grid, a transformed output grid, forward mapping with holes/overlaps, and backward mapping where each output pixel queries the source  
  _Learner should notice:_ why image libraries usually reconstruct transformed images using inverse mapping
- **M02.L01** — Resampling and aliasing — Show an original patterned image, a poor downsample with jagged/moiré artifacts, an anti-aliased downsample, and a nearest-neighbor enlarged version  
  _Learner should notice:_ distinguish resolution change from interpolation quality and recognize aliasing
- **M02.L01** — Point transformation comparison — Show the same grayscale or RGB image as original, inverted, log transformed, gamma transformed, thresholded, solarized, and posterized  
  _Learner should notice:_ compare how different transfer functions redistribute intensities while leaving spatial coordinates unchanged
- **M02.L01** — RGB histograms and channel views — Show an RGB image, separate red/green/blue channel visualizations, and aligned histograms for the three channels  
  _Learner should notice:_ connect visible color structure with the numerical distribution of each channel
- **M02.L01** — Alpha blending versus alpha compositing — Show two source images, a constant 50% blend, an RGBA foreground with a spatially varying alpha mask, and the alpha-composited result  
  _Learner should notice:_ the difference between one global mixing factor and per-pixel transparency
- **M03.L01** — Advanced image manipulation concept map — A diagram connecting value mapping, spatial mapping, interpolation, filtering, masking/compositing, compression, and visualization to example effects such as gamma, homography, blur, vignette, JPEG, and contours  
  _Learner should notice:_ many APIs are implementations of a small number of reusable ideas
- **M03.L01** — JPEG quality comparison with zoomed crop — Show the same photograph saved at high, medium, low, and extremely low JPEG quality, with a magnified crop from each version  
  _Learner should notice:_ dimensions can stay identical while fine detail, blocking, ringing, and file size change
- **M03.L01** — LUT color grading workflow — Show one original photograph, a simple conceptual RGB color cube/LUT mapping, and two different graded outputs from different LUTs  
  _Learner should notice:_ a LUT changes color mapping rather than moving image geometry
- **M03.L01** — Rotation canvas and cropping — Show a rectangular image inside its original canvas, the same rectangle rotated so corners leave the canvas, and an enlarged output canvas containing the full rotation  
  _Learner should notice:_ rotation clipping is a canvas-size problem, not a rotation failure
- **M03.L01** — Four-point homography — Show a photographed book/document as a quadrilateral with four labeled source corners, the four ordered destination rectangle corners, and the perspective-corrected output  
  _Learner should notice:_ each source point must correspond to the correct destination point
- **M03.L01** — Calibrated fisheye correction pipeline — Show a distorted checkerboard, a simplified camera intrinsic/distortion-parameter block, remapping arrows, and the corrected checkerboard with straighter lines  
  _Learner should notice:_ connect calibration parameters to coordinate remapping rather than thinking undistortion is just a cosmetic filter
- **M03.L01** — Wand distortion comparison — Show one source image beside barrel, polar, arc, Shepard/w local warp, and inverse-barrel corrected examples  
  _Learner should notice:_ compare global radial distortion, coordinate-system remapping, arc bending, local control-point warping, and approximate inversion
- **M03.L01** — Grayscale image and contour interpretation — Show a grayscale image as an intensity surface concept, the original image, contour lines at several intensity levels, and filled contours  
  _Learner should notice:_ contours connect equal-intensity locations rather than automatically representing object boundaries
- **M04.L01** — Sampling versus quantization — Show a smooth continuous grayscale surface on the left, a spatial sampling grid in the middle, and the same samples restricted to a small number of intensity levels on the right  
  _Learner should notice:_ clearly distinguish discretizing position from discretizing pixel value
- **M04.L01** — Nearest-neighbor upsampling — Show a tiny 4×4 pixel grid enlarged several times with visible square blocks and duplicated values  
  _Learner should notice:_ nearest-neighbor copies existing samples rather than estimating smooth transitions
- **M04.L01** — Nyquist and image aliasing — Show a fine stripe pattern at high resolution, a badly downsampled version with a Moiré pattern, and a properly low-pass-filtered/anti-aliased downsample  
  _Learner should notice:_ high-frequency detail turning into false lower-frequency structure when undersampled
- **M04.L01** — Intensity quantization levels — Show one smooth grayscale photograph or gradient at high precision, 16 levels, 8 levels, and 4 levels  
  _Learner should notice:_ banding/contouring increasing as the number of allowed intensities decreases
- **M04.L01** — Spatial image, magnitude, and phase — Show one grayscale image beside its centered log-magnitude spectrum and phase spectrum; label center as low frequency and outer regions as higher frequency  
  _Learner should notice:_ connect the image to two complementary Fourier representations
- **M04.L01** — Magnitude versus phase reconstruction — Show two source images, reconstruction using magnitude from A + phase from B, and reconstruction using phase from A + unrelated magnitude; include a random-phase example  
  _Learner should notice:_ phase strongly controls recognizable structure
- **M04.L01** — DCT basis and energy concentration — Show a small grid of low-order 2D DCT basis patterns plus a DCT spectrum whose strong coefficients cluster near the low-frequency origin  
  _Learner should notice:_ the image can be represented as weights on cosine patterns and that much energy often concentrates in a small region
- **M04.L01** — DFT periodicity and boundary discontinuity — Show a single cropped image, a tiled repeated version revealing jumps at tile borders, its spectrum with strong axis artifacts, and a smoothly windowed version  
  _Learner should notice:_ the DFT implicitly sees periodic repetition
- **M04.L01** — Gibbs ringing and smoothing — Show a sharp binary circle, its Fourier spectrum with oscillatory structure, a Gaussian-smoothed circle, and its smoother spectrum/reconstruction  
  _Learner should notice:_ connect sharp discontinuities to high-frequency content and ringing behavior
- **M04.L01** — Fourier transform property summary — A four-panel figure showing spatial rotation with rotated spectrum, spatial stretching with contracted spectrum, spatial translation with unchanged magnitude but changed phase, and linear addition in spatial/frequency domains  
  _Learner should notice:_ visually connect common spatial operations with their Fourier consequences
- **M05.L01** — Sliding 2D convolution — Show a small grayscale image grid, a highlighted 3×3 neighborhood, a 3×3 kernel, element-wise multiplications, their sum, and the resulting output pixel  
  _Learner should notice:_ convolution is repeated local weighted aggregation
- **M05.L01** — Common kernels and outputs — Show one source image with box blur, Laplacian edge, sharpen, and emboss kernels beside their corresponding outputs  
  _Learner should notice:_ changing only kernel weights changes the visual operation
- **M05.L01** — Full same valid convolution modes — Use a simple 5×5 input grid and 3×3 kernel to show visually which output positions are retained for valid, same, and full modes and how their output dimensions differ  
  _Learner should notice:_ mode controls output extent, not the kernel itself
- **M05.L01** — Convolution versus correlation — Show one asymmetric 2×2 or 3×3 kernel, the unchanged kernel used for correlation, the horizontally+vertically flipped kernel used for convolution, and a tiny numeric output example  
  _Learner should notice:_ remember that kernel flipping is the defining distinction
- **M05.L01** — Template matching correlation map — Show a larger face/object image, a cropped template, the resulting correlation heatmap, and the detected best-match location marked on the source  
  _Learner should notice:_ template matching searches for the maximum similarity response
- **M05.L01** — Convolution theorem pipeline — Show spatial image and kernel entering separate FFT blocks, element-wise multiplication of their spectra, then IFFT to produce the filtered image; alongside show the equivalent sliding spatial convolution  
  _Learner should notice:_ spatial convolution and frequency multiplication are two representations of the same linear filtering operation
- **M05.L01** — Gaussian kernel spatial and frequency views — Show a 2D Gaussian kernel as an image/3D surface beside its centered Fourier magnitude response, with low-frequency center bright and high-frequency outer regions dark  
  _Learner should notice:_ why Gaussian convolution behaves as low-pass filtering
- **M05.L01** — 2D versus 3D convolution — Show a 2D kernel sliding across H×W while spanning input channels, then a 3D kernel sliding across D×H×W for a volume/video; label channel versus depth axes carefully  
  _Learner should notice:_ not confuse RGB channels with the third sliding spatial dimension of a true 3D convolution
- **M05.L01** — Upsampling versus transposed convolution — Show one low-resolution feature map passing through fixed interpolation + Conv2d versus ConvTranspose2d, with a small checkerboard artifact example on the transposed-convolution side  
  _Learner should notice:_ distinguish fixed geometric enlargement from learned upsampling and recognize uneven-overlap artifacts
- **M06.L01** — Frequency filtering pipeline — Show one grayscale image, its centered Fourier magnitude spectrum, a circular filter mask, the masked spectrum, and the reconstructed output  
  _Learner should notice:_ frequency filtering is coefficient selection/attenuation followed by inverse transformation
- **M06.L01** — LPF HPF BPF and BSF masks — Show four centered radial frequency masks: low-pass bright center, high-pass dark center, band-pass bright ring, and band-stop dark ring/notches  
  _Learner should notice:_ visually associate each filter name with which frequency region is preserved
- **M06.L01** — Ideal Butterworth Gaussian responses — Show 1D radial response curves and corresponding 2D circular low-pass masks for Ideal, Butterworth at two orders, and Gaussian  
  _Learner should notice:_ how transition smoothness differs and why abrupt filters can ring
- **M06.L01** — LPF cutoff comparison — Show the same image filtered with small, medium, and large low-pass cutoffs, plus their circular masks  
  _Learner should notice:_ increasing cutoff preserves progressively more image detail
- **M06.L01** — LPF versus HPF — Show one source image, its low-pass result, high-pass result, and their corresponding centered masks  
  _Learner should notice:_ coarse structure in LPF and edge/detail structure in HPF
- **M06.L01** — Difference of Gaussians band-pass intuition — Show two Gaussian low-pass response curves with different widths, their subtraction producing a band-shaped response, and an image output emphasizing mid-scale structure  
  _Learner should notice:_ why subtracting two smoothing scales isolates a frequency band
- **M06.L01** — Periodic noise and notch filtering — Show a clean image, same image with sinusoidal stripes, centered spectrum with symmetric bright interference peaks marked, notch mask over those peaks, and restored image  
  _Learner should notice:_ why periodic noise is especially suitable for frequency-domain removal
- **M06.L01** — Fourier Feature Network architecture — Show pixel coordinate (x,y), multiplication by frequency matrix B, parallel sin/cos encoding, concatenated Fourier features, MLP, and predicted RGB pixel  
  _Learner should notice:_ Fourier features enrich the coordinate input before the network
- **M06.L01** — Fourier mapping reconstruction comparison — Show ground-truth image beside reconstructions from raw coordinates, basic Fourier mapping, low-scale Gaussian mapping, medium-scale mapping, and high-scale mapping, plus small PSNR labels  
  _Learner should notice:_ compare how mapping frequency affects fine-detail reconstruction
- **M07.L01** — Image enhancement strategy map — A diagram grouping enhancement methods by information used: single pixel, global histogram, local neighborhood, non-local patches, multi-scale wavelets, and learned models  
  _Learner should notice:_ enhancement methods differ mainly in what context they use to decide a new pixel value
- **M07.L01** — Gamma transform curves and images — Show gamma curves for gamma < 1, gamma = 1, gamma > 1 plus the same image transformed with each case  
  _Learner should notice:_ remember that gamma below one brightens darker intensities while gamma above one darkens them in the source convention
- **M07.L01** — Threshold vs random dithering vs Floyd-Steinberg — Show the same grayscale photograph converted by hard thresholding, random dithering, and Floyd–Steinberg dithering  
  _Learner should notice:_ compare false contours, noise-like halftone structure, and structured error diffusion
- **M07.L01** — Histogram processing comparison — Show original low-contrast image and histogram beside contrast stretching, global histogram equalization, and adaptive histogram equalization with their histograms/CDFs  
  _Learner should notice:_ the difference between global range expansion and local contrast redistribution
- **M07.L01** — Mamdani fuzzy enhancement — Show input intensity axis with dark/medium/bright membership curves, three IF-THEN rules, aggregated output membership functions, and one defuzzified output intensity  
  _Learner should notice:_ the four-step fuzzy inference pipeline
- **M07.L01** — White-balance methods — Show one color-cast input beside Gray World, White Patch, percentile White Patch, and Shades of Gray results  
  _Learner should notice:_ compare how different illuminant assumptions change RGB channel scaling
- **M07.L01** — Box versus Gaussian smoothing — Show a noisy image, box-filter outputs with two kernel sizes, and Gaussian outputs with two sigma/radius values  
  _Learner should notice:_ stronger smoothing with larger neighborhoods and the different weighting behavior of box versus Gaussian filters
- **M07.L01** — Order-statistic filters — Show a salt-and-pepper corrupted image beside median, mode, minimum, maximum, and 25/50/75 percentile outputs  
  _Learner should notice:_ these filters choose ranked neighborhood values rather than averages
- **M07.L01** — Bilateral versus non-local means — Show a target pixel/patch, bilateral local neighborhood weighted by distance+intensity, and NLM searching for similar patches across a larger region  
  _Learner should notice:_ distinguish local pixel similarity from non-local patch similarity
- **M07.L01** — Streamlit enhancement app architecture — Show user/upload controls feeding app.py, then a separate enhancement-engine module, then original/enhanced preview panels  
  _Learner should notice:_ the benefit of keeping UI and image-processing logic modular
- **M07.L01** — BM3D pipeline — Show noisy image, extraction of one reference patch, matching similar patches across the image, stacking into a 3D group, collaborative transform-domain filtering, and aggregation back into a denoised image  
  _Learner should notice:_ why the method is called block-matching and 3D filtering
- **M07.L01** — 2D wavelet decomposition — Show an input image splitting into the four standard wavelet sub-bands LL, LH, HL, HH with labels for approximation and directional details  
  _Learner should notice:_ wavelet decomposition as a multi-scale separation of coarse structure and details
- **M07.L01** — Zero-DCE iterative enhancement — Show low-light input, DCE-Net predicting per-pixel alpha maps, several iterative curve-adjustment stages, and final enhanced image  
  _Learner should notice:_ the network predicts adaptive enhancement curves rather than directly outputting an unrelated image
- **M07.L01** — Dark Channel Prior dehazing — Show hazy input, dark-channel image, estimated atmospheric-light marker/vector, transmission map, and reconstructed dehazed result  
  _Learner should notice:_ the sequence from statistical prior to transmission estimation to scene recovery
- **M07.L01** — Bicubic versus EDSR super-resolution — Show the same low-resolution crop, bicubic ×4 enlargement, and EDSR ×4 output with a magnified edge/texture region  
  _Learner should notice:_ compare fixed interpolation with learned detail reconstruction
- **M08.L01** — Image profile and first derivative — Show a 1D row through alternating dark/bright image regions, the corresponding intensity profile, and derivative spikes at transitions  
  _Learner should notice:_ why edges appear as peaks in first-order derivatives
- **M08.L01** — Laplacian variance blur comparison — Show the same image as original, box-blurred, and Gaussian-blurred, with the Laplacian response and variance score beneath each  
  _Learner should notice:_ why blur reduces derivative energy
- **M08.L01** — Unsharp masking pipeline — Show original image, blurred image, extracted high-frequency detail layer (original minus blur), and sharpened result  
  _Learner should notice:_ sharpening as adding back amplified detail
- **M08.L01** — Classical edge detector comparison — Show one grayscale scene beside Roberts, Prewitt, Sobel, Scharr, and Laplacian edge responses  
  _Learner should notice:_ compare edge thickness, directional sensitivity, and noise response rather than memorizing kernel names
- **M08.L01** — Kirsch compass edge detector — Show the eight compass directions around a central pixel, representative Kirsch masks, and a final map formed by taking the maximum directional response  
  _Learner should notice:_ multi-orientation edge detection
- **M08.L01** — Canny four-stage pipeline — Show noisy/grayscale input, Gaussian-smoothed image, gradient magnitude/orientation, non-maximum-suppressed thin edges, and final hysteresis-linked edge map  
  _Learner should notice:_ Canny is a pipeline, not just one convolution kernel
- **M08.L01** — LoG DoG and zero crossings — Show Gaussian smoothing, LoG kernel/response, DoG approximation, and binary zero-crossing edge contours  
  _Learner should notice:_ connect smoothing, second derivative, and sign changes
- **M08.L01** — Multiscale blob detection — Show the same image with LoG, DoG, and DoH detected blobs drawn as circles of different radii  
  _Learner should notice:_ detector scale becomes an estimate of feature size
- **M08.L01** — Hessian ridge detection — Show a retinal/vessel-like image, local Hessian ellipse/eigen-directions at one vessel point, and Meijering/Sato/Frangi/Hessian outputs  
  _Learner should notice:_ connect directional curvature with vessel-like structure
- **M08.L01** — Isotropic versus anisotropic diffusion — Show a noisy edge profile and two smoothing outcomes: isotropic blur crossing the edge, anisotropic diffusion smoothing inside regions while retaining the boundary  
  _Learner should notice:_ gradient-controlled diffusion
- **M08.L01** — HED versus PiDiNet — Show one natural image beside PiDiNet and HED edge maps, labeling PiDiNet as sparse/crisp and HED as richer/hierarchical  
  _Learner should notice:_ the accuracy/context versus efficiency trade-off described in the source
- **M08.L01** — Gaussian and Laplacian pyramids — Show the same image as a Gaussian pyramid of progressively smaller blurred levels and a Laplacian pyramid of corresponding detail/band-pass layers  
  _Learner should notice:_ distinguish coarse low-frequency representations from multiscale detail layers
- **M08.L01** — Pyramid image blending — Show two source images, a mask, Laplacian levels from both images, Gaussian mask levels, level-wise blending, and final seamless composite  
  _Learner should notice:_ why blending across scales is smoother than direct binary masking
- **M09.L01** — Image restoration degradation model — Show clean image f passing through PSF h and additive noise n to produce degraded image g, then a restoration block estimating f-hat  
  _Learner should notice:_ restoration as reversing a modeled forward process
- **M09.L01** — Inverse filtering instability — Show a blur transfer function with near-zero high-frequency values, a noisy spectrum divided by the transfer function, and amplified high-frequency noise in the restored image  
  _Learner should notice:_ why small H values cause unstable inversion
- **M09.L01** — Inverse vs Wiener deconvolution — Show original, blurred+noisy, inverse-filter restoration with amplified noise, and Wiener restoration balancing sharpness and noise  
  _Learner should notice:_ Wiener filtering as regularized statistical inversion
- **M09.L01** — Data fidelity and regularization balance — Show a slider-like diagram from small lambda with noisy/sharp restoration to large lambda with oversmoothed restoration, with a balanced solution in the middle  
  _Learner should notice:_ regularization as controlled bias added to stabilize inversion
- **M09.L01** — Högbom CLEAN workflow — Show dirty astronomical image, PSF, strongest residual peak selection, subtraction of shifted PSF, accumulated sparse clean components, restoring beam, and final restored image  
  _Learner should notice:_ CLEAN as greedy PSF matching under a sparsity prior
- **M09.L01** — Dictionary-learning denoising — Show noisy image, overlapping 8×8 patches, learned dictionary atoms, sparse coefficient vector with few nonzeros, reconstructed patches, and overlap-averaged restored image  
  _Learner should notice:_ sparse restoration as projection onto learned local structure
- **M09.L01** — Classical prior vs learned prior — Show Tikhonov as explicit formula/prior on one side and NAFNet learning degraded-to-clean mapping from pairs on the other  
  _Learner should notice:_ the shift from hand-designed priors to data-learned priors
- **M09.L01** — InstructIR multimodal restoration — Show degraded image plus natural-language instruction entering image-restoration and language branches, fused representation, and restored output  
  _Learner should notice:_ restoration conditioned jointly on image evidence and user intent
- **M09.L01** — Diffusion inpainting pipeline — Show damaged image, binary mask, encoded latent with masked region noised, text-conditioned denoising UNet, and final completed image  
  _Learner should notice:_ only the masked region should be synthesized while context remains consistent
- **M09.L01** — LaMa large-mask inpainting — Show original image with a large missing region, binary mask, local-context challenge, global/Fourier receptive-field concept, and completed result  
  _Learner should notice:_ why long-range context matters for large holes
- **M09.L01** — DiffEdit workflow — Show original image, source/target prompts, automatically inferred mask, DDIM inversion to latent space, target-conditioned denoising, and edited output  
  _Learner should notice:_ mask inference and latent inversion as separate steps
- **M09.L01** — Inpainting vs editing vs retouching — Show three branches from one source image: masked hole filling, object replacement via prompt, and low-strength whole-image retouch with mostly preserved structure  
  _Learner should notice:_ distinguish the task objective, not just the model family
- **M09.L01** — Outpainting canvas expansion — Show original image centered in a larger blank canvas, mask over added borders, diffusion generation in the new area, and final extended scene  
  _Learner should notice:_ outpainting as inpainting over newly created canvas regions
- **M10.L01** — Segmentation evolution map — Show one image flowing through threshold-based regions, watershed regions, superpixels/graphs, CNN semantic map, instance masks, and panoptic output  
  _Learner should notice:_ segmentation evolving from hand-crafted local rules to learned global/object-centric reasoning
- **M10.L01** — Multi-Otsu histogram segmentation — Show grayscale image, multimodal histogram with two threshold lines, and three-color region label map  
  _Learner should notice:_ connect histogram peaks and valleys with threshold-based class separation
- **M10.L01** — Marker-controlled watershed — Show grayscale image, gradient topography, marker seeds, flooding concept, and final labeled watershed regions  
  _Learner should notice:_ markers controlling where basins begin and strong gradients stopping region growth
- **M10.L01** — Coin counting pipeline — Show original coins, threshold mask, cleaned morphology mask, distance transform, local-max markers, watershed-separated coins, and final counted/centroid-labeled objects  
  _Learner should notice:_ segmentation as a multi-stage pipeline rather than a single function
- **M10.L01** — SLIC MaskSLIC and RAG — Show original image, SLIC superpixels, object mask, MaskSLIC constrained superpixels, adjacency graph over regions, and merged output  
  _Learner should notice:_ distinguish over-segmentation from later region merging
- **M10.L01** — Chan-Vese energy evolution — Show original weak-edge image, initial contour/level set, intermediate evolving contour, final binary region, and decreasing energy curve  
  _Learner should notice:_ segmentation emerging from region statistics rather than explicit edge detection
- **M10.L01** — GrabCut graph model — Show image with bounding box/scribbles, foreground and background GMM appearance models, pixel graph connected to source/sink, min-cut boundary, and extracted object  
  _Learner should notice:_ the combination of user hints, appearance likelihood, and neighborhood smoothness
- **M10.L01** — Random-Forest pixel segmentation — Show image, sparse hand-labeled training regions, multiscale feature stack, Random Forest, and dense predicted segmentation map  
  _Learner should notice:_ the bridge from handcrafted features to supervised pixel classification
- **M10.L01** — FCN semantic segmentation — Show encoder feature hierarchy, 1×1 class-score maps, skip fusion from shallow/deep layers, upsampling, and final pixel-wise semantic map  
  _Learner should notice:_ why dense prediction differs from image classification
- **M10.L01** — DeepLab ASPP — Show feature map entering parallel atrous convolution branches with different dilation rates plus pooled/global context, then feature fusion and semantic prediction  
  _Learner should notice:_ ASPP as multiscale context without aggressive spatial downsampling
- **M10.L01** — Mask R-CNN architecture — Show image→backbone/FPN→RPN proposals→ROIAlign→parallel classification, box regression, and mask branches→separate instance masks  
  _Learner should notice:_ the two-stage instance-segmentation pipeline
- **M10.L01** — Q K V self-attention for image patches — Show image split into patches/tokens, one token producing Query, all tokens providing Keys/Values, attention weights to distant patches, and aggregated context  
  _Learner should notice:_ global interaction between image regions
- **M10.L01** — SETR versus DPT — Show SETR using one final ViT token grid and simple upsampling versus DPT taking features from several transformer depths and fusing them into a dense output  
  _Learner should notice:_ why multi-level fusion improves localization
- **M10.L01** — DETR object queries — Show transformer image features plus several learned object-query tokens attending globally and producing class/mask predictions that combine into a panoptic segmentation map  
  _Learner should notice:_ object-centric query prediction versus per-pixel classification
- **M10.L01** — Pixel classification vs mask classification — Show left: independent per-pixel semantic labels; right: transformer queries predicting mask–class pairs that combine into semantic, instance, or panoptic outputs  
  _Learner should notice:_ the Mask2Former paradigm shift
- **M11.L01** — Fixed-label versus promptable segmentation — Show left: image entering a fixed-class semantic model producing a predefined class map; right: the same image plus point/box/text prompts entering a prompt-conditioned model producing different masks  
  _Learner should notice:_ the prompt changes the requested segmentation without retraining
- **M11.L01** — SAM architecture and prompt types — Show image encoder producing reusable embedding, prompt encoder receiving a point and box, mask decoder, and several candidate masks with quality scores  
  _Learner should notice:_ why the same image representation can answer different segmentation prompts
- **M11.L01** — Language-aligned segmentation — Show image regions encoded into visual embeddings, text prompts such as "car", "person", "water" encoded into text embeddings, cosine-similarity matching, and resulting masks  
  _Learner should notice:_ how text replaces a fixed output-class list
- **M11.L01** — CLIPSeg interactive pipeline — Show image + text prompt entering a shared vision-language encoder/decoder, a soft probability heatmap, thresholded binary mask, and colored overlay  
  _Learner should notice:_ distinguish logits/probabilities from the final thresholded mask
- **M11.L01** — Monocular depth with DPT — Show RGB scene, transformer/DPT block, dense depth prediction, and normalized heatmap with nearby and distant regions labeled  
  _Learner should notice:_ depth as a dense geometric prediction derived from monocular visual cues
- **M11.L01** — Depth to point-cloud projection — Show image pixel (x,y), camera intrinsic model, depth z, back-projection ray, resulting XYZ point, and a colored point cloud reconstructed from all pixels  
  _Learner should notice:_ connect the depth map with actual 3D geometry
- **M11.L01** — Real-time background blur — Show original portrait, semantic foreground mask, strongly blurred full image, and final composite with sharp foreground + blurred background  
  _Learner should notice:_ segmentation as an enabling component inside an application
- **M11.L01** — U-Net architecture — Show contracting encoder, bottleneck, expanding decoder, skip connections at matching scales, and final 1×1 pixel-classification layer  
  _Learner should notice:_ how U-Net combines semantic context and boundary detail
- **M11.L01** — Segmentation training pipeline — Show image/mask dataset → augmentation → batching → encoder-decoder network → logits → segmentation loss → backpropagation → validation metrics → saved model  
  _Learner should notice:_ segmentation training as an end-to-end data/model/evaluation system
- **M11.L01** — Brain tumor MRI segmentation — Show MRI slice, ground-truth tumor mask, predicted probability heatmap, thresholded binary prediction, and colored overlay  
  _Learner should notice:_ why overlap-based loss/metrics matter for small medical regions
- **M11.L01** — Swin-UNETR volumetric segmentation — Show 3D CT volume entering shifted-window Swin encoder stages, U-Net decoder with skips, and 3D multi-organ label volume  
  _Learner should notice:_ how transformer context and U-Net localization are combined in 3D
- **M11.L01** — CT mask to 3D mesh — Show axial CT slices and voxel segmentation feeding marching cubes, resulting liver/organ mesh, then combined 3D volume + colored organ meshes  
  _Learner should notice:_ segmentation can become patient-specific 3D geometry
- **M11.L01** — Remote sensing segmentation challenges — Show large satellite image with tiled grid, class-frequency bar chart with rare roads/water, and same land-cover class under several sensor/season appearances  
  _Learner should notice:_ why patching, class weighting, augmentation, and attention are useful
- **M11.L01** — Satellite tiled inference — Show very large satellite image split into patches, MAnet processing each patch, predicted tiles, stitching/reconstruction, and final full-resolution land-cover map  
  _Learner should notice:_ how models trained on patches can segment images too large for one GPU pass
- **M11.L01** — IoU versus Dice geometry — Show ground-truth and predicted binary masks with intersection/union regions highlighted, plus formulas for IoU and Dice  
  _Learner should notice:_ both metrics from set overlap rather than memorizing equations only
- **M11.L01** — Segmentation metric selection — Show four panels: IoU/Dice overlap for semantic masks, class-imbalance example exposing accuracy weakness, precision-recall curve and AP area, and instance masks evaluated across IoU thresholds for mAP  
  _Learner should notice:_ know which metric matches which segmentation problem
- **M12.L01** — Pixel space to semantic embedding space — Show several animal images passing through a CNN into high-dimensional vectors, then a 2D conceptual embedding where dogs cluster together, cats cluster together, and unrelated animals are farther apart  
  _Learner should notice:_ representation geometry becomes semantically meaningful
- **M12.L01** — PCA versus t-SNE on MNIST — Show the same digit samples projected with PCA and t-SNE, using class colors  
  _Learner should notice:_ PCA preserving linear variance while t-SNE emphasizes local neighborhood separation
- **M12.L01** — CNN feature hierarchy — Show one image with feature visualizations from an early, middle, and deep ResNet layer: edges → textures → object parts/semantic region  
  _Learner should notice:_ how internal representations become increasingly abstract
- **M12.L01** — Transfer learning workflow — Show pretrained ImageNet CNN, removal of original classifier, frozen backbone, new binary cat-vs-dog head, then optional fine-tuning of deepest layers  
  _Learner should notice:_ distinguish feature extraction from fine-tuning
- **M12.L01** — Channel and spatial attention — Show CNN feature tensor, channel-attention weights amplifying selected channels, then spatial mask highlighting important image regions  
  _Learner should notice:_ remember channel attention = what, spatial attention = where
- **M12.L01** — ViT classification and attention rollout — Show image split into patches, tokens entering transformer blocks, CLS/class output, and a patch-level attention heatmap over the source image  
  _Learner should notice:_ both patch tokenization and global self-attention
- **M12.L01** — CLIP zero-shot vs DINOv2 few-shot — Show CLIP comparing one image embedding to several text embeddings; beside it show DINOv2 averaging two support embeddings per class into prototypes and classifying a query by cosine similarity  
  _Learner should notice:_ distinguish language-based zero-shot from visual-prototype few-shot learning
- **M12.L01** — Face embedding recognition — Show several gallery identities mapped to compact clusters/prototypes in embedding space, a query face mapped nearby, cosine similarity scores, and an Unknown threshold  
  _Learner should notice:_ recognition as nearest-prototype metric matching rather than fixed closed-set classification
- **M12.L01** — Deterministic vs Bayesian vs MC Dropout — Show deterministic model producing one prediction; Bayesian model sampling several weight sets; MC Dropout sampling several dropout masks; both stochastic methods producing mean probability + uncertainty  
  _Learner should notice:_ uncertainty as disagreement across plausible model realizations
- **M12.L01** — FixMatch-style learning loop — Show small labeled set and large unlabeled set, weak augmentation creating high-confidence pseudo-labels, strong augmentation, consistency loss, and combined model update  
  _Learner should notice:_ how the model turns reliable guesses into temporary supervision
- **M12.L01** — Masked Autoencoder pipeline — Show image split into patches, ~75% patches hidden, visible patches entering ViT encoder, mask tokens/decoder reconstructing the missing regions, and reconstructed image  
  _Learner should notice:_ how unlabeled images supervise themselves
- **M12.L01** — Federated averaging — Show central server distributing one model to several clients with different private image distributions, local training, model updates returning, weighted aggregation, and next global round  
  _Learner should notice:_ models move while raw data stays local
- **M12.L01** — FGSM adversarial perturbation — Show clean image, loss gradient sign pattern, tiny scaled perturbation, adversarial image that looks visually similar, and changed classifier prediction  
  _Learner should notice:_ the perturbation follows the direction that increases model loss
- **M12.L01** — Semantic image retrieval pipeline — Show image database → EfficientNet embeddings → PCA/vector index; query image → embedding → cosine similarity → ranked visually/semantically similar results  
  _Learner should notice:_ retrieval as nearest-neighbor search in feature space
- **M12.L01** — Classification vs detection — Show same street image: classification returning one global label; detection returning several boxes with class names/confidences  
  _Learner should notice:_ detection combines recognition and spatial localization
- **M12.L01** — RetinaNet and focal loss — Show image pyramid/FPN levels feeding one-stage classification and box heads, plus a small chart where focal loss downweights easy high-confidence background examples  
  _Learner should notice:_ connect FPN with scale and focal loss with foreground-background imbalance
- **M12.L01** — RetinaNet vs Mask R-CNN output — Show one scene with RetinaNet bounding boxes and beside it Mask R-CNN with boxes plus individual colored pixel masks and contours  
  _Learner should notice:_ what instance masks add beyond rectangular localization
- **M12.L01** — OCR model evolution — Show document/scene image passing through Tesseract baseline, PaddleOCR detection+angle+recognition pipeline, EasyOCR detection/recognition, and TrOCR vision-encoder→text-decoder pipeline  
  _Learner should notice:_ distinguish preprocessing-heavy OCR from learned detection/recognition and end-to-end vision-to-text modeling
- **M12.L01** — Face landmarks and AR overlay — Show dense face mesh, selected eye/nose/mouth anchor points, inter-eye distance used for scaling, and final sunglasses/moustache overlay  
  _Learner should notice:_ landmarks as geometric anchors for stable augmentation
- **M12.L01** — Hand landmark graph — Show 21 labeled hand keypoints connected into finger chains, with fingertips emphasized and left/right handedness output  
  _Learner should notice:_ how a dense pose becomes a compact graph representation
- **M12.L01** — FOMM motion transfer — Show static source portrait, driving-video frame with learned motion keypoints, dense deformation field, and generated source-identity frame following the driving pose  
  _Learner should notice:_ appearance comes from the source while motion comes from the driver
- **M12.L01** — YOLOv8 car-damage assessment — Show damaged car, predicted damage instance masks, mask-area pixel count, and rule-based severity label  
  _Learner should notice:_ the separation between learned damage localization and hand-designed downstream severity logic
- **M13.L01** — Evolution of generative vision — Show a timeline/flow from cGAN/CVAE → Pix2Pix/CycleGAN → StyleGAN/GFPGAN → DDPM/LDM → Stable Diffusion/SDXL → ControlNet/IP-Adapter → multimodal image APIs  
  _Learner should notice:_ increasingly flexible conditioning and control
- **M13.L01** — Conditional GAN architecture — Show latent z and class label y entering the generator; real/generated images plus the same label entering a projection discriminator with realism + class-compatibility scoring  
  _Learner should notice:_ conditioning affects both generation and discrimination
- **M13.L01** — CVAE architecture — Show image + class label entering encoder → mu/logvar → reparameterization z → decoder + same class label → reconstruction, with reconstruction loss and KL regularization arrows  
  _Learner should notice:_ why the latent space becomes smooth and sampleable
- **M13.L01** — Conditional latent traversal — Show a row transitioning between two Fashion-MNIST classes and a second row varying style within one fixed class, plus a small t-SNE cluster view  
  _Learner should notice:_ distinguish semantic class control from within-class latent variation
- **M13.L01** — Pix2Pix versus CycleGAN — Show paired input-target examples for Pix2Pix with one generator/discriminator path; beside it show unpaired horse/zebra collections with two generators and cycle-consistency loops  
  _Learner should notice:_ remember paired correspondence versus unpaired reversible translation
- **M13.L01** — StyleGAN latent and style mixing — Show z→mapping→W styles→synthesis layers, plus a grid where row latent controls coarse structure and column latent controls fine appearance  
  _Learner should notice:_ layer-wise semantic control
- **M13.L01** — GFPGAN restoration — Show low-quality face → restoration encoder/network → pretrained StyleGAN facial prior → reconstructed face → paste-back into original image  
  _Learner should notice:_ how a strong learned facial prior can recreate plausible detail
- **M13.L01** — DDPM forward and reverse processes — Show clean image progressively corrupted to Gaussian noise across timesteps, then a U-Net+scheduler iteratively reversing the process from noise back to a synthesized image  
  _Learner should notice:_ generation as repeated denoising
- **M13.L01** — Pixel diffusion vs latent diffusion — Show high-resolution pixel-space diffusion on left; on right VAE encoder compresses image to small latent grid, diffusion happens there, then decoder reconstructs image  
  _Learner should notice:_ why latent diffusion reduces compute
- **M13.L01** — Stable Diffusion architecture — Show text prompt→text encoder, random latent→U-Net denoising loop with scheduler and cross-attention, VAE decoder→image  
  _Learner should notice:_ the four-module latent diffusion pipeline
- **M13.L01** — InstructPix2Pix editing — Show source sketch and text instruction entering an image-conditioned diffusion pipeline, then a realistic edited handbag/product output that preserves silhouette and layout  
  _Learner should notice:_ editing as source-conditioned generation rather than generation from scratch
- **M13.L01** — ControlNet Canny guidance — Show original horse, Canny edge control image, text prompt "zebra", ControlNet branch injecting structure into Stable Diffusion U-Net, and generated zebra preserving pose/composition  
  _Learner should notice:_ structure and semantics as separate conditioning sources
- **M13.L01** — Diffusion application grid — Show six panels: fast text-to-image, typography poster, image-to-image refinement, restoration, style conversion with structural control, super-resolution, and inpainting  
  _Learner should notice:_ recognize one diffusion family solving many image-processing tasks through different conditioning
- **M13.L01** — IP-Adapter plus ControlNet — Show text prompt, reference portrait, OpenPose skeleton entering one diffusion pipeline and producing several portraits with similar appearance but the target pose  
  _Learner should notice:_ independent semantic, appearance, and geometric conditioning
- **M13.L01** — Same-prompt generation comparison — Show one complex prompt above two rows of generated images labeled DALL·E 2 and DALL·E 3, with callouts for composition, prompt adherence, and typography  
  _Learner should notice:_ focus on evaluation dimensions rather than API syntax
- **M13.L01** — Multimodal understand-and-edit loop — Show input image → vision model → textual assessment/instruction plan → image editing model → edited result, with arrows indicating text and image information flow  
  _Learner should notice:_ reasoning/understanding and image synthesis as complementary capabilities
- **M13.L01** — Classical-plus-generative hybrid — Show original image→Canny edge detector→binary/RGBA edge mask→generative editing prompt→glowing artistic edge result  
  _Learner should notice:_ traditional CV used as controllable preprocessing for generative AI
- **M13.L01** — Prompt-driven editing taxonomy — Show one source image branching into colorization, object recolor, object removal, background replacement, style transfer, restoration, and seasonal transformation  
  _Learner should notice:_ distinguish local edits, masked edits, global appearance changes, and full scene transformations
- **M13.L01** — Industrial inspection with structured output — Show manufactured parts image entering a vision-language model and producing a structured defect table/JSON with location, severity, confidence, and summary  
  _Learner should notice:_ multimodal models as report-generating assistants rather than only classifiers
- **M13.L01** — Multimodal visual analysis domains — Show VQA image+question, factory inspection image+JSON, before/after satellite images+change report, and MRI+non-diagnostic educational description  
  _Learner should notice:_ the same image-language interface applied across very different domains
- **M13.L01** — Multimodal scientific workflow — Show scientific image/diagram entering a vision-language model, structured reasoning in the middle, then generated educational/scientific visualization  
  _Learner should notice:_ image→reasoning→image as a reusable workflow pattern

## COURSE-015_Voice_AI_Engineering_Real_Time_Voice_Agents — 121 images

- **M01.L01** — Five-stage evolution of AI agents — A left-to-right diagram showing Stage 0 classical agents, Stage 1 foundation models, Stage 2 foundation models plus RAG, Stage 3 tool-using agents, and Stage 4 multi-agent systems  
  _Learner should notice:_ retrieval adds knowledge, tools add action, and multi-agent systems add specialization and collaboration
- **M01.L01** — Sense-think-act agent loop — A circular diagram with Environment -> Perception -> Foundation Model / Reasoning -> Tool or Action -> Environment, with Goal and Instructions influencing the reasoning step  
  _Learner should notice:_ an agent is a loop interacting with an environment, not merely a single model response
- **M01.L01** — Complete single-turn agent execution loop — A six-stage flow showing User -> Model with instructions/tools -> Function-call request -> Host application execution -> Tool result -> Model final response  
  _Learner should notice:_ the execution boundary: the model requests an action, while application code performs it
- **M01.L01** — Short-term and long-term memory architecture — A diagram showing one active conversation feeding short-term/session memory, with selected durable facts or summaries written to long-term storage and later retrieved into a future session  
  _Learner should notice:_ session history and cross-session memory serve different purposes
- **M01.L01** — Five multi-agent orchestration patterns — One figure containing Router, Parallel, Sequential, Circular, and Dynamic patterns with small labeled node-and-arrow diagrams  
  _Learner should notice:_ compare how control flow differs across the five designs
- **M01.L01** — Cascaded pipeline versus live multimodal session — Side-by-side diagram: left shows Microphone -> ASR -> Text Model -> TTS -> Speaker; right shows Audio + Visual Frames + Text entering one stateful multimodal session that streams audio/text/tool events  
  _Learner should notice:_ fewer developer-visible processing boundaries and that text transcription is no longer the mandatory bridge for every modality
- **M01.L01** — From raw modalities to learned representations — A diagram with Text -> Tokens/Embeddings, Image -> Patches/Visual Representations, and Audio -> Acoustic Features/Audio Representations, all feeding a shared reasoning context  
  _Learner should notice:_ raw media is transformed before cross-modal reasoning occurs
- **M01.L01** — Point-and-ask multimodal fusion — A user points at one component on a circuit board while asking "What is this part?", with arrows from the spoken phrase and indicated image region into one shared context  
  _Learner should notice:_ neither speech nor image alone fully resolves the word "this
- **M01.L02** — Intent-and-slot voice assistant — A diagram showing several example utterances flowing into one Intent block, with extracted slots such as song_title and artist_name feeding a predefined backend action  
  _Learner should notice:_ the system behaves like a structured form-filling pipeline rather than open-ended contextual reasoning
- **M01.L02** — REST versus WebSocket communication — Side-by-side diagram: REST shows separate Request -> Response cycles that repeatedly open logical exchanges, while WebSocket shows one persistent bidirectional connection with audio/events flowing in both directions  
  _Learner should notice:_ live conversation benefits from a continuously open two-way channel
- **M01.L02** — Acoustic echo feedback loop — A diagram showing AI audio leaving the speakers, being picked up by the microphone, entering VAD, and accidentally triggering interruption; beside it, show browser audio processing/AEC reducing that feedback path  
  _Learner should notice:_ why full-duplex voice systems must control self-captured playback
- **M01.L02** — Two-WebSocket real-time voice architecture — Browser on the left with UI, microphone, and speaker; Python proxy in the middle; Live model service on the right; show one bidirectional WebSocket between browser and proxy and another between proxy and model  
  _Learner should notice:_ the proxy protects credentials while relaying a continuous two-way stream
- **M01.L02** — Browser microphone processing pipeline — Microphone -> MediaStream -> AudioContext -> AudioWorklet -> Float32-to-Int16 conversion -> fixed-size PCM chunks -> main thread -> WebSocket  
  _Learner should notice:_ high-frequency audio processing is separated from ordinary UI work
- **M01.L02** — Concurrent proxy forwarding — The proxy in the center with two independent async loops: one arrow Browser -> Proxy -> Model and another arrow Model -> Proxy -> Browser, both running simultaneously  
  _Learner should notice:_ full-duplex communication requires independent concurrent receive/send paths
- **M01.L02** — Streaming audio playback queue — Incoming Base64 audio chunks enter a queue, each is decoded into PCM/Float32 AudioBuffer, then Buffer 1 -> Buffer 2 -> Buffer 3 plays sequentially through the speaker  
  _Learner should notice:_ queueing hides network chunk boundaries and prevents audible gaps
- **M01.L02** — Hot-mic conversational state machine — States: Session inactive -> Listening -> AI speaking -> user interruption -> Listening, plus Mic muted as a side state that preserves the session  
  _Learner should notice:_ session lifetime, microphone state, VAD turn detection, and playback interruption are separate pieces of state
- **M01.L03** — Persona configuration layers — A diagram showing System Instructions controlling tone/rules and Voice Configuration controlling speech sound, both feeding the same live assistant session  
  _Learner should notice:_ character is produced by multiple configuration layers rather than one prompt alone
- **M01.L03** — Local smooth video vs sampled AI frames — A live camera stream displayed smoothly to the user on the left, while only periodic snapshots (for example at t=0s, 1s, 2s) are sent to the AI on the right  
  _Learner should notice:_ the user can see full-motion video while the model receives a much lower-rate visual stream
- **M01.L03** — Multimodal proxy flow — Browser sends two labeled streams, Audio and JPEG Frames, into one backend proxy; proxy decodes each and forwards both into one live model session  
  _Learner should notice:_ one session can receive multiple input types through the same application architecture
- **M01.L03** — Live function-calling loop — User asks weather -> live model chooses get_weather(city) -> backend tool handler calls external weather API -> API result returns to backend -> tool response returns to model -> spoken answer goes back to user  
  _Learner should notice:_ external execution happens in backend code, not inside the model
- **M01.L03** — Mobile-first assistant UI layout — A phone mockup with a large start/play button before session start, then large circular stop/mic/camera controls after connection, a prominent video preview area, and contextual switch-camera control  
  _Learner should notice:_ reduced clutter, large touch targets, and state-dependent controls
- **M01.L03** — From source code to running cloud service — Source files + requirements + Dockerfile -> container image -> registry -> Cloud Run service -> public HTTPS/WSS endpoint  
  _Learner should notice:_ Docker packages the app while Cloud Run runs the resulting container
- **M01.L03** — End-to-end advanced assistant architecture — Mobile browser with microphone/camera on left -> secure frontend connection -> cloud backend proxy in center -> live multimodal model plus external weather/tool APIs on right; show tool-call loop and streamed response returning to phone  
  _Learner should notice:_ how persona, vision, tools, UI, and deployment fit into one coherent system
- **M01.L04** — Agent framework capability map — A central Agent Framework box connected to Orchestration, Memory, Tools, Multi-Agent Communication, Human-in-the-Loop, and Streaming/Observability  
  _Learner should notice:_ the framework surrounds the model with operational capabilities rather than replacing the model
- **M01.L04** — Perceive-reason-act runtime loop — A graph showing Reasoning node -> conditional edge -> Tool node -> back to Reasoning, with an END path when no more actions are required  
  _Learner should notice:_ how a framework turns a manual while-loop into explicit orchestration
- **M01.L04** — Sequential versus parallel agent execution — Left side shows Weather then News sequentially; right side shows Weather and News running simultaneously before a Gather step  
  _Learner should notice:_ the latency advantage when tasks are independent
- **M01.L04** — Long-term memory RAG pipeline — Conversation facts -> Ingest -> Embed -> Vector Store; later Query -> Embed -> Similarity Search -> Relevant memories -> Agent context  
  _Learner should notice:_ retrieval, not just storage, is the core challenge
- **M01.L04** — Code introspection to function calling — Python function -> introspection -> JSON schema -> LLM tool selection -> structured function call -> registered function execution  
  _Learner should notice:_ how frameworks convert native code into model-usable tool interfaces
- **M01.L04** — Multi-agent delegation and shared context — A Supervisor routes work to Researcher and Writer; Researcher writes findings into Shared State, Writer reads them, and the Supervisor maintains control flow  
  _Learner should notice:_ delegation and information sharing are separate but complementary responsibilities
- **M01.L04** — Three framework philosophies — Three side-by-side diagrams: CrewAI as roles/tasks flowing through a managed process, ADK as Agent + Tools + Services + Runner components, LangGraph as explicit nodes and edges over shared state  
  _Learner should notice:_ compare abstraction level and control style rather than treating frameworks as interchangeable
- **M01.L04** — Complete agent framework assembly line — Instructions, short-term memory, long-term memory, and tool schemas feed into Runtime/Orchestration and the LLM; outputs branch to Tools, Other Agents, or Human Approval, then return to state  
  _Learner should notice:_ how the five core components cooperate on every execution turn
- **M01.L05** — Agent design blueprint — A central Math Agent connected to Purpose, Tools, Context, Core Instructions, and Execution Examples  
  _Learner should notice:_ agent design combines capability, knowledge, behavior, and demonstrations before coding begins
- **M01.L05** — ADK basic execution architecture — User Query -> Session Service + Agent Blueprint -> Runner -> Foundation Model -> Event Stream -> Final Response, with Artifact Service alongside Runner  
  _Learner should notice:_ Agent defines behavior while Runner executes it using services
- **M01.L05** — Chained tool execution — User request -> multiply tool call -> result 6 -> add tool call with [6,4] -> result 10 -> final answer  
  _Learner should notice:_ the runtime feeds one tool result back into reasoning before the next tool is selected
- **M01.L05** — Modular agent project structure — Separate boxes for tools.py, context.py, examples.py, and prompt.py all feeding into agent.py, which produces the Agent and session context  
  _Learner should notice:_ how modularization improves maintainability and allows each concern to evolve independently
- **M01.L05** — Manual live architecture vs ADK Live Agent — Left: Browser <-> Backend <-> Live API with two manually managed WebSockets; Right: Browser <-> Backend -> ADK Runner -> Agent/Live Model, with Runner abstracting provider streaming  
  _Learner should notice:_ which low-level responsibilities move from application code into the framework
- **M01.L05** — Agent debugging cockpit — A conceptual UI with chat on the right and a trace/state/events panel on the left, highlighting a tool-call event with function name and arguments  
  _Learner should notice:_ how observability exposes intermediate execution rather than only the final answer
- **M01.L05** — End-to-end agent development lifecycle — A circular or staged diagram: Design Blueprint -> Basic Agent -> Tools -> Modular Refactor -> Live Agent -> Debug/Trace -> Formal Evaluation -> Improve -> back to Design  
  _Learner should notice:_ agent development is iterative, not a one-time coding task
- **M01.L06** — Monolithic agent vs specialist team — Left: one huge agent connected to many unrelated tools; right: an orchestrator connected to Grammar, Math, and Summary specialists  
  _Learner should notice:_ why specialization can reduce complexity
- **M01.L06** — Five multi-agent orchestration patterns — Router, Parallel, Sequential, Circular, and Dynamic shown side by side  
  _Learner should notice:_ visually compare the control flow of each pattern
- **M01.L06** — Teaching Assistant pipeline with shared state — Grammar Agent -> Math Agent -> Summary Agent, with each agent connected to one Shared Session State box  
  _Learner should notice:_ deterministic order and context exchange together
- **M01.L06** — Single Live Agent with background team — User speaks with one Live Agent; behind it, a Sequential Orchestrator runs Grammar, Math, and Summary agents using Shared State  
  _Learner should notice:_ the separation between user-facing conversation and internal collaboration
- **M01.L06** — Five A2A principles — Opaque Execution, Async First, Modality Agnostic, Enterprise Ready, and Simple & Consistent around an A2A hub  
  _Learner should notice:_ remember the protocol design goals
- **M01.L06** — End-User Client Server chain — End-User -> Client/Concierge -> Remote Server/Specialist, with status/results returning in the opposite direction  
  _Learner should notice:_ distinguish who asks, who delegates, and who performs the work
- **M01.L06** — Agent Card anatomy — Structured card showing identity, interfaces, version, capabilities, security, and skills  
  _Learner should notice:_ the Agent Card as a discovery and compatibility contract
- **M01.L06** — A2A Task state machine — submitted -> working -> completed, with side branches to input-required, auth-required, failed, canceled, and rejected  
  _Learner should notice:_ how status coordinates long-running work
- **M01.L06** — A2A content hierarchy — Task contains status Messages and result Artifacts; both can contain TextPart, FilePart, and DataPart  
  _Learner should notice:_ remember the distinction between container and content type
- **M01.L06** — Polling vs SSE vs Webhook — Three timelines showing repeated polls, one streaming connection, and submit-then-later-callback  
  _Learner should notice:_ compare how connection lifetime changes with task duration
- **M01.L06** — Five A2A security layers — Authentication, Transport Security, Authorization/RBAC, Opaque Execution, and Webhook Verification shown as stacked protection layers  
  _Learner should notice:_ security as defense in depth
- **M01.L06** — Internal multi-agent plus external A2A architecture — Student -> Live Agent -> internal Grammar/Math/Summary team; a branch from the orchestrator discovers a remote Research Agent through Agent Card and receives an Artifact through A2A  
  _Learner should notice:_ how internal orchestration and external interoperability combine
- **M01.L06** — A2A Python toolkit roles — Remote Client on the left using Agent Card Resolver + A2AClient; A2A web application in the middle; AgentExecutor on the server side bridging into LangGraph/ADK/internal agent logic  
  _Learner should notice:_ protocol plumbing separated from framework-specific logic
- **M01.L06** — AgentExecutor adapter pattern — A2A RequestContext enters AgentExecutor; executor invokes a framework-specific agent; result is translated into TaskUpdater status and Artifact events  
  _Learner should notice:_ the executor as translation glue rather than the agent's intelligence
- **M01.L06** — Discover-connect-communicate client flow — Client fetches Agent Card -> creates A2AClient -> sends Message -> receives Task -> extracts Artifact  
  _Learner should notice:_ remember this reusable four-step client pattern
- **M01.L06** — Legacy-agent A2A adapter — Existing ADK Math Agent on the right remains unchanged; A2A AgentExecutor wrapper around it translates RequestContext into ADK Runner calls and ADK events into A2A working/completed + Artifact events  
  _Learner should notice:_ how interoperability can be added without rewriting core agent logic
- **M01.L06** — Cross-framework Research Assistant — User -> ADK Coordinator; Coordinator -> A2A -> LangGraph Strategist -> search queries; Coordinator loops over queries -> A2A -> ADK Research Worker -> raw results; results return to Coordinator for final synthesis  
  _Learner should notice:_ the strategize-execute-synthesize workflow across framework boundaries
- **M01.L06** — A2A rich-result dispatcher — Task -> Artifact -> inspect Part type -> Text handler / File handler / Data handler  
  _Learner should notice:_ A2A clients need typed content handling rather than text-only assumptions
- **M01.L06** — A2A debugging ladder — Step 1 inspect Task history/artifacts; Step 2 inspect Server logs; Step 3 call specialist directly with isolated CLI/client; Step 4 reconnect full orchestrator  
  _Learner should notice:_ follow a narrowing debugging strategy rather than debugging the entire distributed system at once
- **M01.L07** — Hard-wired agent vs MCP ecosystem — Left: one agent directly wired to many APIs/tools with tangled connections; right: Host connected through MCP Clients to independent Git, Filesystem, GitHub, Weather servers  
  _Learner should notice:_ how the standardized boundary removes direct coupling
- **M01.L07** — MCP Host-Client-Server architecture — Central Host containing multiple dedicated Client connections, each connected one-to-one to a separate MCP Server  
  _Learner should notice:_ Clients live inside the Host and isolate Server connections
- **M01.L07** — MCP dynamic discovery sequence — Config file -> Host launches Servers -> dedicated Clients -> tools/list requests -> discovered tool schemas -> aggregated toolset -> LLM  
  _Learner should notice:_ why new tools no longer require editing the agent's core source
- **M01.L07** — MCP primitive control triad — Three columns: Tool -> model-controlled -> action; Resource -> application-controlled -> data; Prompt -> user-controlled -> workflow  
  _Learner should notice:_ associate each primitive with who initiates its use
- **M01.L07** — Nested MCP Sampling flow — Outer flow Host -> Flight Server tools/call; inside it, Server -> Host sampling/createMessage -> Host LLM -> reasoning result -> Server -> final tools/call response  
  _Learner should notice:_ two nested conversations inside one apparent tool call
- **M01.L07** — Stdio vs remote MCP transport — Left: Host launches local Server subprocess and exchanges stdin/stdout; right: Host connects over HTTPS to remote shared MCP Server  
  _Learner should notice:_ local-process vs network-service deployment
- **M01.L07** — MCPToolset bridge — ADK Agent/LLM on left -> MCPToolset in center -> Stdio connection -> Stock MCP Server on right  
  _Learner should notice:_ how the framework dynamically adapts remote Server tools into model-callable capabilities
- **M01.L07** — MCP startup handshake — Host starts Server -> initialize -> tools/list -> Server returns get_stock_price schema -> MCPToolset adapts it -> LLM sees new tool  
  _Learner should notice:_ dynamic discovery rather than hard-coded registration
- **M01.L07** — Financial Analyst end-to-end flow — User -> ADK Runner -> LLM decides tool -> MCPToolset -> tools/call over Stdio -> Stock Server -> tool result -> MCPToolset -> LLM -> user response  
  _Learner should notice:_ trace the request across process boundaries
- **M01.L07** — MCP debugging isolation flow — MCP Server tested first by Inspector; after passing, connected to ADK Host. Branches show Server bug vs Host/configuration bug depending on where failure occurs  
  _Learner should notice:_ use isolated testing before debugging full integration
- **M01.L07** — A2A vs MCP boundary diagram — Left: Agent A <-> Agent B via A2A; beneath each agent, Host connects to Tool/Data Servers via MCP  
  _Learner should notice:_ complementary protocol layers rather than competing alternatives
- **M01.L08** — Overloaded live agent vs layered system — Left: one live agent connected directly to stock, weather, documents, customer lookup, compliance, and many rules; right: live host delegates to A2A specialists which use MCP tools  
  _Learner should notice:_ why the live layer should not become a domain monolith
- **M01.L08** — Six-layer responsibility map — Browser, Frontend Service, Backend/ADK Live, Host Agent, A2A Specialist, MCP Server stacked vertically with owned responsibilities and prohibited responsibilities beside each  
  _Learner should notice:_ use this as a boundary checklist
- **M01.L08** — Full NVDA round trip — Browser -> Backend -> ADK Live Host -> A2A Stock Specialist -> MCP Stock Tool -> provider/fallback, then structured result returns back through Specialist -> Host -> Backend -> Browser as text/audio/provenance  
  _Learner should notice:_ trace the whole system without confusing responsibility boundaries
- **M01.L08** — Blocking request vs durable task — Left: browser holds one request open while remote work runs; right: browser submits work, receives task ID, connection closes, task continues in durable store, UI reconnects for updates  
  _Learner should notice:_ why task identity replaces request lifetime
- **M01.L08** — ADK A2A MCP responsibility layers — Local ADK session on left, remote A2A agent task in middle, MCP tool operation on right, with one Durable Application State layer underneath mapping all IDs  
  _Learner should notice:_ no single protocol owns the whole workflow
- **M01.L08** — Polling vs streaming vs push for A2A tasks — Polling timeline, persistent streaming updates, and webhook callback pattern, all pointing into one durable task store  
  _Learner should notice:_ delivery mechanism is separate from state ownership
- **M01.L08** — Human-input suspension sequence — Background task -> input_required -> durable store + prompt -> frontend form -> user response with correlation ID -> task resumes  
  _Learner should notice:_ human interaction is modeled as task state, not a held-open request
- **M01.L08** — Idempotent update handler — Incoming event -> verify sender -> check event ID -> load workflow -> validate ownership/state transition -> apply once -> resume if terminal/suspended  
  _Learner should notice:_ duplicate delivery as expected rather than exceptional
- **M01.L08** — Long-running market report lifecycle — Live request -> workflow record -> A2A research task -> MCP tools -> progress -> input_required approval -> resume -> final Artifact -> cleanup/retention  
  _Learner should notice:_ the full durable lifecycle across all protocol boundaries
- **M01.L09** — Technical state vs user-visible state — Left: backend event graph with listening, tool call, agent delegation, approval, reconnect; right: clean user UI with meaningful labels and controls  
  _Learner should notice:_ UX translates system state into understandable action
- **M01.L09** — Live chat vs live workspace — Left: simple mic + transcript interface; right: live controls plus task cards, source panel, approval card, activity timeline, artifact panel  
  _Learner should notice:_ the interface evolve from conversation-only to task-aware workspace
- **M01.L09** — Live agent UI state machine — States for idle, connecting, listening, user speaking, thinking, speaking, tool running, specialist working, input required, reconnecting, completed, failed, canceled with user actions  
  _Learner should notice:_ why state-specific UI beats one generic spinner
- **M01.L09** — Host-controlled generative UI — Agent proposes structured component description -> host component catalog validates -> safe Task Card / Approval Card / Chart renders  
  _Learner should notice:_ agents do not get unrestricted UI execution
- **M01.L09** — Error recovery matrix — Failure types mapped to user-facing explanation and specific next actions  
  _Learner should notice:_ good errors explain what remains usable
- **M01.L09** — End-to-end live workspace screen composition — Live status strip, task card, activity timeline, approval card, source drawer, final artifact panel, recovery banner  
  _Learner should notice:_ the complete UX surface for long-running agent work
- **M01.L09** — Model creators vs consumers — Left: model creation pipeline with MLOps/FMOps; right: application builders consuming FMs through GenAIOps  
  _Learner should notice:_ the organizational split between model development and application development
- **M01.L09** — Four AgentOps challenge pillars — Autonomous Decisions, Tool Governance, Memory Governance, Multi-Agent Operations around a central AgentOps platform  
  _Learner should notice:_ remember why AgentOps extends GenAIOps
- **M01.L09** — MLOps environment lifecycle — Sandbox -> Development -> Staging -> Production, with Shared Services/Data underneath and Governance/Registry above  
  _Learner should notice:_ separation of concerns across environments
- **M01.L09** — Agent evaluation stack — Tool unit tests -> augmented prompt catalog -> tool selection/argument evaluation -> end-to-end output evaluation -> latency/cost metrics  
  _Learner should notice:_ agent quality includes execution path plus outcome
- **M01.L09** — Unified AgentOps platform — Development/Staging/Production pipeline connected to Evaluation Catalog, Tool Registry, Agent Registry, Short-Term Memory, Long-Term Memory, CI/CD, Governance  
  _Learner should notice:_ AgentOps as an operational platform rather than one library
- **M01.L09** — UX surface connected to AgentOps backbone — Top: live workspace with task card, progress, approval, sources; bottom: monitoring, registries, memory, evaluation, CI/CD, governance supporting those visible states  
  _Learner should notice:_ trustworthy UX depends on operational discipline
- **M01.L10** — Evaluation complexity ladder — Deterministic software -> static LLM -> autonomous tool-using agent -> live multimodal agent, with increasing dimensions of evaluation  
  _Learner should notice:_ why each layer adds new failure modes
- **M01.L10** — Anatomy of an agent golden record — User input -> expected tool -> expected parameters -> simulated/raw tool result -> expected final response  
  _Learner should notice:_ agent evaluation includes the execution path
- **M01.L10** — Multi-turn expected trajectory — User goal -> Tool 1 grades -> Tool 2 curriculum -> Tool 3 study plan -> final response, with golden expected trajectory below  
  _Learner should notice:_ the difference between a single expected tool and a chain
- **M01.L10** — Simulator architecture — Scenario/persona/turn limit/history pointer -> Simulator Agent -> Target Agent -> recorded messages + tool calls + parameters -> evaluation dataset  
  _Learner should notice:_ how synthetic interaction data is generated
- **M01.L10** — Four-quadrant agent evaluation scorecard — Generation & Grounding, Trajectory & Execution, Memory & Context, Operational Health  
  _Learner should notice:_ use this as a complete AgentOps evaluation map
- **M01.L10** — Interruption evaluation timeline — Agent speaking -> Simulator barges in -> measure stop latency -> agent answers new question -> agent returns to original topic  
  _Learner should notice:_ latency, switching, and retention as separate scores
- **M01.L10** — Three enterprise tool categories — Code Functions, Internal VPC APIs, Public APIs with trade-offs for latency, shareability, ownership, security, and monitoring  
  _Learner should notice:_ why registries must manage heterogeneous tools
- **M01.L10** — Generalist vs Specialist agent toolbox — Generalist faces a huge toolbox with many similar tools; Specialist receives a small curated set matching its job  
  _Learner should notice:_ associate narrower search space with predictability and security
- **M01.L10** — Three tool-governance organization models — Decentralized team-local registries, Centralized global team/registry, Federated local registries with promoted tools into global catalog  
  _Learner should notice:_ compare autonomy, speed, and governance
- **M01.L10** — Evaluation–Registry feedback loop — Agent evaluation finds tool problems -> Tool Registry metadata/version/access changes -> agent receives improved curated tools -> re-evaluation -> production monitoring -> new evidence  
  _Learner should notice:_ quality and governance as one continuous AgentOps cycle
- **M01.L11** — Agent sprawl before governance — Many teams creating separate Math, Grammar, SQL, HR, and Legal agents with inconsistent code structures and direct links  
  _Learner should notice:_ why successful adoption creates governance pressure
- **M01.L11** — AgentOps social layer — Template Catalog -> deployed Agent-as-a-Service -> Agent Registry -> Agent Gateway -> authorized consumers  
  _Learner should notice:_ creation, discovery, and governance as separate but connected responsibilities
- **M01.L11** — Standardized agent repository tree — Display the root folders/files with short annotations: Agent Card, deploy, evaluation, monitoring, sub-agents, tests, core logic  
  _Learner should notice:_ be able to mentally map where each responsibility lives
- **M01.L11** — Agent template instantiation workflow — Developer searches catalog -> selects template and metadata -> platform hydrates new repo -> CI/CD pipeline initialized -> custom development begins  
  _Learner should notice:_ remember the four-step flow
- **M01.L11** — Template Catalog vs Agent Registry — Left: Recipe/Blueprint with repo URL, owner, version -> used by developers; right: Live Service Directory with endpoint, Agent Card, health/status -> used by apps/agents  
  _Learner should notice:_ never confuse creation assets with running services
- **M01.L11** — Registry Record wrapper — Inner Agent Card containing standard protocol fields, surrounded by enterprise metadata: identity, code name, owner, compliance, cost center, public facade  
  _Learner should notice:_ standard protocol and enterprise governance as separate layers
- **M01.L11** — Secure Agent Registry runtime flow — Browser requests agents -> Backend queries Registry -> Gateway filters -> Public Facade sanitizes -> Browser sees safe list -> user selects public ID -> Backend resolves internal endpoint and opens agent session  
  _Learner should notice:_ why URLs and auth stay server-side
- **M01.L11** — Federated Agent Gateway governance — Baseline group policies grant common agents automatically; specialized agents appear in marketplace; request routes to Agent Owner; approval updates Gateway policy  
  _Learner should notice:_ how automation and owner review coexist
- **M01.L11** — Three-stream AgentOps lifecycle — Creation stream from Template Catalog to hydrated repo/deployment; Governance stream through Portal and Gateway policy; Usage stream from End User -> Frontend -> Backend -> filtered Registry -> selected Agent  
  _Learner should notice:_ all three lifecycles operating together
- **M01.L12** — Passive chatbot vs acting agent — Left: chatbot only returns text; right: agent connected to payments, email, database, calendar, files  
  _Learner should notice:_ why tool access increases the consequence of failure
- **M01.L12** — Eight layers of defense — Stack from Infrastructure at bottom through Network, Data, AI Application, AI Agent, IAM, Logging/Monitoring, GRC at top  
  _Learner should notice:_ memorize the complete stack
- **M01.L12** — Agent tool security layers — Agent reasoning -> schema validation -> authorization/least privilege -> HITL for high risk -> sandbox/tool execution  
  _Learner should notice:_ multiple controls before a real-world action occurs
- **M01.L12** — Distributed trace across agents — User request -> Tutor Agent -> Search Agent -> Vector DB, all sharing one trace ID with waterfall timings  
  _Learner should notice:_ why local logs are insufficient
- **M01.L12** — Six callback security hooks — User -> before agent -> before model -> after model -> before tool -> after tool -> after agent -> user, with example security checks at each  
  _Learner should notice:_ callbacks as lifecycle interception points
- **M01.L12** — Privacy Buffer architecture — User audio -> Gateway buffer; parallel local STT -> Guardrail Agent -> allow signal; safe audio released to reasoning model, unsafe audio dropped  
  _Learner should notice:_ how inspection happens before model exposure
- **M01.L12** — Parallel multimodal dual-gate architecture — Gateway splits stream: Production path through Input Gate -> reasoning model -> Output Gate -> user; Safety path -> multimodal Guardrail Agent controlling both gates  
  _Learner should notice:_ independent safety monitoring
- **M01.L12** — Unified identity chain — Alice -> Tutor Agent Identity -> Registrar Agent Identity -> Database, with user token context propagating through Token Exchange and agent workloads authenticated by mTLS  
  _Learner should notice:_ user identity and agent identity traveling together
- **M01.L13** — AgentOps automated factory — Developer commit enters CI/CD conveyor belt through validate, test, build, Dev, Staging, evaluate, register, approve, Production  
  _Learner should notice:_ deployment as an assembly line rather than one command
- **M01.L13** — Development feedback loop — Feature branch -> lightweight CI/CD -> private Dev agent -> manual engineer testing -> prompt/code changes -> push again  
  _Learner should notice:_ distinguish fast human iteration from Staging automation
- **M01.L13** — Registration as Code — CI/CD reads Agent Card + evaluation metrics + tool schemas -> updates Agent Registry and Tool Registry -> portal shows version/environment/verified quality  
  _Learner should notice:_ registry state as pipeline-generated operational metadata
- **M01.L13** — Blue/Green vs Canary vs A/B — Three mini diagrams showing full switch, gradual traffic ramp, and fixed experimental cohorts  
  _Learner should notice:_ visually distinguish technical rollout from product experiment
- **M01.L13** — AgentOps Infinity Loop — Production feedback -> triage -> Data/Tool/Frontend/Agent team branches -> separate CI/CD pipelines -> Dev/Staging/Prod -> Registries/Governance -> Production -> feedback  
  _Learner should notice:_ multiple independent loops connected through contracts and governance

## COURSE-016_Machine_Learning_Systems_and_MLOps_Engineering — 156 images

- **M01.L01** — Components of a production ML system — A clean systems diagram showing business requirements, user or API interface, data stack, model development, deployment infrastructure, prediction serving, monitoring, and model/data updates as connected components  
  _Learner should notice:_ the ML algorithm is only one component inside a larger feedback-driven system
- **M01.L01** — Hand-written rules versus learned patterns — A side-by-side diagram where traditional software receives explicit rules plus inputs to produce outputs, while ML receives example inputs and outputs during training and learns a model used for future inputs  
  _Learner should notice:_ ML replaces hand-specified decision logic with patterns learned from examples
- **M01.L01** — Research ML versus production ML — A two-column visual contrasting benchmark performance, static data, training throughput, and limited stakeholder constraints with production requirements, changing data, inference latency, fairness, interpretability, monitoring, and reliability  
  _Learner should notice:_ deployment introduces objectives and constraints that are absent from many research settings
- **M01.L01** — Latency and throughput with batching — Two timelines: one processing requests sequentially and one processing requests in batches, annotated with per-request latency and total requests per second  
  _Learner should notice:_ batching can increase throughput even when latency per batch also increases
- **M01.L01** — Research data versus production data — A side-by-side data-flow illustration showing a clean static benchmark dataset on the research side and noisy, streaming, changing, partially labeled data with privacy checks on the production side  
  _Learner should notice:_ production data is an evolving system dependency rather than a fixed file
- **M02.L01** — From business objective to ML metric — A layered diagram showing a business goal at the top, followed by a product goal, an ML objective, and finally model/system metrics  
  _Learner should notice:_ model metrics are proxies for a higher-level goal, not the final goal themselves
- **M02.L01** — Four requirements of production ML — A four-part diagram around an ML system labeled reliability, scalability, maintainability, and adaptability, with a short example for each  
  _Learner should notice:_ production quality is multidimensional and cannot be reduced to model accuracy alone
- **M02.L01** — Iterative ML system lifecycle — A circular lifecycle containing project scoping, data engineering, model development, deployment, monitoring/continual learning, and business analysis, with arrows looping back  
  _Learner should notice:_ deployment is not the end of ML development
- **M02.L01** — ML task type map — A compact tree showing regression and classification, with classification branching into binary, multiclass, high-cardinality, and multilabel examples  
  _Learner should notice:_ output structure determines the task formulation
- **M02.L01** — Coupled versus decoupled objectives — Side-by-side diagram: one model minimizing a weighted combined loss versus two independent models producing scores that are combined after inference  
  _Learner should notice:_ decoupling allows weights to change without retraining both models
- **M03.L01** — End-to-end data engineering pipeline for ML — A left-to-right diagram showing data sources feeding serialization formats, data models, storage/processing systems, inter-service dataflow, feature generation, and finally an ML model  
  _Learner should notice:_ the model is only one consumer at the end of a larger data pipeline
- **M03.L01** — Row-major versus column-major memory layout — A small table shown beside two storage layouts: one grouped by rows and one grouped by columns  
  _Learner should notice:_ why selecting a few columns is efficient in column-major storage while writing full rows fits naturally with row-major storage
- **M03.L01** — Relational vs document vs graph models — Three side-by-side mini diagrams: normalized relational tables with foreign keys, a self-contained nested document, and a node-edge graph  
  _Learner should notice:_ relational models emphasize tables, document models emphasize locality, and graph models emphasize relationships
- **M03.L01** — ETL pipeline — A simple three-stage pipeline showing raw sources entering Extract, then Transform with cleaning/joining/validation, then Load into a warehouse or database  
  _Learner should notice:_ transformation happens before data reaches the target store
- **M03.L01** — Request-driven versus event-driven dataflow — Side-by-side diagrams showing many direct service-to-service requests versus services communicating through a central event broker  
  _Learner should notice:_ how the broker reduces direct coupling among many services
- **M03.L01** — Batch versus stream feature computation — A split diagram showing historical data feeding a periodic batch job to create static features and a live event stream feeding a stream processor to create dynamic features, with both joining before model inference  
  _Learner should notice:_ real production models may need both slowly changing and real-time features
- **M04.L01** — Iterative training-data lifecycle — A cycle showing sampling, labeling, training, evaluation, discovering data issues, and updating the data before looping back  
  _Learner should notice:_ training-data creation continues as the model and environment evolve
- **M04.L01** — Sampling strategies comparison — One imbalanced population shown with three selection outcomes: simple random sampling, stratified sampling preserving each class, and weighted sampling favoring selected examples  
  _Learner should notice:_ the selection mechanism changes what information reaches training
- **M04.L01** — Reservoir sampling over a stream — A stream of numbered items entering a fixed-size reservoir, with later items sometimes replacing earlier items  
  _Learner should notice:_ memory stays bounded while all observed items retain equal sampling chance
- **M04.L01** — Data lineage for labeled examples — A training-data table with provenance fields pointing to source, collection date, annotator or labeling process, and label version  
  _Learner should notice:_ how provenance enables debugging when a subset of data causes model degradation
- **M04.L01** — Feedback loop signal strength versus delay — A user journey from impression to click, cart, purchase, review, and return, annotated with increasing feedback delay and changing signal strength  
  _Learner should notice:_ the trade-off between fast abundant feedback and slower stronger feedback
- **M04.L01** — Weak supervision with labeling functions — Several labeling functions applying noisy votes to unlabeled examples, followed by a combination/denoising stage that produces probabilistic training labels  
  _Learner should notice:_ programmatic labels can conflict and must be combined rather than blindly trusted
- **M04.L01** — Active learning loop — An unlabeled pool or data stream feeding a model, the model selecting high-uncertainty examples for human annotation, and the new labels returning to training  
  _Learner should notice:_ the model helps decide where scarce labeling effort should be spent
- **M04.L01** — Accuracy can hide minority-class failure — Two confusion matrices with equal overall accuracy but dramatically different cancer recall, followed by a small precision-recall concept diagram  
  _Learner should notice:_ why class-specific metrics matter in imbalanced problems
- **M04.L01** — Oversampling versus undersampling — An imbalanced two-class scatterplot shown before and after undersampling the majority class and oversampling the minority class  
  _Learner should notice:_ resampling changes the training distribution, not reality
- **M04.L01** — Class-imbalance intervention layers — A three-layer diagram showing metric choice, data-level resampling, and algorithm-level loss weighting as different intervention points  
  _Learner should notice:_ imbalance can be addressed at evaluation, data, and learning-algorithm levels
- **M04.L01** — Three families of data augmentation — Three panels showing label-preserving transformation, noisy/perturbed input, and synthesized/mixed examples  
  _Learner should notice:_ augmentation can create diversity by transformation, perturbation, or generating new examples
- **M05.L01** — Learned versus engineered features — A two-part diagram showing raw text/image going directly into a deep model that learns representations, alongside contextual metadata such as user, thread, and behavioral information being explicitly engineered into features  
  _Learner should notice:_ representation learning reduces but does not eliminate feature engineering
- **M05.L01** — MNAR versus MAR versus MCAR — Three small panels showing missing income caused by income itself, missing age explained by another observed group variable, and random missing job values with no visible pattern  
  _Learner should notice:_ the mechanism causing missingness affects how safely data can be removed or imputed
- **M05.L01** — Scaling and standardization comparison — A skewed or differently scaled pair of numerical features shown before and after min-max scaling and standardization  
  _Learner should notice:_ the transformation changes numerical scale while preserving the underlying examples
- **M05.L01** — UNKNOWN bucket versus feature hashing — A categorical stream with old and new brands, showing one approach mapping all unseen brands to UNKNOWN and another hashing every brand into a fixed index space with occasional collisions  
  _Learner should notice:_ why hashing handles open-ended vocabularies more gracefully
- **M05.L01** — Token embeddings plus positional embeddings — A short token sequence with one vector per token and one vector per position, followed by element-wise combination before the model  
  _Learner should notice:_ token identity and token order are supplied as separate signals
- **M05.L01** — Data leakage shortcut example — Training images where hospital or scanner artifacts correlate with the target, followed by deployment images where that artifact-target link disappears  
  _Learner should notice:_ the model learned a shortcut rather than the intended medical signal
- **M05.L01** — Leakage-safe preprocessing pipeline — A diagram showing deduplication/group handling and time-aware splitting before fitting imputation/scaling on train only, then applying those transformations to validation and test  
  _Learner should notice:_ test information must never influence fitted preprocessing steps
- **M05.L01** — Global versus local feature importance — A simple bar chart of global feature importance next to one individual prediction showing positive and negative feature contributions  
  _Learner should notice:_ a feature can be important to the model overall and also contribute differently to individual predictions
- **M06.L01** — Model selection as a multidimensional trade-off — A radar or matrix-style comparison of two model candidates across predictive quality, training cost, inference latency, data requirement, deployability, and interpretability  
  _Learner should notice:_ the highest-accuracy model is not automatically the best production choice
- **M06.L01** — Learning curves for two model families — A plot of validation performance versus number of training examples for a simple model and a higher-capacity model, where the simple model starts stronger but the higher-capacity model continues improving  
  _Learner should notice:_ the best model today may not be the best model after more data arrives
- **M06.L01** — Bagging workflow — One original dataset branching into several bootstrap samples, each training a model, with model outputs merged by majority vote or averaging  
  _Learner should notice:_ learners are trained independently on different resampled datasets
- **M06.L01** — Bagging versus boosting versus stacking — A three-panel comparison: independent bootstrapped models for bagging, sequential error-focused learners for boosting, and parallel base models feeding a meta-model for stacking  
  _Learner should notice:_ the different way each ensemble creates and combines diversity
- **M06.L01** — Reproducible experiment bundle — A central experiment ID connected to code version, data version, hyperparameters, environment, metrics, logs, and model artifacts  
  _Learner should notice:_ reproducing an ML experiment requires much more than remembering the learning rate
- **M06.L01** — Data, model, and pipeline parallelism — Three diagrams: replicated models processing different data shards, one model split across machines, and micro-batches flowing through model stages like an assembly line  
  _Learner should notice:_ what is split in each strategy: data, model components, or staged computation
- **M06.L01** — Three behavioral model tests — Three panels showing realistic perturbation with expected stability, a sensitive attribute swap with an unchanged expected prediction, and a meaningful feature increase with an expected directional output change  
  _Learner should notice:_ evaluation can test behavior, not just aggregate accuracy
- **M06.L01** — Calibration curve — A probability calibration plot with a diagonal perfect-calibration line and one model curve above/below it  
  _Learner should notice:_ calibration measures whether probability values themselves are trustworthy, not merely whether ranking is correct
- **M06.L01** — Aggregate metric versus slice metrics — A large overall accuracy bar beside separate majority/minority bars for two models, showing how the model with the best overall score can perform poorly on one subgroup  
  _Learner should notice:_ aggregate metrics can hide critical weaknesses
- **M07.L01** — Demo deployment versus production deployment — A simple model-plus-API box on the left and a production system on the right containing load balancing, monitoring, alerts, model versions, feature pipelines, and multiple clients  
  _Learner should notice:_ exposing an endpoint is only one small part of production deployment
- **M07.L01** — Model portfolio at production scale — A product with several ML-powered functions connected to many deployed models across regions or countries  
  _Learner should notice:_ production ML infrastructure often manages fleets of models, not one isolated model
- **M07.L01** — Batch versus online prediction architecture — Side-by-side pipelines showing batch feature computation and periodic prediction storage versus request-time model inference through a prediction service  
  _Learner should notice:_ batch prediction computes ahead of requests while online prediction computes in response to requests
- **M07.L01** — Feature freshness and prediction mode — Three horizontal pipelines for batch prediction, online prediction with precomputed batch features, and online prediction combining batch and streaming features  
  _Learner should notice:_ 'online feature' does not necessarily mean 'streaming feature'
- **M07.L01** — Training-serving skew from duplicate feature pipelines — Two paths computing the same feature: an offline batch training pipeline and an online streaming inference pipeline, first matching and then diverging after only one path changes  
  _Learner should notice:_ how duplicated feature logic creates inconsistent model inputs
- **M07.L01** — Four model compression methods — Four panels showing low-rank decomposition, teacher-student distillation, weight pruning to sparse connections, and 32-bit to 8-bit quantization  
  _Learner should notice:_ all four reduce deployment cost through different mechanisms
- **M07.L01** — Cloud versus edge inference — A mobile device sending data across a network to a cloud model versus the same device running the model locally, with callouts for cloud cost, network latency, privacy, memory, compute, and battery  
  _Learner should notice:_ moving inference to the edge removes some network costs but introduces device constraints
- **M07.L01** — Framework to hardware through intermediate representations — Several ML frameworks feeding a shared high-level IR, then lower-level IR, then branching to CPU, GPU, and accelerator machine code  
  _Learner should notice:_ how IRs reduce the need for every framework to directly support every hardware backend
- **M07.L01** — Operator fusion reduces memory traffic — A before/after diagram where two operators each read and write an intermediate tensor versus one fused operator that keeps the intermediate result local  
  _Learner should notice:_ reducing memory movement can speed inference even if the mathematical operations are unchanged
- **M08.L01** — Post-deployment ML lifecycle — A circular flow from deployment to monitoring, detection, diagnosis, correction/retraining, and redeployment  
  _Learner should notice:_ production ML is a continuing feedback process rather than a final release
- **M08.L01** — Operational failure versus silent ML failure — Two examples: one request timing out with an obvious error, and one request returning a normal-looking but incorrect prediction  
  _Learner should notice:_ ML failure can occur while software health looks normal
- **M08.L01** — Degenerate recommendation feedback loop — Two items begin with nearly equal scores, one is ranked slightly higher, receives more exposure and clicks, then receives a larger future score  
  _Learner should notice:_ how model outputs can change future training data
- **M08.L01** — Position bias correction — A ranked recommendation list where top position affects probability of being seen, followed by a two-stage model separating 'seen/considered' from 'clicked given seen'  
  _Learner should notice:_ clicks combine item preference with exposure position
- **M08.L01** — Covariate shift, label shift, and concept drift — Three panels showing changes to P(X), P(Y), and P(Y  
  _Learner should notice:_ X), with the unchanged conditional or marginal distribution noted in each case
- **M08.L01** — Drift detection from source to target distributions — Two overlaid feature distributions with summary-statistic comparison and a two-sample test indicator  
  _Learner should notice:_ the difference between simple summary monitoring and a formal statistical comparison
- **M08.L01** — Sliding versus cumulative monitoring metrics — A time series with a sudden performance drop, alongside a responsive sliding metric and a smoother cumulative metric that barely moves  
  _Learner should notice:_ how cumulative statistics can hide recent incidents
- **M08.L01** — Four monitoring layers in an ML pipeline — A pipeline from raw inputs to transformed features to predictions to accuracy/feedback metrics, with monitoring attached at each layer  
  _Learner should notice:_ the trade-off between upstream root-cause visibility and downstream monitoring simplicity
- **M08.L01** — Feature monitoring with schema and drift checks — A tabular feature set with range checks, category checks, missing-value checks, and distribution comparisons, followed by alerts filtered by model impact  
  _Learner should notice:_ feature drift alone does not prove model degradation
- **M08.L01** — Distributed tracing across microservices — One request ID traveling through several services with timestamps and logs at each hop  
  _Learner should notice:_ how a shared trace identifier reconstructs the path of one request
- **M09.L01** — Continual-learning production loop — A circular production pipeline showing fresh data and feedback feeding candidate training, evaluation, promotion, deployment, and monitoring  
  _Learner should notice:_ continual learning requires an end-to-end update system, not merely a training function
- **M09.L01** — Champion-challenger model update — A deployed champion copied into one or more challengers, with fresh-data training and an evaluation gate before promotion  
  _Learner should notice:_ training and deployment are separated by a quality gate
- **M09.L01** — Stateless versus stateful training — Two parallel timelines: stateless updates repeatedly initialize from scratch using large historical windows, while stateful updates continue from the previous checkpoint using smaller fresh-data windows  
  _Learner should notice:_ the difference in reused model state and data requirements
- **M09.L01** — Fresh-data paths for continual learning — Application events entering a real-time transport, with one path going directly to fresh training/label extraction and another slower path through a warehouse  
  _Learner should notice:_ how bypassing warehouse delay can make training data fresher
- **M09.L01** — Label computation from recommendation and click logs — A recommendation event and a later click event joined by user/item/context identifiers to create a supervised label  
  _Learner should notice:_ user behavior must be matched back to the prediction that generated the opportunity
- **M09.L01** — Four stages of continual-learning maturity — A staircase from manual stateless retraining to automated stateless, automated stateful, and finally trigger-driven continual learning  
  _Learner should notice:_ the progression is mostly about infrastructure automation, state management, monitoring, and evaluation
- **M09.L01** — Log-and-wait feature reuse — A production inference request whose computed features are logged, then later joined with delayed feedback to create a training example  
  _Learner should notice:_ retraining can reuse the exact features seen by the live model
- **M09.L01** — Trigger-driven continual-learning pipeline — Four trigger sources—time, performance, data volume, drift—feeding an update pipeline with training, evaluation gate, model store, and deployment  
  _Learner should notice:_ retraining triggers depend on trustworthy monitoring
- **M09.L01** — Measuring the value of data freshness — Several training windows ending progressively closer to a fixed modern test window, with model performance increasing or flattening as training data becomes fresher  
  _Learner should notice:_ update frequency should be supported by measured performance gain rather than intuition
- **M09.L01** — Monitoring versus test in production — A split diagram where monitoring observes one production model, while test in production deliberately routes or duplicates live traffic among candidate models for comparison  
  _Learner should notice:_ the passive versus proactive distinction
- **M09.L01** — Shadow deployment — One production request duplicated to champion and challenger, with only champion output returned to the user and challenger output stored for analysis  
  _Learner should notice:_ the candidate sees real traffic without affecting users
- **M09.L01** — A/B testing versus interleaving — A/B side shows separate users receiving full lists from A or B; interleaving side shows one list composed of alternating/random contributions from A and B  
  _Learner should notice:_ interleaving compares ranking preferences within the same user experience
- **M09.L01** — Exploration versus exploitation for model traffic — Three candidate models with estimated rewards, most traffic going to the current best while a smaller amount explores uncertain alternatives  
  _Learner should notice:_ bandit allocation adapts as evidence changes
- **M09.L01** — Automated model promotion pipeline — A gated pipeline from new model artifact through offline tests, backtest, shadow/A-B/canary or another production test, then promotion or rejection  
  _Learner should notice:_ model updates move through standardized quality gates
- **M10.L01** — Infrastructure as the foundation of the ML lifecycle — A stack where model development, deployment, monitoring, and continual learning sit above shared infrastructure  
  _Learner should notice:_ earlier ML-system practices depend on enabling infrastructure beneath them
- **M10.L01** — Four layers of ML infrastructure — A four-level stack showing storage/compute at the foundation, resource management, ML platform services, and development environment/user workflows  
  _Learner should notice:_ the layers solve different but connected infrastructure problems
- **M10.L01** — Compute bottleneck mental model — A pipeline from storage to memory to compute, annotated with memory capacity, I/O bandwidth, theoretical FLOPS, and achieved utilization  
  _Learner should notice:_ raw compute capability is useful only if data can reach it efficiently
- **M10.L01** — Public cloud versus private infrastructure trade-off — A comparison showing cloud elasticity and low startup burden versus private infrastructure's higher up-front investment and potential long-term cost control  
  _Learner should notice:_ the economically attractive option can change with scale
- **M10.L01** — Notebook statefulness double-edged sword — One side shows quick rerun after a late-cell failure; the other shows cells executed out of order creating hidden state  
  _Learner should notice:_ the same statefulness that accelerates exploration can damage reproducibility
- **M10.L01** — Dockerfile to image to containers — A Dockerfile producing one immutable image, then multiple running containers from that image, with a registry between build and deployment  
  _Learner should notice:_ the difference between build instructions, packaged environment, and running instances
- **M10.L01** — Cron versus scheduler versus orchestrator — Three layers showing fixed-time triggering by cron, dependency/resource-aware job scheduling, and machine/cluster provisioning by an orchestrator  
  _Learner should notice:_ these tools operate at different abstraction levels
- **M10.L01** — ML workflow DAG — Data ingestion flowing into feature extraction, branching to two model-training tasks, joining at comparison, then conditionally deploying the winner  
  _Learner should notice:_ parallel tasks, dependencies, and conditional execution
- **M10.L01** — Workflow-tool design dimensions — A comparison matrix with Python-vs-YAML definition, dynamic workflows, parameterization, container-per-step design, Kubernetes dependence, and local/cloud execution  
  _Learner should notice:_ workflow tools optimize different developer and infrastructure trade-offs
- **M10.L01** — Shared ML platform across teams — Several ML applications such as fraud, churn, ranking, and pricing consuming common deployment, model-store, feature-store, and monitoring capabilities  
  _Learner should notice:_ why shared platform investment becomes more valuable as ML adoption grows
- **M10.L01** — Model store artifact graph — A model version at the center connected to model definition, weights, feature/predict code, dependencies, data version, generation code, experiment artifacts, owner and task tags  
  _Learner should notice:_ a deployable model is a bundle of related artifacts and lineage
- **M10.L01** — Feature-store three-problem model — A central feature store with three branches labeled catalog/management, computation/storage, and training-serving consistency, connected to multiple models  
  _Learner should notice:_ 'feature store' can refer to several related but distinct capabilities
- **M10.L01** — End-to-end MLOps infrastructure stack — A layered architecture combining development environment, shared ML platform, workflow/resource management, and storage/compute, with model-development-to-production flow through all layers  
  _Learner should notice:_ how the chapter's individual infrastructure components fit into one coherent system
- **M10.L02** — Humans around an ML system — An ML system connected to end users, business stakeholders, data scientists, platform engineers, subject-matter experts, and wider society  
  _Learner should notice:_ system quality depends on technical and human relationships
- **M10.L02** — Deterministic software versus probabilistic ML UX — A side-by-side comparison of consistent deterministic behavior and probabilistic mostly-correct behavior with variable latency  
  _Learner should notice:_ why ML interfaces need explicit design for uncertainty and inconsistency
- **M10.L02** — Consistency-accuracy recommendation trade-off — One interface keeps previously used filters stable while another constantly replaces them with the newest ranked choices  
  _Learner should notice:_ why UX consistency can justify not serving the instantaneous top prediction
- **M10.L02** — Human-in-the-loop candidate selection — One request producing several model outputs rendered into user-evaluable alternatives, with a human selecting or editing the final result  
  _Learner should notice:_ good UX translates model uncertainty into an action the user can understand
- **M10.L02** — Smooth-failing inference path — A request routed to a high-quality primary model with a latency threshold and a guaranteed-fast fallback route  
  _Learner should notice:_ graceful degradation can protect user experience without abandoning the better model
- **M10.L02** — SME contributions across the ML lifecycle — A lifecycle from problem formulation to data, features, evaluation, and UI with SME contribution points at each stage  
  _Learner should notice:_ domain expertise is useful far beyond the initial labeling task
- **M10.L02** — Full-cycle ownership through infrastructure abstractions — Data scientists defining data, steps, dependencies, and resource requirements above specialist-built infrastructure tools  
  _Learner should notice:_ how Chapter 10 tooling enables the team model discussed in Chapter 11
- **M10.L02** — Responsible-AI failure chain in automated grading — Objective choice feeding model decisions, subgroup evaluation, and public transparency, with failure markers at all three stages  
  _Learner should notice:_ how harm can arise from the overall system design
- **M10.L02** — Indirect privacy leakage after anonymization — An aggregated map with direct identities removed but distinctive patterns still exposing sensitive locations or activity  
  _Learner should notice:_ privacy risk can survive removal of names and obvious identifiers
- **M10.L02** — Bias sources across the ML lifecycle — A pipeline from training data through labeling, feature engineering, objective design, and evaluation, with possible bias entering at each stage  
  _Learner should notice:_ Responsible AI is not confined to model architecture
- **M10.L02** — Privacy-accuracy trade-off by subgroup — An overall performance curve declining modestly as privacy strengthens, while an underrepresented subgroup declines more sharply  
  _Learner should notice:_ average privacy-performance trade-offs can hide unequal impact
- **M10.L02** — Similar overall accuracy but different subgroup harm — Two models with nearly equal top-line accuracy but different error rates for a small underrepresented subgroup  
  _Learner should notice:_ why deployment optimization needs fine-grained reevaluation
- **M10.L02** — Model card layout — A one-page structured model card with model details, intended use, factors, metrics, data, subgroup analysis, ethical considerations, and caveats  
  _Learner should notice:_ model documentation should communicate context and limitations, not just accuracy
- **M11.L01** — Continuous delivery feedback loop — A circular process from code/model change to build, test, package, deploy, observe, and improve  
  _Learner should notice:_ feedback and improvement are built into the release process
- **M11.L01** — What a packaged ML model contains — A container boundary around prediction-service code, exact dependencies, tokenizer/preprocessing logic, runtime library, and serialized model  
  _Learner should notice:_ packaging includes the inference environment, not only weights
- **M11.L01** — CI/CD model packaging workflow — Git push triggering source checkout, cloud authentication, model-registry download, container build, checks, and registry publish  
  _Learner should notice:_ how the model artifact and source code are reunited automatically during delivery
- **M11.L01** — Generic CI/CD versus ML-specific pipeline — A comparison of generic source/build/test automation and an ML pipeline with data prep, GPU training, evaluation, model registry, and deployment  
  _Learner should notice:_ the shared automation concept but different domain-specific capabilities
- **M11.L01** — Blue-green versus canary deployment — Blue-green shows separate old/new environments and one traffic switch; canary shows progressive traffic percentages with rollback  
  _Learner should notice:_ both reduce release risk in different ways
- **M11.L01** — AutoML inside KaizenML — A small AutoML circle inside a much larger KaizenML system containing data, features, software, testing, deployment, monitoring, and feedback  
  _Learner should notice:_ automated modeling is only one part of system-wide automation
- **M11.L01** — Data warehouse and feature store roles — Raw data flowing to a warehouse for analytics and to a feature pipeline/store that supplies reusable batch/online ML features  
  _Learner should notice:_ feature stores specialize repeated data preparation for ML use
- **M11.L01** — Managed AutoML lifecycle — Prepared labeled data flowing through inspection, automated training, evaluation, and either hosted endpoint or edge-model export  
  _Learner should notice:_ how one platform can integrate modeling with deployment destinations
- **M11.L01** — Explainability as an MLOps dashboard — An ML operations dashboard combining infrastructure health with global feature importance and one local prediction explanation  
  _Learner should notice:_ model behavior can be monitored alongside software behavior
- **M11.L01** — End-to-end KaizenML automation loop — A full loop from data and feature store through AutoML, evaluation, registry, CI/CD packaging, canary deployment, and production feedback  
  _Learner should notice:_ how both source chapters combine into one continuous-improvement system
- **M12.L01** — Observability questions around a production ML system — A deployed ML service surrounded by logs, metrics, alerts, model-quality signals, and data-drift signals  
  _Learner should notice:_ observability exists to explain system state, not merely collect data
- **M12.L01** — Four monitoring layers — A stack showing infrastructure health, application health, ML/model health, and business/product health  
  _Learner should notice:_ lower layers can look healthy while higher-level outcomes fail
- **M12.L01** — Cloud MLOps observability hub — Servers, training jobs, application logs, and model endpoints all sending logs/metrics to a central observability service, which feeds dashboards, alerts, autoscaling, and human analysis  
  _Learner should notice:_ the many-to-one collection pattern
- **M12.L01** — Context-rich exception logging — A remote job failure where a structured error message includes operation context and a traceback, contrasted with a generic one-line print message  
  _Learner should notice:_ how preserved context makes diagnosis much easier
- **M12.L01** — Python logger hierarchy — A root logger above application logger and library loggers, with different severity thresholds on each branch  
  _Learner should notice:_ one noisy dependency can be tuned without silencing the whole application
- **M12.L01** — Counter timer value metric types — Three cards showing a count of missing values, a timer for prediction latency, and a numeric value such as database size or model score  
  _Learner should notice:_ how different operational questions map to different metric types
- **M12.L01** — Baseline versus target monitoring — A reference dataset generating baseline statistics/constraints, then new serving data being compared against them to produce violations  
  _Learner should notice:_ the difference between the reference and the data being monitored
- **M12.L01** — SageMaker drift monitoring lifecycle — Endpoint traffic being captured to S3, a reference dataset creating baseline statistics and constraints, then an hourly monitor comparing traffic and sending metrics/reports  
  _Learner should notice:_ the three phases: capture, baseline, scheduled comparison
- **M12.L01** — Harmful drift versus seasonal change — Two time-series examples: one showing a sudden schema/unit anomaly and one showing an expected seasonal sales cycle  
  _Learner should notice:_ domain context determines whether distribution change is alarming
- **M13.L01** — AWS MLOps abstraction ladder — A ladder from raw infrastructure/building blocks through containers and serverless to managed AI APIs and full ML platforms  
  _Learner should notice:_ higher levels remove more operational work while lower levels provide more control
- **M13.L01** — Simple S3 continuous-delivery pipeline — Source repository flowing to an automated build step, static-site generation, and S3 website deployment  
  _Learner should notice:_ the source-of-truth and repeatable-deployment pattern
- **M13.L01** — Serverless function mental model — Events from API, schedule, and S3 all invoking a cloud function, with server infrastructure hidden beneath the function abstraction  
  _Learner should notice:_ serverless removes server-management responsibility rather than physical servers
- **M13.L01** — Container portability for AWS MLOps — One container image running locally, stored in ECR, then deployed to Fargate/App Runner or another target  
  _Learner should notice:_ the same packaged runtime can move across environments
- **M13.L01** — Accuracy explainability operations triangle — A triangle with prediction accuracy, explainability, and operations at the corners, with continuous improvement in the center  
  _Learner should notice:_ production success is a systems trade-off rather than accuracy alone
- **M13.L01** — MLOps cookbook project structure — A central mlib.py/model layer connected to CLI, utility CLI, Flask API, notebook, Dockerfile, requirements, and deployment targets  
  _Learner should notice:_ interfaces reuse the same model logic rather than duplicating it
- **M13.L01** — One Flask model service, multiple deployment targets — A containerized Flask prediction service branching to local Docker, Fargate, App Runner, Elastic Beanstalk, and other compatible targets  
  _Learner should notice:_ how containerization separates application packaging from deployment destination
- **M13.L01** — AWS SAM development loop — SAM project files feeding local container-based invocation, then build and guided deployment to Lambda/API Gateway  
  _Learner should notice:_ serverless infrastructure and application logic are developed together
- **M13.L01** — AWS MLOps service-selection matrix — Three columns for small/fast serverless+AI API, containerized App Runner/CaaS, and larger enterprise SageMaker workflows, compared by control, speed, and operational scope  
  _Learner should notice:_ service choice depends on organizational needs
- **M13.L01** — Progressive AWS MLOps adoption — A maturity path from managed API/serverless quick win to containerized service, automated delivery, monitoring, and fuller ML platform adoption  
  _Learner should notice:_ platform complexity grows with actual needs
- **M14.L01** — Azure ML interface map — Azure ML at the center connected to Studio, Designer, notebooks, AutoML, CLI, and Python SDK, all reaching shared models, data, compute, and deployment services  
  _Learner should notice:_ different interfaces operate on the same underlying lifecycle
- **M14.L01** — Secure automation versus permission bypass — Two paths: service identity with scoped permissions versus a shortcut using overly broad permissions, with the second path leading to security exposure  
  _Learner should notice:_ convenience and secure automation are not the same thing
- **M14.L01** — Reproducible Azure compute environment — Several engineers connecting to a managed Azure compute instance with the same libraries, notebook environment, workspace, and data access  
  _Learner should notice:_ how a shared environment reduces machine-specific differences
- **M14.L01** — Azure model registry version history — One model name with versions v1, v2, v3, each with metadata and a production pointer, plus a rollback arrow from v3 to v2  
  _Learner should notice:_ why version identity matters during release and rollback
- **M14.L01** — Azure deployment target trade-off — A simple test deployment path toward ACI and a scalable production deployment path toward AKS/Kubernetes  
  _Learner should notice:_ target choice should follow workload and environment requirements
- **M14.L01** — From logs to observability — A deployed model sending requests, failures, latency, exceptions, and logs into an Application Insights-style dashboard  
  _Learner should notice:_ observability combines multiple signals into a system-level story
- **M14.L01** — Production issue reproduced locally — A production Azure container and an equivalent local Docker container receiving the same failing request, with inspection tools attached locally  
  _Learner should notice:_ reproducibility enables safer and deeper debugging
- **M14.L01** — Azure pipeline step anatomy — A pipeline step showing inputs, Python script/arguments, outputs, compute target, and runtime configuration  
  _Learner should notice:_ execution code and execution environment are separate concerns
- **M14.L01** — Iterative Azure ML lifecycle — A circular lifecycle from training to validation, registration/versioning, deployment, observability, and feedback returning to data/training  
  _Learner should notice:_ production feedback changes earlier stages rather than ending the process
- **M15.L01** — GCP MLOps technology ecosystem — Google Cloud surrounded by Kubernetes, TensorFlow, Go, BigQuery, and Vertex AI, with arrows showing portability beyond one cloud  
  _Learner should notice:_ the source's emphasis on widely adopted technologies rather than only proprietary services
- **M15.L01** — GKE versus Cloud Run abstraction — The same ML container shown on a detailed Kubernetes/GKE stack and on a simplified Cloud Run managed-service stack  
  _Learner should notice:_ the application can be similar while operational responsibility changes
- **M15.L01** — BigQuery-centered MLOps flow — Public/streaming/storage data feeding BigQuery, with outputs branching to analytics/BI and machine-learning/Vertex AI workflows  
  _Learner should notice:_ why keeping data and some ML operations close together simplifies the pipeline
- **M15.L01** — Split CI/CD responsibilities — A Git push feeding GitHub Actions for tests/lint, then a deployment path using Cloud Build into GCP  
  _Learner should notice:_ how two automation systems can serve different strengths in one workflow
- **M15.L01** — Kubernetes HPA control loop — Metrics feeding an autoscaler that changes the replica/pod count behind a load-balanced ML service  
  _Learner should notice:_ the closed loop from observation to scaling action
- **M15.L01** — Serverless DataOps and AI composition — A Cloud Function receiving an event, reading external or cloud data, calling an AI API, and returning/publishing a result  
  _Learner should notice:_ how serverless functions glue managed services together
- **M15.L01** — Light versus heavy GCP MLOps — A lightweight path with App Engine/Cloud Build/API call beside a broader Vertex AI path with data/model management, Feature Store, explainability, and quality tracking  
  _Learner should notice:_ the trade-off between simplicity and platform capability
- **M15.L01** — End-to-end GCP MLOps system — A flow from source and CI/CD through storage/BigQuery, modeling/Vertex AI, deployment targets, monitoring, and feedback  
  _Learner should notice:_ individual GCP services fit into a broader lifecycle rather than being isolated tools
- **M16.L01** — Shell script to Python growth path — A tiny one-purpose shell script on the left and a larger Python CLI with logging, tests, modules, and dependencies on the right  
  _Learner should notice:_ tool choice changes as complexity and maintainability needs grow
- **M16.L01** — Python virtual environment isolation — System Python outside and two isolated project environments containing different dependency versions  
  _Learner should notice:_ project dependencies no longer collide with the system or each other
- **M16.L01** — Three CSV quality failures — A table illustrating an all-null column, an unwanted Unnamed index column, and hidden carriage-return characters inside a text field  
  _Learner should notice:_ how small formatting/data issues can break downstream ML workflows
- **M16.L01** — Failure-to-automation feedback loop — A manual dataset failure becoming a reusable linter rule that protects later ML workflows  
  _Learner should notice:_ automation stores lessons learned from past incidents
- **M16.L01** — Monolith versus reusable microservice pieces — An unstable tall Jenga-like monolith beside smaller independent service blocks that can be rearranged and reused  
  _Learner should notice:_ how reducing coupling improves maintainability and reuse
- **M16.L01** — Authenticated Cloud Function request path — Client sending an authenticated HTTP POST with JSON into a serverless function, with billing/security boundary highlighted  
  _Learner should notice:_ HTTP convenience does not remove the need for authentication
- **M16.L01** — Cloud-backed CLI architecture — A terminal command calling a packaged Click CLI, which authenticates and sends HTTP JSON to a cloud function that invokes a managed ML API  
  _Learner should notice:_ how packaging hides repetitive cloud plumbing behind one stable command
