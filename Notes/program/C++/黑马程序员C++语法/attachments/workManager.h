#pragma once
#include <iostream>
#include <fstream>

#include"worker.h"

#define FILENAME "StaffList.txt"
using namespace std;

class WorkManager
{
public:
	int m_emp_num;// 记录员工数量
	Worker** m_emp_array; // 员工数组的指针
	bool m_file_is_empty;
	//构建函数
	WorkManager();
	//显示菜单
	void show_menu();
	//添加职工
	void add_emp();
	//保存文件
	void save_file();
	//获取员工人数
	int get_emp_num();
	//初始化员工数组
	void init_emp();
	//显示职工
	void show_emp();
	//判断员工是否存在
	int is_exist(int id);
	//删除职工
	void del_emp();
	//修改职工信息
	void mod_emp();
	//查找职工
	void find_emp();
	//排序职工
	void sort_emp();
	//清空文件
	void clean_file();
	//退出系统
	void exit_system();
	//析构函数
	~WorkManager();
};
