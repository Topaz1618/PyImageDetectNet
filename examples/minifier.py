import pyminifier

input_file = 'detect_paddle.py'  # 要混淆的源代码文件名
output_file = 'detect_paddle_mix.py'  # 混淆后的输出文件名

# 执行代码混淆
pyminifier.main(input_file, output_file, remove_literal_statements=True)