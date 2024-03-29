# buptLab-nfa2dfa

这个仓库包含了北京邮电大学 2023-2024 春季学期《形式语言与自动机》课程实验——NFA 到 DFA 的转化的相关代码和报告（见 Release）。

## 文件结构

```
.
├── LICENSE
├── README.md
├── requirements.txt     # 项目所需的 Python 依赖包列表
├── src                  # 源代码目录
│   ├── algorithms               # 算法模块目录
│   │   ├── enfa2nfa.py                  # 将 ε-NFA 转换为 NFA 的算法实现
│   │   ├── minimize_dfa.py              # 最小化 DFA 的算法实现
│   │   └── nfa2dfa.py                   # 将 NFA 转换为 DFA 的算法实现
│   ├── data_structures          # 数据结构模块目录
│   │   ├── dfa.py                       # DFA（确定性有限自动机）的数据结构实现
│   │   ├── epsilon_nfa.py               # ε-NFA（带 ε 转换的非确定性有限自动机）的数据结构实现
│   │   └── nfa.py                       # NFA（非确定性有限自动机）的数据结构实现
│   └── main.py                  # 主程序入口文件
└── tests                # 测试代码目录
    ├── algorithms               # 算法模块的测试目录
    │   ├── test_enfa2nfa.py             # 测试 enfa2nfa 算法的单元测试
    │   ├── test_minimize_dfa.py         # 测试 minimize_dfa 算法的单元测试
    │   └── test_nfa2dfa.py              # 测试 nfa2dfa 算法的单元测试
    └── data_structures          # 数据结构模块的测试目录
        ├── test_dfa.py                  # 测试 dfa 数据结构的单元测试
        ├── test_epsilon_nfa.py          # 测试 epsilon_nfa 数据结构的单元测试
        └── test_nfa.py                  # 测试 nfa 数据结构的单元测试
```

## 使用说明

使用时请确保切换为英文输入模式。拖拽代表状态的圆圈，将它们放在屏幕上的任意位置。使用时按下空格键来输入 ε。

在图形化界面中单击按钮按下即生效，随时点击下方切换按钮，即可切换进对应功能；再次点击可以退出状态：

| 按钮 | 按钮类型 | 使用说明 |
| --- | --- | --- |
| New Delta | 切换 | 点击两个对应状态，再按下字符，添加转换关系 |
| Remove Delta | 切换 | 点击两个对应状态，再按下字符，移除指定转换关系 |
| Reassign Char | 切换 | 点击两个对应状态，按下字符 `a`，再按下字符 `b` 即可完成修改 |
| Rename State | 切换 | 点击状态，输入新名字（数字），再按回车，将对应状态改名 |
| Set as Start | 切换 | 点击状态，将其设为起始状态 |
| Set as Final | 切换 | 点击状态，将其设为终止状态 |
| Remove State | 切换 | 删除点击的状态 |
| New State | 单击 | 添加一个新状态 |
| Conver to DFA | 单击 | 将输入的自动机转化为最简 DFA 并输出。并顺便输出中途产生的 ε-NFA、NFA 和非最简 DFA |
