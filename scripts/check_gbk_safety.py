"""检测 Python print()/logging 调用中的 GBK 不安全字符"""
import ast, sys, os, unicodedata

# GBK 安全的中文/日文/韩文区间
CJK_RANGES = [
    (0x4E00, 0x9FFF),   # CJK Unified Ideographs
    (0x3400, 0x4DBF),   # CJK Extension A
    (0xF900, 0xFAFF),   # CJK Compatibility Ideographs
    (0x3000, 0x303F),   # CJK Symbols and Punctuation
    (0xFF00, 0xFFEF),   # Halfwidth and Fullwidth Forms
]

# GBK 安全的标点/符号
SAFE_CHARS = set("·—×±≥≤≠≈÷°′″℃™®©§《》【】「」『』〔〕·…—～％＠＆＊（）【】「」")


def is_gbk_safe_char(ch: str) -> bool:
    cp = ord(ch)
    # ASCII 肯定安全
    if cp < 128:
        return True
    # CJK 范围安全
    for start, end in CJK_RANGES:
        if start <= cp <= end:
            return True
    # 特殊安全字符
    if ch in SAFE_CHARS:
        return True
    # 其他字符（emoji、dingbat、符号等）不安全
    return False


def scan_file(path: str) -> list:
    """扫描文件，找出 print()/logging 调用中的 GBK 不安全字符"""
    issues = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return issues

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 只检查包含 print 或 logging 调用的行
        if not ('print(' in stripped or '.log(' in stripped or 'logger.' in stripped or 'logging.' in stripped):
            continue
        # 跳过注释行
        if stripped.startswith('#') or stripped.startswith('//'):
            continue
        # 检查行中的每个字符
        bad_chars = set()
        for ch in stripped:
            if not is_gbk_safe_char(ch):
                bad_chars.add(f"U+{ord(ch):04X} {unicodedata.category(ch)} '{ch}'")
        if bad_chars:
            issues.append((path, i, line.strip()[:100], bad_chars))
    return issues


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    all_issues = []
    for dirpath, dirnames, filenames in os.walk(root):
        # 排除 venv/node_modules/.git/__pycache__
        dirnames[:] = [d for d in dirnames if d not in ('venv', 'node_modules', '.git', '__pycache__', '.pytest_cache')]
        for fn in filenames:
            if fn.endswith('.py'):
                path = os.path.join(dirpath, fn)
                all_issues.extend(scan_file(path))

    if all_issues:
        print(f"::error::Found {len(all_issues)} print()/logging calls with GBK-unsafe characters:")
        for path, lineno, snippet, chars in all_issues:
            print(f"  {path}:{lineno}  chars={{{','.join(chars)}}}  {snippet}")
        sys.exit(1)
    else:
        print("All print()/logging calls are GBK-safe.")


if __name__ == '__main__':
    main()
