import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from . import utils
from . import common
from . import backbone


def YOLOv4(input_layer, num_class):
    route_1, route_2, conv = backbone.CSPDarknet53()(input_layer)

    route = conv
    conv = common.convolutional(conv, (1, 1, 512, 256))
    conv = layers.UpSampling2D()(conv)
    route_2 = common.convolutional(route_2, (1, 1, 512, 256))
    conv = tf.concat([route_2, conv], axis=-1)

    conv = common.convolutional(conv, (1, 1, 512, 256))
    conv = common.convolutional(conv, (3, 3, 256, 512))
    conv = common.convolutional(conv, (1, 1, 512, 256))
    conv = common.convolutional(conv, (3, 3, 256, 512))
    conv = common.convolutional(conv, (1, 1, 512, 256))

    route_2 = conv
    conv = common.convolutional(conv, (1, 1, 256, 128))
    conv = layers.UpSampling2D()(conv)
    route_1 = common.convolutional(route_1, (1, 1, 256, 128))
    conv = tf.concat([route_1, conv], axis=-1)

    conv = common.convolutional(conv, (1, 1, 256, 128))
    conv = common.convolutional(conv, (3, 3, 128, 256))
    conv = common.convolutional(conv, (1, 1, 256, 128))
    conv = common.convolutional(conv, (3, 3, 128, 256))
    conv = common.convolutional(conv, (1, 1, 256, 128))

    route_1 = conv
    conv = common.convolutional(conv, (3, 3, 128, 256))
    conv_sbbox = common.convolutional(
        conv, (1, 1, 256, 3 * (num_class + 5)), activate=False, bn=False
    )

    conv = common.convolutional(route_1, (3, 3, 128, 256), downsample=True)
    conv = tf.concat([conv, route_2], axis=-1)

    conv = common.convolutional(conv, (1, 1, 512, 256))
    conv = common.convolutional(conv, (3, 3, 256, 512))
    conv = common.convolutional(conv, (1, 1, 512, 256))
    conv = common.convolutional(conv, (3, 3, 256, 512))
    conv = common.convolutional(conv, (1, 1, 512, 256))

    route_2 = conv
    conv = common.convolutional(conv, (3, 3, 256, 512))
    conv_mbbox = common.convolutional(
        conv, (1, 1, 512, 3 * (num_class + 5)), activate=False, bn=False
    )

    conv = common.convolutional(route_2, (3, 3, 256, 512), downsample=True)
    conv = tf.concat([conv, route], axis=-1)

    conv = common.convolutional(conv, (1, 1, 1024, 512))
    conv = common.convolutional(conv, (3, 3, 512, 1024))
    conv = common.convolutional(conv, (1, 1, 1024, 512))
    conv = common.convolutional(conv, (3, 3, 512, 1024))
    conv = common.convolutional(conv, (1, 1, 1024, 512))

    conv = common.convolutional(conv, (3, 3, 512, 1024))
    conv_lbbox = common.convolutional(
        conv, (1, 1, 1024, 3 * (num_class + 5)), activate=False, bn=False
    )

    return [conv_sbbox, conv_mbbox, conv_lbbox]


def decode(conv_output, num_class, i=0):
    """
    return tensor of shape [batch_size, output_size, output_size, anchor_per_scale, 5 + num_classes]
            contains (x, y, w, h, score, probability)
    """
    conv_shape = tf.shape(conv_output)
    batch_size = conv_shape[0]
    output_size = conv_shape[1]

    conv_output = tf.reshape(
        conv_output, (batch_size, output_size, output_size, 3, 5 + num_class)
    )
    conv_raw_xywh, conv_raw_conf, conv_raw_prob = tf.split(
        conv_output, (4, 1, num_class), axis=-1
    )

    pred_conf = tf.sigmoid(conv_raw_conf)
    pred_prob = tf.sigmoid(conv_raw_prob)

    return tf.concat([conv_raw_xywh, pred_conf, pred_prob], axis=-1)


