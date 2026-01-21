import allure

def log_step(message: str):
    allure.attach(
        message,
        name="Step Log",
        attachment_type=allure.attachment_type.TEXT
    )
