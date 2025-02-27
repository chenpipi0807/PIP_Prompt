# PIP Prompt 节点 - ComfyUI提示词生成器

这是一个自用的ComfyUI自定义节点，用于生成AI图像提示词。它提供了多个类别的提示词模板，支持手动选择和随机生成。选的不随机，没选的随机。

<img width="1324" alt="微信图片_20250218204119" src="https://github.com/user-attachments/assets/286e909b-cd23-4063-8d8e-0a9e55f1460d" />


## 特点

- 14个提示词类别，包括：
  - 镜头视角
  - 角色类型
  - 数量
  - 职业
  - 动漫
  - 五官
  - 表情
  - 头发
  - 装饰
  - 服装
  - 环境
  - 风格
  - 颜色
  - 构图

- 支持随机生成
  - 可以启用随机模式自动生成提示词
  - 支持使用ComfyUI的全局种子
  - 保持用户选择的选项不变
 
## 安装方法

在ComfyUI\custom_nodes执行git clone https://github.com/chenpipi0807/PIP_Prompt.git

## 使用方法

1. 基本使用
   - 在ComfyUI中添加"PIP Prompt"节点
   - 从各个类别中选择想要的提示词
   - 提示词将自动组合并输出

2. 随机生成
   - 打开"随机启用"开关
   - 未选择的类别将自动随机生成
   - 已选择的类别将保持不变

3. 使用全局种子
   - 连接ComfyUI的"Seed"节点到PIP Prompt的seed输入
   - 启用随机模式后，将使用全局种子进行随机生成
   - 可以通过调整种子值来获得不同的随机结果

## 提示词格式

- 所有提示词以逗号分隔
- 自动清理多余的逗号
- 支持中英文混合

## 安装

1. 将整个文件夹复制到ComfyUI的`custom_nodes`目录
2. 重启ComfyUI

## 自定义提示词模板

提示词模板可以在`prompt`目录下找到，都是json文件。每个json文件都包含一个数组，数组中的每个元素是一个提示词。用户可以根据需要自行更改或添加新的提示词模板。

## 目录结构

- `PIP_prompt.py`: 主程序
- `README.md`: 说明文档
- `prompt/`: 提示词模板
  - `Camera.json`
  - `Character.json`
  - ...
  - `Composition.json`
