import customtkinter as ctk
import threading
from main import TravelHelper


class TravelAssistantApp:
    def __init__(self):
        # 设置外观模式
        self.user_input = None
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title("旅游服务智能助手")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)

        # 设置窗口背景色
        self.root.configure(fg_color="#f8fafc")

        # 初始化助手
        self.assistant = TravelHelper()
        self.is_processing = False

        self.setup_ui()

    def setup_ui(self):
        # 配置网格布局
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 主框架 - 现代化设计
        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=20,
            fg_color="#ffffff",
            border_width=1,
            border_color="#e2e8f0"
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # 头部区域
        self.setup_header()

        # 聊天区域
        self.setup_chat_area()

        # 输入区域
        self.setup_input_area()

        # 快速操作区域
        self.setup_quick_actions()

        # 显示欢迎消息
        self.display_welcome_message()

    def setup_header(self):
        header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            height=120
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)

        # 装饰线条
        decoration_frame = ctk.CTkFrame(
            header_frame,
            height=3,
            fg_color="#4c6ef5",
            corner_radius=2
        )
        decoration_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        # 主标题 - 加粗
        title_label = ctk.CTkLabel(
            header_frame,
            text="旅游服务智能助手",
            font=ctk.CTkFont(size=32, weight="bold", family="Microsoft YaHei"),
            text_color="#1a365d"  # 更深的蓝色，更显眼
        )
        title_label.grid(row=1, column=0, pady=(0, 8))

        # 副标题 - 加粗
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="智能旅行伙伴 · 天气查询 · 景点推荐 · 路线规划 · 穿搭建议",
            font=ctk.CTkFont(size=14, weight="bold", family="Microsoft YaHei"),  # 加粗
            text_color="#4a5568"  # 更深的灰色
        )
        subtitle_label.grid(row=2, column=0, pady=(0, 10))

    def setup_chat_area(self):
        chat_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=16,
            fg_color="#f7fafc",
            border_width=1,
            border_color="#e2e8f0"
        )
        chat_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)

        # 聊天显示区域
        self.chat_display = ctk.CTkTextbox(
            chat_container,
            wrap="word",
            font=ctk.CTkFont(size=14, weight="bold", family="Microsoft YaHei"),  # 整体设置为粗体
            scrollbar_button_color="#4c6ef5",
            scrollbar_button_hover_color="#3b5bdb",
            border_width=0,
            corner_radius=12,
            fg_color="#ffffff",
            text_color="#2d3748"
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.chat_display.configure(state="disabled")

        # 配置文本样式 - 只设置颜色，不设置字体
        self.chat_display.configure(state="normal")
        self.chat_display.tag_config("user_prefix", foreground="#dc2626")  # 鲜艳的红色
        self.chat_display.tag_config("user_message", foreground="#2d3748")
        self.chat_display.tag_config("assistant_prefix", foreground="#2563eb")  # 鲜艳的蓝色
        self.chat_display.tag_config("assistant_message", foreground="#2d3748")
        self.chat_display.configure(state="disabled")

    def setup_input_area(self):
        input_container = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        input_container.grid(row=2, column=0, sticky="ew", padx=30, pady=10)
        input_container.grid_columnconfigure(0, weight=1)

        # 输入框容器
        input_frame = ctk.CTkFrame(
            input_container,
            corner_radius=25,
            height=60,
            fg_color="#ffffff",
            border_width=1,
            border_color="#e2e8f0"
        )
        input_frame.pack(fill="x", pady=5)
        input_frame.grid_propagate(False)
        input_frame.grid_columnconfigure(0, weight=1)

        # 输入框
        self.user_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="请输入您的问题，例如：北京天气怎么样？推荐上海景点...",
            font=ctk.CTkFont(size=14, family="Microsoft YaHei"),
            height=50,
            border_width=0,
            fg_color="transparent",
            text_color="#2d3748"
        )
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(25, 15), pady=5)
        self.user_input.bind('<Return>', lambda event: self.send_message())

        # 发送按钮
        send_btn = ctk.CTkButton(
            input_frame,
            text="发送",
            command=self.send_message,
            font=ctk.CTkFont(size=14, weight="bold"),  # 加粗
            height=50,
            width=100,
            fg_color="#4c6ef5",
            hover_color="#3b5bdb",
            corner_radius=20,
            text_color="#ffffff"
        )
        send_btn.grid(row=0, column=1, padx=(0, 15), pady=5)

    def setup_quick_actions(self):
        actions_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        actions_frame.grid(row=3, column=0, sticky="ew", padx=30, pady=(10, 20))

        # 快速提问标题 - 加粗
        actions_label = ctk.CTkLabel(
            actions_frame,
            text="快速提问",
            font=ctk.CTkFont(size=16, weight="bold", family="Microsoft YaHei"),  # 加粗
            text_color="#1a365d",  # 更深的蓝色
            anchor="w"
        )
        actions_label.pack(anchor="w", pady=(0, 15))

        actions_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_container.pack(fill="x")

        # 定义操作按钮 - 按钮文字加粗
        actions = [
            ("北京天气怎么样？", "#4c6ef5", "#3b5bdb"),
            ("北京的红色文化景点都有什么？", "#20c997", "#12b886"),
            ("从北京西站到故宫应该怎么走？", "#fd7e14", "#e8590c"),
            ("我今天应该怎么穿衣服？", "#e64980", "#d6336c"),
        ]

        for i, (text, color, hover_color) in enumerate(actions):
            btn = ctk.CTkButton(
                actions_container,
                text=text,
                command=lambda t=text: self.insert_example(t),
                font=ctk.CTkFont(size=13, weight="bold", family="Microsoft YaHei"),  # 加粗
                fg_color=color,
                hover_color=hover_color,
                text_color="#ffffff",
                height=40,
                corner_radius=20,
                border_width=0
            )
            btn.pack(side="left", padx=8, pady=5)

    def insert_example(self, example):
        self.user_input.delete(0, "end")
        self.user_input.insert(0, example)
        self.user_input.focus()

    def display_welcome_message(self):
        welcome_text = """
欢迎使用旅游服务智能助手！

我是您的专属旅行顾问小智，可以为您提供全方位的旅游服务支持：

天气查询 - 实时天气状况和预警信息
景点推荐 - 热门景点和个性化推荐
路线规划 - 驾车导航和详细指引
穿搭建议 - 基于天气的服装推荐

请随时告诉我您的需求，我会为您提供专业的建议和帮助！
        """.strip()

        self.display_message("assistant", welcome_text)

    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")

        if sender == "user":
            self.chat_display.insert("end", f"用户: ", "user_prefix")
            self.chat_display.insert("end", f"{message}\n\n", "user_message")
        else:
            self.chat_display.insert("end", f"小智: ", "assistant_prefix")
            self.chat_display.insert("end", f"{message}\n\n", "assistant_message")

        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def send_message(self):
        if self.is_processing:
            return

        user_text = self.user_input.get().strip()
        if not user_text:
            return

        # 清空输入框
        self.user_input.delete(0, "end")
        self.is_processing = True

        # 显示用户消息
        self.display_message("user", user_text)

        # 在新线程中处理助手响应
        threading.Thread(target=self.get_assistant_response, args=(user_text,), daemon=True).start()

    def get_assistant_response(self, user_input):
        try:
            response = self.assistant.chat(user_input)
            self.root.after(0, lambda: self.update_assistant_response(response, None))
        except Exception as e:
            self.root.after(0, lambda: self.update_assistant_response(None, str(e)))

    def update_assistant_response(self, response, error):
        self.is_processing = False

        if error:
            error_msg = f"抱歉，处理您的请求时出现了错误：{error}\n请检查网络连接或稍后重试。"
            self.display_message("assistant", error_msg)
        else:
            self.display_message("assistant", response)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TravelAssistantApp()
    app.run()