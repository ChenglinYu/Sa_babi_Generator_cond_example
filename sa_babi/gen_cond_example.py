"""gen_cond_example.py: generate fv_for_examples"""

import argparse
import hashlib
import os
import random
import string
import sys
import json

from pycallgraph.output import GraphvizOutput
from pycallgraph import PyCallGraph

import cond_template as templates

# TODO: move away from this ugly hack by merging the conda enviroment in pipeline/ into Docker
# sys_path_parent = os.path.abspath('..')
# if sys_path_parent not in sys.path:
#    sys.path.append(sys_path_parent)
# from classes.sa_tag import Tag
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
    # check args
    outdir = args.outdir
    seed = int(args.seed)
    num_instances = int(args.num_instances)
    taut_only = args.taut_only
    linear_only = args.linear_only

    # check paths
    outdir = os.path.abspath(os.path.expanduser(outdir))
    if not os.path.isdir(outdir):  # 判断路径是否为目录
        raise OSError("outdir does not exist: '{}'".format(outdir))

    # set seed
    if seed != -1:
        random.seed(seed)

    # Generate metadata only if the metadata_file argument is present
    generate_metadata = args.metadata_file is not None
    # This dict is used to store instance metadata
    tag_metadata = {}
    inst_num = 0

    while inst_num < num_instances:
        # generate example
        include_cond_bufwrite = not taut_only
        instance_str, tags = gen_cond_example(
            include_cond_bufwrite=include_cond_bufwrite)

        # generate filename
        byte_obj = bytes(instance_str, 'utf-8')
        fname = hashlib.shake_128(byte_obj).hexdigest(FNAME_HASHLEN)
        fname = "{}.c".format(fname)
        if fname in tag_metadata:  # 如果刚好生成的两个文件名一样，那就说明这两个文件是一样的。
            # Collision, try again
            continue

        # insert record into metadata for this c file
        tag_metadata[fname] = [tag.value for tag in tags]
        inst_num += 1

        # write to file
        path = os.path.join(outdir, fname)
        with open(path, 'w') as f:
            f.write(instance_str)

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
    buf_var, idx_var, thresh_var = anon_vars[:3]  # 获取前三个变量名 缓存变量，索引变量 阈值变量
    dummy_vars = anon_vars[3:]  # 获取剩下的变量名
    buf_len = random.randrange(MAX_IDX)  # 随机获取一个缓存的长度
    idx_init = random.randrange(MAX_IDX)  # 获取一个初始索引
    thresh = random.randrange(MAX_IDX)  # 获取一个合法阈值索引
    true_idx = random.randrange(MAX_IDX)  # 正确的索引
    false_idx = random.randrange(MAX_IDX)  # 错误的索引
    char = _get_char()  # 随机获取一个数字或者是字母字符
    substitutions = {
        'buf_var': buf_var,
        'idx_var': idx_var,  # 索引变量即为最终索引的索引值
        'buf_len': buf_len,
        'thresh': thresh,
        'thresh_var': thresh_var,
        'idx_init': idx_init,
        'true_idx': true_idx,
        'false_idx': false_idx,
        'char': char
    }
    main_lines = templates.COND_MAIN_LINES  # 主条件语句模板
    cond = idx_init < thresh  # 判断是否满足条件，跟模板中的代码是一致的。

    # 代码安全有两种情况
    # 1.条件判断为真，且true_idx<buf_len
    # 2.条件判断为假，且false_idex<buf_len
    # 因为是条件语句，最后也只能是其中的一种情况，所以只需要满足一种情况就可以了 这与自由的是不一样的。都是可控的
    safe = ((cond and (true_idx < buf_len)) or
            (not cond and (false_idx < buf_len)))
    dec_init_pairs = templates.COND_DEC_INIT_PAIRS  # 条件语句初始化模板

    return _assemble_general_example(dec_init_pairs, main_lines, dummy_vars,
                                     safe, substitutions,
                                     include_cond_bufwrite)


