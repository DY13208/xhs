from core.monitor.content_checker import ContentChecker
from core.monitor.risk_detector import RiskDetector

# 初始化模块
content_checker = ContentChecker()
risk_detector = RiskDetector()

# 示例笔记
note_title = "我最喜欢的旅行地"
note_content = "这是一次美妙的旅程，但千万不要提到违禁词。"

# 内容检测
is_safe, found_words = content_checker.is_content_safe(note_title, note_content)
if not is_safe:
    print(f"[ERROR] 笔记包含违规内容，不能发布。违规词：{found_words}")
else:
    print("[INFO] 笔记内容合规，可以发布。")

# 风控检测
for _ in range(5):
    if risk_detector.detect_risk():
        print("[ERROR] 检测到风险，停止操作。")
        break
    print("[INFO] 执行一次模拟操作...")
    time.sleep(random.randint(1, 3))
