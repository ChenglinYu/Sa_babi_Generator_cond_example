#如何生成sa_babi数据集？
1. run

```bash
python generate.py
destination_src_directory
-seed seed_value
-num_instances instance_num
-metadata_file metadata_file_path
```

PS:
 -  we can replace following args
    -  destination_src_directory. e.g.
    /Users/chenglinyu/PycharmProjects/SystemExperiment/DataDeal/working/sa-train-1000/src
    - seed_value e.g. 0
    - instance_num e.g. 32(which is the amount of c files we will generate)
    - metadata_file_path. e.g. **manifest.json**(**you'd better not change the file's name**, but you can change its parent directory)

2. input those parameters in pycharm, and then run generate.py

3. you can run 



   ```bash
   SA_SEED=0 && ./sa_gen_cfiles.sh working_directory 10
   ```

   Then you will get 10 c files in working_directory/src and **manifest.json** which stores raw labels of program in line level in working_directory

为了保证数据集的一致性，统一规定：

sa-train的种子设置为0

sa-test的种子设置为1

**数据集已经生成，将不再变动！** 

12-17 18:17分生成的数据集。

- sa-train-1000
- sa-test-100

12-19 13:33启动生成数据集

- sa-test-1000

12-19 14:45 启动生成数据集

- sa-train-9600
- sa-test-38400

