"""gen_cond_example.py: generate fv_for_examples"""

import argparse
import hashlib
import os
import random
import string
import sys
import json


import cond_template as templates

from sa_tag import Tag

# maximum number of variable names
MAX_NUM_VARS = 10

# variable name template
VAR_STR = "entity_%s"

# maximum number of flow-insensitive case additions
MAX_NUM_DUMMIES = 2

# minimum number of flow-insensitive case additions, in the
# flow-insensitive-only case
MIN_NUM_DUMMIES_TAUTONLY = 1

# maximum length of arrays and index to try accessing
MAX_IDX = 100

# set of available characters to write to buffer
CHARSET = string.digits + string.ascii_letters

# the number of bytes in each hash filename
FNAME_HASHLEN = 5  # ?

# command-line argument default values
# number of instances to generate
DEFAULT_NUM_INSTANCES = 12000

# random seed
DEFAULT_SEED = 0


def gen_cond_example(include_cond_bufwrite=True):
    """Generate conditional example

    Returns:
        instance_str (str): str of code example
        tags (list of Tag): tag for each line representing buffer safety
    """

    """
    COND_DEC_INIT_PAIRS = 
    [
    ("char $buf_var[$buf_len];", None),
    ("int $idx_var;", "$idx_var = $idx_init;"),
    ("int $thresh_var;", "$thresh_var = $thresh;")
    ]
    
    COND_MAIN_LINES = 
    [
    "if($idx_var < $thresh_var){",
    "$idx_var = $true_idx;",
    "} else {",
    "$idx_var = $false_idx;",
    "}"
    ]
    
    BUFWRITE_LINES = ["$buf_var[$idx_var] = '$char';"]
    """

    anon_vars = _get_anon_vars()  # 生成10个随机的变量名

    # 给模板中所有的变量赋值
    buf_var, idx_var, thresh_var = anon_vars[:3]  # 获取前三个变量名 缓存变量，索引变量 阈值变量
    dummy_vars = anon_vars[3:]  # 获取剩余的变量名（作伪装用）
    buf_len = random.randrange(MAX_IDX)  # 随机获取一个缓存的长度
    idx_init = random.randrange(MAX_IDX)  # 随机获取一个初始索引
    thresh = random.randrange(MAX_IDX)  # 随机获取一个合法阈值索引
    true_idx = random.randrange(MAX_IDX)  # 正确的索引
    false_idx = random.randrange(MAX_IDX)  # 错误的索引
    char = _get_char()  # 随机获取一个数字或字母字符
    substitutions = {
        'buf_var': buf_var,  # 缓存变量
        'idx_var': idx_var,  # 索引变量即为最终索引的索引值
        'buf_len': buf_len,  # 缓存长度
        'thresh': thresh,  # 阈值
        'thresh_var': thresh_var,  # 阈值变量
        'idx_init': idx_init,  # 初始索引
        'true_idx': true_idx,  # 正确索引
        'false_idx': false_idx,  # 错误索引
        'char': char
    }

    # 主条件语句模板
    main_lines = templates.COND_MAIN_LINES

    # 下面是cond_buf_write代码安全(未溢出)的2种情况：
    # 1.cond为真，且true_idx<buf_len
    # 2.cond为假，且false_idex<buf_len
    # 满足任意一种情况，cond_buf_write即安全
    cond = idx_init < thresh
    safe = ((cond and (true_idx < buf_len)) or
            (not cond and (false_idx < buf_len)))

    # 条件语句声明和初始化模板
    dec_init_pairs = templates.COND_DEC_INIT_PAIRS

    # 进一步整合汇聚
    # 1.当include_cond_bufwrite为真时，main_lines将添加cond_buf_write行
    # 2.随机插入若干buf_write干扰组合
    return _assemble_general_example(dec_init_pairs, main_lines, dummy_vars,
                                     safe, substitutions,
                                     include_cond_bufwrite)


