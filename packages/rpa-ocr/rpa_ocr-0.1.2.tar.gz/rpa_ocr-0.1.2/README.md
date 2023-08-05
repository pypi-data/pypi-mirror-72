# **rpa_verification**

##### 用于自主训练测试上线部署验证码算法

### 版本号 

    0.1.2

### 使用方法

 安装

#### 新建conda环境

`conda create -n rpa-ocr python=3.7`

#### 使用pip命令安装
      
`pip install rpa-ocr`

note: 如果在安装过程中发生某些库安装失败，使用`pip`重新安装即可

#### 训练

定义好相关参数然后使用`train.main()`命令训练
    
```python
import rpa_ocr
app_scenes = ""
data_path = ""
train = rpa_ocr.Train(app_scenes=app_scenes,
                      data_path=data_path)
train.main()
```
     
#### 参数说明

```
 app_scenes: 当前验证码的使用场景，也是全局标识符
 alphabet_mode: 使用哪种模式的字母表,目前支持"ch"(中文）,"eng"(英文大小写）,"ENG"（英文大写）
 data_path: 存储数据的位置，按照图片，命名为label
 model_path: model训练完后的保存地址
 short_size: 图片的高度，必须是16的倍数。default:32
 verification_length: 验证码的长度。default:4
 device: 使用cpu还是gpu进行训练，两个模式:"cpu" or "cuda"。default:"cpu"
 epochs: 训练模型的轮数。default:1200
 lr: 学习率。default:1e-3
 batch_size: 每一个batch的大小。default:256
 num_works: 使用多进行进行数据处理，使用进程数。default:0
 target_acc: 目标准确率,如果达到目标准确率将提前结束训练。default:0.95
 cloud_service: 是否将训练好的模型自动上传到云端。default:True
```

#### 预测

定义好相关参数，然后使用`crnn.predict(image)`进行预测

目前支持的image格式为opencv，pillow读入和base64编码后的图片

```python
import rpa_ocr
import cv2
app_scenes = ""
model_path = ""
image_path = ""
image = cv2.imread(image_path)
crnn = rpa_ocr.CRNNInference(app_scenes=app_scenes,
                             model_path=model_path)
crnn.predict(image)
```

#### 参数说明

```
 app_scenes: 当前验证码的使用场景，也是全局标识符
 alphabet_mode: 使用哪种模式的字母表,目前支持"ch"(中文）,"eng"(英文大小写）,"ENG"（英文大写)。default:"eng"
 model_path: 使用model所在文件夹目录
 short_size: 图片的高度，必须是16的倍数。default:32
 verification_length: 验证码的长度。default:4
 device: 使用cpu还是gpu进行训练，两个模式:"cpu" or "cuda"。default:"cpu"
```

### TODO LIST

- [x] 完成训练和测试的一键完成
- [x] 支持多cpu加速训练
- [x] 支持自动提前停止训练
- [x] 针对中文验证码的支持
- [x] 完成训练后的一键部署到云服务器
- [x] 完成可以部署到win32
- [ ] 支持文字点选类验证码
- [ ] 增加对滑块验证码的支持
- [ ] 增加对拼图类验证码的支持