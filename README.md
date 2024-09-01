#运行环境
需要python 3.11

#运行方法
把lifegame.py和glider_gun.csv放在同一目录下
将命令行定位到该目录，并运行：
python lifegame.py glider_gun.csv

#逐步调试
按下空格进入暂停模式，按下 → 方向键使逐步迭代；
再次按下空格可以继续自动迭代。

#检测周期
进入暂停模式后，在英文输入法状态下，按下p键，若控制台有输出则说明周期检测成功，但不代表模型一定具备周期（除非保证模型在周期内的bound_box不变）