def _assemble_general_example(dec_init_pairs, main_lines, dummy_vars,
                              safe, substitutions, include_cond_bufwrite):
    """Get instance lines, convert to string, generate tags
       1.当include_cond_bufwrite为真时，main_lines将添加cond_buf_write行
       2.随机插入若干buf_write干扰组合

    Args:
        dec_init_pairs (list of tuple): declaration/initialization statements,
            e.g. those in templates.py
        main_lines (list of str): lines with the conditional or loop,
            e.g. those in templates.py
        dummy_vars (list of str): variable names available for use
        safe (bool): whether the conditional buffer write is safe
        substitutions (dict): names to substitute into templates
        include_cond_bufwrite (bool): whether to include the
            control flow-sensitive buffer write

    Returns:
        instance_str (str): str of code example
        tags (list of Tag): tag for each line representing buffer safety

    Ensures:
        len(instance_str.split("\n")) == len(tags)
    """

    # 当include_cond_bufwrite为真时，main_lines将添加cond_buf_write行
    if include_cond_bufwrite:
        # copy to avoid changing the template list due to aliasing
        main_lines = main_lines[:]
        main_lines += templates.BUFWRITE_LINES  # 在主条件语句的尾部添加bufwrite行
    else:  # 当include_cond_bufwrite为假时，main_lines将不添加cond_buf_write行，则就不存在safe与否的问题,所以将safe置为None
        safe = None

    # 随机插入若干干扰buf_write组合
    lines, body_tags = _get_lines(dec_init_pairs, main_lines,
                                  dummy_vars, safe, include_cond_bufwrite)
    tags = _get_tags(body_tags)
    instance_str = _get_instance_str(lines, substitutions,
                                     templates.FUNC_TMPL_STR, tags)  # 对模板进行替换。
    return instance_str, tags


# 返回MAX_NUM_VARS个变量名
def _get_anon_vars():
    """Get list of unique, anonymized variable names in random order

    Returns:
        anon_vars (list of str)
    """
    anon_vars = [VAR_STR % itm for itm in range(MAX_NUM_VARS)]  # VAR_STR是变量名模板
    random.shuffle(anon_vars)
    return anon_vars


# 从字符集中任意返回一个字符（数字字符，大小写字母字符）
def _get_char():
    """Get a random single character

    Returns:
        char (str): random single character from charset
    """
    char = random.choice(CHARSET)
    return char


def _get_lines(dec_init_pairs, main_lines, dummy_vars, safe,
               include_cond_bufwrite):
    """Create full body lines with setup, main content, and dummy interaction

    Args:
        dec_init_pairs (list of tuple)
        main_lines (list of str): lines that use the declared vars
        dummy_vars (list of str): variable names available for dummy use
        safe (bool): whether the query line access is safe (for tags)
            or None, if no conditional query line should be added
        include_cond_bufwrite (bool): whether to include the
            control flow-sensitive buffer write

    Returns:
        lines (list of str)
        body_tags (list of Tag instances): tags for each body line
    """
    # setup lines (declaring and initializing variables)
    setup_lines = _get_setup_lines(dec_init_pairs)  # 获得声明初始化代码列表，这样做是为了让每一行只有一条语句
    lines = setup_lines + main_lines
    # construct body tags before adding dummies
    body_tags = [Tag.BODY for _ in lines]  # 将所有行全部打上body tag
    if include_cond_bufwrite:  # 如果包含了cond_bufwrite，则对cond_bufwrite行的tag进行修正
        query_tag = Tag.BUFWRITE_COND_SAFE if safe else Tag.BUFWRITE_COND_UNSAFE
        body_tags[-1] = query_tag  # cond_bufwrite行在主条件语句的尾部

    # 根据是否include_cond_bufwrite设置干扰buf_write代码组合的个数
    min_num_dummies = 0 if include_cond_bufwrite else MIN_NUM_DUMMIES_TAUTONLY  # 如果包含了cond_buf_write，可不包含干扰buf_write代码组合
    num_dummies = random.randrange(min_num_dummies, MAX_NUM_DUMMIES + 1)  # 随机在该区间内去一个值作为干扰buf_write组合

    # Insert dummy array declare/set pairs (all safe sets)
    lines, body_tags = _insert_dummies(
        setup_lines, main_lines, dummy_vars, num_dummies, body_tags,
        include_cond_bufwrite)

    return lines, body_tags


