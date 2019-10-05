#include<iostream>
#include<iomanip>
#include<string>
#include<algorithm>
#include<math.h>
#include <vector>

using namespace std;

string caesar(string plain, int key)
{
	for (int i = 0; i < plain.length(); i++)
	{
		if (plain[i] >= 'a' && plain[i] <= 'z')
		{
			plain[i] = (plain[i] - 97 + key) % 26 + 97;
			plain[i] = toupper(plain[i]);
		}
	}
	return plain;
}
/*string playfair(string plain, string key)
{

}*/
void vernam(string plain, string key)
{
	while (plain.length() > key.length())
		key = key + key;
	//cout << key << endl;;
	int* XOR = new int[plain.length()];
	for (int i = 0; i < plain.length(); i++)
	{
		XOR[i] = (plain[i] - 97) ^ (key[i] - 65);
	}
	char* cypher = new char[plain.length()];
	for (int i = 0; i < plain.length(); i++)
	{
		cypher[i] = XOR[i] + 97;
		cypher[i] = toupper(cypher[i]);
		cout << cypher[i];
	}
	delete[]XOR;
	delete[]cypher;
}

void row(string plain, string key)
{
	int size = key.length();
	char** table = new char* [size];
	for (int i = 0; i < size; ++i)
		table[i] = new char[plain.length() / size + 1];
	//³Ðarray
	for (int j = 0; j < (plain.length() / size + 1); j++)
		for (int i = 0; i < size; i++)
			table[i][j] = 0;


	//¶ñ¤Jplaintext
	int index = 0;
	for (int j = 0; j < (plain.length() / size + 1); j++)
		for (int i = 0; i < size; i++)
		{
			if (index >= plain.length())
				break;
			table[i][j] = plain[index];
			index++;
		}
	for (size_t j = 1; j <= key.length(); j++)
	{
		for (int i = 0; i < key.length(); i++)
		{
			if (key[i] - '1' + 1 == j)
			{
				for (int x = 0; x < (plain.length() / size + 1); x++)
				{
					if (table[i][x] != 0)
						cout << (char)toupper(table[i][x]);
				}
			}
		}
	}
	for (size_t i = 0; i < size; i++)
		delete[] table[i];
	delete[] table;
}
string rail(string text, int key)
{
	// create the matrix 
	char** rail = new char* [key];
	for (int i = 0; i < key; ++i)
		rail[i] = new char[text.length()];

	for (int i = 0; i < key; i++)
		for (int j = 0; j < text.length(); j++)
			rail[i][j] = '\n';

	// to find the direction 
	bool down = false;
	int row = 0, col = 0;

	for (int i = 0; i < text.length(); i++)
	{
		if (row == 0 || row == key - 1)
			down = !down;
		rail[row][col++] = text[i];
		down ? row++ : row--;
	}
	string result;
	for (int i = 0; i < key; i++)
		for (int j = 0; j < text.length(); j++)
			if (rail[i][j] != '\n')
				result.push_back(rail[i][j]);
	for (int i = 0; i < result.length(); i++)
		result[i] = (char)toupper(result[i]);
	for (size_t i = 0; i < key; i++)
		delete[] rail[i];
	delete[] rail;
	return result;
}
int main()
{
	string plaintext, method;

	cin >> method;

	if (method == "caesar")
	{
		int key = 0;
		cin >> key >> plaintext;
		cout << caesar(plaintext, key);
	}
	/*else if (method == "playfair")
	{
		string key = "";
		cin >> plaintext >> key;
		cout << playfair(plaintext, key);
	}*/
	else if (method == "vernam")
	{
		string key;
		cin >> key >> plaintext;
		vernam(plaintext, key);
	}
	else if (method == "row")
	{
		string key;
		cin >> key >> plaintext;
		row(plaintext, key);
	}
	else if (method == "rail_fence")
	{
		int key;
		cin >> key >> plaintext;
		cout << rail(plaintext, key);
	}
	system("pause");
}