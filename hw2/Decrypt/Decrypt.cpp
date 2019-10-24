#include <iostream>
#include <string>
#include <map>
#define SIZE 16

using namespace std;
int IP[] = { 58, 50, 42, 34, 26, 18, 10, 2,
   60, 52, 44, 36, 28, 20, 12, 4,
   62, 54, 46, 38, 30, 22, 14, 6,
   64, 56, 48, 40, 32, 24, 16, 8,
   57, 49, 41, 33, 25, 17, 9,  1,
   59, 51, 43, 35, 27, 19, 11, 3,
   61, 53, 45, 37, 29, 21, 13, 5,
   63, 55, 47, 39, 31, 23, 15, 7 };


int IP_1[] = { 40, 8, 48, 16, 56, 24, 64, 32,
	 39, 7, 47, 15, 55, 23, 63, 31,
	 38, 6, 46, 14, 54, 22, 62, 30,
	 37, 5, 45, 13, 53, 21, 61, 29,
	 36, 4, 44, 12, 52, 20, 60, 28,
	 35, 3, 43, 11, 51, 19, 59, 27,
	 34, 2, 42, 10, 50, 18, 58, 26,
	 33, 1, 41,  9, 49, 17, 57, 25 };


int PC_1[] = { 57, 49, 41, 33, 25, 17, 9,
	  1, 58, 50, 42, 34, 26, 18,
	 10,  2, 59, 51, 43, 35, 27,
	 19, 11,  3, 60, 52, 44, 36,
	 63, 55, 47, 39, 31, 23, 15,
	  7, 62, 54, 46, 38, 30, 22,
	 14,  6, 61, 53, 45, 37, 29,
	 21, 13,  5, 28, 20, 12,  4 };


int PC_2[] = { 14, 17, 11, 24,  1,  5,
	  3, 28, 15,  6, 21, 10,
	 23, 19, 12,  4, 26,  8,
	 16,  7, 27, 20, 13,  2,
	 41, 52, 31, 37, 47, 55,
	 30, 40, 51, 45, 33, 48,
	 44, 49, 39, 56, 34, 53,
	 46, 42, 50, 36, 29, 32 };

int shiftLeft[] = { 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1,0 };


int E[] = { 32,  1,  2,  3,  4,  5,
   4,  5,  6,  7,  8,  9,
   8,  9, 10, 11, 12, 13,
	 12, 13, 14, 15, 16, 17,
	 16, 17, 18, 19, 20, 21,
	 20, 21, 22, 23, 24, 25,
	 24, 25, 26, 27, 28, 29,
	 28, 29, 30, 31, 32,  1 };

int S_BOX[8][64] = {
 {
  14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
  0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
  4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
  15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13
 },
 {
  15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
  3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
  0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
  13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9
 },
 {
  10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
  13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
  13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
  1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12
 },
 {
  7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
  13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
  10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
  3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14
 },
 {
  2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
  14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
  4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
  11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3
 },
 {
  12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
  10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
  9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
  4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13
 },
 {
  4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
  13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
  1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
  6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12
 },
 {
  13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
  1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
  7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
  2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11
 }
};


int P[] = { 16,  7, 20, 21,
	 29, 12, 28, 17,
   1, 15, 23, 26,
   5, 18, 31, 10,
   2,  8, 24, 14,
	 32, 27,  3,  9,
	 19, 13, 30,  6,
	 22, 11,  4, 25 };


int main(int argc, char* argv[])
{
	char* change = new char[16]{ '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F' };
	
	map<char, string> data;
	data['0'] = "0000";
	data['1'] = "0001";
	data['2'] = "0010";
	data['3'] = "0011";
	data['4'] = "0100";
	data['5'] = "0101";
	data['6'] = "0110";
	data['7'] = "0111";
	data['8'] = "1000";
	data['9'] = "1001";
	data['A'] = "1010";
	data['B'] = "1011";
	data['C'] = "1100";
	data['D'] = "1101";
	data['E'] = "1110";
	data['F'] = "1111";

	map<string, char> r_data;
	r_data["0000"] = '0';
	r_data["0001"] = '1';
	r_data["0010"] = '2';
	r_data["0011"] = '3';
	r_data["0100"] = '4';
	r_data["0101"] = '5';
	r_data["0110"] = '6';
	r_data["0111"] = '7';
	r_data["1000"] = '8';
	r_data["1001"] = '9';
	r_data["1010"] = 'a';
	r_data["1011"] = 'b';
	r_data["1100"] = 'c';
	r_data["1101"] = 'd';
	r_data["1110"] = 'e';
	r_data["1111"] = 'f';

	string input = argv[2], key = argv[1];
	string b_input, b_key;

	for (int i = 2; i < 16 + 2; i++)
	{
		b_input += data.find(input[i])->second;
		b_key += data.find(key[i])->second;
	}

	string left = ""
		, right = "";
	for (int i = 0; i < 64; i++)
	{
		if (i < 32) left += b_input[IP[i] - 1];
		else right += b_input[IP[i] - 1];
	}

	string pc_1key;
	for (int i = 0; i < 56; i++)
		pc_1key += b_key[PC_1[i] - 1];

	for (int times = 0; times < 16; times++)
	{
		string new_right;
		for (int i = 0; i < 48; i++)
			new_right += right[E[i] - 1];

		for (int j = 0; j < shiftLeft[16 - times]; j++)
		{
			char tmp1 = pc_1key[0], tmp2 = pc_1key[28];
			for (int i = 27; i >= 1; i--)
			{
				pc_1key[(i + 1) % 28] = pc_1key[i];
				pc_1key[28 + (i + 1) % 28] = pc_1key[28 + i];
			}
			pc_1key[1] = tmp1;
			pc_1key[29] = tmp2;
		}

		string pc_2key;
		for (int i = 0; i < 48; i++)
			pc_2key += pc_1key[PC_2[i] - 1];

		//new_right XOR pc_2key
		string _xor;
		for (int i = 0; i < 48; i++)
			_xor += (new_right[i] ^ pc_2key[i]) + '0';
		string s_result, new_s_result;
		for (int i = 0; i < 48; i += 6)
		{
			int row = (_xor[i + 0] - '0') * 2 + (_xor[i + 5] - '0');
			int column = (_xor[i + 1] - '0') * 8 + (_xor[i + 2] - '0') * 4 + (_xor[i + 3] - '0') * 2 + (_xor[i + 4] - '0');
			s_result += data.find(change[S_BOX[i / 6][row * 16 + column]])->second;
		}

		for (int i = 0; i < 32; i++)
			new_s_result += s_result[P[i] - 1];
		string tmp_right = right.substr(0, 32);
		right = "";
		for (int i = 0; i < 32; i++)
			right += (left[i] ^ new_s_result[i]) + '0';
		left = tmp_right;
	}

	right += left;
	string result;
	for (int i = 0; i < SIZE * 4; i++)
		result += right[IP_1[i] - 1];
	cout << "0x";
	for (int i = 0; i < 64; i += 4)
		cout << r_data.find(result.substr(i, 4))->second;


	return 0;
}