# 将声明和定义语句对排好。因为字符数组只声明，不赋值。则用None表示
def _get_setup_lines(dec_init_pairs):
    """Get setup lines (declaring and initializing variables) in random order
    so that variables are declared before initialized. If the second entry of
    the tuple is None, this line only needs to be declared, not initialized,
    e.g. for char arrays.

    The point of this is that the variables collectively can be declared
    and initialized in any order, as long as each variable is declared
    before it is initialized.

    E.g. dec_init_pairs = [("int $idx_var;", "$idx_var = $idx_init;"),
                           ("char $buf_var[$buf_len];", None)]
         _get_setup_lines(dec_init_pairs) could be any of
         ["int $idx_var;", "$idx_var = $idx_init;", "char $buf_var[$buf_len];"]
         ["int $idx_var;", "char $buf_var[$buf_len];", "$idx_var = $idx_init;"]
         ["char $buf_var[$buf_len];", "int $idx_var;", "$idx_var = $idx_init;"]

    Args:
        dec_init_pairs (list of tuple)

    Returns:
        setup_lines (list of str)
    """
    setup_lines = []
    for (dec_str, init_str) in dec_init_pairs:
        if init_str is None:  # 表明是个数组声明模板 可以随机插入到任意一行
            idx = random.randrange(len(setup_lines) + 1)
            setup_lines = setup_lines[:idx] + [dec_str] + setup_lines[idx:]  # 因为是只声明，所以可以直接插入进来。
        else:
            idxes = sorted(  # 表明既有声明，又有初始化，则需要随机选择两个位置，而且要从小到大进行排序
                [random.randrange(len(setup_lines) + 1) for _ in range(2)])
            # 插入这两个特定的位置，先插入声明语句，再插入赋值语句
            setup_lines = (setup_lines[:idxes[0]] + [dec_str] +
                           setup_lines[idxes[0]:idxes[1]] + [init_str] +
                           setup_lines[idxes[1]:])

    return setup_lines


def _insert_dummies(setup_lines, main_lines, dummy_vars, num_dummies,
                    body_tags, include_cond_bufwrite):
    """Insert dummy array declare/set pairs (all safe sets)

    Args:
        setup_lines (list of str): declaration and initialization lines
        main_lines (list of str): control flow lines
        dummy_vars (list of str): variable names available for dummy use
        num_dummies (int): number of dummy vars to insert
        body_tags (list of Tag instances): tags before adding dummies
        include_cond_bufwrite (bool): whether to include the
            control flow-sensitive buffer write

    Returns:
        lines (list of str): with dummy dec/set pairs added
        body_tags (list of Tag instances): with tags added for dummy lines
    """

    lines = setup_lines + main_lines  # 将声明初始化列表和主行合并，main_lines仅包含有控制语句(包括cond_buf_write)

    # 确定main_lines的开始和结束索引，为插入干扰buf_write组合做准备
    # first line of control flow, inclusive
    control_flow_start = len(setup_lines)
    # last line of control flow, exclusive
    control_flow_end = len(setup_lines + main_lines)
    if include_cond_bufwrite:
        control_flow_end -= 1

    # 根据control_flow_start和control_flow_end,向lines插入num_dummies个干扰buf_write语句组合
    for _ in range(num_dummies):
        (lines, dummy_vars, body_tags, control_flow_start, control_flow_end
         ) = _insert_referential_dummy(
            lines, dummy_vars, body_tags, control_flow_start,
            control_flow_end)

    return lines, body_tags


