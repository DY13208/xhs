class LoginManager:
    _instance = None
    logged_in = False
    input_validator = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoginManager, cls).__new__(cls)
        return cls._instance

    def login_successful(self):
        self.logged_in = True

    def logout(self):
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in

    def set_input_validator(self, input_validator):
        self.input_validator = input_validator

    def show_login_prompt(self, parent=None):
        """ 提示用户登录 """
        if self.input_validator:
            try:
                print("Displaying login prompt...")  # Debugging line
                self.input_validator.show_empty_input_dialog(
                    title='未登录',
                    content="请先登录才能进行此操作"
                )
            except Exception as e:
                print(f"Error displaying login prompt: {e}")
                # Handle any unexpected error gracefully
        else:
            print("InputValidator is not set. Cannot show prompt.")
            if parent:
                print(parent, "错误", "登录提示框无法显示，未设置输入验证器。")
