"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Callable, List

import numpy

from pyjamas.rimage.rimclassifier.rimclassifier import rimclassifier
import pyjamas.rimage.rimclassifier.nn.cnn as cnn
from pyjamas.rimage.rimutils import rimutils


class LeNet(rimclassifier):
    CONV_FILTER_SIZE: List[int] = [5, 5]
    CONV_FILTER_NUMBER: List[int] = [20, 50]
    ACTIVATION_FN: Callable = cnn.tanh
    POOL_SIZE: List[int] = [2, 2]
    FULLY_CONNECTED_NEURON_NUMBER: int = 500
    OUTPUT_CLASSES: int = 2
    MINI_BATCH_SIZE: int = 16
    EPOCHS: int = 60
    LEARNING_RATE: float = 0.001
    GPU: bool = False

    def __init__(self, parameters: dict = None):
        super().__init__(parameters)

        mini_batch_size: int = parameters.get('mini_batch_size', LeNet.MINI_BATCH_SIZE)
        epochs: int = parameters.get('epochs', LeNet.EPOCHS)
        learning_rate: float = parameters.get('learning_rate', LeNet.LEARNING_RATE)

        # These parameters have standard values for LeNet and do not need to be modified.
        # This code is here in case in the future we want to allow changes.
        conv_filter_size: List[int] = parameters.get('conv_filter_size', LeNet.CONV_FILTER_SIZE)
        conv_filter_number: List[int] = parameters.get('conv_filter_number', LeNet.CONV_FILTER_NUMBER)
        activation_fn: Callable = parameters.get('activation_fn', LeNet.ACTIVATION_FN)
        pool_size: List[int] = parameters.get('pool_size', LeNet.POOL_SIZE)
        fully_connected_neuron_number = parameters.get('fully_connected_neuron_number', LeNet.FULLY_CONNECTED_NEURON_NUMBER)
        output_classes: int = parameters.get('output_classes', LeNet.OUTPUT_CLASSES)
        gpu: bool = parameters.get('GPU', LeNet.GPU)

        conv_layer_2_size: List[int] = [(self.train_image_size[0]-conv_filter_size[0]+1)//pool_size[0],
                                        (self.train_image_size[1]-conv_filter_size[1]+1)//pool_size[1]]

        fully_connected_size: List[int] = [(conv_layer_2_size[0]-conv_filter_size[0]+1)//pool_size[0],
                                           (conv_layer_2_size[1]-conv_filter_size[1]+1)//pool_size[1]]

        self.classifier = parameters.get('classifier', cnn.Network([
            cnn.ConvPoolLayer(image_shape=(mini_batch_size, 1, self.train_image_size[0], self.train_image_size[1]),
                              filter_shape=(conv_filter_number[0], 1, conv_filter_size[0], conv_filter_size[1]),
                              poolsize=(pool_size[0], pool_size[1]),
                              activation_fn=activation_fn),
            cnn.ConvPoolLayer(image_shape=(mini_batch_size, conv_filter_number[0], conv_layer_2_size[0], conv_layer_2_size[1]),
                              filter_shape=(conv_filter_number[1], conv_filter_number[0], conv_filter_size[0], conv_filter_size[1]),
                              poolsize=(pool_size[0], pool_size[1]),
                              activation_fn=activation_fn),
            cnn.FullyConnectedLayer(n_in=conv_filter_number[1] * fully_connected_size[0] * fully_connected_size[1], n_out=fully_connected_neuron_number, activation_fn=activation_fn),
            cnn.SoftmaxLayer(n_in=fully_connected_neuron_number, n_out=output_classes)],
            epochs, mini_batch_size, learning_rate, gpu))

    def predict(self, image: numpy.ndarray) -> (numpy.ndarray, numpy.ndarray):
        if self.fc is None or self.fc is False or image is None or image is False:
            return False

        image = numpy.squeeze(image)

        row_rad = int(numpy.floor(self.train_image_size[0] / 2))
        col_rad = int(numpy.floor(self.train_image_size[1] / 2))

        self.object_positions: list = []
        self.object_map: numpy.ndarray = numpy.zeros(image.shape)
        box_list: list = []
        prob_list: list = []

        subimages = rimutils.generate_subimages(image, self.train_image_size, self.step_sz)

        row_ims = int(numpy.ceil((image.shape[0]-self.train_image_size[0]+1) / self.step_sz[0]))
        col_ims = int(numpy.ceil((image.shape[1]-self.train_image_size[1]+1) / self.step_sz[1]))

        n_iter = (row_ims * col_ims) // self.classifier.mini_batch_size

        for theiter in range(n_iter):
            im_batch = []
            rows = []
            cols = []

            for i in range(self.classifier.mini_batch_size):
                asubim, row, col = next(subimages)
                self.fc.calculate_features(asubim)
                im_batch.append(self.fc.gimme_features().squeeze())
                rows.append(row)
                cols.append(col)

            output = self.classifier.predict_batch(numpy.asarray(im_batch))

            theclass = output[0]
            theP = output[1]

            # If there is an object, store the position of the bounding box.
            for aclass, aP, arow, acol in zip(theclass, theP, rows, cols):
                if aclass == 1:
                    minrow = arow - row_rad
                    maxrow = arow + row_rad
                    if self.train_image_size[0] % 2 == 1:
                        maxrow += 1

                    mincol = acol - col_rad
                    maxcol = acol + col_rad
                    if self.train_image_size[1] % 2 == 1:
                        maxcol += 1

                    self.object_positions.append([arow, acol])
                    self.object_map[arow, acol] = 1
                    box_list.append([minrow, mincol, maxrow, maxcol])
                    prob_list.append(aP)  # theP[0][0] contains the probability of the other class (-1)

                # print(f"{arow}, {acol}: class - {aclass}, prob - {aP}")

        self.box_array = numpy.asarray(box_list)
        self.prob_array = numpy.asarray(prob_list)

        return self.box_array.copy(), self.prob_array.copy()