def _insert_referential_dummy(lines, dummy_vars, body_tags,
                              control_flow_start, control_flow_end,
                              require_safe=False):
    """Insert dummy declare/set lines with referential index access
    下面是干扰语句组合的例子
    E.g. char entity_0[10];
         int entity_1;
         entity_1 = 5;
         entity_0[entity_1] = 'a';
    该函数讲解了如何将上述4条语句添加到lines中

    The char and int declarations happen first in a random order, followed by
    the int initialization and the buffer set.


    Args:
        lines (list of str): lines to insert dummy lines around
        dummy_vars (list of str): variable names available for dummy use
        body_tags (list of Tag instance): body tags before adding dummies
        control_flow_start (int): first idx of control flow lines
        control_flow_end (int): last idx of control flow lines
        require_safe (bool): if True, then require that dummy accesses are
            all safe


    Returns:
         lines (list of str): with dummy dec/set pair added
         dummy_vars (list of str): with used dummy varnames removed
         body_tags (list of Tag instance): with dummy tags added
         control_flow_start (int): updated from args
         control_flow_end (int): updated from args
    """
    if len(dummy_vars) < 2:  # 一个干扰buf_write组合至少需要利用2个dummy_var
        raise ValueError("Trying to insert more dummy vars than available")

    # 是否要求干扰buf_write语句组合必须安全
    if require_safe:
        dum_len = random.randrange(1, MAX_IDX)
        dum_idx = random.randrange(dum_len)  # dum_idx小于dum_len，则干扰buf_write语句安全
    else:
        # dum_len和dum_idx均随机取自[0,MAX_IDX),无法保证dum_idx<dum_len
        dum_len = random.randrange(MAX_IDX)  # dum数组的长度
        dum_idx = random.randrange(MAX_IDX)  # dum的index

    dum_buf_var = dummy_vars.pop()  # 弹出一个变量名作为数组变量名
    dum_int_var = dummy_vars.pop()  # 弹出一个变量名作为索引变量名
    buf_dec_line = "char %s[%s];" % (dum_buf_var, dum_len)  # 干扰数组声明语句
    idx_dec_line = "int %s;" % dum_int_var  # 索引变量声明语句
    idx_init_line = "%s = %s;" % (dum_int_var, dum_idx)  # 索引变量赋值语句
    buf_set_line = "%s[%s] = '%s';" % (dum_buf_var, dum_int_var,
                                       random.choice(CHARSET))  # buf_write语句

    """
    char $dum_buf_var[$dum_len]            buf_dec_line 干扰数组声明语句
    int $dum_int_var;                          idx_dec_line 索引变量声明语句
    $dum_int_var = $dum_idx;               idx_init_line 索引变量赋值语句
    $dum_buf_var[$dum_int_var] = $char;    buf_set_line 
    其中$char = random.choice(CHARSET)
    """

    # idx declaration must go before idx initialization
    setup_lines = [idx_dec_line, idx_init_line]
    # buffer declaration can go anywhere between them
    buf_dec_idx = random.randrange(3)  # 将buf_write语句随意选择一个位置插入
    setup_lines = (setup_lines[:buf_dec_idx] + [buf_dec_line] +
                   setup_lines[buf_dec_idx:])

    # 至此，setup_lines内部3条语句的相对位置已确定
    # 干扰组合的setup_lines和控制流无关，因此不能放在控制流里面，所以要么放在控制流行的前面，要么放在控制流行的后面。

    # whether these setup lines go before the control flow lines
    before_control_flow = random.choice([True, False])
    if before_control_flow:
        range_start = 0
        range_end = control_flow_start + 1
    else:  # 若将setup语句放在control flow语句后面
        range_start = control_flow_end
        range_end = len(lines) + 1

    # lines where buffer and index are declared; index is initialized
    setup_idxes = sorted([random.randrange(range_start, range_end)
                          for _ in range(3)])  # setup lines共3条语句，因此需要寻找3个位置，并从小到大进行排序，保持setup lines内部语句相对位置不变

    # line where buffer is set
    buf_set_idx = random.randrange(max(setup_idxes), len(lines) + 1)  # buf_set语句需要放到setup_lines语句之后

    # the amounts by which control_flow_{start, end} increase
    # after inserting these lines
    d_start = 0
    d_end = 0
    for idx in setup_idxes + [buf_set_idx]:
        if idx <= control_flow_start:
            d_start += 1
        if idx < control_flow_end:
            d_end += 1
    control_flow_start += d_start
    control_flow_end += d_end

    # 将干扰代码组合添加到lines中
    """
    setup_inxes[0]放buf_dec,idx_dec,idx_init中的一条，（之前已经排好了顺序）setup_lines[0]
    setup_idxes[1]放buf_dec,idx_dec,idx_init中的一条，setup_lines[1]
    setup_idxes[2]放buf_dec,idx_dec,idx_init中的一条，setup_lines[2]
    接下来是buf_set_idx放buf_set_line
    """

    lines = (lines[:setup_idxes[0]] + [setup_lines[0]] +
             lines[setup_idxes[0]:setup_idxes[1]] + [setup_lines[1]] +
             lines[setup_idxes[1]:setup_idxes[2]] + [setup_lines[2]] +
             lines[setup_idxes[2]:buf_set_idx] + [buf_set_line] +
             lines[buf_set_idx:])

    # 判断这个干扰组合中的buf_write是否安全，并修改body_tags
    safe = dum_idx < dum_len
    bufwrite_tag = Tag.BUFWRITE_TAUT_SAFE if safe else Tag.BUFWRITE_TAUT_UNSAFE
    body_tags = (body_tags[:setup_idxes[0]] + [Tag.BODY] +
                 body_tags[setup_idxes[0]:setup_idxes[1]] + [Tag.BODY] +
                 body_tags[setup_idxes[1]:setup_idxes[2]] + [Tag.BODY] +
                 body_tags[setup_idxes[2]:buf_set_idx] + [bufwrite_tag] +
                 body_tags[buf_set_idx:])  # 更新boday_tags

    return lines, dummy_vars, body_tags, control_flow_start, control_flow_end


