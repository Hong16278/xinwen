import os
import sys

import requests


def main() -> int:
    webhook_url = ""
    source = ""
    if len(sys.argv) > 1 and sys.argv[1].strip():
        webhook_url = sys.argv[1].strip()
        source = "argv"
    else:
        webhook_url = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
        source = "env" if webhook_url else ""

    if not webhook_url:
        try:
            from trendradar.core import load_config
            config = load_config()
            webhook_url = (config.get("FEISHU_WEBHOOK_URL") or "").strip()
            source = "config" if webhook_url else source
        except Exception:
            pass

    if not webhook_url:
        print("缺少飞书 Webhook URL：请在 config/config.local.yaml 配置或设置 FEISHU_WEBHOOK_URL，或传入第一个参数")
        return 2

    print(f"使用飞书 Webhook 来源: {source}")
    text = os.environ.get("FEISHU_TEST_TEXT", "").strip() or "TrendRadar 本地飞书推送测试"
    payload = {"msg_type": "text", "content": {"text": text}}

    resp = requests.post(webhook_url, json=payload, timeout=30)
    print(f"HTTP {resp.status_code}")
    try:
        print(resp.json())
    except Exception:
        print(resp.text)
    return 0 if resp.status_code == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main())
