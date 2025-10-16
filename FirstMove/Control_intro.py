import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
frames = [
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

def main():
    toy = scanner.find_toy(toy_name="SB-D96A")
    if not toy:
        print("❌ 没找到 Sphero SB-D96A")
        return

    with SpheroEduAPI(toy) as api:
        for _ in range(10):  # 循环次数，可以调大
            for frame in frames:
                # 清空矩阵
                api.clear_matrix()
                
                # 蓝色海浪 - 逐个设置像素
                for row in range(len(frame)):
                    for col in range(len(frame[row])):
                        if frame[row][col] == 1:
                            api.set_matrix_pixel(col, row, Color(0, 0, 255))  # 蓝色
                time.sleep(0.2)
                
                # 白色浪花 - 逐个设置像素
                for row in range(len(frame)):
                    for col in range(len(frame[row])):
                        if frame[row][col] == 1:
                            api.set_matrix_pixel(col, row, Color(255, 255, 255))  # 白色
                time.sleep(0.2)

if __name__ == "__main__":
    main()
