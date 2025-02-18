import json
import os
import random
import re
import time

def read_json_file(file_path):
    if not os.access(file_path, os.R_OK):
        print(f"Warning: No read permissions for file {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)
            if not isinstance(content, list):
                print(f"Warning: Invalid content in file {file_path}")
                return None
            return content
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {str(e)}")
        return None

def find_templates_by_category(category):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'prompt', f'{category}.json')
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return []
        
    return read_json_file(file_path)

class PIP_prompt:

    _execution_counter = 0  # 每次执行增加
    _last_prompt = None    # 存储上一次的提示词
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "style_prompt"

    def __init__(self):
        self.template_names = {
            "Camera": [],        # 镜头视角
            "Character": [],     # 角色类型
            "Number": [],        # 数量
            "Occupation": [],    # 职业
            "Anime": [],        # 动漫
            "Face": [],         # 五官
            "Expression": [],    # 表情
            "Hair": [],         # 头发
            "Decoration": [],    # 装饰
            "Clothing": [],      # 服装
            "Environment": [],   # 环境
            "Style": [],        # 风格
            "Color": [],        # 颜色
            "Composition": []    # 构图
        }
        self.update_all_template_names()
        self.chinese_names = {
            "Camera": "镜头视角",
            "Character": "角色类型",
            "Number": "数量",
            "Occupation": "职业",
            "Anime": "动漫",
            "Face": "五官",
            "Expression": "表情",
            "Hair": "头发",
            "Decoration": "装饰",
            "Clothing": "服装",
            "Environment": "环境",
            "Style": "风格",
            "Color": "颜色",
            "Composition": "构图"
        }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "随机启用": ("BOOLEAN", {"default": False}),
                "镜头视角": (cls.get_template_names("Camera"), {"default": None}),
                "角色类型": (cls.get_template_names("Character"), {"default": None}),
                "数量": (cls.get_template_names("Number"), {"default": None}),
                "职业": (cls.get_template_names("Occupation"), {"default": None}),
                "动漫": (cls.get_template_names("Anime"), {"default": None}),
                "五官": (cls.get_template_names("Face"), {"default": None}),
                "表情": (cls.get_template_names("Expression"), {"default": None}),
                "头发": (cls.get_template_names("Hair"), {"default": None}),
                "装饰": (cls.get_template_names("Decoration"), {"default": None}),
                "服装": (cls.get_template_names("Clothing"), {"default": None}),
                "环境": (cls.get_template_names("Environment"), {"default": None}),
                "风格": (cls.get_template_names("Style"), {"default": None}),
                "颜色": (cls.get_template_names("Color"), {"default": None}),
                "构图": (cls.get_template_names("Composition"), {"default": None}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    def update_all_template_names(self):
        for category in self.template_names.keys():
            self.template_names[category] = self.get_template_names(category)

    def get_random_template(self, category, seed_value):
        templates = find_templates_by_category(category)
        if templates:
            # 排除 "none" 选项
            valid_templates = [t for t in templates if t['name'] != "none"]
            if valid_templates:
                random.seed(seed_value)
                return random.choice(valid_templates)['name']
        return None

    def style_prompt(self, 随机启用=False, seed=None, **kwargs):
        prompts = []
        current_seed = 0
        
        # 如果随机启用且提供了种子，使用提供的种子
        if 随机启用 and seed is not None:
            current_seed = seed
            
        for category, chinese_name in self.chinese_names.items():
            template_name = kwargs.get(chinese_name)
            
            # 只在用户没有选择且随机启用时进行随机
            if 随机启用 and (template_name is None or template_name == "none"):
                template_name = self.get_random_template(category, current_seed + hash(category))
            
            if template_name is not None:
                templates = find_templates_by_category(category)
                if templates:
                    template = next((t for t in templates if t['name'] == template_name), None)
                    if template:
                        prompts.append(template['prompt'])

        # 合并提示词并清理连续逗号
        styled_prompt = clean_prompt(", ".join(prompts))
        
        # 只在提示词发生变化时才打印
        if styled_prompt != PIP_prompt._last_prompt:
            if 随机启用 and seed is not None:
                print(f"Styled Prompt: {styled_prompt} (Seed: {current_seed})")
            else:
                print(f"Styled Prompt: {styled_prompt}")
            PIP_prompt._last_prompt = styled_prompt
            
        return (styled_prompt,)

    @classmethod
    def get_template_names(cls, category):
        templates = find_templates_by_category(category)
        # 添加 None 作为默认选项
        return [None] + [template['name'] for template in templates] if templates else [None]

class ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "utils"

    def notify(self, text, unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif (
                not isinstance(extra_pnginfo[0], dict)
                or "workflow" not in extra_pnginfo[0]
            ):
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    node["widgets_values"] = [text]

        # 确保返回的结果是完整的字符串
        return {"ui": {"text": text}, "result": (text,)}

NODE_CLASS_MAPPINGS = {
    "PIP_prompt": PIP_prompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PIP_prompt": "PIP Prompt",
}

def clean_prompt(prompt):
    # 使用正则表达式替换连续的两个或更多逗号为单个逗号
    return re.sub(r',{2,}', ',', prompt)