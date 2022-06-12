#include<stdio.h>
#include<iostream>
#include<vector>
#include<set>
#include<string>
#include<map>
#include<queue>
#include<stack>
#include<utility>
#include<algorithm>
using namespace std;
/******************************************
Vectot的常见用途：存储数据，用邻接表存储图;
常用函数：
push_back(),
pop_back(),
size(),
clear(),
insert(),
erase()，
迭代器iterator,
*******************************************/
class VectorStudy {
public:
	//vector<int>vi;
	void VectorTest() {
		printf("**********vector及其常用函数**********\n");
		vector<int>vi;
		for (int i = 0; i <= 10; i++)
			vi.push_back(i);//在末尾插入元素；
		for (vector<int>::iterator it = vi.begin(); it != vi.end(); it++)
			printf("%d", *it);//迭代器用法；
		printf("\n");
		printf("删除前size的值为：%d\n", vi.size());
		vi.pop_back();//删除结尾元素；
		printf("删除后size的值为：%d\n", vi.size());//size()获取元素个数
		for (int i = 0; i <vi.size(); i++)
			printf("%d", vi[i]);
		printf("\n");
		vi.insert(vi.begin() + 1, -1);//将-1插入vi[1]的位置；
		for (int i = 0; i < vi.size(); i++)
			printf("%d", vi[i]);
		printf("\n");
		vi.erase(vi.begin() + 2);//删除vi[2]处的元素；
		for (int i = 0; i < vi.size(); i++)
			printf("%d", vi[i]);
		printf("\n");
		vi.erase(vi.begin() + 3, vi.begin() + 6);//删除vi[3]-vi[6]区间内的元素，即vi[3],vi[4],vi[5]；
		for (int i = 0; i < vi.size(); i++)
			printf("%d", vi[i]);
		printf("\n");
		vi.clear();//清除vector里的值；
		printf("清除后size的值为：%d\n", vi.size());
	}
};
/*******************************************
set是一个内部自动有序且不含重复元素的集合
只能通过迭代器iterator()访问，主要用途自动去重且按升序排列；
相关函数：
迭代器iterator
insert();
find();
erase();//删除单个元素，删除一个区间内的元素；
size();
clear();
*********************************************/
class SetStudy{
public:
	void SetTest() {
		printf("**********set及其常用函数**********\n");
		set<int>st;
		for (int i = 0; i < 10; i++)
			st.insert(i);
		set<int>::iterator it = st.find(2);//返回元素2的迭代器；
		printf("%d\n", *it);
		for (it = st.begin(); it != st.end(); it++)
			printf("%d", *it);
		printf("\n");
		st.erase(st.find(5));//用find函数找到5并删除它；
		for(it=st.begin();it!=st.end();it++)
	    printf("%d", *it);
		printf("\n");
		st.erase(st.find(1), st.find(4));
		for (it = st.begin(); it != st.end(); it++)
			printf("%d", *it);
		printf("\n");
		printf("size的值：%d\n", st.size());
		st.clear();
		printf("清空后size的值：%d\n", st.size());
	}
};
/**************************************************************
string
输入和输出整个字符串只能用cin,cout;
可以通过下标或迭代器进行访问；
相关函数：
c_str();将string类型转化为字符数组进行输出；
迭代器iterator:string::iterator it;
operator+=;
compare operator:> ,<,<=,>=,!=,==;
length()/size();
insert();
erase();
clear();
substr();
string::npos作为find()函数失配时的返回值；一般为-1或4294967295(unsigned_int类型最大值）
find();
replace();
***************************************************************/
class StringStudy {
public:
	void StringTest() {
		printf("**********string及其常用函数**********\n");
		string str = "abcd",str1="sun",str2="iloveyou",str3;
		for (int i = 0; i < str.length(); i++)
			printf("%c", str[i]);
		printf("\n");
		cin >> str;
		cout << str << endl;;
		printf("%s\n", str.c_str());
		for (string::iterator it = str.begin(); it != str.end(); it++)
			printf("%c", *it);
		printf("\n");
		cout <<"str1="<<str1 <<endl<< "str2=" << str2 <<endl<< "str3=" << str3 << endl;
		str3 = str1 + str2;
		str1 += str2;
		cout << "str3=" << str3 << endl << "str1=" << str1 << endl;
		str1.insert(2, str2);
		cout << "str1=" << str1 << endl;
		str1.insert(str1.begin(), str.begin(), str.end());
		cout << "str1=" << str1 << endl;
		cout << "str=" << str << endl;
		str.erase(str.begin()+1);//erase(it),删除单个元素，it为迭代器；
		cout << "str=" << str << endl;
		str1.erase(str1.begin() + 1, str1.end() - 2);
		cout << "str1=" << str1 << endl;//erase(first,last),删除first-last之间的元素；
		cout << "str3=" << str3 << endl;
		str3.erase(3, 2);//erase(pos,length)删除从3号位开始的两个字符；
		cout << "str3=" << str3 << endl;
		str3.clear();
		printf("%d", str3.length());
		cout << "str2=" << str2 << endl;
		cout << str2.substr(0, 3) << endl;//substr(pos,len)返回从pos号开始长度为len的字串；
		str += str1;
		cout << "str=" << str << endl << "str1=" << str1 << endl;
		cout << str.find(str1) << endl;
		cout << str.find(str1, 2) << endl;//从2号位置开始匹配str1;
		str.replace(2,3,str1);//str.repalce(pos,len,str1)将从pos号开始长度为len的字串替换为str1；
		cout << "str=" << str << endl;
		str.replace(str.begin() + 2, str.begin() + 8, str1);
		cout << "str=" << str << endl;
	}
};
/*************************************************************
map映射主要用途：map可以将任何基本类型映射到任何基本类型
需要建立字符（或字符串）与整数之间映射的题目
判断大整数或其他类型数据是否存在的题目，可把map当作bool数组用；
字符串和字符串的映射也可能用到
相关操作：
可通过下标访问也可通过迭代器访问；
find(key);
erase(it),erase(key),erase(first,last);
size();
clear();
**************************************************************/
class MapStudy{
	void MapTest() {

	}

};
/*************************************************************
*queue先进先出，使用广度优先搜索时，不用自己手动实现队列，用queue代替；
*front()访问队首元素；
*back()访问队尾元素；
*push(x)入队；
*pop首元素出队；
*empty()检测是否为空；true空，false非空；使用front(),back()前，先用empty判断是否为空；
*size()返回queue内元素个数；
*************************************************************/
class QueueStudy {

};
int main() {
	VectorStudy v;
	v.VectorTest();
	SetStudy s;
	s.SetTest();
	StringStudy str;
	str.StringTest();
	return 0;
}