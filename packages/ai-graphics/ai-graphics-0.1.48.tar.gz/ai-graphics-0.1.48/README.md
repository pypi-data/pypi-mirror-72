# AI-Graphics

AI-Graphics 是一个应用于实际项目的计算机视觉工具包，提供了包括常用图像处理函数，图像识别，目标检测，图像分割，文本检测，人脸识别，视频处理等算法，方便项目快速部署，缩短开发周期。

## Demo
[立即体验](http://180.76.141.139:32092/)

## Installation

使用pip安装

```bash
pip install ai-graphics
```

## Usage
No. | Function |  Description  
-|-|-
1 | Classifier | 图像识别，eg.场景图识别、多商品图识别 |
2 | Detection | 主体检测，eg.商品、人物、logo |
3 | FaceDetector | 人脸检测 |
4 | FaceRecognition | 人脸识别 |
5 | Graphics | 图像处理方法，eg.添加倒影、添加阴影|
6 | ImageCrop | 图像裁剪 |
7 | Matting | 图像抠图，eg.商品、人物 |
8 | OcrDetector | 场景文本检测，eg.banner、视频 |
9 | Segmentation | 图像分割，eg.人像分割 |
10 | VideoProcess | 视频处理，eg.logo添加、字幕添加、视频变速 |


## QuickStart

```python
import cv2
import graphics as g

src = cv2.imread('27.png', cv2.IMREAD_UNCHANGED) 

# 场景图识别
cl = g.Classifier(model_name="../models/classifier.pth", ctx_id=-1)   
label = cl.predict(src)

# 图片裁剪 
ic = g.ImageCrop(model_dir='models', ctx_id=-1)
image = ic.crop_image(src, (1000, 1000))

# 图像抠图
ma = g.Matting(model_name='models/indexnet_matting.pth.tar', ctx_id=0)
trimap = ma.generate_trimap(mask)
alpha = ma.predict(src, trimap)
png = ma.save_png(src, alpha)

```

## Download
[模型下载路径](https://ai.tezign.com/web-filesystem?path=/data/User/chenghong/CNN/models/)
