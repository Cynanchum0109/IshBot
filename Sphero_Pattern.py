from spherov2.types import Color


class SpheroPattern:
    """Sphero LED矩阵图案数据和基础渲染"""
    
    def __init__(self):
        # 颜色调色板
        self.palette = {
            "w": Color(255, 255, 255),  # 白色
            "o": Color(220, 80, 0),     # 橘色（更暗、饱和度更高）
            "y": Color(255, 255, 0),    # 黄色
            "b": Color(150, 100, 60),   # 棕色
            "r": Color(255, 0, 0),      # 红色
            "a": Color(189, 102, 58),   # 棕褐色
            "l": Color(70, 138, 255),   # 浅蓝色
            "0": None                   # 透明/关闭
        }
        
        # Ishmael待机图案
        self.pattern_ishmael = [
            ["0","w","b","b","b","b","w","0"],
            ["w","o","o","o","o","o","o","w"],
            ["o","o","o","o","o","o","o","o"],
            ["o","o","y","o","o","y","o","o"],
            ["o","o","y","o","o","y","o","o"],
            ["o","o","o","o","o","o","o","o"],
            ["0","o","0","o","o","0","o","0"],
            ["o","o","0","o","o","0","o","o"]
        ]
        
        # 愤怒Ishmael图案
        self.pattern_angry = [
            ["0","w","b","b","b","b","w","0"],
            ["w","o","o","o","r","o","r","w"],
            ["o","o","o","r","r","o","r","r"],
            ["o","o","o","o","o","o","o","o"],
            ["o","o","o","r","r","o","r","r"],
            ["o","o","o","o","r","o","r","o"],
            ["0","o","0","o","o","0","o","0"],
            ["o","o","0","o","o","0","o","o"]
        ]
        
        # 微笑Ishmael图案
        self.pattern_ishmael_smile = [
            ["0","w","b","b","b","b","w","0"],
            ["w","o","o","o","o","o","o","w"],
            ["o","o","o","o","o","o","o","o"],
            ["o","y","o","o","o","o","y","o"],
            ["y","o","y","o","o","y","o","y"],
            ["o","o","o","o","o","o","o","o"],
            ["0","o","0","o","o","0","o","0"],
            ["o","o","0","o","o","0","o","o"]
        ]
        
        # 皱眉Ishmael图案
        self.pattern_ishmael_frown = [
            ["0","w","b","b","b","b","w","0"],
            ["w","o","o","o","o","o","o","w"],
            ["o","o","o","o","o","o","o","o"],
            ["o","o","o","o","o","o","o","o"],
            ["o","y","y","a","a","y","y","o"],
            ["o","o","o","o","o","o","o","o"],
            ["0","o","0","o","o","0","o","0"],
            ["o","o","0","o","o","0","o","o"]
        ]
        
        # 流泪Ishmael图案
        self.pattern_ishmael_tear = [
            ["0","w","b","b","b","b","w","0"],
            ["w","o","o","o","o","o","o","w"],
            ["o","o","o","o","o","o","o","o"],
            ["o","o","o","o","o","o","o","o"],
            ["o","y","y","o","o","y","y","o"],
            ["o","o","o","o","o","o","l","o"],
            ["0","o","0","o","o","0","o","0"],
            ["o","o","0","o","o","0","o","o"]
        ]
        
        # 波浪动画帧
        self.wave_frames = [
            [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,1,1],
                [0,0,0,0,0,0,1,0],
                [0,0,0,0,1,1,1,0],
                [0,0,0,0,1,0,0,0],
                [0,0,1,1,1,0,0,0],
                [0,0,1,0,0,0,0,0],
                [1,1,1,0,0,0,0,0]
            ],
            [
                [0,0,0,0,0,0,1,0],
                [0,0,0,0,1,1,1,0],
                [0,0,0,0,1,0,0,0],
                [0,0,1,1,1,0,0,0],
                [0,0,1,0,0,0,0,0],
                [1,1,1,0,0,0,0,0],
                [1,0,0,0,0,0,0,0],
                [1,0,0,0,0,0,0,0]
            ]
        ]
        
        # 预转换颜色矩阵
        self.color_matrix_ishmael = self.convert_pattern_to_colors(self.pattern_ishmael)
        self.color_matrix_angry = self.convert_pattern_to_colors(self.pattern_angry)
        self.color_matrix_ishmael_smile = self.convert_pattern_to_colors(self.pattern_ishmael_smile)
        self.color_matrix_ishmael_frown = self.convert_pattern_to_colors(self.pattern_ishmael_frown)
        self.color_matrix_ishmael_tear = self.convert_pattern_to_colors(self.pattern_ishmael_tear)
    
    def convert_pattern_to_colors(self, pattern):
        """将字符图案转换为颜色矩阵"""
        return [[self.palette[cell] for cell in row] for row in pattern]
    
    def render_matrix(self, api, color_matrix):
        """
        将颜色矩阵渲染到LED屏幕
        
        Args:
            api: SpheroEduAPI实例
            color_matrix: 8x8颜色矩阵
        """
        try:
            api.clear_matrix()
            for row in range(len(color_matrix)):
                for col in range(len(color_matrix[row])):
                    color = color_matrix[row][col]
                    if color is not None:
                        api.set_matrix_pixel(col, row, color)
        except Exception as e:
            import traceback
            print(f"渲染矩阵失败: {e}")
            traceback.print_exc()
    
    def show_expression(self, api, expression_name):
        """
        显示指定的表情，包括LED矩阵和前后LED灯
        
        Args:
            api: SpheroEduAPI实例
            expression_name: 表情名称，可选值：
                - "ishmael" (默认待机)
                - "smile" (微笑)
                - "frown" (皱眉)
                - "angry" (愤怒)
                - "tear" (哭泣/流泪)
        """
        # 表情到颜色矩阵和LED颜色的映射
        expressions = {
            "ishmael": {
                "matrix": self.color_matrix_ishmael,
                "led_color": Color(0, 0, 0),  # 不亮灯（黑色）
                "name": "待机"
            },
            "smile": {
                "matrix": self.color_matrix_ishmael_smile,
                "led_color": self.palette["y"],  # 黄灯
                "name": "微笑"
            },
            "frown": {
                "matrix": self.color_matrix_ishmael_frown,
                "led_color": self.palette["b"],  # 棕色灯
                "name": "皱眉"
            },
            "angry": {
                "matrix": self.color_matrix_angry,
                "led_color": self.palette["r"],  # 红灯
                "name": "愤怒"
            },
            "tear": {
                "matrix": self.color_matrix_ishmael_tear,
                "led_color": self.palette["l"],  # 蓝灯
                "name": "哭泣"
            }
        }
        
        # 检查表情是否存在
        if expression_name not in expressions:
            print(f"未知表情: {expression_name}")
            print(f"可用表情: {', '.join(expressions.keys())}")
            return False
        
        expr = expressions[expression_name]
        
        try:
            # 渲染LED矩阵图案
            self.render_matrix(api, expr["matrix"])
            
            # 设置前后LED灯
            api.set_front_led(expr["led_color"])
            api.set_back_led(expr["led_color"])
            
            print(f"显示表情: {expr['name']}")
            return True
            
        except Exception as e:
            import traceback
            print(f"显示表情失败: {e}")
            traceback.print_exc()
            return False
