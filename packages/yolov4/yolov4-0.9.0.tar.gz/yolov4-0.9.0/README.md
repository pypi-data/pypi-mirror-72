![license](https://img.shields.io/github/license/hhk7734/tensorflow-yolov4)
![pypi](https://img.shields.io/pypi/v/yolov4)
![language](https://img.shields.io/github/languages/top/hhk7734/tensorflow-yolov4)

# tensorflow-yolov4

```shell
python3 -m pip install yolov4
```

YOLOv4 Implemented in Tensorflow 2.
Convert YOLOv4, YOLOv3, YOLO tiny .weights to .pb, .tflite and trt format for tensorflow, tensorflow lite, tensorRT.

Download yolov4.weights file: https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT

## Performance

<p align="center"><img src="data/performance.png" width="640"\></p>

## Help

```python
>>> from yolov4.tf import YOLOv4
>>> help(YOLOv4)
```

## Inference

### tensorflow

```python
from yolov4.tf import YOLOv4

yolo = YOLOv4()

yolo.classes = "/home/hhk7734/tensorflow-yolov4/data/classes/coco.names"

yolo.make_model()
yolo.load_weights("/home/hhk7734/Desktop/yolov4.weights", weights_type="yolo")

yolo.inference(
    media_path="/home/hhk7734/tensorflow-yolov4/data/kite.jpg",
    cv_waitKey_delay=1000,
)
```

### tensorflow lite

```python
import yolov4.tflite as yolo

detector = yolo.YOLOv4(
    names_path="/home/hhk7734/tensorflow-yolov4/data/classes/coco.names",
    tflite_path="/home/hhk7734/Desktop/yolov4.tflite",
)

detector.inference(
    media_path="/home/hhk7734/tensorflow-yolov4/data/road.mp4",
    is_image=False,
    cv_waitKey_delay=1,
)
```

## Training

```python
from yolov4.tf import YOLOv4

yolo = YOLOv4()

yolo.classes = "/home/hhk7734/tensorflow-yolov4/data/classes/coco.names"

yolo.input_size = 416
yolo.make_model()
yolo.load_weights("/home/hhk7734/Desktop/yolov4.conv.137", weights_type="yolo")

yolo.train(
    train_annote_path="/home/hhk7734/tensorflow-yolov4/data/dataset/val2017.txt",
    test_annote_path="/home/hhk7734/tensorflow-yolov4/data/dataset/val2017.txt",
)
```

```python
from yolov4.tf import YOLOv4

yolo = YOLOv4()

yolo.classes = "/home/hhk7734/darknet/data/class.names"

yolo.input_size = 416
yolo.make_model()

yolo.train(
    train_annote_path="/home/hhk7734/darknet/data/train.txt",
    test_annote_path="/home/hhk7734/darknet/data/train.txt",
    dataset_type="yolo",
)
```
