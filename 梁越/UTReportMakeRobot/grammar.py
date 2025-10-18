__package__ = "grammar"

grammar = r"""
start:stmt+
stmt: if_stmt
    | arithmetic_stmt
    | evaluation_stmt
    | call_stmt
    | assignment
    | exit_stmt
    | continue_stmt
    | section_name_stmt
    | section_exit_name_stmt
    | section_end_stmt
    | program_end_stmt
    | repeat_until_stmt
    | nihongo_macro_call_stmt
    | file_open_stmt
    | file_read_stmt
    | file_write_stmt
    | file_close_stmt
    | function_call_stmt
    | "."


if_stmt: "もし" condition "ならば" then_block ("上記条件以外のとき" else_block)? "終わり" (".")?
then_block: (stmt)+
else_block: (stmt)+

arithmetic_stmt: "計算" IDENTIFIER "=" arithmetic_expr (".")?

evaluation_stmt: "判定条件" evaluation_item_name ("条件は" evaluation_cond (stmt)+)+ "判定終了" (".")?
evaluation_item_name : IDENTIFIER | "TRUE"
evaluation_cond :IDENTIFIER | condition

call_stmt: "<->" IDENTIFIER (".")?

assignment: assignable_value "→" IDENTIFIER (".")?
assignable_value: IDENTIFIER | NUMBER | STRING | arithmetic_expr | builtin_function | "SPACE" | "ZERO"

exit_stmt: "セクション出口へ飛ぶ" IDENTIFIER (".")?
continue_stmt: "続ける" (".")?
section_name_stmt: IDENTIFIER "SECTION" (".")?
section_exit_name_stmt: IDENTIFIER ":"
section_end_stmt: "セクションの終わり" "."
program_end_stmt: "プログラムの終わり" "."

repeat_until_stmt: "条件" condition "になるまで下記処理を繰り返す" repeat_block "繰り返し終了" ("." )?
repeat_block: (stmt)+

function_call_stmt: builtin_function (".")?
builtin_function: "LENGTH" "OF" IDENTIFIER

nihongo_macro_call_stmt: "#" nihongo_macro_call ("#" nihongo_macro | nihongo_macro_parameter)* ","?
nihongo_macro_call: IDENTIFIER
nihongo_macro: IDENTIFIER
nihongo_macro_parameter: IDENTIFIER

file_open_stmt: "オープン" ("入力" | "出力") IDENTIFIER "."?
file_read_stmt: "ファイル" IDENTIFIER "を" IDENTIFIER "へ読み込む" "終了時" (stmt)+ "読む終了" (".")?
file_write_stmt: "出力エリア" IDENTIFIER "をファイル" IDENTIFIER "へ書く" (".")?
file_close_stmt: "クローズ" IDENTIFIER (".")?


condition: compare_expr | condition logic_op condition | "(" condition ")"
compare_expr: value compare_op value | value NOT compare_op value
value: IDENTIFIER | NUMBER | STRING | arithmetic_expr | builtin_function
arithmetic_expr: value arithmetic_op value | arithmetic_expr arithmetic_op value | "(" arithmetic_expr ")"

logic_op: LOGIC_OP
compare_op: COMPARE_OP
arithmetic_op: ARITHMETIC_OP


NOT: "NOT"
LOGIC_OP: "AND" | "OR" 
COMPARE_OP: "=" | "<" | "<=" | ">" | ">="
ARITHMETIC_OP : "+" | "-" | "*" | "/"


SPACE: "SPACE"
ZERO: "ZERO"
LENGTH: "LENGTH"
OF: "OF"

NUMBER: /-?\d+(\.\d+)?/
STRING: /'[^']*'|"[^"]*"/


IDENTIFIER: /(?!(?:AND|OR|NOT|SPACE|ZERO|LENGTH|OF)\b)[a-zA-Z0-9\uFF10-\uFF19\uFF21-\uFF3A\uFF41-\uFF5A\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\uFF00-\uFFEF\u4E00-\u9FFF\-\u2212\uFF0D]+/

%import common.WS
%ignore WS
%ignore /\r?\n/
"""