def decode_train(
    conv_output, num_class, strides, anchors, i=0, xyscale=[1, 1, 1]
):
    conv_shape = tf.shape(conv_output)
    batch_size = conv_shape[0]
    output_size = conv_shape[1]

    conv_output = tf.reshape(
        conv_output, (batch_size, output_size, output_size, 3, 5 + num_class)
    )
    conv_raw_dxdy, conv_raw_dwdh, conv_raw_conf, conv_raw_prob = tf.split(
        conv_output, (2, 2, 1, num_class), axis=-1
    )

    x = tf.tile(
        tf.expand_dims(tf.range(output_size, dtype=tf.int32), axis=0),
        [output_size, 1],
    )
    y = tf.tile(
        tf.expand_dims(tf.range(output_size, dtype=tf.int32), axis=1),
        [1, output_size],
    )
    xy_grid = tf.expand_dims(
        tf.stack([x, y], axis=-1), axis=2
    )  # [gx, gy, 1, 2]
    # xy_grid = np.meshgrid(np.arange(output_size), np.arange(output_size))
    # xy_grid = np.expand_dims(np.stack(xy_grid, axis=-1), axis=2)  # [gx, gy, 1, 2]

    xy_grid = tf.tile(tf.expand_dims(xy_grid, axis=0), [batch_size, 1, 1, 3, 1])
    xy_grid = tf.cast(xy_grid, tf.float32)

    pred_xy = (
        (tf.sigmoid(conv_raw_dxdy) * xyscale[i])
        - 0.5 * (xyscale[i] - 1)
        + xy_grid
    ) * strides[i]
    pred_wh = tf.exp(conv_raw_dwdh) * anchors[i]
    pred_xywh = tf.concat([pred_xy, pred_wh], axis=-1)

    pred_conf = tf.sigmoid(conv_raw_conf)
    pred_prob = tf.sigmoid(conv_raw_prob)

    return tf.concat([pred_xywh, pred_conf, pred_prob], axis=-1)


def bbox_iou(boxes1, boxes2):

    boxes1_area = boxes1[..., 2] * boxes1[..., 3]
    boxes2_area = boxes2[..., 2] * boxes2[..., 3]

    boxes1_coor = tf.concat(
        [
            boxes1[..., :2] - boxes1[..., 2:] * 0.5,
            boxes1[..., :2] + boxes1[..., 2:] * 0.5,
        ],
        axis=-1,
    )
    boxes2_coor = tf.concat(
        [
            boxes2[..., :2] - boxes2[..., 2:] * 0.5,
            boxes2[..., :2] + boxes2[..., 2:] * 0.5,
        ],
        axis=-1,
    )

    left_up = tf.maximum(boxes1_coor[..., :2], boxes1_coor[..., :2])
    right_down = tf.minimum(boxes2_coor[..., 2:], boxes2_coor[..., 2:])

    inter_section = tf.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[..., 0] * inter_section[..., 1]
    union_area = boxes1_area + boxes2_area - inter_area

    return 1.0 * inter_area / union_area


def bbox_ciou(boxes1, boxes2):
    boxes1_coor = tf.concat(
        [
            boxes1[..., :2] - boxes1[..., 2:] * 0.5,
            boxes1[..., :2] + boxes1[..., 2:] * 0.5,
        ],
        axis=-1,
    )
    boxes2_coor = tf.concat(
        [
            boxes2[..., :2] - boxes2[..., 2:] * 0.5,
            boxes2[..., :2] + boxes2[..., 2:] * 0.5,
        ],
        axis=-1,
    )

    left = tf.maximum(boxes1_coor[..., 0], boxes2_coor[..., 0])
    up = tf.maximum(boxes1_coor[..., 1], boxes2_coor[..., 1])
    right = tf.maximum(boxes1_coor[..., 2], boxes2_coor[..., 2])
    down = tf.maximum(boxes1_coor[..., 3], boxes2_coor[..., 3])

    c = (right - left) * (right - left) + (up - down) * (up - down)
    iou = bbox_iou(boxes1, boxes2)

    u = (boxes1[..., 0] - boxes2[..., 0]) * (
        boxes1[..., 0] - boxes2[..., 0]
    ) + (boxes1[..., 1] - boxes2[..., 1]) * (boxes1[..., 1] - boxes2[..., 1])
    d = u / c

    ar_gt = boxes2[..., 2] / boxes2[..., 3]
    ar_pred = boxes1[..., 2] / boxes1[..., 3]

    ar_loss = (
        4
        / (np.pi * np.pi)
        * (tf.atan(ar_gt) - tf.atan(ar_pred))
        * (tf.atan(ar_gt) - tf.atan(ar_pred))
    )
    alpha = ar_loss / (1 - iou + ar_loss + 0.000001)
    ciou_term = d + alpha * ar_loss

    return iou - ciou_term


