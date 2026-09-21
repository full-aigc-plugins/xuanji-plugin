# 基础示例：一轮记账与决策

```bash
python3 scripts/loop_ledger.py append --ledger .xuanji/loop-ledger.json \
  --entry '{"round":1,"artifact":".xuanji/round-1.png","scores":{"composition":2.5,"symbol":2.0,"mood":1.5,"detail":1.0},"total":7.0,"verdict":"continue","notes":"符号缺一枚"}'
python3 scripts/loop_ledger.py decide --ledger .xuanji/loop-ledger.json
```

输出 `continue` → 按解象意见改提示词后重成象。
