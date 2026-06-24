#pragma once
#include <iostream>
#include "worker.h"
using namespace std;

//经理类
class Boss :public Worker {
public:
	//构造函数
	Boss(int id, string name, int dept);
	//显示职工信息
	virtual void show_info();
	//获取职工岗位
	virtual string get_dept();
};

