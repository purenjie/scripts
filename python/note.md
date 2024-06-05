## 格式化字符串

```python
s = "格式化"
# 方式1
print("{0}字符串".format(s))
# 方式2 字符串中包含 { 或 } 时无法使用 
# f"{s}}"--报错
print(f"{s}字符串") 
# 方式3
print(s + "字符串")
```

## 命令行参数解析

```python
import argparse

parser = argparse.ArgumentParser(description="Realtime region query script")
parser.add_argument("-r", "--region", required=True, help="Region ID")
parser.add_argument("-d", "--date", required=True, help="Date in format 'YYYY-MM-DD'")
parser.add_argument("-e", "--env", default="", help="Environment")
parser.add_argument("--skip", default=False, help="skip no value key")

args = parser.parse_args()

region_id = args.region
```