# 对某一个模块语句而言，将其拼凑起来凑成一整个模块
def _assemble_general_example(dec_init_pairs, main_lines, dummy_vars,
                              safe, substitutions, include_cond_bufwrite):
    """Get instance lines, convert to string, generate tags

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
    # 如果后面跟buffer write的话，就存在safe与否的问题
    if include_cond_bufwrite:
        # copy to avoid changing the template list due to aliasing
        main_lines = main_lines[:]
        main_lines += templates.BUFWRITE_LINES  # 赋值语句是直接在条件语句后面加的。相当于将后面的赋值作为了条件语句的一部分
    else:  # 如果后面不跟buffer write的话，就不存在safe与否的问题。
        safe = None

    # _get_lines函数最关键！
    lines, body_tags = _get_lines(dec_init_pairs, main_lines,
                                  dummy_vars, safe, include_cond_bufwrite)  # 引进dummy_vars，以及打乱顺序，其实就是taut_only的一些
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
    setup_lines = _get_setup_lines(dec_init_pairs)  # 获得初始化代码列表，这样做是为了让每一行只有一个代码
    lines = setup_lines + main_lines  # mainlines则不存在声明和初始化的问题，所以不需要这样

    # construct body tags before adding dummies
    body_tags = [Tag.BODY for _ in lines]  # 将所有行全部打上body tag
    if include_cond_bufwrite:  # 如果包含了数组赋值，则需要对数组赋值语句的tag进行修正
        query_tag = Tag.BUFWRITE_COND_SAFE if safe else Tag.BUFWRITE_COND_UNSAFE
        body_tags[-1] = query_tag  # 数组赋值语句肯定在最后一行

    min_num_dummies = 0 if include_cond_bufwrite else MIN_NUM_DUMMIES_TAUTONLY  # 如果包含了条件赋值语句，最小的dummie数为0
    num_dummies = random.randrange(min_num_dummies, MAX_NUM_DUMMIES + 1)  # 在min_num_dummies和3得到一个数作为dummy的数目
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
    lines = setup_lines + main_lines  # 重用了初始化代码列表

    # first line of control flow, inclusive 到这里,main_lines依然是仅仅有控制语句
    control_flow_start = len(setup_lines)
    # last line of control flow, exclusive
    control_flow_end = len(setup_lines + main_lines)
    if include_cond_bufwrite:
        control_flow_end -= 1

    for _ in range(num_dummies):  # 向其中插入num_dummies个dummy
        (lines, dummy_vars, body_tags, control_flow_start, control_flow_end
         ) = _insert_referential_dummy(
            lines, dummy_vars, body_tags, control_flow_start,
            control_flow_end)

    return lines, body_tags


def _insert_referential_dummy(lines, dummy_vars, body_tags,
                              control_flow_start, control_flow_end,
                              require_safe=False):
    """Insert dummy declare/set lines with referential index access
    E.g. char entity_0[10];
         int entity_1;
         entity_1 = 5;
         entity_0[entity_1] = 'a';

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
    if len(dummy_vars) < 2:  # 至少要插入两个dummy_var
        raise ValueError("Trying to insert more dummy vars than available")

    if require_safe:  # 默认是不要求安全
        dum_len = random.randrange(1, MAX_IDX)
        dum_idx = random.randrange(dum_len)
    else:
        dum_len = random.randrange(MAX_IDX)  # dum数组的长度
        dum_idx = random.randrange(MAX_IDX)  # dum的index

    dum_buf_var = dummy_vars.pop()  # 弹出一个dummy var作为buffer_var
    dum_int_var = dummy_vars.pop()  # 弹出一个变量作为index变量
    buf_dec_line = "char %s[%s];" % (dum_buf_var, dum_len)  # dummy buffer声明
    idx_dec_line = "int %s;" % dum_int_var  # 声明索引变量
    idx_init_line = "%s = %s;" % (dum_int_var, dum_idx)  # 索引变量赋值
    buf_set_line = "%s[%s] = '%s';" % (dum_buf_var, dum_int_var,  # 给buffer赋值
                                       random.choice(CHARSET))

    """
    char $dum_buf_var[$dum_len]            buf_dec_line
    int $int_var;                          idx_dec_line
    $dum_int_var = $dum_idx;               idx_init_line
    $dum_buf_var[$dum_int_var] = $char;    buf_set_line 这个肯定是放在最后的，因为要前面3个做基础。
    其中$char = random.choice(CHARSET)
    """

    # idx declaration must go before idx initialization
    setup_lines = [idx_dec_line, idx_init_line]
    # buffer declaration can go anywhere between them
    buf_dec_idx = random.randrange(3)  # 声明可以随意挑个位置 因为现在setup_lines只有两个元素
    setup_lines = (setup_lines[:buf_dec_idx] + [buf_dec_line] +
                   setup_lines[buf_dec_idx:])

    # whether these setup lines go before the control flow lines
    before_control_flow = random.choice([True, False])
    if before_control_flow:
        range_start = 0
        range_end = control_flow_start + 1
    else:  # 如果将setup行放在control flow的后面的话
        range_start = control_flow_end
        range_end = len(lines) + 1

    # lines where buffer and index are declared; index is initialized
    setup_idxes = sorted([random.randrange(range_start, range_end)
                          for _ in range(3)])  # 因为有3条语句，所以需要寻找3个为位置，三条语句的内部顺序
    # 已经进行过打乱

    # line where buffer is set
    buf_set_idx = random.randrange(max(setup_idxes), len(lines) + 1)  # buf_set_idx只需要放到之前的3条之后即可！

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

    # 这才真正的添加到lines当中来
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

    safe = dum_idx < dum_len  # 判断这个dum赋值是安全还是不安全
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
    lines = [string.Template(itm).substitute(substitutions) for itm in lines]  # 这行代码不知道是什么意思！
    body = "\n".join("    " + line for line in lines)  # 对body进行重新赋值
    substitutions['body'] = body
    instance_str = string.Template(func_tmpl_str).substitute(substitutions)

    if tags_as_comments:  # tags作为注释
        lines = instance_str.split("\n")
        max_linelen = max(len(line) for line in lines)  # 获得最长的行的长度
        fmt_str = "{:<{width}} // {}"  # 左对齐
        lines = [fmt_str.format(line, tag, width=max_linelen)
                 for (line, tag) in zip(lines, tags)]
        instance_str = "\n".join(lines)

    return instance_str


# 加上开始和最后的标注
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


# 获取来自命令行的参数 搞清楚了要传进来哪些参数，就知道该如何解析参数了！
def _get_args():  # 今天搞到了这里！
    """Get command-line arguments"""
    separator = '\n' + "#" * 79 + '\n'
    parser = argparse.ArgumentParser(
        description=__doc__ + separator,
        formatter_class=argparse.RawDescriptionHelpFormatter)

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
    return args  # 根据我们输入的参数，直接就可以传入main函数中


# _test() # 在正式生成之前，先进行了一个测试。

if __name__ == '__main__':
    graphviz = GraphvizOutput()

    graphviz.output_file = 'gen_cond_example.png'

    # with PyCallGraph(output=graphviz):
    #     RET = main(_get_args())
    #     sys.exit(RET)
    RET = main(_get_args())
    sys.exit(RET)
