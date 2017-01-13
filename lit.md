# Relevant literature overview

* **Deep Convolution Networks for Compression Artifacts Reduction**
*Dong et al. April 2015 [link](https://arxiv.org/pdf/1504.06993.pdf)*
AR-CNN. Really the first paper about using CNNs for artifact reduction, often used as baseline in the other papers.

* **Compression Artifacts Removal Using Convolutional Neural Networks**
*Svoboda et al. 2016 [link](https://arxiv.org/pdf/1605.00366.pdf)*
Residual learning/skip architecture deep CNN, pretty simple (8 layers). Beats AR-CNN

* **Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising**
*Zhang et al. August 2016 [link](https://arxiv.org/pdf/1608.03981v1.pdf)*
Skip connection architecture, but as an added gimmick takes the residual image as the target.

* **CAS-CNN: A Deep Convolutional Neural Network for Image Compression Artifact Suppression**
*Cavigelli et al. November 2016 [link](https://arxiv.org/pdf/1611.07233v1.pdf)*
Deep, skip architecture with multiple exit points (loss at different depths). Similar to Unet (but much more complex architecture). The same architecture can do many tasks such as denoising, JPEG artifact removal, and more (large capacity).


* **D3: Deep Dual-Domain Based Fast Restoration of JPEG-Compressed Images**
*Zhang et al. 2014  [link](https://arxiv.org/pdf/1601.04149v3.pdf)*
End to end training of *One-Step Sparse Inference* modules which are efficient feed-forward approximations of sparse codings. Much faster and outperforms AR-CNN (like they all do).



* **Image Restoration Using Convolutional Auto-encoders with Symmetric Skip Connections**
*Xiao-Jiao Mao et al. June 2016 [link](https://arxiv.org/pdf/1606.08921v3.pdf)*

* **One-to-Many Network for Visually Pleasing Compression Artifacts Reduction**
*Guo et al. November 2016 [link](https://arxiv.org/pdf/1611.04994v1.pdf)*
Approach that uses perceptual loss as a measure for training as well. Also, JPEG loss (if a pixel is out of possible bounds extra loss is applied).
They also do deconvolutions (learned upsampling) by what they call "shift-and-average", which I think is the same as shift-and-stitch described by Long et al. (original fully convolutional neural networks paper). This would eliminate grid-like artifacts due to upsampling and demonstrate a *"dramatic visual improvement"*.

* **FractalNet: Ultra-Deep Neural Networks without Residuals**
*Larsson et al. May 2016 [link](https://arxiv.org/pdf/1605.07648v2.pdf)*


* **U-Net: Convolutional Networks for Biomedical Image Segmentation**
*Ronneberger et al. May 2015 [link](https://arxiv.org/pdf/1505.04597v1.pdf)
Unet architecture for dense predictions, which is really per pixel regression like our problem.
