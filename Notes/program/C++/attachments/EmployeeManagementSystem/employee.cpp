#include "employee.h"

//构造函数
Employee::Employee(int id, string name, int dept)
{
	this->m_id = id;
	this->m_name = name;
	this->m_dept = dept;
}
//显示职工信息
void Employee::show_info()
{
	cout << "编号：" << this->m_id
		<< "\t姓名：" << this->m_name
		<< "\t岗位：" << this->get_dept()
		<< "\t指责：完成任务" << endl;
}
//获取职工岗位
string Employee::get_dept()
{
	return string("员工");
}