def _get_instance_str(lines, substitutions, func_tmpl_str, tags,
                      tags_as_comments=True):
    """Make substitutions and construct function instance string

    Args:
        lines (list of str): lines in body, to be substituted
        substitutions (dict)
        func_tmpl_str (str): string for function template to substitute
        tags (list of Tag)
        tags_as_comments (bool): if True, then add the tag as a comment at the
            end of each line

    Returns:
        instance_str (str): complete function as string
    """
    lines = [string.Template(itm).substitute(substitutions) for itm in lines]  # 将所有模板代码语句进行替换
    body = "\n".join("    " + line for line in lines)  # 对body进行重新赋值
    substitutions['body'] = body
    instance_str = string.Template(func_tmpl_str).substitute(substitutions)

    # 如果需要添加tag作为注释
    if tags_as_comments:
        lines = instance_str.split("\n")
        max_linelen = max(len(line) for line in lines)  # 获得最长的行的长度
        fmt_str = "{:<{width}} // {}"  # 左对齐
        lines = [fmt_str.format(line, tag, width=max_linelen)
                 for (line, tag) in zip(lines, tags)]  # TODO(chenglinyu): Python zip函数的使用方法
        instance_str = "\n".join(lines)

    return instance_str


def _get_tags(body_tags):
    """Get full list of tags by adding wrappers

    Args:
        body_tags (list of Tag instances): for body lines only

    Returns:
        tags (list of Tag instances): for full function
    """
    #        #include... int main()    {
    tags = ([Tag.OTHER, Tag.OTHER, Tag.OTHER] +
            body_tags +
            # return 0;     }
            [Tag.BODY, Tag.OTHER])
    return tags


