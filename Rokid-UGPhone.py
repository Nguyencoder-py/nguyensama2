import cv2
import numpy as np
import time
import os

def adb_tap(x, y):
    """Hàm nhấn vào vị trí trên màn hình thông qua ADB."""
    os.system(f"adb shell input tap {x} {y}")

def find_image_on_screen(image_path, confidence=0.8):
    """Hàm tìm kiếm hình ảnh trên màn hình."""
    os.system("adb exec-out screencap -p > screen.png")  # Chụp màn hình thiết bị
    screenshot = cv2.imread("screen.png")
    template = cv2.imread(image_path)

    if screenshot is None or template is None:
        raise FileNotFoundError("Không thể đọc được ảnh chụp hoặc ảnh mẫu. Kiểm tra đường dẫn.")

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        print(f"Hình ảnh được tìm thấy với độ tin cậy: {max_val}")
        return max_loc  # Trả về tọa độ của hình ảnh trên màn hình
    else:
        print("Hình ảnh không được tìm thấy!")
        return None

def main():
    try:
        # Tìm và nhấn nút "Thêm nhanh cầu thủ"
        print("Tìm nút 'Thêm nhanh cầu thủ'...")
        add_quick_button_img = "add_quick_button.png"
        location = find_image_on_screen(add_quick_button_img)
        if location:
            adb_tap(location[0], location[1])
            time.sleep(1)

            # Nhấn nút "Trao đổi"
            print("Tìm nút 'Trao đổi'...")
            exchange_button_img = "confirm_button3.png"
            location = find_image_on_screen(exchange_button_img)
            if location:
                adb_tap(location[0], location[1])
                time.sleep(2)

                # Nhấn vào vị trí bất kỳ
                print("Nhấn vào vị trí bất kỳ...")
                adb_tap(100, 100)
                time.sleep(0.5)
                print("Nhấn vào vị trí bất kỳ...")
                adb_tap(100, 100)
                time.sleep(1)

                # Kiểm tra nút "Confirm"
                print("Tìm nút 'Confirm'...")
                confirm_button_img = "continue.png"
                location = find_image_on_screen(confirm_button_img)
                if location:
                    # Nhấn hai lần nút "Confirm"
                    adb_tap(location[0], location[1])
                    time.sleep(1)  # Đợi 400ms
                    adb_tap(location[0], location[1])
                    print("Hoàn tất!")
                else:
                    print("Nút 'Confirm' không tìm thấy! Dừng chương trình.")
            else:
                print("Nút 'Trao đổi' không tìm thấy! Dừng chương trình.")
                return False  # Ngừng chương trình nếu nút Trao đổi không tìm thấy
        else:
            print("Nút 'Thêm nhanh cầu thủ' không tìm thấy!")
            return False  # Ngừng chương trình nếu nút "Thêm nhanh cầu thủ" không tìm thấy
    except Exception as e:
        print(f"Lỗi: {e}")
        return False  # Nếu có lỗi, dừng chương trình

    return True  # Tiếp tục chạy nếu không có lỗi

if __name__ == "__main__":
    while True:  # Vòng lặp vô hạn
        if not main():  # Nếu không tìm thấy nút hoặc gặp lỗi, chương trình dừng lại
            print("Chương trình kết thúc.")
            break  # Dừng vòng lặp khi main trả về False
        time.sleep(1)  # Tạm nghỉ 1 giây trước khi lặp lại
