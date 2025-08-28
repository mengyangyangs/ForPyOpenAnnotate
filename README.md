# ForPyOpenAnnotate
这是一个半自动的标注工具，以下是他的操作步骤：
# 操作步骤：
## 1.创建虚拟环境
- 创建之前先检查python环境是否是3.7+
    - python --version 如果大于3.7则不必理会，不是则自行下载
- 创建并激活虚拟环境
    - python3 -m venv annotate_env
    - source annotate_env/bin/activate
## 2.安装pyOpenAnontate
- pip install pyOpenAnnotate==0.4.2
## 3.工具用法
- 标注图像目录中的图片
    - annotate --img ./your_images_folder
- 标注视频中的目标帧
    - annotate --vid ./your_video.mp4
- 参数说明
    - --img ***指定图像文件夹路径***
    - --vid ***指定视频文件路径***
    - --resume ***从上次中断处继续***
    - --skip N ***跳过每 N 帧（视频标注时常用）***
    - -T ***打开 mask 处理视图（实验性）***
## 4.可视化已标注数据
- showlbls --img ./your_images_folder --ann ./your_annotations_folder
- 使用视频抽帧标注，可以这样做：
    - annotate --vid ./your_video.mp4 --skip 5

# 注意事项：
***目录下的labels是annotate --img后，得到的***
***name.txt对应的是 annotate --img /your_path_foldter 生成的对应的名称***

***ToTxt.py的效果是使用模型预测图片后生成的.txt的标注***
***而forPyOpenAnnotate.py则是把yolo格式转换成它自己能识别的格式***

***这里有一些文件夹和图片，可以自己去试一下，切记如果要运行ToTxt.py一定要在yolov8的环境下运行，因为涉及到ultralytics这个库*

### 超级注意事项，如果showlbls运行不出来，则使用python /Users/yang/Desktop/annotate_env/lib/python3.13/site-packages/tools/visualize.py --img /Users/yang/Desktop/zhao --ann /Users/yang/Desktop/zhao_abs，至于为什么修改了这个路径下的annotate_env/lib/python3.13/site-packages/tools/visualize.py文件，还是用不了showlbls，那是因为他妈的这个showlbls的路径根本就不在这里！！！！！在他妈的miniconda3/lib/python3.13/site-packages/tools/visualize.py这里！！！！

# 超级天坑，如果遇到这个报错 
Traceback (most recent call last):
  File "/Users/yang/miniconda3/bin/showlbls", line 8, in <module>
    sys.exit(main())
             ~~~~^^
  File "/Users/yang/miniconda3/lib/python3.13/site-packages/tools/visualize.py", line 126, in main
    annotated_img = draw_annotations(img, bounding_boxes, thickness)
  File "/Users/yang/miniconda3/lib/python3.13/site-packages/tools/visualize.py", line 63, in draw_annotations
    cv2.rectangle(img, p1, p2, (0,255,0), thickness)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cv2.error: OpenCV(4.12.0) :-1: error: (-5:Bad argument) in function 'rectangle'
> Overload resolution failed:
>  - Can't parse 'pt1'. Sequence item with index 0 has a wrong type
>  - Can't parse 'rec'. Expected sequence length 4, got 2
>  - Can't parse 'pt1'. Sequence item with index 0 has a wrong type
>  - Can't parse 'rec'. Expected sequence length 4, got 2

***很可能是那个visualize.py文件的内容没有修改 使用这个指令查看 python -c "import tools.visualize; print(tools.visualize.__file__)" 然后去修改visualize.py***
