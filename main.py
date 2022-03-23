import sys
import traceback

from PyQt5.QtWidgets import QApplication

from ui.mainProgram import MainProgram


def _main():
    app = 0
    try:
        # 代码顺序：新建 QApplication后 再新建MainProgram对象， 否则会报异常，待查资料
        app = QApplication(sys.argv)
        main_ui = MainProgram()

        # # 初始化全局变量
        # 显示在屏幕中央
        desktop = QApplication.desktop()  # 获取坐标
        x = (desktop.width() - main_ui.width()) // 2
        y = (desktop.height() - main_ui.height()) // 2
        main_ui.move(x, y)  # 移动
        main_ui.show()
        sys.exit(app.exec_())
    except:
        traceback.print_exc()
        if app != 0:
            app.closeAllWindows()


if __name__ == '__main__':
    _main()

