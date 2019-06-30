#!/usr/bin/env bash
# sa-bAbI: An automated software assurance code dataset generator
# 
# Copyright 2018 Carnegie Mellon University. All Rights Reserved.
#
# NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE
# ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS.
# CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER
# EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED
# TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY,
# OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON
# UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO
# FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
#
# Released under a MIT (SEI)-style license, please see license.txt or
# contact permission@sei.cmu.edu for full terms.
#
# [DISTRIBUTION STATEMENT A] This material has been approved for
# public release and unlimited distribution. Please see Copyright
# notice for non-US Government use and distribution.
# 
# Carnegie Mellon (R) and CERT (R) are registered in the U.S. Patent
# and Trademark Office by Carnegie Mellon University.
#
# This Software includes and/or makes use of the following Third-Party
# Software subject to its own license:
# 1. clang (http://llvm.org/docs/DeveloperPolicy.html#license)
#     Copyright 2018 University of Illinois at Urbana-Champaign.
# 2. frama-c (https://frama-c.com/download.html) Copyright 2018
#     frama-c team.
# 3. Docker (https://www.apache.org/licenses/LICENSE-2.0.html)
#     Copyright 2004 Apache Software Foundation.
# 4. cppcheck (http://cppcheck.sourceforge.net/) Copyright 2018
#     cppcheck team.
# 5. Python 3.6 (https://docs.python.org/3/license.html) Copyright
#     2018 Python Software Foundation.
# 
# DM18-0995
#

# 如果参数个数不等于2，则给出help message并退出
if [ "$#" -ne 2 ]; then
    echo "Usage: sa_gen_cfiles.sh <working_dir> <num_instances>"
    echo "e.g.: sa_gen_cfiles.sh data 10"
    exit
fi

working_dir=$(realpath $1) # 获取输出文件夹路径
num_instances=$2 # 获取实例个数
SA_SEED="${SA_SEED:--1}" #如果SA_SEED为空，则将SA_SEED的值设置为-1
echo SA_SEED

mkdir -p $working_dir/src # 创建$working_dir/src

# DATA_DIR作为环境变量传入，并使用服务执行Python命令
DATA_DIR=$working_dir docker-compose run --rm sababi \
    python /sa_babi/generate.py \
    /mnt/data/src \
    -seed $SA_SEED \
    -num_instances $num_instances \
    -metadata_file /mnt/data/manifest.json

# SA_SEED = 0
# mkdir -p $working_dir/src 可以手工创建
# DATA_DIR = working/sa-train-1000
# docker-compose run --rm sababi 启动sababi服务，并且将DATA_DIR环境变量传入
# python /sa_babi/generate.py /mnt/data/src -seed 0 -num_instances 1000 -metadata_file /mnt/data/manifest.json
# docker-compose是跟docker-compose.yml文件联系起来的，所以必须要输入DATA_DIR命令

# 明天接着搞吧，算是把docker搞懂了。TODO