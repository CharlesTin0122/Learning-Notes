#pragma once
#include<iostream>
#include<string>
using namespace std;

//抽象职工类
class Worker {
public:
	int m_id;//编号
	string m_name;//姓名
	int m_dept;//部门

	//显示职工信息
	virtual void show_info() = 0;
	//获取职工岗位
	virtual string get_dept() = 0;
};
