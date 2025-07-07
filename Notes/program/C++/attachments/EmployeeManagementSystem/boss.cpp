#include "boss.h"

//构造函数
Boss::Boss(int id, string name, int dept)
{
	this->m_id = id;
	this->m_name = name;
	this->m_dept = dept;
}
//显示职工信息
void Boss::show_info()
{
	cout << "编号：" << this->m_id
		<< "\t姓名：" << this->m_name
		<< "\t岗位：" << this->get_dept()
		<< "\t指责：管理公司" << endl;
}
//获取职工岗位
string Boss::get_dept()
{
	return string("老板");
}