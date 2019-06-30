COND_DEC_INIT_PAIRS = [
    ("char $buf_var[$buf_len];", None),
    ("int $idx_var;", "$idx_var = $idx_init;"),
    ("int $thresh_var;", "$thresh_var = $thresh;")
]  # 每个元组有2个维度。第1个维度为声明语句，第2个维度为初始化语句

COND_MAIN_LINES = [
    "if($idx_var < $thresh_var){",
    "$idx_var = $true_idx;",
    "} else {",
    "$idx_var = $false_idx;",
    "}"
]

BUFWRITE_LINES = ["$buf_var[$idx_var] = '$char';"]

FUNC_TMPL_STR = """#include <stdlib.h>
int main()
{
$body
    return 0;
}"""
