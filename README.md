# 3 methods to generate COND examples
## 方式1：execute command in terminal

```bash
python generate.py
destination_src_directory
-seed seed_value
-num_instances instance_num
-metadata_file metadata_file_path
```

- destination_src_directory: 代码实例输出文件夹
- seed_value： 随机种子,e.g. 0
- instance_num e.g. 32(which is the amount of c files we will generate)
- metadata_file_path. e.g. **manifest.json**(**you'd better not change the file's name**, but you can change its parent directory)

## 方式2： PyCharm parameter settings

input those parameters in pycharm, and then run generate.py

## 方式3：execute .sh file in terminal

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

After you execute these commands, you will get **10** c files in **working_directory/src** and **manifest.json** which stores raw labels of program in line level in **working_directory**.

为了保证后续实验的可重复性，建议特定的数据集使用特定的随机种子。

训练集的随机种子设置为：0

测试集的随机种子设置为：1