def bbox_giou(boxes1, boxes2):

    boxes1 = tf.concat(
        [
            boxes1[..., :2] - boxes1[..., 2:] * 0.5,
            boxes1[..., :2] + boxes1[..., 2:] * 0.5,
        ],
        axis=-1,
    )
    boxes2 = tf.concat(
        [
            boxes2[..., :2] - boxes2[..., 2:] * 0.5,
            boxes2[..., :2] + boxes2[..., 2:] * 0.5,
        ],
        axis=-1,
    )

    boxes1 = tf.concat(
        [
            tf.minimum(boxes1[..., :2], boxes1[..., 2:]),
            tf.maximum(boxes1[..., :2], boxes1[..., 2:]),
        ],
        axis=-1,
    )
    boxes2 = tf.concat(
        [
            tf.minimum(boxes2[..., :2], boxes2[..., 2:]),
            tf.maximum(boxes2[..., :2], boxes2[..., 2:]),
        ],
        axis=-1,
    )

    boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * (
        boxes1[..., 3] - boxes1[..., 1]
    )
    boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * (
        boxes2[..., 3] - boxes2[..., 1]
    )

    left_up = tf.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down = tf.minimum(boxes1[..., 2:], boxes2[..., 2:])

    inter_section = tf.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[..., 0] * inter_section[..., 1]
    union_area = boxes1_area + boxes2_area - inter_area
    iou = inter_area / union_area

    enclose_left_up = tf.minimum(boxes1[..., :2], boxes2[..., :2])
    enclose_right_down = tf.maximum(boxes1[..., 2:], boxes2[..., 2:])
    enclose = tf.maximum(enclose_right_down - enclose_left_up, 0.0)
    enclose_area = enclose[..., 0] * enclose[..., 1]
    giou = iou - 1.0 * (enclose_area - union_area) / enclose_area

    return giou


def compute_loss(
    pred, conv, label, bboxes, strides, num_class, iou_loss_threshold, i=0
):
    conv_shape = tf.shape(conv)
    batch_size = conv_shape[0]
    output_size = conv_shape[1]
    input_size = strides[i] * output_size
    conv = tf.reshape(
        conv, (batch_size, output_size, output_size, 3, 5 + num_class)
    )

    conv_raw_conf = conv[:, :, :, :, 4:5]
    conv_raw_prob = conv[:, :, :, :, 5:]

    pred_xywh = pred[:, :, :, :, 0:4]
    pred_conf = pred[:, :, :, :, 4:5]

    label_xywh = label[:, :, :, :, 0:4]
    respond_bbox = label[:, :, :, :, 4:5]
    label_prob = label[:, :, :, :, 5:]

    giou = tf.expand_dims(bbox_giou(pred_xywh, label_xywh), axis=-1)
    input_size = tf.cast(input_size, tf.float32)

    bbox_loss_scale = 2.0 - 1.0 * label_xywh[:, :, :, :, 2:3] * label_xywh[
        :, :, :, :, 3:4
    ] / (input_size ** 2)
    giou_loss = respond_bbox * bbox_loss_scale * (1 - giou)

    iou = bbox_iou(
        pred_xywh[:, :, :, :, np.newaxis, :],
        bboxes[:, np.newaxis, np.newaxis, np.newaxis, :, :],
    )
    max_iou = tf.expand_dims(tf.reduce_max(iou, axis=-1), axis=-1)

    respond_bgd = (1.0 - respond_bbox) * tf.cast(
        max_iou < iou_loss_threshold, tf.float32
    )

    conf_focal = tf.pow(respond_bbox - pred_conf, 2)

    conf_loss = conf_focal * (
        respond_bbox
        * tf.nn.sigmoid_cross_entropy_with_logits(
            labels=respond_bbox, logits=conv_raw_conf
        )
        + respond_bgd
        * tf.nn.sigmoid_cross_entropy_with_logits(
            labels=respond_bbox, logits=conv_raw_conf
        )
    )

    prob_loss = respond_bbox * tf.nn.sigmoid_cross_entropy_with_logits(
        labels=label_prob, logits=conv_raw_prob
    )

    giou_loss = tf.reduce_mean(tf.reduce_sum(giou_loss, axis=[1, 2, 3, 4]))
    conf_loss = tf.reduce_mean(tf.reduce_sum(conf_loss, axis=[1, 2, 3, 4]))
    prob_loss = tf.reduce_mean(tf.reduce_sum(prob_loss, axis=[1, 2, 3, 4]))

    return giou_loss, conf_loss, prob_loss
