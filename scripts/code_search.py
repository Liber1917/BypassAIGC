"""AI Code Review 搜索工具 — 模拟 Copilot 的 search_dir + read_code 流程"""
import os, sys, re, json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def search_dir(term: str, exts: list, path: str = ".") -> list:
    """搜索代码文件中的匹配行（模拟 Copilot search_dir）"""
    results = []
    root = PROJECT / path
    for f in root.rglob("*"):
        if f.suffix not in exts:
            continue
        if any(d in str(f) for d in ("node_modules", "venv", "__pycache__", ".git")):
            continue
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").split("\n"), 1):
                if term in line:
                    results.append({"file": str(f.relative_to(PROJECT)), "line": i, "snippet": line.strip()[:120]})
        except Exception:
            pass
    return results


def read_code(filepath: str, start: int, end: int) -> str:
    """读取指定文件的行范围（模拟 Copilot read_code）"""
    try:
        lines = (PROJECT / filepath).read_text(encoding="utf-8").split("\n")
        return "\n".join(f"{i+1}:{lines[i]}" for i in range(start - 1, min(end, len(lines))))
    except Exception as e:
        return f"[read error] {e}"


def check_gbk_safety() -> list:
    """检查 print()/logging 中的 GBK 不安全字符"""
    findings = []
    for f in PROJECT.rglob("*.py"):
        if any(d in str(f) for d in ("node_modules", "venv", "__pycache__", ".git")):
            continue
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
                s = line.strip()
                if not ("print(" in s or ".log(" in s or "logger." in s or "logging." in s):
                    continue
                if s.startswith("#"):
                    continue
                bad = []
                for ch in s:
                    cp = ord(ch)
                    if cp < 128 or (0x4E00 <= cp <= 0x9FFF) or (0x3000 <= cp <= 0x303F) or (0xFF00 <= cp <= 0xFFEF):
                        continue
                    if ch in "·—×±≥≤≠≈÷°′″℃™®©§《》【】「」『』（）—…～％＠＆＊":
                        continue
                    bad.append(f"U+{cp:04X}")
                if bad:
                    findings.append({"severity": "P0", "file": str(f.relative_to(PROJECT)), "line": i,
                                     "desc": f"print()含GBK不安全字符 {set(bad)}", "snippet": s[:100]})
        except Exception:
            pass
    return findings


def check_storage() -> list:
    """检查前端 localStorage 使用"""
    findings = []
    for f in (PROJECT / "package/frontend/src").rglob("*"):
        if f.suffix not in (".js", ".jsx"):
            continue
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
                if "localStorage" in line and "getItem" not in line:
                    findings.append({"severity": "P0", "file": str(f.relative_to(PROJECT)), "line": i,
                                     "desc": "使用了 localStorage（必须用 sessionStorage）", "snippet": line.strip()[:100]})
        except Exception:
            pass
    return findings


def check_sse_dead_code() -> list:
    """检查 SSE 路由中 Depends() 后面的死代码"""
    findings = []
    for pattern, desc in [
        (r"if token and not\s*\w+", "SSE路由中 token 检查在 Depends() 401 之后不可达"),
        (r"token.*=.*Query\(None\)", "Query token 声明"),
        (r"get_current_user\(\s*$", "get_current_user 调用（检查参数完整性）"),
    ]:
        for f in (PROJECT / "package/backend/app/routes").rglob("*.py"):
            for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
                if re.search(pattern, line):
                    findings.append({"file": str(f.relative_to(PROJECT)), "line": i, "pattern": pattern, "snippet": line.strip()[:100], "desc": desc})
    return findings


def check_token_passing() -> list:
    """检查 get_current_user 调用是否缺失 token 参数"""
    findings = []
    routes_file = PROJECT / "package/backend/app/word_formatter/routes.py"
    if not routes_file.exists():
        return findings
    lines = routes_file.read_text(encoding="utf-8").split("\n")
    for i, line in enumerate(lines, 1):
        if "= get_current_user(" in line and "def get_current_user" not in line:
            if "token=token" not in line and "token=" not in line:
                # 检查该路由是否声明了 token 参数
                for j in range(max(0, i - 10), i):
                    if "token:" in lines[j] and "Query" in lines[j]:
                        findings.append({"severity": "P0", "file": "package/backend/app/word_formatter/routes.py",
                                         "line": i, "desc": "get_current_user()调用缺失 token=token 参数",
                                         "snippet": line.strip()[:100]})
                        break
    return findings


