import re
import logging
import sys
import os

os.makedirs("Logs", exist_ok=True)

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("Logs/file_txt.log", encoding="utf-8")
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")


BLACKLIST = {
    "admin", "root", "user", "test", "guest",
    "administrator", "moderator", "support", "system", "vladislav"
}

PHONE_RE  = re.compile(r"^\+\d{1,3}-\d{3}-\d{3}-\d{4}$")
EMAIL_RE  = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
STRING_RE = re.compile(r"^[A-Za-z0-9_]{5,}$")

PASSWORD_ALLOWED_RE = re.compile(r"^[А-Яа-яЁё0-9!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]+$")
HAS_UPPER_CYR = re.compile(r"[А-ЯЁ]")
HAS_LOWER_CYR = re.compile(r"[а-яё]")
HAS_DIGIT     = re.compile(r"\d")
HAS_SPECIAL   = re.compile(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]")


def _validate_login(login: str):
    if login is None or login == "":
        return False, "Логин не может быть пустым"

    if login.startswith("+"):
        if not PHONE_RE.match(login):
            return False, "Неверный формат телефона (ожидается +x-xxx-xxx-xxxx)"
        return True, ""

    if "@" in login:
        if not EMAIL_RE.match(login):
            return False, "Неверный формат email"
        return True, ""

    if not STRING_RE.match(login):
        return False, ("Логин-строка должен содержать минимум 5 символов "
                       "и состоять только из латиницы, цифр и '_'")

    if login.lower() in BLACKLIST:
        return False, f"Логин '{login}' находится в чёрном списке"

    return True, ""

def _validate_password(password: str):
    if password is None or password == "":
        return False, "Пароль не может быть пустым"

    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов"

    if not PASSWORD_ALLOWED_RE.match(password):
        return False, ("Пароль может содержать только кириллицу, "
                       "цифры и спецсимволы")

    if not HAS_UPPER_CYR.search(password):
        return False, "Пароль должен содержать минимум одну заглавную букву (кириллица)"

    if not HAS_LOWER_CYR.search(password):
        return False, "Пароль должен содержать минимум одну строчную букву (кириллица)"

    if not HAS_DIGIT.search(password):
        return False, "Пароль должен содержать минимум одну цифру"

    if not HAS_SPECIAL.search(password):
        return False, "Пароль должен содержать минимум один спецсимвол"

    return True, ""


def register_user(login: str, password: str, confirm: str):
    logger = logging.getLogger(__name__)

    try:
        ok, reason = _validate_login(login)
        if not ok:
            return False, reason

        ok, reason = _validate_password(password)
        if not ok:
            return False, reason

        if password != confirm:
            return False, "Пароль и подтверждение пароля не совпадают"

        return True, ""

    except Exception:
        logger.error("Непредвиденная ошибка при валидации регистрации")
        logger.exception("Traceback:")
        return False, "Внутренняя ошибка валидации"


def main():
    while True:
        try:
            print("=== Регистрация пользователя ===")
            login    = input("Введите логин (телефон/email/строка): ")
            password = input("Введите пароль: ")
            confirm  = input("Подтвердите пароль: ")

        except (EOFError, KeyboardInterrupt):
            logging.warning("Ввод прерван пользователем")
            print("\nВвод прерван.")
            return
        
        if login.strip().lower() in ("q"):
                break

        logging.info(
            f"Запрос регистрации | login='{login}' | "
            f"password='{password}' | confirm='{confirm}'"
        )

        result, message = register_user(login, password, confirm)

        if result:
            logging.info(
                f"УСПЕХ регистрации | login='{login}' | "
                f"password='{password}' | result=True"
            )
            print("\n--- Результат ---")
            print("True")
            print("")
        else:
            logging.warning(
                f"ОТКАЗ регистрации | login='{login}' | "
                f"password='{password}' | reason='{message}'"
            )
            print("\n--- Результат ---")
            print("False")
            print(message)

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()