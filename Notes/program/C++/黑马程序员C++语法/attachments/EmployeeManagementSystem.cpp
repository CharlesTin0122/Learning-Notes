#include <iostream>

#include "workManager.h"
#include "worker.h"
#include "employee.h"
#include "manager.h"
#include "boss.h"

using namespace std;

//void test01()
//{
//	Worker* worker = NULL;
//	worker = new Employee(1, "张三", 1);
//	worker->show_info();
//	delete worker;
//
//	worker = new Manager(2, "李四", 2);
//	worker->show_info();
//	delete worker;
//
//	worker = new Boss(3, "王五", 3); 
//	worker->show_info();
//	delete worker;
//}

int main() {
	WorkManager wm1;

	int choise = 0;//存储用户选项
	while (true) {
		wm1.show_menu();
		cout << "请输入您的选择：" << endl;
		cin >> choise;

		switch (choise) {
		case 0: // 退出系统
			wm1.exit_system();
			break;
		case 1: // 增加职工
			wm1.add_emp();
			break;
		case 2: // 显示职工
			wm1.show_emp();
			break;
		case 3: // 删除职工
			wm1.del_emp();
			break;
		case 4: // 修改职工
			wm1.mod_emp();
			break;
		case 5: // 查找职工
			wm1.find_emp();
			break;
		case 6: // 排序职工
			wm1.sort_emp();
			break;
		case 7: // 清空表单
			wm1.clean_file();
			break;
		default:
			system("cls"); // 清屏
			break;
		}
	}

	system("pause");
	return 0;
}