def check_deprecated_apis() -> list:
    """检查废弃 API 使用"""
    findings = []
    for f in PROJECT.rglob("*.py"):
        if any(d in str(f) for d in ("node_modules", "venv", "__pycache__", ".git")):
            continue
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
                if "utcnow" in line and "datetime" in line:
                    findings.append({"severity": "P1", "file": str(f.relative_to(PROJECT)), "line": i,
                                     "desc": "弃用: datetime.utcnow()，使用 datetime.now(timezone.utc)", "snippet": line.strip()[:100]})
                if "@app.on_event" in line:
                    findings.append({"severity": "P1", "file": str(f.relative_to(PROJECT)), "line": i,
                                     "desc": "弃用: @app.on_event，使用 lifespan handlers", "snippet": line.strip()[:100]})
        except Exception:
            pass
    return findings


def check_version_consistency() -> list:
    """检查版本号一致性"""
    versions = {}
    for path, pattern in [
        ("package/backend/app/main.py", r'version="([\d.]+)"'),
        ("package/frontend/package.json", r'"version":\s*"([\d.]+)"'),
        ("package/main.py", r'version="([\d.]+)"'),
    ]:
        try:
            m = re.search(pattern, (PROJECT / path).read_text(encoding="utf-8"))
            if m:
                versions[path] = m.group(1)
        except Exception:
            pass
    if len(set(versions.values())) > 1:
        return [{"severity": "P1", "file": "多处", "line": 0,
                  "desc": f"版本号不一致: {json.dumps(versions, ensure_ascii=False)}"}]
    return []


def build_findings_report(findings: list) -> str:
    """构建结构化发现报告"""
    if not findings:
        return "无发现问题。"
    lines = []
    for f in sorted(findings, key=lambda x: x.get("severity", "P2")):
        sev = f.get("severity", "P2")
        file = f.get("file", "?")
        line = f.get("line", "?")
        desc = f.get("desc", "?")
        snippet = f.get("snippet", "")
        lines.append(f"[{sev}] {file}:{line} - {desc}")
        if snippet:
            lines.append(f"      代码: {snippet}")
    return "\n".join(lines)


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.chdir(PROJECT)

    print("=" * 60)
    print("AI Code Review — 多阶段搜索与审查")
    print("=" * 60)

    all_findings = []

    # Stage 1: GBK 安全
    print("\n>>> Stage 1: GBK安全扫描...")
    findings = check_gbk_safety()
    all_findings.extend(findings)
    print(f"    发现 {len(findings)} 个问题")

    # Stage 2: localStorage
    print("\n>>> Stage 2: localStorage扫描...")
    findings = check_storage()
    all_findings.extend(findings)
    print(f"    发现 {len(findings)} 个问题")

    # Stage 3: SSE 死代码
    print("\n>>> Stage 3: SSE死代码扫描...")
    findings = check_sse_dead_code()
    all_findings.extend(findings)
    print(f"    发现 {len(findings)} 个问题")

    # Stage 4: token 传参
    print("\n>>> Stage 4: token参数完整性扫描...")
    findings = check_token_passing()
    all_findings.extend(findings)
    print(f"    发现 {len(findings)} 个问题")

    # Stage 5: 废弃 API
    print("\n>>> Stage 5: 废弃API扫描...")
    findings = check_deprecated_apis()
    all_findings.extend(findings)
    print(f"    发现 {len(findings)} 个问题")

    # Stage 6: 版本号
    print("\n>>> Stage 6: 版本号一致性...")
    findings = check_version_consistency()
    all_findings.extend(findings)
    print(f"    发现 {len(findings)} 个问题")

    # 输出报告
    report = build_findings_report(all_findings)
    print("\n" + "=" * 60)
    print("审查结果报告")
    print("=" * 60)
    print(report)

    # 同时保存到文件供后续步骤使用
    with open("/tmp/review_findings.json", "w") as f:
        json.dump(all_findings, f, ensure_ascii=False, indent=2)
    with open("/tmp/review_report.txt", "w") as f:
        f.write(report)

    if all_findings:
        sys.exit(1)  # 有问题
    else:
        sys.exit(0)  # 干净


if __name__ == "__main__":
    main()