def _get_args():
    """Get command-line arguments 返回从命令行解析之后的参数"""
    separator = '\n' + "#" * 79 + '\n'
    parser = argparse.ArgumentParser(
        description=__doc__ + separator,
        formatter_class=argparse.RawDescriptionHelpFormatter)  # 描述已经正确排好格式
    parser.add_argument('outdir',
                        help=("(str) Path to directory to write instance.c files to. Must "
                              "exist before running"),
                        metavar="<path>")

    parser.add_argument('-num_instances',
                        help=("(int) Number of instance.c files to create; default "
                              "{}".format(DEFAULT_NUM_INSTANCES)),
                        default=DEFAULT_NUM_INSTANCES,
                        metavar="<int>")

    parser.add_argument('-seed',
                        help=("(int) Seed for random number generator, to reproduce results; "
                              "default {}. If -1 is passed, then use default Python "
                              "seed".format(DEFAULT_SEED)),
                        default=DEFAULT_SEED,
                        metavar="<int>")

    parser.add_argument('-metadata_file',
                        help=("(str) Path to a file which shall be used to store simple "
                              "json metadata about the generated instances"),
                        metavar="<path>")

    parser.add_argument('--taut_only',
                        action='store_true',
                        help=("If passed, then generate examples with only flow-insensitive "
                              "buffer writes"))

    parser.add_argument('--linear_only',
                        action='store_true',
                        help="If passed, then generate only flow-insensitive linear examples")

    args = parser.parse_args()
    return args  # 返回从命令行解析之后的参数


def main(args):
    """With fixed initial seed, generate instances and save as C files

    Args:
        args (argparse.Namespace), with attributes:
            num_instances (int): how many instances to generate
            outdir (str): path to directory to save instances; must exist
            seed (int): seed to use for random.seed(). If -1, then seed by
                default Python seeding

    Returns: 0 if no error
    """

    # check outdir paths
    outdir = args.outdir
    outdir = os.path.abspath(os.path.expanduser(outdir))
    if not os.path.isdir(outdir):  # 判断路径是否为目录
        raise OSError("outdir does not exist: '{}'".format(outdir))

    # set seed
    seed = int(args.seed)
    if seed != -1:
        random.seed(seed)

    tag_metadata = {} # store instance tag metadata
    taut_only = args.taut_only
    include_cond_bufwrite = not taut_only # 要么所有代码实例都包含cond_buf_write，要不都不包含
    inst_num = 0
    num_instances = int(args.num_instances)
    while inst_num < num_instances:
        # generate example
        instance_str, tags = gen_cond_example(
            include_cond_bufwrite=include_cond_bufwrite)

        # generate filename by instance_str
        fname = _generate_file_name(instance_str)
        if fname in tag_metadata:  # 如果刚好生成的两个文件名一样，那就说明这两个文件是一样的。
            # Collision, try again
            continue

        # insert record into metadata for this c file
        tag_metadata[fname] = [tag.value for tag in tags]

        # write instance_str to file
        path = os.path.join(outdir, fname)
        with open(path, 'w') as f:
            f.write(instance_str)

        inst_num += 1

    # Generate metadata only if the metadata_file argument is present
    generate_metadata = args.metadata_file is not None
    if generate_metadata:
        # construct the complete metadata
        metadata = {
            "working_dir": outdir,
            "num_instances": num_instances,
            "tags": tag_metadata
        }
        with open(args.metadata_file, 'w') as f:
            json.dump(metadata, f)

    return 0


def _generate_file_name(instance_str):
    """generate filename according to instance_str"""
    byte_obj = bytes(instance_str, 'utf-8')
    fname = hashlib.shake_128(byte_obj).hexdigest(FNAME_HASHLEN)
    fname = "{}.c".format(fname)
    return fname


if __name__ == '__main__':
    RET = main(_get_args())
    sys.exit(RET)
