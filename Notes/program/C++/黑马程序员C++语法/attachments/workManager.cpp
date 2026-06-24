#include "workManager.h"
#include "worker.h"
#include "employee.h"
#include "manager.h"
#include "boss.h"

//构造函数
WorkManager::WorkManager()
{
	ifstream ifs;//实例化输入流
	ifs.open(FILENAME, ios::in); // 输入流对象读取文件

	//如果文件不存在
	if (!ifs.is_open())
	{
		cout << "File does not exist..." << endl;
		this->m_emp_num = 0;//初始化人数为0
		this->m_file_is_empty = true;//初始化文件为空
		this->m_emp_array = NULL;//初始员工数组为空
		ifs.close(); // 关闭文件
		return;
	}
	//如果文件存在且数据为空。
	char ch; // 创建一个字符变量
	ifs >> ch; // 将'ifs'中的最后一个字符右移到字符变量'ch'
	if (ifs.eof())
	{
		cout << "File is empty..." << endl;
		this->m_emp_num = 0;//初始化人数为0
		this->m_file_is_empty = true;//初始化文件为空
		this->m_emp_array = NULL;//初始员工数组为空
		ifs.close(); // 关闭文件
		return;
	}
	//文件存在，且记录数据
	int num = this->get_emp_num();//通过get_emp_num()函数，初始化员工数量
	cout << "The number of employees is:" << num << endl;
	this->m_emp_num = num;//成员属性赋值
	//根据员工数创建数组
	this->m_emp_array = new Worker * [this->m_emp_num];
	//初始化职工数组
	init_emp();
}
//显示菜单
void WorkManager::show_menu()
{
	cout << "*****************************************" << endl;
	cout << "**********欢迎使用职工管理系统***********" << endl;
	cout << "********** 0.退出管理程序 ***************" << endl;
	cout << "********** 1.添加职工信息 ***************" << endl;
	cout << "********** 2.显示职工信息 ***************" << endl;
	cout << "********** 3.删除职工信息 ***************" << endl;
	cout << "********** 4.修改职工信息 ***************" << endl;
	cout << "********** 5.查找职工信息 ***************" << endl;
	cout << "********** 6.排序职工信息 ***************" << endl;
	cout << "********** 7.清空职工信息 ***************" << endl;
	cout << "*****************************************" << endl;
	cout << endl;
}
//添加职工
void WorkManager::add_emp()
{
	cout << "请输入增加职工的数量：" << endl;

	int add_num = 0;
	cin >> add_num;

	if (add_num > 0) 
	{
		//计算所需空间大小：原来职工数 + 新增职工数
		int new_size = this->m_emp_num + add_num;
		//在堆区开辟空间，堆区开辟Worker*数组数据，返回Work**数据，是指向指针的指针，为二级指针。
		Worker** new_space = new Worker * [new_size];
		//将原空间下的内容放到新空间下
		if (this->m_emp_array != NULL)
		{
			for (int i = 0; i < this->m_emp_num; i++)
			{
				new_space[i] = this->m_emp_array[i];
			}
		}
		//添加新数据
		for (int i = 0; i < add_num; i++)
		{
			int id;//职工编号
			string name;//职工姓名
			int d_select;//部门选择

			cout << "请输入第" << i + 1 << "个新职工编号：" << endl;
			//循环输入编号，直到输入不重复的编号
			while (true) {
				cin >> id;

				int res = this->is_exist(id);
				if (res != -1) {
					cout << "此员工编号已存在，请重新输入" << endl;
				}
				else {
					break;
				}
			}


			cout << "请输入第" << i + 1 << "个新职工姓名：" << endl;
			cin >> name;
			cout << "请选择职工岗位：" << endl;
			cout << "1.职工" << endl;
			cout << "2.经理" << endl;
			cout << "3.老板" << endl;
			cin >> d_select;
			//创建基类指针，用于接受子类对象。
			Worker* worker = NULL;
			//根据不同的部门选择，创建不同的子类对象
			switch (d_select)
			{
			case 1:
				worker = new Employee(id, name, 1);
				break;
			case 2:
				worker = new Manager(id, name, 2);
				break;
			case 3:
				worker = new Boss(id, name, 3);
				break;
			default:
				cout << "无效的岗位选择，职工未被添加。" << endl;
				i--; // Decrement to retry this index
				add_num--; // Decrease the total count of employees to be added
				continue;
			}
			//数据存入数组
			new_space[this->m_emp_num + i] = worker;
		}
		//释放原有空间
		delete[] this->m_emp_array;
		//指针指向新空间
		this->m_emp_array = new_space;
		//更新员工个数
		this->m_emp_num = new_size;

		//提示信息
		cout << "成功添加" << add_num << "名新职工" << endl;
		//打印信息
		for (int i = 0; i < this->m_emp_num; i++)
		{
			cout << this->m_emp_array[i]->m_id << "   "
				<< this->m_emp_array[i]->m_name << "   "
				<< this->m_emp_array[i]->m_dept << endl;
		}
		//保存文件
		this->save_file();
		//更新文件不为空变量
		this->m_file_is_empty = false;
	}
	else
	{
		cout << "输入有误" << endl;
	}
	//按任意键清屏并回到上级目录
	system("pause");
	system("cls");
}
//保存文件
void WorkManager::save_file()
{
	ofstream ofs;//实例化流对象
	ofs.open(FILENAME, ios::out);//打开/创建文件
	//写入文件
	for (int i = 0; i < this->m_emp_num; i++)
	{
		ofs << this->m_emp_array[i]->m_id << " "
			<< this->m_emp_array[i]->m_name << " "
			<< this->m_emp_array[i]->m_dept << endl;
	}
	ofs.close();//关闭文件
}
//统计人数
int WorkManager::get_emp_num() 
{
	//实例化输入流对象并打开文件
	ifstream ifs;
	ifs.open(FILENAME, ios::in);
	//设置读取变量
	int id;
	string name;
	int dep;

	int num = 0;
	//读完一行数据之后，num变量自增以获取数据中的员工个数
	while (ifs >> id && ifs >> name && ifs >> dep)
	{
		num++;
	}
	ifs.close();
	return num;
}
//初始化数据
void WorkManager::init_emp()
{
	//实例化输入流对象并打开文件
	ifstream ifs;
	ifs.open(FILENAME, ios::in);
	//设置读取变量
	int id;
	string name;
	int dep;

	int index = 0;
	while (ifs >> id && ifs >> name && ifs >> dep)
	{
		Worker* worker = NULL;
		//根据不同的部门创建不同的对象
		if (dep == 1) {
			worker = new Employee(id, name, dep);
		}
		else if (dep == 2) {
			worker = new Manager(id, name, dep);
		}
		else {
			worker = new Boss(id, name, dep);
		}
		//存放在数组中
		this->m_emp_array[index] = worker;
		//索引自增
		index++;
	}
	ifs.close();
}
//显示员工
void WorkManager::show_emp() 
{
	if (this->m_file_is_empty) {
		cout << "File does not exist or data is empty" << endl;
	}
	else {
		for (int i = 0; i < m_emp_num; i++) {
			this->m_emp_array[i]->show_info();
		}
	}
	system("pause");
	system("cls");
}
//判断员工是否存在.存在返回编号，不存在返回-1
int WorkManager::is_exist(int id)
{
	int index = -1;
	for (int i = 0; i < this->m_emp_num; i++)
	{
		if (this->m_emp_array[i]->m_id == id)
		{
			index = i;
			break;
		}
	}
	return index;
}
//删除职工
void WorkManager::del_emp()
{
	if (this->m_file_is_empty) {
		cout << "File does not exist or data is empty" << endl;
	}
	else {
		//按照编号删除
		cout << "请输入要删除的职工编号" << endl;
		int id = 0;
		cin >> id;

		int index = this->is_exist(id);//判断该职工是否存在，不存在返回-1，存在返回员工编号
		// 如果该员工存在，则执行删除。
		if (index != -1) {
			//该员工之后的数组成员前移，覆盖该员工。
			for (int i = index; i < this->m_emp_num - 1; i++) {
				this->m_emp_array[i] = this->m_emp_array[i + 1];
			}
			
			this->m_emp_num--;//修改员工个数减一
			this->save_file();//数据存盘
		}
		else {
			cout << "Deletion failed, the employee was not found." << endl;
		}

	}
	system("pause");
	system("cls");

}
//修改职工信息
void WorkManager::mod_emp() 
{
	if (this->m_file_is_empty) {
		cout << "File does not exist or data is empty" << endl;
	}
	else {
		cout << "请输入要修改职工的编号" << endl;
		int id;
		cin >> id;
		//查询此ID员工是否存在
		int res = this->is_exist(id);
		//如果存在，删除之前的员工数据，创建新的员工数据
		if (res != -1) {
			delete this->m_emp_array[res];//释放之前的员工数据
			//创建新的员工信息
			int new_id = 0;
			string new_name = "";
			int new_dep = 0;

			cout << "查询到：" << id << "号员工，请输入新职工号：" << endl;
			cin >> new_id;

			cout << "请输入新姓名：" << endl;
			cin >> new_name;

			cout << "请输入岗位：" << endl;
			cout << "1.职工" << endl;
			cout << "2.经理" << endl;
			cout << "3.老板" << endl;
			cin >> new_dep;
			//创建新的员工数据
			Worker* worker = NULL;
			switch (new_dep) {
			case 1:
				worker = new Employee(new_id, new_name, new_dep);
				break;
			case 2:
				worker = new Manager(new_id, new_name, new_dep);
				break;
			case 3:
				worker = new Boss(new_id, new_name, new_dep);
				break;
			default:
				break;
			}
			//新的员工数据加入数组
			this->m_emp_array[res] = worker;
			cout << "修改成功！" << endl;
			this->save_file();
		}
		else {
			cout << "修改失败，查无此人" << endl;
		}
	}
	system("pause");
	system("cls");
}
//查询员工
void WorkManager::find_emp()
{
	if (this->m_file_is_empty) {
		cout << "File does not exist or data is empty" << endl;
	}
	else {
		cout << "请输入查找方式：" << endl;
		cout << "1.按职工编号查找：" << endl;
		cout << "2.按姓名查找：" << endl;

		int input_mod = 0;
		cin >> input_mod;
		//按职工编号查找
		if (input_mod == 1) {
			int id;
			cout << "请输入要查找的职工编号" << endl;
			cin >> id;

			int res = this->is_exist(id);
			if (res != -1) {
				cout << "查找成功，职工信息如下：" << endl;
				this->m_emp_array[res]->show_info();
			}
			else {
				cout << "查无此人" << endl;
			}
		}
		//按姓名查找
		else if (input_mod == 2) {
			string name;
			cout << "请输入要查找的姓名" << endl;
			cin >> name;

			bool flag = false;//创建一个布尔变量用于接收遍历结果
			for (int i = 0; i < m_emp_num; i++) {
				if (this->m_emp_array[i]->m_name == name) {
					cout << "查找成功，职工编号为："
						<< this->m_emp_array[i]->m_id
						<< "号的信息如下：" << endl;
					this->m_emp_array[i]->show_info();

					flag = true;
				}
			}
			if (flag == false) {
				cout << "查无此人" << endl;
			}
		}
		else {
			cout << "输入选项有误" << endl;
		}
	}
	system("pause");
	system("cls");
}
//排序职工
void WorkManager::sort_emp() {
	if (this->m_file_is_empty) {
		cout << "File does not exist or data is empty" << endl;
		system("pause");
		system("cls");
	}
	else {
		cout << "请选择排序方式" << endl;
		cout << "1.按照工号进行升序排列" << endl;
		cout << "2.按照工号进行降序排列" << endl;

		int sort_mod = 0;
		cin >> sort_mod;
		//选择排序
		for (int i = 0; i < m_emp_num; i++) {
			int min_or_max = i;//最大值或最小值的索引
			for (int j = i + 1; j < m_emp_num; j++) {
				//升序排列
				if (sort_mod == 1) {
					if (this->m_emp_array[min_or_max]->m_id > this->m_emp_array[j]->m_id) {
						min_or_max = j;
					}
				}
				//降序排序
				else if (sort_mod == 2) {
					if (this->m_emp_array[min_or_max]->m_id < this->m_emp_array[j]->m_id) {
						min_or_max = j;
					}
				}
				//输入选项有误
				else {
					cout << "输入选项有误" << endl;
					system("pause");
					system("cls");
					return;
				}
			}
			//如果最大最小值索引和原来索引不一致，交换成员
			if (i != min_or_max) {
				Worker* temp = this->m_emp_array[i];
				this->m_emp_array[i] = this->m_emp_array[min_or_max];
				this->m_emp_array[min_or_max] = temp;
			}
		}
		cout << " 排序成功" << endl;
		this->save_file();
		this->show_emp();

	}
}
//清空文件
void WorkManager::clean_file() {
	cout << "确认清空？" << endl;
	cout << "1.确认" << endl;
	cout << "2.返回" << endl;

	int select = 0;
	cin >> select;

	if (select == 1) {
		//打开模式 ios::trunc,如果文件存在则删除文件并重新创建
		ofstream ofs(FILENAME, ios::trunc);
		ofs.close();

		if (this->m_emp_array != NULL) {
			for (int i = 0; i < m_emp_num; i++) {
				if (this->m_emp_array[i] != NULL) {
					delete this->m_emp_array[i];
				}
			}
			this->m_emp_num = 0;
			delete[] this->m_emp_array;
			this->m_emp_array = NULL;
			this->m_file_is_empty = true;
		}
		cout << "数据已清空" << endl;
	}
	system("pause");
	system("cls");
}
//退出系统
void WorkManager::exit_system()
{
	cout << "欢迎下次使用" << endl;
	system("pause");
	exit(0);//程序退出，返回0
}
//析构函数
WorkManager::~WorkManager()
{
	if (this->m_emp_array != NULL)
	{
		for (int i = 0; i < this->m_emp_num; i++) {
			if (this->m_emp_array[i] != NULL) {
				delete this->m_emp_array[i];
			}
		}
		delete[] this->m_emp_array;
		this->m_emp_array = NULL;
	}
}
