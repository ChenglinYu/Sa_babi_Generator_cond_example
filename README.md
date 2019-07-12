# Background

本项目参考paper[Towards security defect prediction with AI](https://arxiv.org/pdf/1808.09897.pdfv)和该paper的[code](https://github.com/cmu-sei/sa-bAbI)构建了一个代码生成器，可以生成特定规则的语法正确的c语言代码。每一行代码均有1种标签，共6种标签，这6种标签分别是：

```python
    # Function wrapping lines
    OTHER = 0
    # Lines inside body that aren't buffer writes
    BODY = 1
    # Buffer write that requires control flow analysis to prove safe
    BUFWRITE_COND_SAFE = 2
    # Buffer write that requires control flow analysis to prove unsafe
    BUFWRITE_COND_UNSAFE = 3
    # Buffer write that is provably safe even without control flow
    BUFWRITE_TAUT_SAFE = 4
    # Buffer write that is provably unsafe even without control flow
    BUFWRITE_TAUT_UNSAFE = 5
```



# Instructions
## Method 1: execute command in terminal

在项目根目录下创建**代码实例输出文件夹**

```bash
mkdir work_directory
```

运行*gen_cond_example.py*生成代码实例
```bash
python sa_babi/gen_cond_example.py
destination_src_directory
-seed seed_value
-num_instances instance_num
-metadata_file metadata_file_path
```
- **destination_src_directory**是work_directory的绝对路径
- **seed_value**： 随机种子。e.g. 0
- **instance_num** e.g. 32(which is the amount of c files we will generate)
- **metadata_file_path**. e.g. **manifest.json**(**you'd better not change the file's name**, but you can change its parent directory)

For example, in my Mac machine, I just type the following code:

```shell
python sa_babi/gen_cond_example.py work_directory -seed 0 -num_instances 10 -metadata_file work_directory/manifest.json
```

### result

After you execute these commands, you will get **10** c files and **manifest.json** in **working_directory**. 

**manifest.json** stores raw labels of program in line level in **working_directory**.

You can look up the details in the *example* branch.

We randomly have a look one file,  **4a2405d586.c**

```c
#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    int entity_1;             // Tag.BODY
    int entity_7;             // Tag.BODY
    char entity_0[24];        // Tag.BODY
    entity_7 = 75;            // Tag.BODY
    char entity_9[86];        // Tag.BODY
    int entity_8;             // Tag.BODY
    int entity_5;             // Tag.BODY
    char entity_4[90];        // Tag.BODY
    entity_1 = 86;            // Tag.BODY
    entity_5 = 45;            // Tag.BODY
    entity_8 = 89;            // Tag.BODY
    entity_4[entity_1] = 'A'; // Tag.BUFWRITE_TAUT_SAFE
    if(entity_5 < entity_7){  // Tag.BODY
    entity_5 = 81;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_0[entity_8] = 'l'; // Tag.BUFWRITE_TAUT_UNSAFE
    entity_5 = 79;            // Tag.BODY
    }                         // Tag.BODY
    entity_9[entity_5] = '8'; // Tag.BUFWRITE_COND_SAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER
```

**manifest.json**

```json
{
  "working_dir": "/Users/chenglinyu/PycharmProjects/SystemExperiment/Sa_babi_all/Sa_babi_Generator_cond_example/work_directory",
  "num_instances": 10,
  "tags": {
    "d97aec156b.c": [
      0,
      0,
      0,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      2,
      1,
      0
    ],
    "77ec1d72c7.c": [
      0,
      0,
      0,
      1,
      1,
      1,
      1,
      1,
      .
      .
    ]
    .
    .
    ]
  }
}
```

manifest.json中有关4a2405d586.c的部分如下：

```json
"4a2405d586.c": [
  0,
  0,
  0,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  4,
  1,
  1,
  1,
  5,
  1,
  1,
  2,
  1,
  0
],
```

以上代码表明：**manifest.json记录了每个代码实例每一行的标签。**

### note

为了保证后续实验的**可重复性**，建议使用**特定种子**产生特定的数据集。

例如，将训练集的随机种子设置为**0**，将测试集的种子设置为**1**.

## Method 2: PyCharm parameter settings

input those parameters above in pycharm, and then run **gen_cond_example.py**

## Method 3: Use docker, and then execute .sh file in terminal

该方法适用于环境**非Linux系统/MacOS系统**的的用户，或者**电脑中没有安装python3的用户**，使用docker则不需安装任何环境。缺点是：下载docker linux镜像和docker python镜像耗时较长，需耐心等待。

e.g.

```bash
cd Sa_babi_Generator_cond_example
```

```bash
docker-compose build
```

```bash
SA_SEED=0 && ./sa_gen_cfiles.sh working_directory 10
```


## 生成器构造思路

生成器的具体构造思路请参见https://blog.csdn.net/ChenglinBen/article/details/94122037





