# finger_net
finger_net is  neural network that finds minutiaes on fingerprint image.

## How it works
Architecture was inspired by [MENet](https://www.benjaminrosman.com/papers/ijcb17.pdf).
It takes enhaced by gabor filter fingerprint image and returns probability matrix that corresponds to probability whether a
given square has minutiae or not.I recommend use [this implementation](https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python) of Gabor filter
Model uses [Convolutioanl sliding window](https://medium.com/ai-quest/convolutional-implementation-of-the-sliding-window-algorithm-db93a49f99a0) algorithm to produce the probabality matrix 
Then minutiaes points are extracted from probabilty matrix.

## Fingerprint comparison
To compare two fingerprint you need to find corresponding minutiaes. Therefore  affine transformation is needed.
To do this RANSAC algorithm was used. 
Determining whether fingerprints are same or not is made by dividing quantity of matching to all points

