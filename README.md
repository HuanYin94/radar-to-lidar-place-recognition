# radar-to-lidar-place-recognition

This page is the coder of a pre-print, implemented by PyTorch.

If you have some questions on this project, please feel free to contact [Huan Yin](https://yinhuan.site/) `zjuyinhuan@gmail.com` .

If you use our code in an academic work, please cite the following paper:

    @article{xu2020disco,
        title={DiSCO: Differentiable Scan Context with Orientation},
        author={Xu, Xuecheng and Yin, Huan and Chen, Zexi and Wang, Yue and Xiong, Rong},
        journal={arXiv preprint arXiv:2010.10949},
        year={2020}
        }

And also, another implementation is avaliable at [DiSCO](https://github.com/MaverickPeter/DiSCO-pytorch).

### Method
<img src="https://github.com/ZJUYH/radar-to-lidar-place-recognition/blob/main/image/methods.png" width= 1000>

### Data

The files in `matlab/RobotCar_data` and `matlab/MulRan_data` can help you generate scancontext of radar and lidar submaps. Also, the generation of lidar submaps is included.

### Training
The `train_disco_lidar_quad.py` is used for training lidar-to-lidar DiSCO.

The `train_disco_radar_quad.py` is used for training radar-to-radar DiSCO.

The `train_joint_radar_lidar.py` is used for training L2L, R2R and R2L jointly based on DiSCO implementation.

The trained models are listed in the `trained_models` respectively.

### Inference
Please use the files in `inference` folder.

### Evaluation

In addition, the `matlab/evaluate_recall@1` contains the files to calculate the recall@1 for place recognition evaluation.

### Case Example

Multi-session place recognition: radar-to-lidar in different days of Mulran-Riverside

<img src="https://github.com/ZJUYH/radar-to-lidar-place-recognition/blob/main/image/case.png" width= 1000>

## TODO

Make the original data and lidar filter files avaliable.
